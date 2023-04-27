from DriverBuilder import getDriver
from Logger import log
from Downloader import download, getDirectory

#declarations
googleUrl = [
    "https://www.google.com/search?q=",
    "%20site%3Ayoutube.com"
    ]
enter = u'\ue007'
html = ""
artists = ["Third Day",
    "MercyMe",
    "TobyMac",]
wait = 15

def run():
    try:
        log("Starting MultiSearcher")
        headless = input("Run headless? (y/n): ").lower() == "y"
        directory = getDirectory("")
        
        for artist in artists:
            log("Searching for {}".format(artist))
            
            url = googleUrl[0] + artist + googleUrl[1]
            log("Navigating to {}".format(url))
            driver = getDriver(wait, directory, headless)
            driver.get(url)
            
            html = driver.page_source
            log("html line count: {}".format(len(html.splitlines())))
            driver.close()
            
            directory = getDirectory(artist)
            log("Setting directory to {}".format(directory))
            driver = getDriver(wait, directory, headless)
            
            log("Starting download")
            download(driver, html, directory)
            driver.close()
            
        log("Complete.")
    except Exception as e:
        log("An error occurred")
        log("Error: {}".format(e))
        log("Error: {}".format(e.__traceback__))
    finally:
        exit()

if __name__ == "__main__":
    run()