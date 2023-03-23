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

def clickDownload(driver):
    log("Trying to find download button")
    downloadButton = driver.find_element(By.LINK_TEXT, "Download")
    log("Download button found, clicking download")
    downloadButton.click()

def openNewDriverAndDownload(url, video, wait = 15, directory = r"C:\Users\nathaniel\Downloads"):
    driver = getDriver(wait, directory)
    driver.get(url)
    inputVideoUrl(driver, video)
    for j in range(25):
        try:
            log("Try {} to download".format(j + 1))
            clickDownload(driver)
            break
        except KeyboardInterrupt:
            log("KeyboardInterrupt, exiting")
            exit()
        except:
            log("Could not find download button")