"""
Залогиниться на сайте(https://www.scrapethissite.com/pages/advanced/?gotcha=login).
Вывести сообщение, которое появляется после логина (связка логин/пароль может быть любой).
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

s = Service('./chromedriver')
options = Options()
options.add_argument('start-maximized')
options.add_experimental_option('excludeSwitches', ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(service=s, options=options)
driver.get('https://www.scrapethissite.com/pages/advanced/?gotcha=login')

driver.implicitly_wait(10)

login = driver.find_element(By.NAME, 'user')
login.send_keys("scraping@gb.ru")
password = driver.find_element(By.NAME, 'pass')
password.send_keys("password123")
password.submit()

text = driver.find_element(By.XPATH, "//div[@class='col-md-4 col-md-offset-4']").text

print(f'Сообщение: {text}')
