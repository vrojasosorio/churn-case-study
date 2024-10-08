import os
import random
import string
from datetime import timedelta

import mysql.connector
from dotenv import load_dotenv
from faker import Faker

# Lista de regiones de Chile
regiones_chile = [
    "Arica y Parinacota", "Tarapacá", "Antofagasta", "Atacama", "Coquimbo",
    "Valparaíso", "Metropolitana de Santiago", "Libertador General Bernardo O'Higgins",
    "Maule", "Ñuble", "Biobío", "La Araucanía", "Los Ríos", "Los Lagos",
    "Aysén del General Carlos Ibáñez del Campo", "Magallanes y de la Antártica Chilena"
]

load_dotenv()
fake = Faker('es_CL')

db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

# Crear una única conexión para todo el script
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()


def run_query(query, params=None):
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        conn.rollback()
        raise


def generate_unique_id():
    return fake.unique.random_number(digits=8)


def generate_table_a(num_records):
    for _ in range(num_records):
        col_a1 = generate_unique_id()
        col_a2 = fake.uuid4()
        col_a3 = fake.random_int(min=1, max=100)
        col_a4 = fake.random_int(min=1, max=50)
        col_a5 = fake.date_time_between(start_date='-5y', end_date='now')

        query = """
        INSERT INTO table_a (col_a1, col_a2, col_a3, col_a4, col_a5)
        VALUES (%s, %s, %s, %s, %s)
        """
        run_query(query, (col_a1, col_a2, col_a3, col_a4, col_a5))


def generate_table_b():
    query = "SELECT col_a1 FROM table_a"
    cursor.execute(query)
    col_a1_list = [row[0] for row in cursor.fetchall()]

    for col_a1 in col_a1_list:
        col_b1 = fake.uuid4()
        col_b3 = fake.company_suffix()
        col_b4 = fake.job()
        col_b5 = fake.city()

        query = """
        INSERT INTO table_b (col_b1, col_b2, col_b3, col_b4, col_b5)
        VALUES (%s, %s, %s, %s, %s)
        """
        run_query(query, (col_b1, col_a1, col_b3, col_b4, col_b5))


def generate_table_c(num_records):
    for _ in range(num_records):
        col_c1 = generate_unique_id()
        col_c2 = fake.street_address()
        col_c3 = fake.city()
        col_c4 = fake.word()
        col_c5 = random.choice(regiones_chile)
        col_c6 = random.choice(['Type A', 'Type B', 'Type C'])
        col_c7 = random.choice([True, False])
        col_c8 = fake.date_time_this_decade() if not col_c7 else None
        col_c9 = float(fake.latitude())
        col_c10 = float(fake.longitude())

        query = """
        INSERT INTO table_c (col_c1, col_c2, col_c3, col_c4, col_c5, col_c6, col_c7, col_c8, col_c9, col_c10)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        run_query(query, (col_c1, col_c2, col_c3, col_c4, col_c5, col_c6, col_c7, col_c8, col_c9, col_c10))


def generate_table_d():
    query = "SELECT col_a1 FROM table_a"
    cursor.execute(query)
    col_a1_list = [row[0] for row in cursor.fetchall()]

    for col_d1 in col_a1_list:
        col_d2 = random.randint(1, 5)
        col_d3 = fake.date_time_this_year()
        col_d4 = fake.date_time_between(start_date='-5y', end_date=col_d3)
        col_d5 = random.randint(1, 3)

        query = """
        INSERT INTO table_d (col_d1, col_d2, col_d3, col_d4, col_d5)
        VALUES (%s, %s, %s, %s, %s)
        """
        run_query(query, (col_d1, col_d2, col_d3, col_d4, col_d5))


def generate_table_e(num_users_per_account):
    query = "SELECT col_d1 FROM table_d"
    cursor.execute(query)
    col_d1_list = [row[0] for row in cursor.fetchall()]

    for col_e2 in col_d1_list:
        for _ in range(num_users_per_account):
            col_e1 = generate_unique_id()
            col_e3 = random.randint(1, 5)
            col_e4 = fake.date_time_between(start_date='-2y', end_date='now')
            col_e5 = fake.date_time_between(start_date=col_e4, end_date='now')

            query = """
            INSERT INTO table_e (col_e1, col_e2, col_e3, col_e4, col_e5)
            VALUES (%s, %s, %s, %s, %s)
            """
            run_query(query, (col_e1, col_e2, col_e3, col_e4, col_e5))


def generate_unique_col_f1():
    letters = ''.join(random.choices(string.ascii_uppercase, k=2))
    numbers = ''.join(random.choices(string.digits, k=4))
    return f"{letters}{numbers}"


def generate_table_f(num_records):
    generated_col_f1 = set()

    for _ in range(num_records):
        while True:
            col_f1 = generate_unique_col_f1()
            if col_f1 not in generated_col_f1:
                generated_col_f1.add(col_f1)
                break

        col_f2 = random.randint(1, 5)

        query = """
        INSERT INTO table_f (col_f1, col_f2)
        VALUES (%s, %s)
        """
        try:
            run_query(query, (col_f1, col_f2))
        except mysql.connector.IntegrityError as e:
            if e.errno == 1062:  # Código de error para entrada duplicada
                print(f"Duplicate entry found: {col_f1}. Skipping and generating a new one.")
                continue
            else:
                raise

    print(f"Successfully generated {len(generated_col_f1)} unique records for table_f.")


def generate_table_g():
    query = "SELECT col_d1 FROM table_d"
    cursor.execute(query)
    col_d1_list = [row[0] for row in cursor.fetchall()]

    query = "SELECT col_f1 FROM table_f"
    cursor.execute(query)
    col_f1_list = [row[0] for row in cursor.fetchall()]

    for col_g1 in col_d1_list:
        num_vehicles = random.randint(1, 3)
        for _ in range(num_vehicles):
            col_g2 = generate_unique_id()
            col_g3 = fake.random_letter()
            col_g4 = random.randint(1, 5)
            col_g5 = fake.company()
            col_g6 = random.randint(1, 3)
            col_g7 = fake.word()
            col_g8 = fake.date_time_between(start_date='-3y', end_date='now')
            col_g9 = fake.date_time_between(start_date=col_g8, end_date='now')
            col_g10 = random.choice(col_f1_list)

            query = """
            INSERT INTO table_g (col_g1, col_g2, col_g3, col_g4, col_g5, col_g6, col_g7, col_g8, col_g9, col_g10)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            run_query(query, (col_g1, col_g2, col_g3, col_g4, col_g5, col_g6, col_g7, col_g8, col_g9, col_g10))


def generate_table_h():
    query = "SELECT col_e1, col_e2 FROM table_e"
    cursor.execute(query)
    col_e_list = cursor.fetchall()

    query = "SELECT col_g1, col_g2 FROM table_g"
    cursor.execute(query)
    col_g_list = cursor.fetchall()

    for col_h1, col_h2 in col_e_list:
        for col_g1, col_h3 in col_g_list:
            if col_h2 == col_g1:
                col_h4 = random.choice([0, 1])
                col_h5 = fake.date_time_between(start_date='-1y', end_date='now')

                query = """
                INSERT INTO table_h (col_h1, col_h2, col_h3, col_h4, col_h5)
                VALUES (%s, %s, %s, %s, %s)
                """
                run_query(query, (col_h1, col_h2, col_h3, col_h4, col_h5))


def generate_table_i(num_transactions):
    query = "SELECT col_e1, col_e2 FROM table_e"
    cursor.execute(query)
    col_e_list = cursor.fetchall()

    query = "SELECT col_f1 FROM table_f"
    cursor.execute(query)
    col_f1_list = [row[0] for row in cursor.fetchall()]

    # Definir una fecha de inicio para las transacciones
    start_date = fake.date_time_between(start_date='-2y', end_date='now')

    for _ in range(num_transactions):
        col_i1 = generate_unique_id()
        col_i3, col_i2 = random.choice(col_e_list)
        col_i4 = random.randint(1, 10)  # Ampliado el rango de formas de pago
        col_i5 = fake.uuid4()
        col_i6 = fake.uuid4()

        # Generar montos con mayor variabilidad
        base_amount = random.randint(1000, 500000)  # Ampliado el rango
        col_i7 = int(base_amount * random.uniform(0.8, 1.2))  # Añadir variabilidad

        col_i8 = random.choice(['Type X', 'Type Y', 'Type Z'])  # Añadido un tipo más
        col_i9 = random.randint(1, 5)  # Ampliado el rango

        # Añadir variabilidad al monto total
        col_i10 = int(col_i7 * random.uniform(0.95, 1.05))

        # Generar fechas con mayor variabilidad
        days_offset = random.randint(0, 730)  # Hasta 2 años de offset
        col_i11 = start_date + timedelta(days=days_offset)

        # Añadir variabilidad entre fechas
        time_diff = timedelta(minutes=random.randint(0, 60))
        col_i12 = col_i11 + time_diff
        col_i13 = col_i12 + timedelta(minutes=random.randint(1, 30))

        col_i14 = fake.word()
        col_i15 = fake.word()
        col_i16 = random.choice(col_f1_list)

        # Ocasionalmente, generar transacciones con montos muy altos o muy bajos
        if random.random() < 0.05:  # 5% de las transacciones
            if random.choice([True, False]):
                col_i7 = random.randint(500000, 1000000)  # Monto muy alto
            else:
                col_i7 = random.randint(100, 999)  # Monto muy bajo
            col_i10 = col_i7  # Igualar el monto total al monto pagado en estos casos especiales

        query = """
        INSERT INTO table_i (col_i1, col_i2, col_i3, col_i4, col_i5, col_i6, col_i7, col_i8, col_i9, col_i10,
                             col_i11, col_i12, col_i13, col_i14, col_i15, col_i16)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        run_query(query, (col_i1, col_i2, col_i3, col_i4, col_i5, col_i6, col_i7, col_i8, col_i9, col_i10,
                          col_i11, col_i12, col_i13, col_i14, col_i15, col_i16))

    print(f"Generated {num_transactions} records for table_i")


def generate_table_j():
    products = ['Product A', 'Product B', 'Product C', 'Product D', 'Product E']

    query = "SELECT col_i1, col_i12 FROM table_i"
    cursor.execute(query)
    col_i_list = cursor.fetchall()

    for col_j1, col_j12 in col_i_list:
        num_products = random.randint(1, 3)
        for col_j2 in range(1, num_products + 1):
            col_j3 = random.randint(1, len(products))
            col_j4 = random.randint(1, 50)
            col_j5 = random.randint(1000, 50000)
            col_j6 = products[col_j3 - 1]
            col_j7 = random.choice(['Normal', 'Discount', 'Promotion'])
            col_j8 = col_j12
            col_j9 = random.randint(0, 1000)
            col_j10 = col_j5 // col_j4
            col_j11 = col_j9 // col_j4

            query = """
            INSERT INTO table_j (col_j1, col_j2, col_j3, col_j4, col_j5, col_j6, col_j7, col_j8, col_j9, col_j10, col_j11, col_j12)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            run_query(query, (
                col_j1, col_j2, col_j3, col_j4, col_j5, col_j6, col_j7, col_j8, col_j9, col_j10, col_j11, col_j12))


def generate_all_data():
    print("Starting data generation...")

    num_accounts = 1000
    num_stations = 50
    num_users_per_account = 3
    num_vehicles = 5000
    num_transactions = 100000

    try:
        print("Generating table_a...")
        generate_table_a(num_accounts)

        print("Generating table_b...")
        generate_table_b()

        print("Generating table_c...")
        generate_table_c(num_stations)

        print("Generating table_d...")
        generate_table_d()

        print("Generating table_e...")
        generate_table_e(num_users_per_account)

        print("Generating table_f...")
        generate_table_f(num_vehicles)

        print("Generating table_g...")
        generate_table_g()

        print("Generating table_h...")
        generate_table_h()

        print("Generating table_i...")
        generate_table_i(num_transactions)

        print("Generating table_j...")
        generate_table_j()

        print("Data generation completed.")
    except Exception as e:
        print(f"An error occurred during data generation: {e}")
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    generate_all_data()
