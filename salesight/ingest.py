# Se importan las librerías que se usarán en la ingesta
import zipfile
import os
from pathlib import Path
from kaggle.api.kaggle_api_extended import KaggleApi
from loguru import logger
import typer
from salesight.config import datos_brutos

# Configuración de la CLI
app = typer.Typer()

@app.command()
def descargar_datos(
    dataset_kaggle: str = "sahilprajapati143/retail-analysis-large-dataset",
    carpeta_destino: Path = datos_brutos
):
    """
    Fase de Extracción (ingesta) (E)
    """
    logger.info(f"Iniciando descarga de {dataset_kaggle}.")

    # Si no existe la carpeta de destino, la crea
    if not carpeta_destino.exists():
        carpeta_destino.mkdir(parents=True, exist_ok=True)

    # Se autentica en Kaggle para descargar el dataset
    try:
        api = KaggleApi()
        api.authenticate()
        logger.success("Conexión con Kaggle exitosa.")
    except Exception as e:
        logger.error(f"Fallo en la autenticación: {e}")
        raise typer.Exit(code=1)
    
    # Realiza la descarga de los datos
    logger.info(f"Bajando archivos...")
    try:
        api.dataset_download_files(dataset_kaggle, path=str(carpeta_destino), unzip=False)
    except Exception as e:
        logger.error(f"Fallo en la descarga: {e}")
        raise typer.Exit(code=1)

    # Crea una lista con los archivos ZIP que encuentra
    comprimidos = list(carpeta_destino.glob("*.zip"))

    # Si hay zips
    if comprimidos:
        # Se toma el último zip agregado
        archivo_zip = sorted(comprimidos, key=os.path.getmtime)[-1]
        logger.info(f"Descomprimiendo {archivo_zip.name}...")

        # Extrae los datos y elimina el .zip
        try:
            with zipfile.ZipFile(archivo_zip, 'r') as ref:
                ref.extractall(carpeta_destino)
                logger.success(f"Archivos extraídos: {ref.namelist()}")
            
            archivo_zip.unlink()
            logger.info("Archivo ZIP eliminado.")
        except Exception as e:
            logger.error(f"Error en la extracción: {e}")
            raise typer.Exit(code=1)
    else:
        logger.warning("No se encontró el archivo ZIP descargado.")


# Ejecución del script
if __name__ == "__main__":
    app()