import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from urllib.parse import urljoin
# import pandas as pd

def search_and_scrape_1gl(query: str):
    """
    Выполняет поиск на сайте 1gl.ru и извлекает результаты,
    адаптировано под новую структуру HTML.
    """
    print("--- Запуск браузера ---")
    driver = webdriver.Chrome()
    base_url = "https://1gl.ru/"

    try:
        # 1. Заход на сайт
        print(f"--- Переход на сайт: {base_url} ---")
        driver.get(base_url)

        # 2. Поиск строки поиска и ввод текста
        print(f"--- Поиск элемента 'строка поиска' и ввод текста '{query}' ---")
        wait = WebDriverWait(driver, 10)
        search_box_xpath = '//*[@id="search-text"]'
        
        search_box = wait.until(EC.element_to_be_clickable((By.XPATH, search_box_xpath)))
        driver.execute_script("arguments[0].value = arguments[1];", search_box, query)
        print(f"--- Успешно введен запрос: '{query}' ---")
        
        # 3. Нажатие на кнопку поиска
        print("--- Нажатие кнопки поиска ---")
        search_button_xpath = '//*[@id="search-form"]/label[3]'
        search_button = driver.find_element(By.XPATH, search_button_xpath)
        search_button.click()
        
        time.sleep(0.5)

        # 4. Ожидание загрузки результатов
        print("--- Ожидание загрузки страницы с результатами ---")
        # ИЗМЕНЕНО: Ждем главный контейнер, который содержит ВСЕ результаты.
        # Этот селектор стабилен и надежен.
        results_main_container_selector = "div[data-id='search-results-section']"
        wait_res = WebDriverWait(driver, 25)
        wait_res.until(EC.presence_of_element_located((By.CSS_SELECTOR, results_main_container_selector)))
        
        print("--- Результаты загружены. Начинаем извлечение данных. ---")

        # 5. Получение HTML-кода страницы и его парсинг
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'lxml')

        # 6. Извлечение текстов, ссылок и описаний
        # ИЗМЕНЕНО: Полностью новая логика парсинга.
        
        # Находим все отдельные блоки с результатами по их data-id
        result_items = soup.select('div[data-id="search-item"]')
        
        if not result_items:
            print("!!! Основные результаты (search-item) не найдены на странице. !!!")
            # Можно добавить вывод HTML для отладки, если нужно
            # print(soup.prettify())
            return

        print(f"--- Найдено {len(result_items)} основных результатов на странице ---")
        
        extracted_data = []
        for item in result_items:
            # Ищем ссылку и заголовок внутри элемента
            # У ссылки нет уникального класса, но она находится внутри заголовка
            title_element = item.select_one('div[data-qa-locator="title"] a')
            
            # Ищем описание
            description_element = item.select_one('div[data-qa-locator="description"]')
            
            if title_element:
                title = title_element.get_text(strip=True)
                relative_link = title_element.get('href')
                absolute_link = urljoin(base_url, relative_link)
                
                # Получаем текст описания, если он есть
                description = description_element.get_text(strip=True) if description_element else "Описание не найдено"
                
                extracted_data.append({
                    "title": title, 
                    "link": absolute_link,
                    "description": description
                })
        
        return extracted_data

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return None
    finally:
        # 7. Закрытие браузера
        print("--- Закрытие браузера ---")
        driver.quit()

if __name__ == "__main__":
    search_query = "ндфл"
    results = search_and_scrape_1gl(search_query)

    if results:
        print(f"\n✅ Найдено {len(results)} результатов по запросу '{search_query}':\n")
        
        # Вывод в простом цикле для наглядности
        for i, result in enumerate(results, 1):
            print(f"{i}. {result['title']}")
            print(f"   Ссылка: {result['link']}")
            print(f"   Описание: {result['description']}\n")
            
        # # Если хотите вывод в виде таблицы через pandas:
        # df = pd.DataFrame(results)
        # pd.set_option('display.max_colwidth', 80)
        # pd.set_option('display.width', 120)
        # print(df)# import pandas as pd

def search_and_scrape_1gl(query: str):
    """
    Выполняет поиск на сайте 1gl.ru и извлекает результаты,
    адаптировано под новую структуру HTML.
    """
    print("--- Запуск браузера ---")
    driver = webdriver.Chrome()
    base_url = "https://1gl.ru/"

    try:
        # 1. Заход на сайт
        print(f"--- Переход на сайт: {base_url} ---")
        driver.get(base_url)

        # 2. Поиск строки поиска и ввод текста
        print(f"--- Поиск элемента 'строка поиска' и ввод текста '{query}' ---")
        wait = WebDriverWait(driver, 10)
        search_box_xpath = '//*[@id="search-text"]'
        
        search_box = wait.until(EC.element_to_be_clickable((By.XPATH, search_box_xpath)))
        driver.execute_script("arguments[0].value = arguments[1];", search_box, query)
        print(f"--- Успешно введен запрос: '{query}' ---")
        
        # 3. Нажатие на кнопку поиска
        print("--- Нажатие кнопки поиска ---")
        search_button_xpath = '//*[@id="search-form"]/label[3]'
        search_button = driver.find_element(By.XPATH, search_button_xpath)
        search_button.click()
        
        time.sleep(0.5)

        # 4. Ожидание загрузки результатов
        print("--- Ожидание загрузки страницы с результатами ---")
        # ИЗМЕНЕНО: Ждем главный контейнер, который содержит ВСЕ результаты.
        # Этот селектор стабилен и надежен.
        results_main_container_selector = "div[data-id='search-results-section']"
        wait_res = WebDriverWait(driver, 25)
        wait_res.until(EC.presence_of_element_located((By.CSS_SELECTOR, results_main_container_selector)))
        
        print("--- Результаты загружены. Начинаем извлечение данных. ---")

        # 5. Получение HTML-кода страницы и его парсинг
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'lxml')

        # 6. Извлечение текстов, ссылок и описаний
        # ИЗМЕНЕНО: Полностью новая логика парсинга.
        
        # Находим все отдельные блоки с результатами по их data-id
        result_items = soup.select('div[data-id="search-item"]')
        
        if not result_items:
            print("!!! Основные результаты (search-item) не найдены на странице. !!!")
            # Можно добавить вывод HTML для отладки, если нужно
            # print(soup.prettify())
            return

        print(f"--- Найдено {len(result_items)} основных результатов на странице ---")
        
        extracted_data = []
        for item in result_items:
            # Ищем ссылку и заголовок внутри элемента
            # У ссылки нет уникального класса, но она находится внутри заголовка
            title_element = item.select_one('div[data-qa-locator="title"] a')
            
            # Ищем описание
            description_element = item.select_one('div[data-qa-locator="description"]')
            
            if title_element:
                title = title_element.get_text(strip=True)
                relative_link = title_element.get('href')
                absolute_link = urljoin(base_url, relative_link)
                
                # Получаем текст описания, если он есть
                description = description_element.get_text(strip=True) if description_element else "Описание не найдено"
                
                extracted_data.append({
                    "title": title, 
                    "link": absolute_link,
                    "description": description
                })
        
        return extracted_data

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return None
    finally:
        # 7. Закрытие браузера
        print("--- Закрытие браузера ---")
        driver.quit()

if __name__ == "__main__":
    search_query = "ндфл"
    results = search_and_scrape_1gl(search_query)

    if results:
        print(f"\n✅ Найдено {len(results)} результатов по запросу '{search_query}':\n")
        
        # Вывод в простом цикле для наглядности
        for i, result in enumerate(results, 1):
            print(f"{i}. {result['title']}")
            print(f"   Ссылка: {result['link']}")
            print(f"   Описание: {result['description']}\n")
            
        # # Если хотите вывод в виде таблицы через pandas:
        # df = pd.DataFrame(results)
        # pd.set_option('display.max_colwidth', 80)
        # pd.set_option('display.width', 120)
        # print(df)