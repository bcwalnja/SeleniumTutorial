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
artists = ["Chris Tomlin",
    "Michael W. Smith",
    "MercyMe"]
wait = 15

def run():
    log("Starting MultiSearcher")
    
    for artist in artists:
        log("Searching for {}".format(artist))
        
        driver = getDriver()
        url = googleUrl[0] + artist + googleUrl[1]
        log("Navigating to {}".format(url))
        driver.get(url)
        
        html = driver.page_source
        log("html line count: {}".format(len(html.splitlines())))
        
        directory = getDirectory(artist)
        log("Setting directory to {}".format(directory))
        
        log("Starting download")
        download(driver, html, directory)
        
    log("Complete.")
    driver.close()
    exit()

if __name__ == "__main__":
    run()