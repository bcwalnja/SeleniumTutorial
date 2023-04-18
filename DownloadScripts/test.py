from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium import chromedriver_autoinstaller


chromedriver_autoinstaller.install()

options = Options()
driver = webdriver.Chrome(options=options)
driver.get("https://www.google.com")