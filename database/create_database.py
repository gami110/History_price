import psycopg2
from psycopg2 import sql, Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def create_database():
    conn = psycopg2.connect(database="postgres", user="postgres", password="qwerty", host="localhost", port="5432")
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

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


def create_product_link_table():
    try:
        conn = psycopg2.connect(database="planeta_zdorovo", user="postgres", password="qwerty", host="localhost", port="5432")
    except Error as e:
        print(f"Ошибка при подключении к базе данных: {e}")
        exit(1)
    cur = conn.cursor()
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS product_links (
                id SERIAL PRIMARY KEY, 
                link TEXT);
        """)
        conn.commit()
    except Error as e:
        print(f"Ошибка при создании таблицы: {e}")
        exit(1)
