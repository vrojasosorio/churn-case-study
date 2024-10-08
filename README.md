# churn-case-study

Este proyecto implica la generación de datos sintéticos para una base de datos y la realización de un Análisis Exploratorio de Datos (EDA) sobre los datos generados. El proyecto se estructura en dos partes principales: generación de datos y análisis de datos.

## Tabla de Contenidos
1. [Requisitos del Sistema](#requisitos-del-sistema)
2. [Estructura del Proyecto](#estructura-del-proyecto)
3. [Configuración](#configuración)
4. [Generación de Datos](#generación-de-datos)
5. [Esquema de la Base de Datos](#esquema-de-la-base-de-datos)
6. [Análisis Exploratorio de Datos](#análisis-exploratorio-de-datos)
7. [Análisis de Abandono (Churn)](#análisis-de-abandono-churn)

## Requisitos del Sistema

- Python 3.10
- Se recomienda el uso de un entorno virtual

## Estructura del Proyecto

El proyecto consta de los siguientes archivos principales:

- `schema.sql`: Define el esquema de la base de datos
- `column_mapping-example.yaml`: Proporciona un ejemplo de mapeo de los nombres de las columnas a sus significados
- `column_mapping.yaml`: Archivo que debe crear el usuario para el mapeo real de las columnas
- `.env.example`: Archivo de ejemplo de entorno para la configuración de la base de datos
- `data.py`: Script para generar datos sintéticos
- `eda.py`: Script para realizar el Análisis Exploratorio de Datos
- `requirements.txt`: Lista de dependencias del proyecto

## Configuración

1. Asegúrese de tener Python 3.10 instalado en su sistema.

2. Se recomienda crear y activar un entorno virtual antes de instalar las dependencias:
   ```
   python3.10 -m venv venv
   source venv/bin/activate  # En Windows use `venv\Scripts\activate`
   ```

3. Cree una base de datos MySQL llamada `dinoco_anon`.

4. Ejecute el script `schema.sql` para crear las tablas necesarias.

5. Copie `.env.example` a `.env` y actualícelo con sus credenciales de base de datos.

6. Cree un archivo `column_mapping.yaml` basado en `column_mapping-example.yaml`. Este archivo es crucial para mapear los nombres de las columnas en la base de datos a sus significados reales. Puede usar el archivo de ejemplo como plantilla y ajustarlo según sea necesario.

7. Instale las dependencias del proyecto utilizando el archivo `requirements.txt`:
   ```
   pip install -r requirements.txt
   ```

   Este comando instalará las siguientes dependencias:
   - Faker==30.3.0
   - mysql-connector-python==9.0.0
   - mysqlclient==2.2.4
   - python-dateutil==2.9.0.post0
   - six==1.16.0
   - typing_extensions==4.12.2
   - python-dotenv==1.0.1
   - pandas~=2.2.3
   - matplotlib~=3.9.2
   - seaborn~=0.13.2
   - PyYAML~=6.0.2
   - numpy~=2.1.2
   - scikit-learn~=1.5.2
   - lifelines~=0.29.0

## Generación de Datos

El script `data.py` genera datos sintéticos para todas las tablas de la base de datos. Aquí hay una visión general del proceso de generación de datos:

1. Genera perfiles de clientes (`table_a`)
2. Crea detalles de clientes (`table_b`)
3. Genera puntos de servicio (`table_c`)
4. Crea estados de cuentas de clientes (`table_d`)
5. Genera enlaces de cuentas de usuarios (`table_e`)
6. Crea un registro de activos (`table_f`)
7. Genera detalles de activos de clientes (`table_g`)
8. Crea enlaces usuario-activo (`table_h`)
9. Genera resúmenes de transacciones (`table_i`)
10. Crea líneas de artículos de transacciones (`table_j`)

Para generar los datos, ejecute:
```
python data.py
```

## Esquema de la Base de Datos

La base de datos consta de 10 tablas (de la a a la j) que representan varios aspectos de un negocio, incluyendo información del cliente, activos y transacciones. Consulte el archivo `schema.sql` para obtener estructuras detalladas de las tablas y relaciones.

## Análisis Exploratorio de Datos

El script `eda.py` realiza varios análisis sobre los datos generados:

1. **Transacciones a lo largo del tiempo**: Analiza el número y el monto total de transacciones por día.
2. **Productos principales**: Identifica los 10 productos más vendidos.
3. **Frecuencia de clientes**: Muestra los 20 principales clientes por frecuencia de compra.
4. **Métodos de pago**: Muestra la distribución de los métodos de pago utilizados.
5. **Abandono de clientes**: Analiza el abandono de clientes basado en el tiempo desde la última compra, el monto promedio de transacción y la frecuencia de compra.

Para ejecutar el EDA, ejecute:
```
python eda.py
```

## Análisis de Abandono (Churn)

El análisis de abandono se realiza utilizando los siguientes parámetros:

- Días sin compra: 10
- Monto mínimo: 225,000
- Frecuencia mínima: 85

El script calcula el abandono basado en estos parámetros y proporciona visualizaciones para entender los patrones de abandono.

---

Este README proporciona una visión general de la estructura y los procesos del proyecto. Para obtener información más detallada, consulte los archivos de script individuales y sus comentarios.