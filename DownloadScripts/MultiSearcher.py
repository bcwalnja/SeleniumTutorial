from ScrapeLinks import getVideoIds
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
artists = ["Piece of Heaven",
    "Knit Together",
    "Masterpiece",
    "Your Body Is a Temple",
    "Let It Shine Reprise"]
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

            #get the first two links
            links = getVideoIds(html)
            log("Found {} links".format(len(links)))
            if len(links) > 1:
                # html = concat the first two links
                html = "youtube.com/watch?v=" + links[0] + \
                "\n" + "youtube.com/watch?v=" + links[1]
            
            # directory = getDirectory(artist)
            directory = "Heaven in Your Home"
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