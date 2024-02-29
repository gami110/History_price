from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc

from database.job_database import insert_links_to_db


def get_product_links_selenium(driver, page_number):
    url = f"https://planetazdorovo.ru/ekaterinburg/catalog/lekarstva-i-bad/prostuda-i-gripp/?PAGEN_1={page_number}&sort=name&city_code=ekaterinburg"
    driver.get(url)
    wait = WebDriverWait(driver, 5)

    try:
        product_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.item-card-labels')))
    except TimeoutException:
        product_elements = []

    product_links = [element.get_attribute('href') for element in product_elements]

    # Добавляем ссылки в базу данных
    insert_links_to_db(product_links)

    return product_links

options = uc.ChromeOptions()
options.headless = False
try:
    with uc.Chrome(options=options) as driver:
        page_number = 1
        while True:
            product_links = get_product_links_selenium(driver, page_number)
            if not product_links:  # Если на странице нет ссылок, значит, это последняя страница
                break
            page_number += 1
except Exception as e:
    print(f"Ошибка при парсинге страниц: {e}")