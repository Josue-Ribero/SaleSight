# Librerías utilizadas
import pandas as pd
from pathlib import Path
from loguru import logger
import typer
from enum import Enum
from salesight.config import datos_procesados, datos_brutos, NOMBRE_DB
from salesight.ingest import descargar_datos
from salesight.features import procesar_caracteristicas
from salesight.plots import ejecutar_graficacion
from salesight.dataset import guardar_datos_db, obtener_datos_db

# Controlador de la aplicación
app = typer.Typer()

# Enumeración para escoger la fase o el ETL completo
class modo_ejecucion(str, Enum):
    completo = "completo"
    ingesta = "ingesta"
    transformacion = "transformacion"
    carga = "carga"

# Conversión de funciones a un comando en CLI
@app.command()
def orquestar_pipeline(
    modo: modo_ejecucion = typer.Option(modo_ejecucion.completo, "--modo", help="Define qué partes del pipeline ejecutar"),
    dataset_id: str = "sahilprajapati143/retail-analysis-large-dataset",
    bd_ventas: str = NOMBRE_DB
):
    """
    SaleSight - Orquestador ETL (Extraer, Transformar/EDA, Cargar)
    """
    archivo_csv_procesado = datos_procesados / "processed_data.csv"
    
    # 1. Extracción (ingesta) (E)
    if modo in [modo_ejecucion.ingesta, modo_ejecucion.completo]:
        logger.info("ETAPA 1: EXTRACCIÓN (E)...")
        descargar_datos(dataset_kaggle=dataset_id, carpeta_destino=datos_brutos)

    # 2. Transformación (T) + EDA
    if modo in [modo_ejecucion.transformacion, modo_ejecucion.completo]:
        logger.info("ETAPA 2: TRANSFORMACIÓN (T) + EDA...")
        df_limpio = procesar_caracteristicas(archivo_raw="new_retail_data.csv")
        
        if df_limpio is not None:
            logger.info("Generando Análisis Exploratorio de Datos (EDA)...")
            ejecutar_graficacion(df_limpio)
            # Se guarda el DF en el contexto del script para carga posterior si es modo completo
            globals()['_df_limpio_cache'] = df_limpio
        else:
            logger.error("No se pudo completar la transformación.")
            raise typer.Exit(code=1)

    # 3. CARGA (L)
    if modo in [modo_ejecucion.carga, modo_ejecucion.completo]:
        logger.info("ETAPA 3: CARGA (L)...")
        
        # Se obtiene el DF del cache si venimos del modo completo
        df_para_cargar = globals().get('_df_limpio_cache')
        
        # Si se ejecuta 'carga' por separado, se lee el CSV procesado o se transforma de nuevo
        if df_para_cargar is None:
            logger.info("Modo carga independiente: recuperando datos...")
            df_para_cargar = procesar_caracteristicas(archivo_raw="new_retail_data.csv")

        if df_para_cargar is not None:
            # L en CSV
            if not archivo_csv_procesado.parent.exists():
                archivo_csv_procesado.parent.mkdir(parents=True, exist_ok=True)
            df_para_cargar.to_csv(archivo_csv_procesado, index=False)
            logger.success(f"Archivo CSV guardado en: {archivo_csv_procesado}")
            
            # L en Base de Datos
            guardar_datos_db(df_para_cargar, nombre_db=bd_ventas)
        else:
            logger.error("No hay datos disponibles para cargar.")
            raise typer.Exit(code=1)

    logger.success(f"Pipeline ejecutado correctamente en modo: {modo.value}")

# Ejecución del script
if __name__ == "__main__":
    app()