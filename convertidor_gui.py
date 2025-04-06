import os
import datetime
import re
from PIL import Image
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QFileDialog,
                             QMessageBox, QProgressBar, QComboBox, QSpinBox, QListWidget, QSlider)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QScreen

class ConvertidorAvanzado(QMainWindow):
        
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Convertidor Multifuncional de Imágenes")
        self.setGeometry(100, 100, 600, 600)
        self.centrar_ventana()

        # Variables para carpetas y configuración
        self.input_folder = ""
        self.output_folder = ""
        self.imagenes = []  # Lista de nombres de imágenes en la carpeta seleccionada
        self.formatos_disponibles = ["JPG", "PNG", "BMP", "TIFF", "GIF"]
        self.log_folder = os.path.join(os.getcwd(), "logs")
        os.makedirs(self.log_folder, exist_ok=True)

        # Configuración del GUI
        self.configurar_gui()

    def configurar_gui(self):
        """
        Configura los elementos del GUI y aplica estilos personalizados.
        """
        layout = QVBoxLayout()

        # Etiquetas principales
        self.label_input = QLabel("Carpeta de entrada: No seleccionada")
        self.label_output = QLabel("Carpeta de salida: No seleccionada")
        self.label_input.setStyleSheet("color: #333; font-size: 16px;")
        self.label_output.setStyleSheet("color: #333; font-size: 16px;")

        # Barra de progreso personalizada
        self.progress_bar = QProgressBar()
        self.progress_bar.setAlignment(Qt.AlignCenter)
        self.progress_bar.setStyleSheet("QProgressBar { background-color: #f0f0f0; border: 1px solid #ccc; } "
                                        "QProgressBar::chunk { background-color: #4CAF50; }")

        # Combobox para elegir formato
        self.combo_format = QComboBox()
        self.combo_format.addItems(self.formatos_disponibles)
        self.combo_format.setStyleSheet("padding: 5px; font-size: 14px;")

        # Spinbox para ajustar calidad
        self.spin_quality = QSpinBox()
        self.spin_quality.setRange(1, 100)
        self.spin_quality.setValue(80)
        self.spin_quality.setSuffix("%")
        self.spin_quality.setStyleSheet("padding: 5px; font-size: 14px;")

        # Slider para redimensionar imágenes
        self.slider_size = QSlider(Qt.Horizontal)
        self.slider_size.setRange(50, 5000)
        self.slider_size.setValue(1024)
        self.slider_size.setStyleSheet("padding: 5px; font-size: 12px;")

        # Lista para seleccionar imágenes
        self.lista_imagenes = QListWidget()
        self.lista_imagenes.setFixedHeight(100)
        self.lista_imagenes.itemSelectionChanged.connect(self.mostrar_vista_previa)

        # Vista previa de imágenes
        self.label_preview = QLabel()
        self.label_preview.setFixedHeight(200)
        self.label_preview.setStyleSheet("border: 1px solid #ccc; border-radius: 5px;")
        self.label_preview.setAlignment(Qt.AlignCenter)

        # Botones principales
        btn_seleccionar_entrada = QPushButton("Seleccionar carpeta de entrada")
        btn_seleccionar_entrada.clicked.connect(self.seleccionar_carpeta_entrada)
        btn_seleccionar_entrada.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; font-size: 14px;")

        btn_seleccionar_salida = QPushButton("Seleccionar carpeta de salida")
        btn_seleccionar_salida.clicked.connect(self.seleccionar_carpeta_salida)
        btn_seleccionar_salida.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; font-size: 14px;")

        btn_procesar_imagen = QPushButton("Procesar imagen seleccionada")
        btn_procesar_imagen.clicked.connect(self.procesar_imagen_seleccionada)
        btn_procesar_imagen.setStyleSheet("background-color: #FF5722; color: white; padding: 10px; font-size: 14px;")

        btn_procesar_lote = QPushButton("Procesar lote completo")
        btn_procesar_lote.clicked.connect(self.procesar_lote_completo)
        btn_procesar_lote.setStyleSheet("background-color: #FF5722; color: white; padding: 10px; font-size: 14px;")

        btn_ayuda = QPushButton("Ayuda")
        btn_ayuda.clicked.connect(self.mostrar_informacion_desarrollador)
        btn_ayuda.setStyleSheet("background-color: #2196F3; color: white; padding: 10px; font-size: 14px;")

        # Añadir elementos al layout
        layout.addWidget(self.label_input)
        layout.addWidget(btn_seleccionar_entrada)
        layout.addWidget(self.label_output)
        layout.addWidget(btn_seleccionar_salida)
        layout.addWidget(QLabel("Selecciona el formato de salida:"))
        layout.addWidget(self.combo_format)
        layout.addWidget(QLabel("Calidad de salida:"))
        layout.addWidget(self.spin_quality)
        layout.addWidget(QLabel("Redimensionar tamaño (px):"))
        layout.addWidget(self.slider_size)
        layout.addWidget(QLabel("Selecciona una imagen para vista previa:"))
        layout.addWidget(self.lista_imagenes)
        layout.addWidget(self.label_preview)
        layout.addWidget(self.progress_bar)
        layout.addWidget(btn_procesar_imagen)
        layout.addWidget(btn_procesar_lote)
        layout.addWidget(btn_ayuda)

        # Configurar la ventana
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
    def centrar_ventana(self):
        """
        Centra la ventana en la pantalla.
        """
        pantalla = QApplication.primaryScreen()
        tamaño_ventana = self.frameGeometry()
        centro_pantalla = pantalla.availableGeometry().center()
        tamaño_ventana.moveCenter(centro_pantalla)
        self.move(tamaño_ventana.topLeft())
    
    def seleccionar_carpeta_entrada(self):
        carpeta = QFileDialog.getExistingDirectory(self, "Seleccionar carpeta de entrada")
        if carpeta:
            self.input_folder = carpeta
            self.label_input.setText(f"Carpeta de entrada: {carpeta}")
            self.cargar_imagenes()
            self.guardar_log(f"Carpeta de entrada seleccionada: {carpeta}")

    def seleccionar_carpeta_salida(self):
        carpeta = QFileDialog.getExistingDirectory(self, "Seleccionar carpeta de salida")
        if carpeta:
            self.output_folder = carpeta
            self.label_output.setText(f"Carpeta de salida: {carpeta}")
            self.guardar_log(f"Carpeta de salida seleccionada: {carpeta}")

    def cargar_imagenes(self):
        """
        Carga los nombres de las imágenes en la lista desplegable.
        """
        self.lista_imagenes.clear()
        self.imagenes = [f for f in os.listdir(self.input_folder) if f.lower().endswith(("png", "jpg", "jpeg", "bmp", "tiff", "gif"))]
        self.lista_imagenes.addItems(self.imagenes)
        if self.imagenes:
            self.lista_imagenes.setCurrentRow(0)
            self.mostrar_vista_previa()

    def mostrar_vista_previa(self):
        """
        Muestra una vista previa de la imagen seleccionada.
        """
        item = self.lista_imagenes.currentItem()
        if item:
            ruta_imagen = os.path.join(self.input_folder, item.text())
            pixmap = QPixmap(ruta_imagen).scaled(200, 200, Qt.KeepAspectRatio)
            self.label_preview.setPixmap(pixmap)
        else:
            self.label_preview.clear()
            self.label_preview.setText("No hay imágenes para mostrar.")

    def procesar_imagen_seleccionada(self):
        """
        Procesa solo la imagen seleccionada en la vista previa.
        """
        item = self.lista_imagenes.currentItem()
        if not item:
            QMessageBox.warning(self, "Advertencia", "No hay ninguna imagen seleccionada.")
            return

        imagen = item.text()
        self.procesar_imagen(imagen)

    def procesar_lote_completo(self):
        """
        Procesa todas las imágenes en el lote.
        """
        for imagen in self.imagenes:
            self.procesar_imagen(imagen)

    def procesar_imagen(self, imagen):
        """
        Procesa una imagen específica aplicando redimensionamiento y conversión.
        """
        try:
            ruta_entrada = os.path.join(self.input_folder, imagen)
            nombre_salida = os.path.splitext(imagen)[0] + f".{self.combo_format.currentText().lower()}"
            ruta_salida = os.path.join(self.output_folder, nombre_salida)

            with Image.open(ruta_entrada) as img:
                # Redimensionar la imagen
                nuevo_ancho = self.slider_size.value()
                proporción = nuevo_ancho / img.width
                nuevo_alto = int(img.height * proporción)
                img = img.resize((nuevo_ancho, nuevo_alto))

                # Guardar la imagen en el formato seleccionado
                if self.combo_format.currentText().lower() == "jpg":
                    img = img.convert("RGB")  # JPG no soporta transparencias
                img.save(ruta_salida, format=self.combo_format.currentText(), quality=self.spin_quality.value())

            self.guardar_log(f"Imagen procesada: {imagen} -> {ruta_salida}")
        except Exception as e:
            self.guardar_log(f"Error al procesar {imagen}: {e}")
            QMessageBox.critical(self, "Error", f"Error al procesar {imagen}: {e}")
            
    def guardar_log(self, mensaje):
        """
        Guarda un mensaje en el archivo de logs con marca de tiempo.
        """
        log_path = os.path.join(self.log_folder, "eventos.log")
        with open(log_path, "a", encoding="utf-8") as log_file:
            log_file.write(f"[{datetime.datetime.now()}] {mensaje}\n")

    def mostrar_informacion_desarrollador(self):
        """
        Muestra información del desarrollador en una ventana emergente.
        """
        QMessageBox.information(
            self,
            "Información del Desarrollador",
            "Desarrollador: Nahum Flores\nCorreo: excalibur_965@hotmail.com\nVersión: 1.0.3"
        )
        

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ventana = ConvertidorAvanzado()
    ventana.show()
    sys.exit(app.exec_())
    
