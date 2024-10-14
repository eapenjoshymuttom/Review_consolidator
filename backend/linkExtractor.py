from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import re

def get_product_links(product_name):
    links = []

    search_query = f"{product_name} site:amazon.com"
    url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"

    print(f"Searching Google with query: {search_query}")

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(f"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get(url)
        time.sleep(2)  # Wait for page to load

        search_results = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.g"))
        )

        for result in search_results:
            try:
                link = result.find_element(By.CSS_SELECTOR, "a").get_attribute('href')
                if re.search(r'amazon\.com', link):
                    links.append(link)
            except:
                continue

            if len(links) >= 5:
                break

    except Exception as e:
        print(f"An error occurred while fetching data: {e}")

    finally:
        driver.quit()
    for i, link in enumerate(links, 1):
        print(f"{i}. {link}")

    return links

# Usage
# product_name = input("Enter product name: ")
# product_links = get_product_links(product_name)

# print("Product links:")
# for i, link in enumerate(product_links, 1):
#     print(f"{i}. {link}")