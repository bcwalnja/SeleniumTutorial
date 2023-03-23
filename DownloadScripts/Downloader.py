from os import path
from time import sleep
from selenium.webdriver.common.by import By
from DriverBuilder import getDriver
from Logger import log

#####################
#     functions     #
#####################
def inputVideoUrl(driver, video):
    log("Trying to url text edit")
    urlInput = driver.find_element(By.ID, "url")
    playlistUrlWithoutIndex = "https://www.youtube.com/watch?v="
    videoUrl = playlistUrlWithoutIndex + video
    log("Url text edit found, inputting url {}".format(videoUrl))
    urlInput.send_keys(videoUrl)
    enter = u'\ue007'
    urlInput.send_keys(enter)

def closeIfPopUp(driver):
    #the expected page title is "YtMp3  YouTube to MP3 Converter"
    log("Checking if popup")
    #while window handles is greater than 1, close the popup
    while len(driver.window_handles) > 1:
        log("Popup detected, closing popup " + driver.window_handles[1].title)
        driver.switch_to.window(driver.window_handles[1])
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

def clickDownload(driver):
    log("Trying to find download button")
    downloadButton = driver.find_element(By.LINK_TEXT, "Download")
    log("Download button found, clicking download")
    title = driver.find_element(By.CSS_SELECTOR, "form > div:nth-child(1)")
    downloadButton.click()
    return title

def openNewDriverAndDownload(url, video, wait = 15, directory = r"C:\Users\nathaniel\Downloads", headless = False):
    try:
        driver = getDriver(wait, directory, headless)
        driver.get(url)
        inputVideoUrl(driver, video)
        found = False

        for j in range(25):
            try:
                log("Try {} to download".format(j + 1))
                title = clickDownload(driver)
                found = True
                break
            except KeyboardInterrupt:
                log("KeyboardInterrupt, exiting")
                exit()
            except:
                pass
        if not found:
            log("Download button not found")
            exit()

        sleep(1)
        closeIfPopUp(driver)
        
        log("Title found: " + title.text)

        text = title.text.replace(":", "_")

        while path.exists(directory + "\\" + text + ".mp3" + ".crdownload"):
            log("Waiting for download")
            sleep(1)
    except KeyboardInterrupt:
        log("KeyboardInterrupt, exiting")
        exit()