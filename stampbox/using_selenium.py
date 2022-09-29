import re
import chromedriver_autoinstaller
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from scrapy import Selector
from selenium.webdriver.chrome.options import Options
from stampbox.location_finder import locate_text


chromedriver_autoinstaller.install()

s = Service(ChromeDriverManager().install())


def use_sel_model(img_param):
    try:
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--incognito')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
        chrome_options.headless = True

        driver = webdriver.Chrome(options=chrome_options, service=s)

        driver.get('https://images.google.com/')
        try:
            driver.execute_script("arguments[0].click();", WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[aria-label="Search by image"]'))))
        except Exception as e:
            driver.find_element(By.XPATH, '//*[@id="sbtc"]/div/div[3]/div[2]').click()
        # driver.find_element(By.CSS_SELECTOR, 'a[href="about:invalid#zClosurez"]').click()
        # try:
        #     driver.find_element(By.CSS_SELECTOR, '#awyMjb').send_keys(img_param)
        # except:
        #     driver.find_element(By.CSS_SELECTOR, 'input[type="file"]').send_keys(img_param)
        driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Paste image link"]').send_keys(
            'https://www.pakpost.gov.pk/images/2016-08-17-Abdul-Sattar-Edhi-Philanthropist-1926-2016-Stamp.jpg')
        driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Paste image link"]').send_keys(Keys.ENTER)
        response = Selector(text=driver.page_source)
        # pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))
        first_text = response.css('a[style="font-style:italic"] ::text').get(None)
        if not first_text:
            google_page = response.css('a[data-tooltip-classes="UOPJud"] ::attr(href)').get('')
            driver.get(google_page)

        response = Selector(text=driver.page_source)
        first_text = response.css('a[style="font-style:italic"] ::text').get('')
        text = ' '.join(response.css('#rcnt ::text').getall())
        years_list = re.findall(r" \b\d{4}\b", text)
        year = years_list[0] if years_list else None
        if text:
            text = locate_text(text, tag_line=first_text, year=year)
            driver.close()
            return text
        else:
            driver.close()
            return None
    except Exception as e:
        print('[METHOD: POST] [USING SELENIUM] caught exception, ', e)
        return None


if __name__ == '__main__':
    image_path = r"C:\Users\pixarsart\PycharmProjects\StampBox Classifications\Images\Stamps_images\Untitled design (" \
                 r"15).png "
    use_sel_model(image_path)
