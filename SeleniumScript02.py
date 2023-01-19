from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
import time

def findLink(driver, linkText):
    return WebDriverWait(driver, timeout=3).until(lambda d: d.find_element(By.LINK_TEXT, linkText))

#strings
#PATH = "C:\Program Files (x86)\chromedriver.exe" # deprecated
url = "https://techwithtim.net"
options = Options()
options.page_load_strategy = 'normal'
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(10)

driver.get(url)

linkText = "Python Programming"
link = findLink(driver, linkText)
print("LINK FOUND: " + str(link))

link.click()

linkText = "Beginner Python Tutorials"
link = findLink(driver, linkText)
print("LINK FOUND: " + str(link))

link.click()

time.sleep(10)