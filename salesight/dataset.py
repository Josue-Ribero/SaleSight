# Librerías que se usarán
import sqlite3
import pandas as pd
from pathlib import Path
from loguru import logger
from salesight.config import datos_procesados, datos_brutos, NOMBRE_DB

def obtener_datos_db(nombre_db: str = NOMBRE_DB):
    """
    Esta función lee los datos procesados desde la base de datos SQLite.
    """

    # Lee la ruta de la db. Si no está, envía un mensaje de alerta
    ruta_db = datos_procesados / nombre_db
    if not ruta_db.exists():
        logger.warning(f"La base de datos no existe en: {ruta_db}\n")
        return None
    
    # Se realiza la conexión con la DB
    logger.info(f"Conectando con la base de datos en: {ruta_db}...\n")
    try:
        with sqlite3.connect(ruta_db) as conexion:
            query = "SELECT * FROM ventas"
            df = pd.read_sql_query(query, conexion)
        
        if 'Order Date' in df.columns:
            df['Order Date'] = pd.to_datetime(df['Order Date'])
        return df
    except Exception as e:
        logger.error(f"Error al acceder a la DB: {e}")
        return None

# Función para obtener los datos brutos
def obtener_datos_raw(nombre_archivo: str = "new_retail_data.csv"):
    """
    Lee los datos brutos desde la carpeta de raw/
    Centraliza el acceso inicial para la etapa de transformación.
    """
    ruta_csv = datos_brutos / nombre_archivo
    if not ruta_csv.exists():
        logger.error(f"No se encontró el archivo RAW en: {ruta_csv}.\n")
        return None
        
    logger.info(f"Cargando datos brutos desde: {ruta_csv}...\n")
    try:
        return pd.read_csv(ruta_csv)
    except Exception as e:
        logger.error(f"Error al leer el CSV raw: {e}")
        return None

def guardar_datos_db(df: pd.DataFrame, nombre_db: str = NOMBRE_DB):
    """
    Carga un DataFrame en la base de datos SQLite procesada.
    """
    ruta_db = datos_procesados / nombre_db
    logger.info(f"Cargando datos en la base de datos: {ruta_db}...\n")

    try:
        # Envía los datos del df a la db
        df_db = df.copy()
        cols_fecha = df_db.select_dtypes(include=['datetime64', 'datetime', 'datetimetz']).columns
        for col in cols_fecha:
            df_db[col] = df_db[col].astype(str)

        # Se realiza la carga y si ya existe la db, la reemplaza  
        with sqlite3.connect(ruta_db) as conexion:
            df_db.to_sql('ventas', conexion, if_exists='replace', index=False)
        logger.success(f"Datos guardados exitosamente en '{nombre_db}'.\n")
        return True
    except Exception as e:
        logger.error(f"Error en la persistencia: {e}\n")
        return False
