import os
import datetime
from PIL import Image
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QFileDialog,
                             QMessageBox, QProgressBar, QComboBox, QListWidget)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

class ConvertidorAvanzado(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Convertidor Multifuncional de Imágenes")
        self.setGeometry(100, 100, 600, 500)
        self.centrar_ventana()

        # Variables para carpetas y configuración
        self.input_folder = ""
        self.output_folder = ""
        self.imagenes = []
        self.formatos_disponibles = ["jpg", "png", "bmp", "tiff", "gif"]
        self.log_folder = os.path.join(os.getcwd(), "logs")
        os.makedirs(self.log_folder, exist_ok=True)

        # Configuración del GUI
        self.configurar_gui()

    def configurar_gui(self):
        """
        Configura los elementos del GUI y aplica estilos personalizados.
        """
        layout = QVBoxLayout()

        # Etiquetas
        self.label_input = QLabel("Carpeta de entrada: No seleccionada")
        self.label_output = QLabel("Carpeta de salida: No seleccionada")
        self.label_input.setStyleSheet("color: #333; font-size: 16px; padding: 5px;")
        self.label_output.setStyleSheet("color: #333; font-size: 16px; padding: 5px;")

        # Barra de progreso
        self.progress_bar = QProgressBar()
        self.progress_bar.setAlignment(Qt.AlignCenter)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: #f0f0f0;
                border: 1px solid #ccc;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                width: 20px;
            }
        """)

        # Formato de salida
        self.combo_format = QComboBox()
        self.combo_format.addItems(self.formatos_disponibles)
        self.combo_format.setStyleSheet("padding: 5px; font-size: 14px;")

        # Lista de imágenes
        self.lista_imagenes = QListWidget()
        self.lista_imagenes.setFixedHeight(100)
        self.lista_imagenes.itemSelectionChanged.connect(self.mostrar_vista_previa)

        # Vista previa
        self.label_preview = QLabel()
        self.label_preview.setFixedHeight(200)
        self.label_preview.setAlignment(Qt.AlignCenter)
        self.label_preview.setStyleSheet("border: 1px solid #ccc; border-radius: 5px;")

        # Botones
        btn_seleccionar_entrada = QPushButton("Seleccionar carpeta de entrada")
        btn_seleccionar_entrada.clicked.connect(self.seleccionar_carpeta_entrada)
        btn_seleccionar_entrada.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; font-size: 14px;")

        btn_seleccionar_salida = QPushButton("Seleccionar carpeta de salida")
        btn_seleccionar_salida.clicked.connect(self.seleccionar_carpeta_salida)
        btn_seleccionar_salida.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; font-size: 14px;")

        btn_procesar = QPushButton("Procesar lote completo")
        btn_procesar.clicked.connect(self.procesar_lote_completo)
        btn_procesar.setStyleSheet("background-color: #FF5722; color: white; padding: 10px; font-size: 14px;")

        btn_ayuda = QPushButton("Ayuda")
        btn_ayuda.clicked.connect(self.mostrar_informacion_desarrollador)
        btn_ayuda.setStyleSheet("background-color: #2196F3; color: white; padding: 10px; font-size: 14px;")

        # Añadir elementos al layout
        layout.addWidget(self.label_input)
        layout.addWidget(btn_seleccionar_entrada)
        layout.addWidget(self.label_output)
        layout.addWidget(btn_seleccionar_salida)
        layout.addWidget(QLabel("Formato de salida:"))
        layout.addWidget(self.combo_format)
        layout.addWidget(QLabel("Lista de imágenes:"))
        layout.addWidget(self.lista_imagenes)
        layout.addWidget(self.label_preview)
        layout.addWidget(self.progress_bar)
        layout.addWidget(btn_procesar)
        layout.addWidget(btn_ayuda)

        # Configuración del contenedor principal
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
        """
        Abre un diálogo para seleccionar la carpeta de entrada y carga las imágenes disponibles.
        """
        carpeta = QFileDialog.getExistingDirectory(self, "Seleccionar carpeta de entrada")
        if carpeta:
            self.input_folder = carpeta
            self.label_input.setText(f"Carpeta de entrada: {carpeta}")
            self.cargar_imagenes()
            self.guardar_log(f"Carpeta de entrada seleccionada: {carpeta}")
            
    def seleccionar_carpeta_salida(self):
        """
        Abre un diálogo para seleccionar la carpeta de salida y crea una subcarpeta para los resultados.
        """
        carpeta = QFileDialog.getExistingDirectory(self, "Seleccionar carpeta de salida")
        if carpeta:
            self.output_folder = os.path.join(carpeta, "resultados")  # Subcarpeta "resultados"
            os.makedirs(self.output_folder, exist_ok=True)  # Crear la subcarpeta si no existe
            self.label_output.setText(f"Carpeta de salida: {self.output_folder}")
            self.guardar_log(f"Carpeta de salida seleccionada: {self.output_folder}")

    #def seleccionar_carpeta_salida(self):
    #    """
    #    Abre un diálogo para seleccionar la carpeta de salida.
    #    """
    #    carpeta = QFileDialog.getExistingDirectory(self, "Seleccionar carpeta de salida")
    #    if carpeta:
    #        self.output_folder = carpeta
    #        self.label_output.setText(f"Carpeta de salida: {carpeta}")
    #        self.guardar_log(f"Carpeta de salida seleccionada: {carpeta}")

    def cargar_imagenes(self):
        """
        Carga las imágenes de la carpeta seleccionada en la lista.
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

    def procesar_lote_completo(self):
        """
        Procesa todas las imágenes de la carpeta seleccionada.
        """
        if not self.input_folder or not self.output_folder:
            QMessageBox.warning(self, "Advertencia", "Debe seleccionar carpetas de entrada y salida.")
            return

        self.progress_bar.setMaximum(len(self.imagenes))
        for i, imagen in enumerate(self.imagenes, start=1):
            self.procesar_imagen(imagen)
            self.progress_bar.setValue(i)

        QMessageBox.information(self, "Éxito", "Procesamiento completado.")

    
    def procesar_lote_completo(self):
        """
        Procesa todas las imágenes de la carpeta seleccionada.
        """
        if not self.input_folder or not self.output_folder:
            QMessageBox.warning(self, "Advertencia", "Debe seleccionar carpetas de entrada y salida.")
            return

        self.progress_bar.setMaximum(len(self.imagenes))
        for i, imagen in enumerate(self.imagenes, start=1):
            self.procesar_imagen(imagen)
            self.progress_bar.setValue(i)

        QMessageBox.information(self, "Éxito", "Procesamiento completado.")

    #def procesar_imagen(self, imagen):
    #    """
    #    Simplifica el flujo para convertir una imagen a JPG y registrar el resultado.
    #    """
    #    try:
    #        # Definir rutas de entrada y salida
    #        ruta_entrada = os.path.join(self.input_folder, imagen)
    #        ruta_salida = os.path.join(self.output_folder, imagen.rsplit(".", 1)[0] + ".jpg")
    #
    #        # Abrir y procesar la imagen
    #        with Image.open(ruta_entrada) as img:
    #            rgb_img = img.convert("RGB")  # Convertir a RGB para JPG
    #            rgb_img.save(ruta_salida, "JPEG")  # Guardar como JPG
    #
    #        # Registrar éxito en el log
    #        log_path = os.path.join(self.output_folder, "log.txt")
    #        with open(log_path, "a") as log_file:
    #            log_file.write(f"{imagen} convertido con éxito.\n")
    #
    #        print(f"Imagen procesada: {imagen} -> {ruta_salida}")
    #
    #    except Exception as e:
    #        # Registrar errores en el log
    #        log_path = os.path.join(self.output_folder, "log.txt")
    #        with open(log_path, "a") as log_file:
    #            log_file.write(f"Error al convertir {imagen}: {e}\n")
    #
    #        print(f"Error al procesar {imagen}: {e}")
    def procesar_imagen(self, imagen):
        """
        Simplifica el flujo para convertir una imagen a JPG y guardar en la subcarpeta de resultados.
        """
        try:
            # Definir rutas de entrada y salida dentro de la subcarpeta
            ruta_entrada = os.path.join(self.input_folder, imagen)
            ruta_salida = os.path.join(self.output_folder, imagen.rsplit(".", 1)[0] + ".jpg")
    
            # Abrir y procesar la imagen
            with Image.open(ruta_entrada) as img:
                rgb_img = img.convert("RGB")  # Convertir a RGB para JPG
                rgb_img.save(ruta_salida, "JPEG")  # Guardar como JPG
    
            # Registrar éxito en el log
            log_path = os.path.join(self.output_folder, "log.txt")
            with open(log_path, "a") as log_file:
                log_file.write(f"{imagen} convertido con éxito.\n")
    
            print(f"Imagen procesada: {imagen} -> {ruta_salida}")
    
        except Exception as e:
            # Registrar errores en el log
            log_path = os.path.join(self.output_folder, "log.txt")
            with open(log_path, "a") as log_file:
                log_file.write(f"Error al convertir {imagen}: {e}\n")
    
            print(f"Error al procesar {imagen}: {e}")
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
            "Desarrollador: Nahum Flores\nCorreo: excalibur_965@hotmail.com\nVersión: 1.1.0"
        )

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ventana = ConvertidorAvanzado()
    ventana.show()
    sys.exit(app.exec_())

