import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def parse_product_data_selenium(url):
    options = uc.ChromeOptions()
    options.headless = False
    driver = uc.Chrome(options=options)

    driver.get(url)

    wait = WebDriverWait(driver, 10)  # ждем до 10 секунд

    product_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-id]')))

    product_id = product_element.get_attribute('data-id')
    product_name = product_element.get_attribute('data-name')
    product_price = product_element.get_attribute('data-price')
    product_brand = product_element.get_attribute('data-brand')

    driver.quit()

    return product_id, product_name, product_price, product_brand
