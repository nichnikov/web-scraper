import os
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool
from langchain_openai import OpenAI
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Установите ваш API-ключ OpenAI
os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"

# Инициализация Selenium WebDriver
driver = webdriver.Chrome()

@tool
def navigate_to_url(url: str) -> str:
    """Переходит по указанному URL в браузере."""
    driver.get(url)
    return f"Успешно перешел на {url}"

@tool
def find_element_and_type(element_description: str, text_to_type: str) -> str:
    """Находит элемент на странице по его описанию и вводит в него текст."""
    prompt = f"Найди XPath для элемента с описанием: '{element_description}' на текущей веб-странице."
    # В реальном приложении здесь будет вызов LLM для получения XPath
    # Для демонстрации используем предопределенный XPath
    # llm_response = llm.invoke(prompt)
    # xpath = llm_response.strip()
    
    # Пример для сайта https://www.python.org/
    if "строка поиска" in element_description:
        xpath = '//*[@id="id-search-field"]'
    else:
        return "Не удалось определить XPath для элемента."

    try:
        search_box = driver.find_element(By.XPATH, xpath)
        search_box.send_keys(text_to_type)
        return f"Успешно ввел '{text_to_type}' в элемент '{element_description}'."
    except Exception as e:
        return f"Ошибка при поиске или вводе текста: {e}"

@tool
def click_element(element_description: str) -> str:
    """Находит элемент по описанию и кликает по нему."""
    prompt = f"Найди XPath для элемента с описанием: '{element_description}'."
    # llm_response = llm.invoke(prompt)
    # xpath = llm_response.strip()

    # Пример для сайта https://www.python.org/
    if "кнопка поиска" in element_description:
        xpath = '//*[@id="submit"]'
    else:
        return "Не удалось определить XPath для кнопки."
        
    try:
        button = driver.find_element(By.XPATH, xpath)
        button.click()
        return f"Успешно нажал на '{element_description}'."
    except Exception as e:
        return f"Ошибка при клике на элемент: {e}"

@tool
def wait_for_results_and_extract(results_container_description: str) -> str:
    """Ожидает загрузки результатов и извлекает тексты и ссылки."""
    try:
        # Ожидаем появления контейнера с результатами
        wait = WebDriverWait(driver, 10)
        # Для python.org результаты находятся в <ul class="list-recent-events menu">
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul.list-recent-events.menu")))
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results_list = soup.select('ul.list-recent-events.menu li')
        
        extracted_data = []
        for item in results_list:
            title_element = item.find('a')
            if title_element:
                title = title_element.get_text(strip=True)
                link = title_element.get('href')
                if not link.startswith('http'):
                    link = "https://www.python.org" + link
                extracted_data.append({"title": title, "link": link})
        
        return f"Извлечено {len(extracted_data)} результатов: {extracted_data}"
    except Exception as e:
        return f"Ошибка при ожидании или извлечении результатов: {e}"

# Инструменты, которые будет использовать агент
tools = [
    navigate_to_url,
    find_element_and_type,
    click_element,
    wait_for_results_and_extract
]

# Создание промпта для агента
prompt_template = """
Ты — ассистент, который помогает пользователям искать информацию на веб-сайтах.
Используй доступные инструменты для выполнения следующих шагов:
1. Перейди на указанный URL.
2. Найди строку поиска и введи в нее поисковый запрос.
3. Нажми на кнопку поиска.
4. Дождись загрузки результатов и извлеки их.

Вопрос: {input}

{agent_scratchpad}
"""

prompt = PromptTemplate.from_template(prompt_template)

# Инициализация LLM и агента
llm = OpenAI(temperature=0)
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Запуск агента
query = "Найди информацию о 'asyncio' на сайте https://www.python.org/"
try:
    result = agent_executor.invoke({"input": query})
    print("\nИтоговый результат:")
    print(result['output'])
finally:
    # Закрываем браузер после выполнения
    driver.quit()