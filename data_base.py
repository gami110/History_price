import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def create_database():
    conn = psycopg2.connect(database="postgres", user="postgres", password="qwerty", host="localhost", port="5432")
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    # Проверяем, существует ли база данных
    cur.execute("SELECT datname FROM pg_database;")
    list_database = cur.fetchall()
    if ('planeta_zdorovo',) in list_database:
        print('Database already exists')
    else:
        cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier("planeta_zdorovo")))

    conn.close()


def create_product_table():
    conn = psycopg2.connect(database="planeta_zdorovo", user="postgres", password="qwerty", host="localhost", port="5432")
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS PRODUCT
        (ID INT PRIMARY KEY,
        NAME           TEXT    NOT NULL,
        BRAND          TEXT);
    ''')

    conn.commit()
    conn.close()


def insert_into_product(product_id, product_name, product_brand):
    conn = psycopg2.connect(database="planeta_zdorovo", user="postgres", password="qwerty", host="localhost", port="5432")
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO PRODUCT (ID, NAME, BRAND) 
        VALUES (%s, %s, %s)
        ON CONFLICT (ID) 
        DO NOTHING;
    """, (product_id, product_name, product_brand))

    conn.commit()
    conn.close()


def create_price_history_table():
    conn = psycopg2.connect(database="planeta_zdorovo", user="postgres", password="qwerty", host="localhost", port="5432")
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS PRICE_HISTORY
        (ID SERIAL PRIMARY KEY,
        PRODUCT_ID INT NOT NULL,
        PRICE REAL,
        DATE TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP);
    ''')

    conn.commit()
    conn.close()


def insert_into_price_history(product_id, price):
    conn = psycopg2.connect(database="planeta_zdorovo", user="postgres", password="qwerty", host="localhost", port="5432")
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO PRICE_HISTORY (PRODUCT_ID, PRICE) 
        VALUES (%s, %s);
    """, (product_id, price))

    conn.commit()
    conn.close()
