import psycopg2
from psycopg2 import Error


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


def insert_into_price_history(product_id, price):
    conn = psycopg2.connect(database="planeta_zdorovo", user="postgres", password="qwerty", host="localhost", port="5432")
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO PRICE_HISTORY (PRODUCT_ID, PRICE) 
        VALUES (%s, %s);
    """, (product_id, price))

    conn.commit()
    conn.close()


def insert_links_to_db(links):
    try:
        conn = psycopg2.connect(
            database="planeta_zdorovo", user="postgres", password="qwerty", host="localhost", port="5432"
        )
    except Error as e:
        print(f"Ошибка при подключении к базе данных: {e}")
        exit(1)

    cur = conn.cursor()
    for link in links:
        # Проверяем, есть ли ссылка уже в базе данных
        try:
            cur.execute("SELECT link FROM product_links WHERE link = %s", (link,))
            if cur.fetchone() is None:
                # Если ссылки нет в базе данных, добавляем ее
                cur.execute("INSERT INTO product_links (link) VALUES (%s)", (link,))
            conn.commit()
        except Error as e:
            print(f"Ошибка при добавлении ссылки в базу данных: {e}")

def get_links_from_db():
    with psycopg2.connect(
        dbname='planeta_zdorovo',
        user='postgres',
        password='qwerty',
        host='localhost',
        port="5432"
    ) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT link FROM product_links")
            links = [row[0] for row in cur.fetchall()]
    return links