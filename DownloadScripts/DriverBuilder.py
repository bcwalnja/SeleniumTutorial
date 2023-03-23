from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from Logger import log

def getDriver(wait = 15, directory = r"C:\Users\nathaniel\Downloads"):
    log("Building driver options")
    options = Options()
    options.page_load_strategy = 'normal'

    #if user inputs "y", add headless option
    if input("Headless? (y/n): ") == "y":
        log("** ADDING HEADLESS **")
        options.add_argument('headless')

    log("Setting download directory to {}".format(directory))
    options.add_experimental_option("prefs", { "profile.default_content_settings.popups": 0,\
                                            "download.default_directory":directory,\
                                            "download.prompt_for_download": False,\
                                            "download.directory_upgrade": True })
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(wait)
    return driver