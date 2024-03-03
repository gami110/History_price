import undetected_chromedriver as uc
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
# from database.job_database import get_links_from_db
# from tqdm import tqdm
# from concurrent.futures import ThreadPoolExecutor

def create_driver():
    """Создаем новый драйвер"""
    options = uc.ChromeOptions()
    options.headless = False
    driver = uc.Chrome(options=options)
    return driver

def get_product_attribute(product_element, attribute_name):
    """Получаем атрибут продукта"""
    try:
        attribute = product_element.get_attribute(attribute_name)
    except NoSuchElementException:
        attribute = None
    return attribute

def get_product_element_text(product_element, xpath):
    """Получаем текст элемента продукта"""
    try:
        element = product_element.find_element(By.XPATH, xpath).find_elements(By.TAG_NAME, 'td')
        if len(element) > 1:
            text = element[1].text
    except NoSuchElementException:
        text = None
    return text

def parse_product_data_selenium(urls):
    driver = create_driver()
    wait = WebDriverWait(driver, 10)

    products_data = []
    for url in urls[0:1]:
        driver.get(url)

        product_element = wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, 'div[data-id]')))

        product_id = get_product_attribute(product_element, 'data-id')
        product_name = get_product_attribute(product_element, 'data-name')
        product_brand = get_product_attribute(product_element, 'data-brand')
        product_price = get_product_attribute(product_element, 'data-price')
        product_section = get_product_attribute(product_element, 'data-section')

        product_manufactured = get_product_element_text(product_element, '//tr[td[contains(text(), "Завод производитель:")]]')
        product_manufacturer = get_product_element_text(product_element, '//tr[td[contains(text(), "Производитель:")]]')
        product_release = get_product_element_text(product_element, '//tr[td[contains(text(), "Форма выпуска:")]]')
        product_age = get_product_element_text(product_element, '//tr[td[contains(text(), "Возраст от:")]]')
        product_count_in_package = get_product_element_text(product_element, '//tr[td[contains(text(), "Количество в упаковке:")]]')
        product_active_ingredients = get_product_element_text(product_element, '//tr[td[contains(text(), "Действующие вещества:")]]')

        links = url
        product_data = (product_id, product_name, product_price, product_brand, product_section, product_manufactured,
                        product_manufacturer, product_release, product_age, product_count_in_package, product_active_ingredients, links)

        products_data.append(product_data)

    driver.quit()

    return products_data

# def parse_products_data_selenium_multithreaded():
#     urls = get_links_from_db()
#
#     # Количество потоков
#     num_threads = 10
#
#     # Разделить список ссылок на равные части
#     urls_chunks = [urls[i::num_threads] for i in range(num_threads)]
#
#     with ThreadPoolExecutor(max_workers=num_threads) as executor:
#         products_data = list(tqdm(executor.map(parse_product_data_selenium, urls_chunks), total=len(urls_chunks), desc="Parsing product data", unit="url"))
#
#     return products_data
