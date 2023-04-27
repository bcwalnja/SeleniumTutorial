from selenium.webdriver.chrome.options import Options
from selenium import webdriver

options = Options()
options.page_load_strategy = 'normal'


options.add_experimental_option("prefs", { "profile.default_content_settings.popups": 0,\
                                        "download.prompt_for_download": False,\
                                        "download.directory_upgrade": True })
driver = webdriver.Chrome(options=options)
driver.get("https://wiki.python.org/moin/BeginnersGuide")