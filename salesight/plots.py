# Se importan las librerías para visualización y análisis de datos
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from loguru import logger
import typer
from salesight.config import ruta_graficos, NOMBRE_DB
from salesight.dataset import obtener_datos_db

# Configuración de la CLI
app = typer.Typer()

def formato_moneda(x, pos):
    """
    Función para formatear los números del eje como dinero.
    """
    if x >= 1_000_000:
        return f'${x*1e-6:1.1f}M'
    return f'${x:,.0f}'

def ejecutar_graficacion(df: pd.DataFrame):
    """
    Fase de Visualización Lógica (EDA) que exporta los gráficos a reports/figures en formato png
    """

    # Si no existe la ruta, la crea
    if not ruta_graficos.exists():
        ruta_graficos.mkdir(parents=True, exist_ok=True)

    logger.info(f"Generando visualizaciones en: {ruta_graficos}...")

    # Configuración de estilo global
    sns.set_theme(style="whitegrid")
    plt.rcParams['figure.autolayout'] = True
    formateador = ticker.FuncFormatter(formato_moneda)

    # 1. Ventas por Categoría
    col_cat = 'Product' if 'Product' in df.columns else 'Product_Category'
    # Verificación de si existe la columna de cantidad vendida
    if col_cat in df.columns and 'Total_Amount' in df.columns:
        # Características de la gráfica
        plt.figure(figsize=(10, 6))
        ventas_cat = df.groupby(col_cat)['Total_Amount'].sum().sort_values(ascending=True)
        ax = ventas_cat.plot(kind='barh', color='steelblue')
        ax.xaxis.set_major_formatter(formateador) 
        plt.title(f'Ingresos Totales por {col_cat}', fontsize=14)
        plt.xlabel('Ventas ($)')
        plt.ylabel(col_cat)

        # Guardado del gráfico en la ruta de destino
        plt.savefig(ruta_graficos / "ventas_por_categoria.png")
        plt.close()
        logger.info("Guardado: ventas_por_categoria.png")


    # 2. Perfil del Cliente: Ingresos y Género

    # Verificación de si existen la columnas de ingresos y género
    if 'Income' in df.columns and 'Gender' in df.columns:
        # Características de la gráfica
        plt.figure(figsize=(10, 6))
        sns.countplot(x='Income', hue='Gender', data=df, palette='muted')
        plt.title('Perfil del Cliente: Nivel de Ingreso y Género', fontsize=14)
        plt.xlabel('Nivel de Ingreso')
        plt.ylabel('Cantidad de Clientes')

        # Guardado del gráfico en la ruta de destino
        plt.savefig(ruta_graficos / "perfil_cliente_ingresos.png")
        plt.close()
        logger.info("Guardado: perfil_cliente_ingresos.png")


    # 3. Preferencia de Métodos de Pago

    # Verificación de si existe la columna de métodos de pago
    if 'Payment_Method' in df.columns:
        # Características de la gráfica
        plt.figure(figsize=(8, 8))
        pagos = df['Payment_Method'].value_counts()
        pagos.plot(kind='pie', autopct='%1.1f%%', colormap='Pastel1', startangle=90)
        plt.title('Distribución de Métodos de Pago', fontsize=14)
        plt.ylabel('')
        # Guardado del gráfico en la ruta de destino
        plt.savefig(ruta_graficos / "preferencia_metodos_pago.png")
        plt.close()
        logger.info("Guardado: preferencia_metodos_pago.png")


    # 4. Tendencia de Ventas Mensuales

    # Verificación de si existen la columnas de fecha de orden y total comprado
    if 'Date' in df.columns and 'Total_Amount' in df.columns:
        plt.figure(figsize=(12, 6))
        # Validación de que sea datetime para extraer el nombre del mes
        df_temp = df.copy()
        if not pd.api.types.is_datetime64_any_dtype(df_temp['Date']):
            df_temp['Date'] = pd.to_datetime(df_temp['Date'])
        
        # Características del gráfico
        df_temp['Month_Name'] = df_temp['Date'].dt.month_name()
        orden_meses = ['January', 'February', 'March', 'April', 'May', 'June', 
                       'July', 'August', 'September', 'October', 'November', 'December']
        df_temp['Month_Name'] = pd.Categorical(df_temp['Month_Name'], categories=orden_meses, ordered=True)
        tendencia = df_temp.groupby('Month_Name', observed=True)['Total_Amount'].sum()
        ax = tendencia.plot(kind='line', marker='o', color='forestgreen', linewidth=2)
        ax.yaxis.set_major_formatter(formateador)
        plt.title('Tendencia Histórica de Ventas Mensuales', fontsize=14)
        plt.xlabel('Mes')
        plt.ylabel('Ventas Totales ($)')
        plt.grid(True, linestyle='--', alpha=0.7)

        # Guardado del gráfico en la ruta de destino
        plt.savefig(ruta_graficos / "tendencia_mensual_ventas.png")
        plt.close()
        logger.info("Guardado: tendencia_mensual_ventas.png")


    # 5. Top 5 Países por Ventas

    # Valicación de si existen las columnas de país y valor de compra
    if 'Country' in df.columns and 'Total_Amount' in df.columns:
        # Características del gráfico
        plt.figure(figsize=(10, 6))
        paises = df.groupby('Country')['Total_Amount'].sum().nlargest(5).sort_values(ascending=True)
        ax = paises.plot(kind='barh', color='salmon')
        ax.xaxis.set_major_formatter(formateador)
        plt.title('Top 5 Países con Mayor Facturación', fontsize=14)
        plt.xlabel('Ventas Totales ($)')
        plt.ylabel('País')

        # Guardado del gráfico en la ruta de destino
        plt.savefig(ruta_graficos / "top_paises_ventas.png")
        plt.close()
        logger.info("Guardado: top_paises_ventas.png")

    logger.success(f"¡Éxito! Gráficos monetarios generados correctamente en {ruta_graficos}.")


# Conversión de función a comando de CLI
@app.command()
def generar_reporte_visual(nombre_bd: str = NOMBRE_DB):
    """
    Comando para generar el reporte desde la base de datos.
    """
    df = obtener_datos_db(nombre_bd)
    if df is not None:
        ejecutar_graficacion(df)
    else:
        logger.error("No hay datos para graficar.")
        raise typer.Exit(code=1)


# Ejecución del script
if __name__ == "__main__":
    app()