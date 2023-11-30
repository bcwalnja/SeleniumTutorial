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
artists = ["Switchfoot LET IT HAPPEN",
    "Switchfoot NATIVE TONGUE",
    "Switchfoot Al I I NEED",
    "Switchfoot VOICES",
    "Switchfoot DIG NEW STREAMS",
    "Switchfoot JOY INVINCIBLE",
    "Switchfoot PRODIGAL SOUL",
    "Switchfoot THE HARDEST ART",
    "Switchfoot WONDERFUL FEELING",
    "Switchfoot TAKE MY FIRE",
    "Switchfoot THE STRENGTH TO Let Go"]
wait = 15

def run():
    try:
        log("Starting MultiSearcher")
        headless = input("Run headless? (y/n): ").lower() == "y"

        folderName = input("Enter the name of the folder you want to download to: ")
        directory = getDirectory(folderName)
        
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