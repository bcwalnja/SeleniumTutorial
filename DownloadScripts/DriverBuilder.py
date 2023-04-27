from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from Logger import log

def getDriver(wait = 15, directory = r"C:\Users\nathaniel\Downloads", headless = False):
    log("Building driver options")
    options = Options()
    options.page_load_strategy = 'normal'

    if headless:
        log("** ADDING HEADLESS **")
        options.add_argument('headless')

    log("Setting download directory to {}".format(directory))
    options.add_experimental_option("prefs", { "profile.default_content_settings.popups": 0,\
        "download.default_directory":directory,\
        "download.prompt_for_download": False,\
        "download.directory_upgrade": True })
    log("Starting web driver")
    driver = webdriver.Chrome(options=options)
    log("Setting implicit wait to {} seconds".format(wait))
    driver.implicitly_wait(wait)
    return driver