from Parsing.parsing_product import parse_product_data_selenium
from database.job_database import insert_into_product, insert_into_price_history, \
    update_table_product_links, get_links_from_db


def main():

    products_data = parse_product_data_selenium(urls=get_links_from_db())

    for (product_id, product_name, product_price, product_brand, product_section, product_manufactured,
         product_manufacturer,  product_release, product_age, product_count_in_package, product_active_ingredients, links)\
            in products_data:

        insert_into_product(product_id, product_name, product_brand, product_section,
                            product_manufacturer, product_manufactured, product_release, product_age,
                            product_count_in_package, product_active_ingredients)
        update_table_product_links(product_id, links)

        insert_into_price_history(product_id, product_price)


if __name__ == "__main__":
    main()



