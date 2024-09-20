from os import makedirs, path
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
searchTerms = [
    "Tron Soundtrack Solar Sailer",
    "Tron Soundtrack Rectifier",
    "Tron Soundtrack Disc Wars",
    "Tron Soundtrack C.L.U.",
    "Tron Soundtrack Arrival",
    "Tron Soundtrack Flynn Lives",
    "Tron Soundtrack Legacy (End Titles)",
    "Tron Soundtrack Finale",
    "Tron Soundtrack Sea of Simulation",
    "Tron Soundtrack ENCOM Part II",
    "Tron Soundtrack ENCOM Part I",
    "Tron Soundtrack Round One",
    "Tron Soundtrack Castor",
    "Tron Soundtrack Reflections",
    "Tron Soundtrack Sunrise Prelude",
    "Tron Soundtrack Father and Son",
    "Tron Soundtrack Outlands, Part II"
    ]
wait = 15

def run():
    try:
        log("Starting MultiSearcher")
        headless = input("Run headless? (y/n): ").lower() == "y"

        folderName = input("Enter the name of the folder you want to download to: ")
        directory = getDirectory(folderName)
        
        for artist in searchTerms:
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
        
def getDirectory(artist):
    #get environment downloads directory
    downloadsFolder = path.expanduser("~\\Downloads")
    #if downloads folder does not contain a Music folder, create one
    if not path.exists(downloadsFolder + "\\Music"):
        log("Creating directory {}".format(downloadsFolder + "\\Music"))
        makedirs(downloadsFolder + "\\Music")
    
    directoryBase = downloadsFolder + "\\Music"
    if artist == "" or artist == None:
        return directoryBase
    result = directoryBase + "\\" + artist
    log("Setting directory to {}".format(result))
    return result


if __name__ == "__main__":
    run()

