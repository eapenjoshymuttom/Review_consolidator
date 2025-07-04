from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import re

def get_product_links(product_name, max_retries=5):
    """Search Google for Flipkart product links and extract the first few."""
    links = []
    search_query = f"{product_name} site:flipkart.com"
    url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"

    print(f"Searching Google with query: {search_query}")

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--disable-features=NetworkService")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-extensions")
    options.add_argument(f"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.6834.111 Safari/537.36")

    for attempt in range(max_retries):
        driver = None
        try:
            # Initialize ChromeDriver
            driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=options
            )
            
            # Set page load timeout
            driver.set_page_load_timeout(30)
            print("Chrome WebDriver initialized successfully")
            
            # Navigate to Google search URL
            print(f"Navigating to Google search URL: {url}")
            driver.get(url)
            time.sleep(5)

            # Wait for and find search results
            wait = WebDriverWait(driver, 20)
            search_results = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.tF2Cxc"))
            )

            print(f"Found {len(search_results)} search results")

            for result in search_results:
                try:
                    link_element = result.find_element(By.CSS_SELECTOR, "a")
                    link = link_element.get_attribute('href')

                    # Flipkart URL pattern matching
                    if re.search(r'flipkart\.com.*?/p/', link) and "google.com" not in link:
                        links.append(link)
                        print(f"Found valid Flipkart link: {link}")
                except Exception as e:
                    print(f"Error extracting link from result: {str(e)}")
                    continue

                if len(links) >= 5:
                    break

            if links:
                break
            
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt == max_retries - 1:
                print("Failed to fetch product links after maximum retries")
                return []
            time.sleep(2 * (attempt + 1))
            
        finally:
            if driver:
                try:
                    driver.quit()
                    print("Chrome WebDriver closed successfully")
                except Exception as e:
                    print(f"Error closing driver: {str(e)}")

    print(f"\nTotal Flipkart links found: {len(links)}")
    for i, link in enumerate(links, 1):
        print(f"{i}. {link}")

    return links

# Example Usage:
# if __name__ == "__main__":
#     product_name = input("Enter product name: ")
#     product_links = get_product_links(product_name)
#     print("\nExtracted Flipkart Links:", product_links)
