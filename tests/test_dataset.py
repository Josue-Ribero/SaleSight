import pytest
import pandas as pd
from salesight.dataset import guardar_datos_db, obtener_datos_db
from salesight.config import datos_procesados

def test_guardar_y_cargar_dataset(tmp_path):
    """
    Prueba que el guardado y la carga de datos en la base de datos 
    SQLite centralizada funcionen correctamente usando las columnas originales.
    """
    # Configuración: Crear un nombre de base de datos temporal y un DataFrame de prueba
    nombre_db_test = "test_ventas.db"
    
    # Usamos los nombres de columnas originales según tu implementación en features.py
    df_test = pd.DataFrame({
        'Product_Type': ['Producto A', 'Producto B'],
        'Total_Amount': [150.5, 300.75],
        'Date': pd.to_datetime(['2026-03-01', '2026-03-02'])
    })
    
    # Guardar los datos en la base de datos de prueba
    exito = guardar_datos_db(df_test, nombre_db=nombre_db_test)
    assert exito is True, "No se pudo guardar el DataFrame en la base de datos."
    
    # Cargar los datos desde la base de datos de prueba
    df_cargado = obtener_datos_db(nombre_db=nombre_db_test)
    
    # Comprobar que los datos cargados coinciden con los guardados
    assert df_cargado is not None, "El DataFrame cargado es nulo."
    assert len(df_cargado) == 2, "La cantidad de registros no coincide."
    
    # Verificación de que las columnas originales existan en el DF cargado
    assert 'Product_Type' in df_cargado.columns, "Falta la columna 'Product_Type'."
    assert 'Total_Amount' in df_cargado.columns, "Falta la columna 'Total_Amount'."
    assert 'Date' in df_cargado.columns, "Falta la columna 'Date'."
    
    # Borrar el archivo de la base de datos de prueba
    ruta_db = datos_procesados / nombre_db_test
    if ruta_db.exists():
        ruta_db.unlink()

def test_obtener_datos_db_no_existente():
    """
    Prueba que la función de carga maneje correctamente bases de datos que no existen.
    """
    df = obtener_datos_db(nombre_db="base_de_datos_inexistente.db")
    
    # Verificación
    assert df is None, "Debería retornar None si la base de datos no existe."
