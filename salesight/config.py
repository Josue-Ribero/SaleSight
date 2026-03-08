# importación de librerías que se usarán
from pathlib import Path
from dotenv import load_dotenv
from loguru import logger
from tqdm import tqdm

# cargar configuración de entorno
load_dotenv()

# definición de rutas base
ruta_raiz = Path(__file__).resolve().parents[1]
logger.info(f"ruta raíz del proyecto: {ruta_raiz}")

# directorios de datos
carpeta_datos = ruta_raiz / "data"
datos_brutos = carpeta_datos / "raw"
datos_intermedios = carpeta_datos / "interim"
datos_procesados = carpeta_datos / "processed"
datos_externos = carpeta_datos / "external"

# modelos y reportes
carpeta_modelos = ruta_raiz / "models"
carpeta_reportes = ruta_raiz / "reports"
ruta_graficos = carpeta_reportes / "figures"

# Configuración de la base de datos
NOMBRE_DB = "ventas_procesadas.db"

# configuración de logs con soporte para tqdm
try:
    logger.remove(0)
    logger.add(lambda msg: tqdm.write(msg, end=""), colorize=True)
except ModuleNotFoundError:
    pass
