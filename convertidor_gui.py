import os
import datetime
import re
from PIL import Image
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QFileDialog,
                             QMessageBox, QProgressBar, QComboBox, QSpinBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QScreen

class ConvertidorAvanzado(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Convertidor Multifuncional de Imágenes")
        self.setGeometry(100, 100, 500, 400)
        self.centrar_ventana()

        # Variables para carpetas y configuración
        self.input_folder = ""
        self.output_folder = ""
        self.formatos_disponibles = ["JPG", "PNG", "BMP", "TIFF", "GIF"]
        self.log_folder = os.path.join(os.getcwd(), "logs")
        os.makedirs(self.log_folder, exist_ok=True)

        # Configuración del GUI
        layout = QVBoxLayout()

        self.label_input = QLabel("Carpeta de entrada: No seleccionada")
        self.label_output = QLabel("Carpeta de salida: No seleccionada")
        self.progress_bar = QProgressBar()
        self.progress_bar.setAlignment(Qt.AlignCenter)

        # Combobox para elegir formato
        self.combo_format = QComboBox()
        self.combo_format.addItems(self.formatos_disponibles)

        # Spinbox para ajustar calidad
        self.spin_quality = QSpinBox()
        self.spin_quality.setRange(1, 100)
        self.spin_quality.setValue(80)
        self.spin_quality.setSuffix("%")

        btn_seleccionar_entrada = QPushButton("Seleccionar carpeta de entrada")
        btn_seleccionar_entrada.clicked.connect(self.seleccionar_carpeta_entrada)

        btn_seleccionar_salida = QPushButton("Seleccionar carpeta de salida")
        btn_seleccionar_salida.clicked.connect(self.seleccionar_carpeta_salida)

        btn_convertir = QPushButton("Iniciar conversión")
        btn_convertir.clicked.connect(self.iniciar_conversion)

        btn_ayuda = QPushButton("Ayuda")
        btn_ayuda.clicked.connect(self.mostrar_informacion_desarrollador)

        # Añadir elementos al layout
        layout.addWidget(self.label_input)
        layout.addWidget(btn_seleccionar_entrada)
        layout.addWidget(self.label_output)
        layout.addWidget(btn_seleccionar_salida)
        layout.addWidget(QLabel("Selecciona el formato de salida:"))
        layout.addWidget(self.combo_format)
        layout.addWidget(QLabel("Calidad de salida:"))
        layout.addWidget(self.spin_quality)
        layout.addWidget(self.progress_bar)
        layout.addWidget(btn_convertir)
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
            self.guardar_log(f"Carpeta de entrada seleccionada: {carpeta}")

    def seleccionar_carpeta_salida(self):
        carpeta = QFileDialog.getExistingDirectory(self, "Seleccionar carpeta de salida")
        if carpeta:
            self.output_folder = carpeta
            self.label_output.setText(f"Carpeta de salida: {carpeta}")
            self.guardar_log(f"Carpeta de salida seleccionada: {carpeta}")

    def corregir_nombre(self, nombre):
        """
        Corrige nombres de archivos eliminando caracteres no válidos.
        """
        nombre_original = nombre
        nombre_corregido = re.sub(r'[<>:"/\\|?*]', '_', nombre)  # Reemplazar caracteres no válidos
        nombre_corregido = re.sub(r'\s+', ' ', nombre_corregido).strip()  # Eliminar espacios innecesarios
        if nombre_original != nombre_corregido:
            self.guardar_log(f"Nombre corregido: '{nombre_original}' -> '{nombre_corregido}'")
        return nombre_corregido

    def iniciar_conversion(self):
        if not self.input_folder or not self.output_folder:
            QMessageBox.warning(self, "Advertencia", "Debe seleccionar ambas carpetas.")
            self.guardar_log("Advertencia: no se seleccionaron ambas carpetas.")
            return

        # Configurar el formato de salida y calidad
        formato_salida = self.combo_format.currentText().lower()
        calidad = self.spin_quality.value()

        # Crear carpeta para los archivos convertidos
        output_folder = os.path.join(self.output_folder, f"Convertidos_{formato_salida.upper()}")
        os.makedirs(output_folder, exist_ok=True)

        # Obtener archivos de entrada
        archivos = [f for f in os.listdir(self.input_folder) if f.lower().endswith(("png", "jpg", "jpeg", "bmp", "tiff", "gif"))]
        total_archivos = len(archivos)
        if total_archivos == 0:
            QMessageBox.information(self, "Información", "No se encontraron imágenes compatibles para convertir.")
            self.guardar_log("No se encontraron imágenes en la carpeta de entrada.")
            return

        # Configurar barra de progreso
        self.progress_bar.setMaximum(total_archivos)

        # Procesar cada archivo
        for i, archivo in enumerate(archivos, start=1):
            try:
                archivo_corregido = self.corregir_nombre(archivo)
                ruta_entrada = os.path.join(self.input_folder, archivo)
                nombre_salida = os.path.splitext(archivo_corregido)[0] + f".{formato_salida}"
                ruta_salida = os.path.join(output_folder, nombre_salida)

                with Image.open(ruta_entrada) as img:
                    if formato_salida == "jpg":
                        img = img.convert("RGB")  # JPG no soporta transparencias
                    img.save(ruta_salida, format=formato_salida.upper(), quality=calidad)

                self.progress_bar.setValue(i)
                self.guardar_log(f"Imagen convertida: {archivo} -> {nombre_salida}")
            except Exception as e:
                self.guardar_log(f"Error al convertir {archivo}: {e}")
                QMessageBox.critical(self, "Error", f"Error al convertir {archivo}: {e}")

        QMessageBox.information(self, "Éxito", f"Conversión completada. Archivos guardados en:\n{output_folder}")
        self.guardar_log(f"Conversión completada. Archivos guardados en: {output_folder}")

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
            "Desarrollador: Nahum Flores\nCorreo: excalibur_965@hotmail.com\nVersión: 1.0.0\nFuncionalidad: Corrección de nombres de archivo"
        )

# Ejecutar la aplicación
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ventana = ConvertidorAvanzado()
    ventana.show()
    sys.exit(app.exec_())