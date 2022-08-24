from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

from pymongo import MongoClient
from pymongo import errors

s = Service('./chromedriver')
options = Options()
options.add_argument("start-maximized")
driver = webdriver.Chrome(options=options)
driver.get('https://www.mvideo.ru/')
page = driver.find_element(By.XPATH, "//html")

while True:
    try:
        trend_button = driver.find_element(By.XPATH, "//button[.//span[contains(text(), 'В тренде')]]")
        break
    except NoSuchElementException:
        page.send_keys(Keys.DOWN)

trend_button.send_keys(Keys.ENTER)

goods = driver.find_elements(By.XPATH, "//mvid-shelf-group[@class = 'page-carousel-padding ng-star-inserted']//"
                                       "div[@class='product-mini-card__name ng-star-inserted']//a")

client = MongoClient('127.0.0.1', 27017)
db = client['user51']
collection_name = 'trend_goods'

try:
    db.create_collection(collection_name)
except errors.CollectionInvalid:
    pass

collection = db.get_collection(collection_name)

for good in goods:
    data = {'title': good.text, 'link': good.get_attribute('href')}
    collection.insert_one(data)

print(collection)
driver.close()
