import os
import subprocess
import sys
import importlib.util
import time



def verificar_e_instalar_libreria(libreria, timeout=300):
    """
    Verifica e instala una librería. Detiene el proceso si excede el tiempo límite.
    :param libreria: Nombre de la librería a verificar/instalar.
    :param timeout: Tiempo máximo en segundos antes de detener el intento de instalación.
    """
    if importlib.util.find_spec(libreria) is not None:
        print(f"[ OK ] La librería '{libreria}' ya está instalada.")
    else:
        print(f"[ ERROR ] La librería '{libreria}' no está instalada. Intentando instalarla ahora...")
        try:
            start_time = time.time()  # Registro del tiempo inicial
            process = subprocess.Popen([sys.executable, "-m", "pip", "install", libreria], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # Verificar tiempo límite
            while process.poll() is None:
                elapsed_time = time.time() - start_time
                if elapsed_time > timeout:
                    process.terminate()  # Detener proceso si excede el tiempo límite
                    print(f"[ ERROR ] El intento de instalar '{libreria}' excedió el tiempo límite de {timeout} segundos.")
                    print("Por favor, verifica tu conexión a internet o instala manualmente la librería.")
                    exit(1)

            print(f"[ OK ] La librería '{libreria}' se instaló correctamente.")
        except Exception as e:
            print(f"[ ERROR ] Error al intentar instalar '{libreria}': {e}")
            exit(1)

def verificar_archivos_necesarios(archivos_requeridos):
    """
    Verifica que los archivos necesarios estén en la carpeta actual.
    """
    print("[ BUSCAR ] Verificando archivos necesarios en la carpeta actual...")
    faltantes = []
    for archivo in archivos_requeridos:
        if not os.path.exists(archivo):
            faltantes.append(archivo)
    if faltantes:
        print("[ ERROR ] Faltan los siguientes archivos necesarios:")
        for archivo in faltantes:
            print(f"- {archivo}")
        print("Por favor coloca los archivos en la carpeta antes de continuar.")
        exit(1)
    print("[ OK ] Todos los archivos necesarios están presentes.")

def convertir_a_exe(script_gui, timeout=600):
    """
    Convierte un script a ejecutable. Detiene el proceso si excede el tiempo límite.
    :param script_gui: Nombre del script Python a convertir.
    :param timeout: Tiempo máximo en segundos antes de detener el intento de conversión.
    """
    print(" Convirtiendo el script del GUI a ejecutable...")
    try:
        start_time = time.time()  # Registro del tiempo inicial
        process = subprocess.Popen(["pyinstaller", "--onefile", "--noconsole", script_gui], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Verificar tiempo límite
        while process.poll() is None:
            elapsed_time = time.time() - start_time
            if elapsed_time > timeout:
                process.terminate()  # Detener proceso si excede el tiempo límite
                print(f"[ ERROR ] El intento de convertir '{script_gui}' a ejecutable excedió el tiempo límite de {timeout} segundos.")
                print("Por favor verifica el entorno o intenta de nuevo.")
                exit(1)

        print("[ OK ] El ejecutable ha sido creado exitosamente.")
        print(f"Encuentra el archivo en la carpeta 'dist/{script_gui.split('.')[0]}.exe'")
    except Exception as e:
        print(f"[ ERROR ] Error al intentar convertir el script a ejecutable: {e}")
        exit(1)

# Librerías necesarias
librerias = ["Pillow", "PyQt5"]

# Archivos necesarios
archivos_requeridos = ["convertidor_gui.py"]

# 1. Verificar e instalar librerías necesarias
for libreria in librerias:
    verificar_e_instalar_libreria(libreria, timeout=300)

# 2. Verificar la existencia de archivos requeridos
verificar_archivos_necesarios(archivos_requeridos)

# 3. Convertir el GUI a ejecutable
convertir_a_exe("convertidor_gui.py", timeout=600)

print("\n[ OK ] El instalador completó su trabajo. Ahora puedes usar el convertidor fácilmente.")