import psycopg2
from contextlib import closing

db_params = "dbname=planeta_zdorovo user=postgres password=qwerty host=localhost port=5432"
def insert_into_product(product_id, product_name, product_brand, product_section,
                        product_manufacturer, product_manufactured, product_release, product_age, product_count_in_package, product_active_ingredients):
    with closing(psycopg2.connect(db_params)) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO PRODUCT (ID, NAME, BRAND, SECTION, MANUFACTURER, MANUFACTURED, RELEASE, AGE, COUNT_IN_PACKAGE, ACTIVE_INGREDIENTS) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (ID) 
                DO NOTHING;
            """, (product_id, product_name, product_brand, product_section,
                  product_manufacturer, product_manufactured, product_release, product_age, product_count_in_package, product_active_ingredients))
            conn.commit()


def update_table_product_links(product_id, links):
    with closing(psycopg2.connect(db_params)) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE PRODUCT_LINKS 
                SET product_id = %s
                WHERE link = %s;
            """, (product_id, links))
            conn.commit()


def insert_into_price_history(product_id, price):
    with closing(psycopg2.connect(db_params)) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO PRICE_HISTORY (PRODUCT_ID, PRICE) 
                VALUES (%s, %s);
            """, (product_id, price))
            conn.commit()


def insert_links_to_db(links):
    with closing(psycopg2.connect(db_params)) as conn:
        with conn.cursor() as cur:
            for link in links:
                # Проверяем, есть ли ссылка уже в базе данных
                cur.execute("SELECT link FROM product_links WHERE link = %s", (link,))
                if cur.fetchone() is None:
                    # Если ссылки нет в базе данных, добавляем ее
                    cur.execute("INSERT INTO product_links (link) VALUES (%s)", (link,))
                conn.commit()


def get_links_from_db():
    with closing(psycopg2.connect(db_params)) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT link FROM product_links")
            links = [row[0] for row in cur.fetchall()]
    return links
