from parsing import parse_product_data_selenium
from data_base import create_database, insert_into_product, create_product_table, create_price_history_table, \
    insert_into_price_history
import schedule
import time

def job():
    print("I'm working...")
    url = "https://planetazdorovo.ru/ekaterinburg/catalog/lekarstva-i-bad/prostuda-i-gripp/nasmork/akvalor-soft-sredstvo-dlya-nosa-18348311/"
    product_id, product_name, product_price, product_brand = parse_product_data_selenium(url)

    insert_into_product(product_id, product_name, product_brand)
    insert_into_price_history(product_id, product_price)
    print("обновлено")
def main():
    # Запуск задания каждый час
    schedule.every(1).minutes.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
