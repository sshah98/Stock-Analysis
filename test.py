from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

options = Options()

options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--headless')
options.add_argument("--disable-extensions")

driver = webdriver.Chrome(executable_path='chromedriver', chrome_options=options)
print("opening chrome")

driver.get('https://finance.yahoo.com/quote/SYF')

soup = BeautifulSoup(driver.page_source, "lxml")

driver.close()

for s in soup(['script', 'style']):
    s.decompose()
    
print(soup)