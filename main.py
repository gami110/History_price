from Parsing.parsing_product import parse_product_data_selenium
from database.job_database import insert_into_product, insert_into_price_history

def main():
    # Парсим данные продуктов с каждого URL
    products_data = parse_product_data_selenium()

    # Добавляем данные каждого продукта в базу данных
    for product_id, product_name, product_price, product_brand in products_data:
        insert_into_product(product_id, product_name, product_brand)
        insert_into_price_history(product_id, product_price)

if __name__ == "__main__":
    main()
