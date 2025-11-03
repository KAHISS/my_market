
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os


def make_chrome_driver(*options):
    chrome_options = webdriver.ChromeOptions()
    if options is not None:
        for option in options:
            chrome_options.add_argument(option)
    if os.getenv('SELENIUM_HEADLESS', '0') == '1':
        chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=chrome_options)
    return driver


if __name__ == '__main__':
    n = make_chrome_driver()
    n.get('https://atacadinhocristao.cloud/admin')
    time.sleep(5)
    n.quit()
