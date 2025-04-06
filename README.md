# Super_convertidor
Convertidor de imágenes por lotes simple (Simple Python Image converter with GUI)

===========================================
    Convertidor Multifuncional de Imágenes
===========================================

Versión: 1.0.1
Desarrollador: Nahum Flores
Correo: excalibur_965@hotmail.com

Descripción:
------------
El Convertidor Multifuncional de Imágenes es una herramienta avanzada diseñada para simplificar la conversión y edición básica de imágenes. Con soporte para múltiples formatos de entrada y salida, opciones de compresión, y funcionalidades inteligentes como la corrección de nombres, este convertidor es ideal para usuarios que buscan una experiencia completa y sencilla.

Características Principales:
----------------------------
1. **Soporte para múltiples formatos:**
   - Formatos de entrada admitidos: PNG, JPG, JPEG, BMP, GIF, TIFF.
   - Formatos de salida disponibles: JPG, PNG, BMP, TIFF, GIF.

2. **Compresión y ajuste de calidad:**
   - Permite configurar la calidad de las imágenes de salida con un rango de 1% a 100%.

3. **Corrección automática de nombres:**
   - Detecta nombres de archivo ilegibles o con caracteres no permitidos.
   - Corrige automáticamente los nombres y registra los cambios en los logs.

4. **Procesamiento por lotes:**
   - Convierte múltiples imágenes a la vez, ahorrando tiempo.

5. **Organización automática:**
   - Los archivos convertidos se guardan en subcarpetas organizadas por formato.

6. **Logs detallados:**
   - Registra eventos importantes como:
     - Selección de carpetas.
     - Conversión de imágenes.
     - Correcciones de nombres.
     - Errores detectados.
   - Los logs se guardan en la carpeta `logs/eventos.log`.

7. **Interfaz gráfica fácil de usar:**
   - Diseño intuitivo con botones claros para cada funcionalidad.
   - Barra de progreso para indicar el estado de la conversión.

8. **Ayuda y soporte:**
   - Incluye un botón de "Ayuda" que muestra información sobre el desarrollador.

Requisitos del sistema:
-----------------------
- **Para el desarrollador**:
  - Python 3.9 o superior.
  - Librerías requeridas: Pillow, PyQt5.
  - Herramienta: PyInstaller para generar el ejecutable.

- **Para el usuario final**:
  - NO es necesario instalar Python ni ninguna librería adicional.
  - Simplemente ejecuta el archivo `convertidor_gui.exe`.

Nota Importante: Excepciones en el Antivirus
--------------------------------------------
El archivo ejecutable `convertidor_gui.exe` puede ser detectado por algunos antivirus como una posible amenaza debido a su naturaleza de archivo portable. Si esto ocurre:
- Agrega el ejecutable a las excepciones de tu antivirus para permitir su ejecución.
- Consulta la documentación de tu antivirus para obtener instrucciones específicas sobre cómo realizar este proceso.

Cómo usar el convertidor:
-------------------------
1. Ejecuta la aplicación.
2. Selecciona una carpeta de entrada que contenga las imágenes a convertir.
3. Selecciona una carpeta de salida donde se guardarán las imágenes convertidas.
4. Elige el formato de salida (JPG, PNG, BMP, etc.).
5. Configura la calidad de las imágenes (opcional, predeterminada al 80%).
6. Haz clic en "Iniciar conversión" y observa el progreso en la barra de estado.
7. Una vez completado, los archivos convertidos estarán organizados en la carpeta de salida.

Notas importantes:
------------------
- El convertidor detectará automáticamente imágenes compatibles en la carpeta de entrada.
- Si los nombres de los archivos son ilegibles, se corregirán automáticamente.
- Asegúrate de que las imágenes no estén en uso por otro programa durante la conversión.

Contacto:
---------
Si tienes preguntas, sugerencias o necesitas soporte, no dudes en contactarme:
Correo: nahum.flores@example.com

Notas para desarrolladores:
--------------------------
Esta carpeta contiene el código fuente Python en el archivo:
convertidor_gui.py
# Dependencias necesarias para el Convertidor Multifuncional de Imágenes

# Librerías externas
pillow
pyqt5

# Herramientas opcionales
pyinstaller  # Solo necesario para crear un ejecutable portátil

# Módulos estándar de Python (no requieren instalación):
# - os: Manejo de archivos y rutas
# - datetime: Registro de marcas de tiempo en logs
# - re: Corrección de nombres con expresiones regulares
