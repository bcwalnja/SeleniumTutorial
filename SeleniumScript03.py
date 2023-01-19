from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

def getCount(count):
    try:
        v = int(str(count).split(" ")[0])
        return v
    except:
        return 0

#strings
url = "https://orteil.dashnet.org/cookieclicker/"
english = "langSelect-EN"
bigCookie = "bigCookie"
cookieCount = "cookies"

options = Options()
options.page_load_strategy = 'normal'
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(10)
driver.get(url)

print("Looking for language button")
language = driver.find_element(By.ID, english)
language.click()

for i in range(5000): 
    try:
        print("Cycle " + str(i))
        cookie = driver.find_element(By.ID, bigCookie)
        counter = driver.find_element(By.ID, cookieCount)
        cookies = getCount(counter.text)
        items = [driver.find_element(By.ID, "productPrice" + str(i)) for i in range(2, -1, -1) ]
        
        # I tried this both ways, and it's significantly faster to not use "ActionChains"
        # actions = ActionChains(driver)
        # actions.move_to_element(cookie)
        # actions.click(cookie)
        # actions.perform()
        cookie.click()

        for item in items:
            price = getCount(item.text)
            if price > 0 and price <= cookies:
                actions = ActionChains(driver)
                actions.move_to_element(item)
                actions.click()
                actions.perform()
    except:
        print(f"Cycle {i} Failed :-(")
