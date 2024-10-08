import os
from datetime import timedelta

import matplotlib.pyplot as plt
import mysql.connector
import pandas as pd
import seaborn as sns
from dotenv import load_dotenv

load_dotenv()

# Database configuration
db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

# Parámetros de churn
churn_params = {
    'dias_sin_compra': 10,
    'monto_minimo': 225000,
    'frecuencia_minima': 85
}


def run_query(query):
    conn = mysql.connector.connect(**db_config)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def analyze_transactions_over_time():
    query = """
    SELECT DATE(col_i11) as fecha, COUNT(*) as num_transacciones, SUM(col_i10) as monto_total
    FROM table_i
    GROUP BY DATE(col_i11)
    ORDER BY fecha
    """
    df = run_query(query)
    df['fecha'] = pd.to_datetime(df['fecha'])

    plt.figure(figsize=(12, 6))
    plt.plot(df['fecha'], df['num_transacciones'])
    plt.title('Número de Transacciones por Día')
    plt.xlabel('Fecha')
    plt.ylabel('Número de Transacciones')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(12, 6))
    plt.plot(df['fecha'], df['monto_total'])
    plt.title('Monto Total de Transacciones por Día')
    plt.xlabel('Fecha')
    plt.ylabel('Monto Total')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def analyze_top_products():
    query = """
    SELECT col_j6 as producto_nombre, SUM(col_j4) as cantidad_total, SUM(col_j5) as monto_total
    FROM table_j
    GROUP BY col_j6
    ORDER BY cantidad_total DESC
    LIMIT 10
    """
    df = run_query(query)

    plt.figure(figsize=(12, 6))
    sns.barplot(x='cantidad_total', y='producto_nombre', data=df)
    plt.title('Top 10 Productos más Vendidos')
    plt.xlabel('Cantidad Total')
    plt.ylabel('Producto')
    plt.tight_layout()
    plt.show()


def analyze_customer_frequency():
    query = """
    SELECT col_i2 as cuenta_id, COUNT(*) as num_transacciones
    FROM table_i
    GROUP BY col_i2
    ORDER BY num_transacciones DESC
    LIMIT 20
    """
    df = run_query(query)

    plt.figure(figsize=(12, 6))
    sns.barplot(x='num_transacciones', y='cuenta_id', data=df)
    plt.title('Top 20 Clientes por Frecuencia de Compra')
    plt.xlabel('Número de Transacciones')
    plt.ylabel('ID de Cuenta')
    plt.tight_layout()
    plt.show()


def analyze_payment_methods():
    query = """
    SELECT col_i14 as tipo_forma_pago_nombre, COUNT(*) as num_transacciones
    FROM table_i
    GROUP BY col_i14
    """
    df = run_query(query)

    plt.figure(figsize=(10, 10))
    plt.pie(df['num_transacciones'], labels=df['tipo_forma_pago_nombre'], autopct='%1.1f%%')
    plt.title('Distribución de Formas de Pago')
    plt.axis('equal')
    plt.show()


def analyze_customer_churn(churn_params_x):
    query = """
    SELECT c.col_i2 as cuenta_id, 
           MAX(c.col_i11) as ultima_compra,
           COUNT(*) as num_transacciones,
           AVG(c.col_i10) as monto_promedio
    FROM table_i c
    GROUP BY c.col_i2
    """
    df = run_query(query)

    columnas_originales = df.columns.tolist()

    df['ultima_compra'] = pd.to_datetime(df['ultima_compra'])
    fecha_actual = df['ultima_compra'].max() + timedelta(days=1)
    df['dias_desde_ultima_compra'] = (fecha_actual - df['ultima_compra']).dt.days

    df['churn_por_tiempo'] = df['dias_desde_ultima_compra'] > churn_params_x['dias_sin_compra']
    df['churn_por_monto'] = df['monto_promedio'] < churn_params_x['monto_minimo']
    df['churn_por_frecuencia'] = df['num_transacciones'] < churn_params_x['frecuencia_minima']

    df['churned'] = (df['churn_por_tiempo'] | df['churn_por_monto'] | df['churn_por_frecuencia'])

    tasa_churn = df['churned'].mean()
    print(f"Tasa de churn de clientes: {tasa_churn:.2%}")

    plt.figure(figsize=(12, 6))
    sns.histplot(data=df, x='dias_desde_ultima_compra', bins=50, hue='churned')
    plt.title('Distribución de Días desde la Última Compra')
    plt.xlabel('Días desde la Última Compra')
    plt.ylabel('Número de Clientes')
    plt.axvline(x=churn_params_x['dias_sin_compra'], color='r', linestyle='--',
                label=f'Umbral de Churn ({churn_params_x["dias_sin_compra"]} días)')
    plt.legend()
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(12, 6))
    sns.scatterplot(data=df, x='monto_promedio', y='num_transacciones', hue='churned')
    plt.title('Relación entre Monto Promedio y Número de Transacciones')
    plt.xlabel('Monto Promedio')
    plt.ylabel('Número de Transacciones')
    plt.axhline(y=churn_params_x['frecuencia_minima'], color='r', linestyle='--',
                label=f'Umbral de Frecuencia ({churn_params_x["frecuencia_minima"]} transacciones)')
    plt.axvline(x=churn_params_x['monto_minimo'], color='g', linestyle='--',
                label=f'Umbral de Monto (${churn_params_x["monto_minimo"]})')
    plt.legend()
    plt.tight_layout()
    plt.show()

    razones_churn = {
        'Tiempo': df['churn_por_tiempo'].sum(),
        'Monto': df['churn_por_monto'].sum(),
        'Frecuencia': df['churn_por_frecuencia'].sum()
    }

    plt.figure(figsize=(10, 6))
    sns.barplot(x=list(razones_churn.keys()), y=list(razones_churn.values()))
    plt.title('Razones de Churn de Clientes')
    plt.xlabel('Razón')
    plt.ylabel('Número de Clientes')
    plt.tight_layout()
    plt.show()

    columnas_nuevas = [col for col in df.columns if col not in columnas_originales]

    print("\nColumnas originales de la base de datos:")
    print(columnas_originales)

    print("\nColumnas creadas durante el análisis:")
    print(columnas_nuevas)

    print("\nResumen de todas las columnas:")
    print(df.info())

    return df


if __name__ == "__main__":
    analyze_transactions_over_time()
    analyze_top_products()
    analyze_customer_frequency()
    analyze_payment_methods()
    df_churn = analyze_customer_churn(churn_params)

    print("\nSegmentación de clientes:")
    segmentos = df_churn.groupby('churned').agg({
        'monto_promedio': 'mean',
        'num_transacciones': 'mean',
        'dias_desde_ultima_compra': 'mean'
    })
    print(segmentos)
