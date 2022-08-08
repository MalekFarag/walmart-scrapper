from multiprocessing import Value
from multiprocessing.connection import wait
from selenium import webdriver
from selenium.webdriver.common.by import By # targetting
from pkg_resources import run_script

#chrome
from webdriver_manager.chrome import ChromeDriverManager #pip install webdriver-manager
from webdriver_manager.firefox import GeckoDriverManager

# firefox
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.service import Service as FirefoxService

import random
import pandas as pd

barcode_num = input('what is the barcode number?    ')

URL = "https://www.google.com/"

product_data_list = []
walmart_image_list = []
#Walmart
WALMART_PRODUCT = f"https://www.walmart.ca/search?q={barcode_num}&f=12"

def get_product_data():
    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
    driver.get(URL)

    driver.implicitly_wait(10)
    driver.get("javascript: window.location.href = '{}'".format(WALMART_PRODUCT) )
    driver.implicitly_wait(10)

    first_product_url = driver.find_element(By.CSS_SELECTOR, '[class = "css-15x41f3 epettpn1"]').get_attribute('href')
    driver.get("javascript: window.location.href = '{}'".format(first_product_url) )
     
   
                   
    title = driver.find_element(By.CSS_SELECTOR, '[data-automation = "product-title"]').text # IMPORTANT ADD "." AT THE BEGINNING OF X PATH TO SEARCH WITHIN
    price = driver.find_element(By.CSS_SELECTOR, '[data-automation = "buybox-price"]').text
    link = first_product_url

    num_of_image_links = driver.find_elements(by=By.XPATH, value="/html/body/div[1]/div/div[4]/div/div/div[1]/div[3]/div[1]/div/div/div/div/div[1]/div/div/div/div/*")
    image_link = (repr(driver.find_element(By.CSS_SELECTOR, '[class = "css-128ipej"]').get_attribute('style')).replace('background-image: url("', '')).replace('"");', '')

    product_data = {
    'title' : title,
    'price' : price,
    'link' : link,
    'image link' : image_link
    }
    product_data_list.append(product_data)
    #print(product_data_list)
   
    CSV_PATH ="product_data.csv"
    data = pd.DataFrame(product_data_list)
    data.to_csv(CSV_PATH, index=False, encoding='utf-8')
    print(data)
   
   
    for image in num_of_image_links:
        image_link = image.find_element(By.CSS_SELECTOR, '[class = "css-128ipej"]').get_attribute('style')

        """
            Notes for Gabe:
                - sample string "background-image: url(""https://i5.walmartimages.ca/images/Large/900/662/6000200900662.jpg"");"
                - removing quotations with replace
                - we're splitting from "(" and taking the last entry [-1] -> "https://i5.walmartimages.ca/images/Large/900/662/6000200900662.jpg"");"
                - then we're taking that new string and splitting it by ")" and using the first entry -> "https://i5.walmartimages.ca/images/Large/900/662/6000200900662.jpg"

            Look up "python split" to learn more
        """
        split_url = image_link.split("(")[-1].split(")")[0]
        url = split_url.replace('"', '')

        product_image_data = {
        'image link' : url
        }
        walmart_image_list.append(product_image_data)
        #print(product_data_list)
   
    CSV_PATH ="walmart_product_image_data.csv"
    data = pd.DataFrame(walmart_image_list)
    data.to_csv(CSV_PATH, index=False, encoding='utf-8')
    print(data)

get_product_data()
