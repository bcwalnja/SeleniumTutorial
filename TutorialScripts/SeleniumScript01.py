from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
import time

#strings
#PATH = "C:\Program Files (x86)\chromedriver.exe" # deprecated
searchName = "s"
mainName = "main"
url = "https://techwithtim.net"

options = Options()
options.page_load_strategy = 'normal'
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(10)

driver.get(url)
print( driver.title )

search = driver.find_element(By.NAME, searchName)
search.send_keys("test")
search.send_keys(Keys.RETURN)


main = driver.find_element(By.ID, mainName)
articles = main.find_elements(By.TAG_NAME, "")

time.sleep(5)
  