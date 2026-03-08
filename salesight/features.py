# Se importan las librerías que se usarán en la transformación
import pandas as pd
from pathlib import Path
from loguru import logger
import typer
from salesight.config import datos_procesados, NOMBRE_DB
from salesight.dataset import obtener_datos_raw, guardar_datos_db

# Configuración de la CLI
app = typer.Typer()

# Conversión de función a comando CLI
@app.command()
def procesar_caracteristicas(
    archivo_raw: str = "new_retail_data.csv"
):
    """
    Fase de Transformación (T) que retorna el DataFrame procesado.
    """
    logger.info(f"Iniciando transformación de datos...\n")

    # Obtiene los datos y si no  puede, lanza error.
    df = obtener_datos_raw(archivo_raw)
    if df is None:
        logger.error("No se pudieron cargar los datos para transformar.\n")
        return None

    # Elimina los registros nulos y convierte en numérico los registros de cantidad, precio y ventas
    df = df.dropna(how='all')
    columnas_num = ['Total_Purchases', 'Amount', 'Total_Amount']
    for col in columnas_num:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Imputación
    for col in columnas_num:
        if col in df.columns and df[col].isnull().any():
            df[col] = df.groupby('Product_Type')[col].transform(lambda x: x.fillna(x.median()) if not x.median() is None else x)
            df[col] = df[col].fillna(df[col].median())
    
    # Si hay Product_Typeos nulos, solo lo coloca como desconocido
    if 'Product_Type' in df.columns and df['Product_Type'].isnull().any():
        df['Product_Type'] = df['Product_Type'].fillna('Unknown')

    # Fechas
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df = df.dropna(subset=['Date'])
        df['Date'] = df['Date'].dt.date

    logger.success(f"Transformación (T) completada. Registros: {len(df)}\n")
    return df


# Ejecución del script
if __name__ == "__main__":
    app()
