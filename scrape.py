from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import logging

logging.basicConfig(filename='logs/log.txt', level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
logger=logging.getLogger(__name__)

base_url = "http://www.amazon.com/exec/obidos/ASIN/"

def scrape_amz(asin):
    try:
        webdriver_path = os.path.abspath("chromedriver/chromedriver.exe")
        chrome_options = webdriver.ChromeOptions()

        #chrome_options.add_argument("--headless")
        #chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--incognito")
        prefs = {"profile.managed_default_content_settings.images":2}
        chrome_options.add_experimental_option("prefs",prefs)
        driver = webdriver.Chrome(webdriver_path, chrome_options=chrome_options)  # Optional argument, if not specified will search path.

        direct_to_cart = False

        #load product page
        driver.get(base_url + asin);
        product_html = driver.page_source
        #click add to cart
        driver.find_element_by_id('add-to-cart-button').click()

        #wait for view cart button
        for i in range(2):
            try:
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "hlb-view-cart-announce")))
                break
            except:
                if i == 0:
                    print(asin + " Cart button not found, pressing ESC to close popover")
                    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
                else:
                    print("Following cart link in nav bar")
                    driver.find_element_by_id('nav-cart').click()
                    direct_to_cart = True

        if direct_to_cart == False:
            driver.find_element_by_id('hlb-view-cart-announce').click()
        #click drop-down
        driver.find_element_by_id('a-autoid-0-announce').click()
        #Click 10+
        driver.find_element_by_id('dropdown1_9').click()
        #Set quantity to 999
        driver.find_element_by_name("quantityBox").send_keys('999')
        driver.find_element_by_name("quantityBox").send_keys(Keys.RETURN)
        #wait for stock level message to appear
        try:
            element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "sc-quantity-update-message")))
        except:
            print(asin + " More than 999 available")
        #retrieve message
        cart_html = driver.page_source
        logging.info("Scrape successful. ")

    except:
        logging.exception("Scrape error ")
        return(1)

    return([product_html,cart_html])
