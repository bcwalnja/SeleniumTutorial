from DriverBuilder import getDriver
from Logger import log
from Downloader import download, setDirectory, setHtml

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
    #get the list of artists
    for artist in artists:
        log("Searching for {}".format(artist))
        #for each artist, navigate the driver to the googleUrl search page for that artist
        driver = getDriver()
        url = googleUrl[0] + artist + googleUrl[1]
        log("Navigating to {}".format(url))
        driver.get(url)

        #extract the html from the page
        html = driver.page_source
        log("html line count: {}".format(len(html.splitlines())))
        #in Downloader.py set the html to the html from the page
        log("Setting html")
        setHtml(html)
        #set the directory to the artist name
        log("Setting directory to {}".format(artist))
        setDirectory(artist)
        #call the download function\
        log("Downloading")
        download()

