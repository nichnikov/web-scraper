import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from urllib.parse import urljoin # <-- ИМПОРТИРОВАЛИ НУЖНУЮ ФУНКЦИЮ
# import pandas as pd

def search_and_scrape_python_org(query: str):
    """
    Выполняет поиск на сайте python.org и извлекает результаты.

    Args:
        query: Строка для поискового запроса.
    """
    print("--- Запуск браузера ---")
    # Инициализация драйвера Chrome
    # Selenium 4+ может автоматически управлять драйвером
     # <-- ОПРЕДЕЛИЛИ БАЗОВЫЙ URL ДЛЯ СОЗДАНИЯ ПОЛНЫХ ССЫЛОК
    base_url = "https://www.python.org"
    
    driver = webdriver.Chrome()

    try:
        # 1. Заход на сайт
        url = "https://www.python.org/"
        print(f"--- Переход на сайт: {url} ---")
        driver.get(url)

        # 2. Поиск строки поиска и ввод текста
        print(f"--- Поиск элемента 'строка поиска' и ввод текста '{query}' ---")
        # Находим элемент по его ID 'id-search-field'
        search_box = driver.find_element(By.ID, "id-search-field")
        search_box.send_keys(query)

        # 3. Нажатие на кнопку поиска
        print("--- Нажатие кнопки 'GO' ---")
        # Находим кнопку поиска по ее ID 'submit'
        search_button = driver.find_element(By.ID, "submit")
        search_button.click()

        # 4. Ожидание загрузки результатов
        print("--- Ожидание загрузки страницы с результатами ---")
        # Мы будем ждать до 10 секунд, пока не появится элемент, 
        # содержащий результаты (ul с классом 'list-recent-events')
        wait = WebDriverWait(driver, 10)
        results_container_selector = "ul.list-recent-events.menu"
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, results_container_selector)))
        
        print("--- Результаты загружены. Начинаем извлечение данных. ---")

        # 5. Получение HTML-кода страницы и его парсинг
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'lxml')

        # 6. Извлечение текстов и ссылок
        results_list = soup.select(f"{results_container_selector} li")
        
        if not results_list:
            print("!!! Результаты не найдены на странице. !!!")
            return
        
        extracted_data = []
        for item in results_list:
            title_element = item.find("h3")
            if title_element and title_element.find("a"):
                title = title_element.a.get_text(strip=True)
                relative_link = title_element.a.get('href')
                
                # <-- ИЗМЕНЕНИЕ: Преобразуем относительную ссылку в абсолютную
                absolute_link = urljoin(base_url, relative_link)
                
                extracted_data.append({"title": title, "link": absolute_link})
        
        return extracted_data

        '''
        extracted_data = []
        for item in results_list:
            # Находим заголовок внутри тега <h3><a>
            title_element = item.find("h3")
            if title_element and title_element.find("a"):
                title = title_element.a.get_text(strip=True)
                link = title_element.a.get('href')
                extracted_data.append({"title": title, "link": link})
        
        return extracted_data'''

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return None
    finally:
        # 7. Закрытие браузера в любом случае
        print("--- Закрытие браузера ---")
        driver.quit()

if __name__ == "__main__":
    search_query = "pandas"
    
    results = search_and_scrape_python_org(search_query)


    if results:
        print(f"\n✅ Найдено {len(results)} результатов по запросу '{search_query}':\n")
        
        # Красивый вывод с помощью pandas DataFrame
        # df = pd.DataFrame(results)
        # print(df)
        
        # Или простой вывод в цикле
        for i, result in enumerate(results, 1):
            print(f"{i}. {result['title']}")
            print(f"   Ссылка: {result['link']}\n")