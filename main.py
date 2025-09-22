import time

from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
import csv, os


uc.Chrome.__del__ = lambda self: None


def create_driver(url='https://www.goodreads.com/shelf/show/autobiography'):
    options = uc.ChromeOptions()
    options.add_argument("--window-size=1920,1080")
    # options.add_argument("--headless=new")
    # options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = uc.Chrome(options=options)
    driver.implicitly_wait(4)
    driver.get(url)
    return driver


def close_overlay_window(driver):
    try:
        for i in range(1):
            btn = driver.find_element(
                By.XPATH,
                '//div[@class="Overlay__window"]//button[@aria-label="Close"]'
            )
            btn.click()
            time.sleep(0.3)

    except:
        pass

    try:
        iframe = driver.find_element(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframe)
        for i in range(2):
            btn = driver.find_element(
                By.XPATH,
                '//div[@class="Overlay__window"]//button[@aria-label="Close"]'
            )
            btn.click()
            time.sleep(0.3)
        driver.switch_to.default_content()
    except:
        driver.switch_to.default_content()
        pass

def scrape_books(driver, wait):
    results = []


    books = driver.find_elements(By.XPATH, "//div[@class='elementList']/div[@class='left']/a[1]")
    urls = [book.get_attribute("href") for book in books]

    for url in urls:
        driver.get(url)

        time.sleep(1)

        close_overlay_window(driver)

        title = 'None'
        original_title = 'None'
        autor = 'None'
        genres = 'None'
        firs_publish_date = 'None'
        ratings = 'None'
        reviews = 'None'
        rating_score = 'None'
        description = 'None'
        language = 'None'
        isbn = 'None'

        try:
            title = driver.find_element(By.XPATH, "//div[@class='BookPageTitleSection__title']/h1").text
        except:
            pass

        try:
            original_title = driver.find_element(By.XPATH,'//*[@id="__next"]/div[2]/main/div[1]/div[2]/div[2]/div[1]/div[1]/h3').text.strip()
        except:
            pass

        try:
            autor = driver.find_element(By.XPATH, "//div[@class='ContributorLinksList']//span[@class='ContributorLink__name']").text
        except:
            pass

        try:
            all_genres = driver.find_elements(
                By.XPATH,
                "//div[@data-testid='genresList']//span[@class='BookPageMetadataSection__genreButton']"
            )
            genres = "; ".join([g.text for g in all_genres if g.text])
        except:
            pass

        try:
            firs_publish_date = driver.find_element(By.XPATH, "//div[@class='FeaturedDetails']/p[@data-testid='publicationInfo']").text
        except:
            pass

        try:
            ratings = driver.find_element(By.XPATH,"//div[@class='RatingStatistics__meta']/span[@data-testid='ratingsCount']").text
        except:
            pass

        try:
            reviews = driver.find_element(By.XPATH,"//div[@class='RatingStatistics__meta']/span[@data-testid='reviewsCount']").text
        except:
            pass

        try:
            rating_score = driver.find_element(By.XPATH,"//div[@class='RatingStatistics__rating']").text
        except:
            pass

        try:
            description = driver.find_element(By.XPATH, "//div[@class='BookPageMetadataSection__description']//span[@class='Formatted']").text
        except:
            pass

        try:
            details = driver.find_element(By.XPATH,
                                          "//span[normalize-space()='Book details & editions']/ancestor::button[1]")
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", details)
            details.click()
            time.sleep(0.3)
            language = driver.find_element(
                By.XPATH,
                "//dt[normalize-space()='Language']/following-sibling::dd[1]//div[@data-testid='contentContainer']"
            ).text
        except:
            pass

        try:
            isbn = driver.find_element(
                By.XPATH,
                "//dt[normalize-space()='ISBN']/following-sibling::dd[1]//div[@data-testid='contentContainer']"
            ).text
        except:
            pass

        row = {
            'Title':title,
            'Original Title': original_title,
            'Autor': autor,
            'Genres': genres,
            'First Published Date': firs_publish_date,
            'Number of Ratings': ratings,
            'Number of Reviews': reviews,
            'Rating Score': rating_score,
            'Description': description,
            'Language': language,
            'ISBN': isbn
        }

        results.append(row)

    return results



def save_to_csv(data, filename="books.csv"):
    if not data:
        return
    keys = data[0].keys()
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)




def main():
    driver = None
    try:
        driver = create_driver()
        wait = WebDriverWait(driver, 3)
        data = scrape_books(driver, wait)
        save_to_csv(data)
    finally:
        if driver:
            try:
                driver.quit()
            except Exception:
                pass


if __name__ == '__main__':
    main()