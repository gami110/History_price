import undetected_chromedriver as uc
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from database.job_database import get_links_from_db


def parse_product_data_selenium():
    urls = get_links_from_db()
    options = uc.ChromeOptions()
    options.headless = False
    driver = uc.Chrome(options=options)
    wait = WebDriverWait(driver, 10)

    products_data = []
    for url in urls:
        driver.get(url)

        try:
            product_element = wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, 'div[data-id]')))

            product_id = product_element.get_attribute('data-id')
            product_name = product_element.get_attribute('data-name')
            product_price = product_element.get_attribute('data-price')
            product_brand = product_element.get_attribute('data-brand')

            products_data.append((product_id, product_name, product_price, product_brand))
        except TimeoutException:
            print(f"TimeoutException for URL: {url}")

    driver.quit()

    return products_data
