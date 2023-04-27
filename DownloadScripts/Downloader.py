from os import listdir, makedirs, path
from selenium.webdriver.common.by import By
from ScrapeLinks import getVideoIds
from HtmlFile import getHtml
from DriverBuilder import getDriver
from Logger import log

#declarations
url = "https://ytmp3.nu/7/youtube-to-mp3"
googleUrl = "https://www.google.com/search?q=hillsong%20site%3Ayoutube.com"
videoUrlBase = "https://www.youtube.com/watch?v="
enter = u'\ue007'
videos = []
wait = 15
def inputVideoUrl(enter, driver, videoUrl):
    urlInput = driver.find_element(By.ID, "url")
    urlInput.send_keys(videoUrl)
    urlInput.send_keys(enter)

def ifErrorClickBack(driver):
    try:
        log("Trying to find error/back button")
        driver.implicitly_wait(1)
        errorButton = driver.find_element(By.LINK_TEXT, "Back")
        log("Back button found, error must have occurred, clicking back")
        errorButton.click()
        raise Exception("Error/Back button found")
    except:
        pass
    driver.implicitly_wait(wait)

def clickDownload(driver):
    log("Trying to find download button")
    downloadButton = driver.find_element(By.LINK_TEXT, "Download")
    log("Download button found, clicking download")
    downloadButton.click()

def closeIfPopUp(driver):
    #the expected page title is "YtMp3 - YouTube to MP3 Converter"
    log("Checking if popup")
    #while window handles is greater than 1, close the popup
    while len(driver.window_handles) > 1:
        log("Popup detected, closing popup")
        driver.switch_to.window(driver.window_handles[1])
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

def clickConvertNext(driver):
    log("Trying to find convert next button")
    convertNextButton = driver.find_element(By.LINK_TEXT, "Convert next")
    log("Convert next button found, clicking convert next")
    convertNextButton.click()

def runDownloadLoop(driver, directory, videos):
    if not path.exists(directory):
        log("Creating directory {}".format(directory))
        makedirs(directory)
        
    i = len(listdir(directory))
    for video in videos:
        log("Cycle " + str(i))
        #the video url is the playlist url without the index and the video id
        videoUrl = videoUrlBase + video
        log("Video url: " + videoUrl)
        inputVideoUrl(enter, driver, videoUrl)
        i += 1
            #if the error button is found, click it and continue to the next loop
        try:
            ifErrorClickBack(driver)
                #if cannot find download button, check for popup or error
            for j in range(35):
                try:
                    log("Try {} to download".format(j + 1))
                    clickDownload(driver)
                    closeIfPopUp(driver)
                    break
                except:
                    log("Could not find download button")
                    closeIfPopUp(driver)
            clickConvertNext(driver)
        except:
            continue
    return i

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

def download(driver = None, html = "", directory = "C:\\Users\\nathaniel\\Downloads\\Music"):
    log("Getting driver")
    if driver == None:
        headless = input("Run headless? (y/n): ").lower() == "y"
        driver = getDriver(wait, directory, headless)

    
    if html == None or html == "":
        html = getHtml()
    if html == "":
        # use the code in ScrapeLinks.py to get the video ids
        playlistUrl = input("Paste the youtube playlist url here: ")

        try:
            driver.get(playlistUrl)
            html = driver.page_source
        except:
            log("Error getting html from playlist url")
            driver.quit()
            exit()

    videos = getVideoIds(html)

    count = len(videos)

    #if count is 0, print "no videos in playlist" and exit
    if count == 0:
        log("No videos in playlist")
        exit()

    log("Number of videos in playlist: " + str(count))

    driver.get(url)

    try:
        i = runDownloadLoop(driver, directory, videos)

    except Exception as e:
        log("Error on cycle " + str(i))
        print(e)
    finally:
        if __name__ == "__main__":
            log("Closing driver")
            driver.quit()
            exit()


if __name__ == "__main__":
    download()