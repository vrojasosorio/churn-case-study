import os
import yaml
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
    'database': os.getenv('DB_NAME'),
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci'
}

# Parámetros de churn
churn_params = {
    'dias_sin_compra': 10,
    'monto_minimo': 225000,
    'frecuencia_minima': 85
}

# Load column mapping
with open('column_mapping.yaml', 'r') as file:
    column_mapping = yaml.safe_load(file)


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

    columnas_nuevas = [column for column in df.columns if column not in columnas_originales]

    print("\nColumnas originales de la base de datos:")
    print(columnas_originales)

    print("\nColumnas creadas durante el análisis:")
    print(columnas_nuevas)

    print("\nResumen de todas las columnas:")
    print(df.info())

    return df


def analyze_customer_profile():
    query = """
    SELECT *
    FROM table_a
    LIMIT 1000
    """
    df = run_query(query)

    print("\nAnálisis del perfil del cliente:")
    print(f"Número total de clientes: {len(df)}")
    print(f"Fecha de registro más antigua: {df['col_a5'].min()}")
    print(f"Fecha de registro más reciente: {df['col_a5'].max()}")

    plt.figure(figsize=(12, 6))
    df['col_a5'] = pd.to_datetime(df['col_a5'])
    df['col_a5'].hist(bins=50)
    plt.title('Distribución de Fechas de Registro de Clientes')
    plt.xlabel('Fecha de Registro')
    plt.ylabel('Número de Clientes')
    plt.tight_layout()
    plt.show()


def analyze_service_points():
    query = """
    SELECT *
    FROM table_c
    """
    df = run_query(query)

    print("\nAnálisis de puntos de servicio:")
    print(f"Número total de puntos de servicio: {len(df)}")
    print(f"Número de puntos de servicio activos: {df['col_c7'].sum()}")
    print(f"Número de puntos de servicio inactivos: {len(df) - df['col_c7'].sum()}")

    plt.figure(figsize=(10, 6))
    df['col_c5'].value_counts().plot(kind='bar')
    plt.title('Distribución de Puntos de Servicio por Región')
    plt.xlabel('Región')
    plt.ylabel('Número de Puntos de Servicio')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def analyze_asset_types():
    query = """
    SELECT f.col_f2 as asset_type, COUNT(*) as count
    FROM table_f f
    JOIN table_g g ON f.col_f1 = g.col_g10
    GROUP BY f.col_f2
    ORDER BY count DESC
    """
    df = run_query(query)

    print("\nAnálisis de tipos de activos:")
    print(df)

    plt.figure(figsize=(10, 6))
    sns.barplot(x='count', y='asset_type', data=df)
    plt.title('Distribución de Tipos de Activos')
    plt.xlabel('Número de Activos')
    plt.ylabel('Tipo de Activo')
    plt.tight_layout()
    plt.show()


def analyze_transaction_details():
    query = """
    SELECT 
        i.col_i8 as document_type,
        i.col_i14 as payment_method,
        AVG(i.col_i10) as avg_transaction_value,
        COUNT(*) as transaction_count
    FROM table_i i
    GROUP BY i.col_i8, i.col_i14
    ORDER BY transaction_count DESC
    """
    df = run_query(query)

    print("\nAnálisis de detalles de transacciones:")
    print(df)

    plt.figure(figsize=(12, 6))
    sns.scatterplot(data=df, x='avg_transaction_value', y='transaction_count',
                    hue='document_type', size='transaction_count', sizes=(20, 200))
    plt.title('Relación entre Valor Promedio de Transacción y Número de Transacciones')
    plt.xlabel('Valor Promedio de Transacción')
    plt.ylabel('Número de Transacciones')
    plt.tight_layout()
    plt.show()


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

    # Nuevos análisis
    analyze_customer_profile()
    analyze_service_points()
    analyze_asset_types()
    analyze_transaction_details()

    # Imprimir el mapeo de columnas para referencia
    print("\nMapeo de columnas:")
    for table, columns in column_mapping.items():
        print(f"\nTabla: {table}")
        for col, description in columns.items():
            print(f"  {col}: {description}")
