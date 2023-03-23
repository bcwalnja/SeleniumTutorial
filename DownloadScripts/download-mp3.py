from os import listdir
from selenium.webdriver.common.by import By
from ScrapeLinks import getVideoIds
from HtmlFile import getHtml
from Logger import log
from DriverBuilder import getDriver


#####################
#     functions     #
#####################
def inputVideoUrl(playlistUrlWithoutIndex, enter, driver, i):
    log("Trying to url text edit")
    urlInput = driver.find_element(By.ID, "url")
    videoUrl = playlistUrlWithoutIndex + videos[i]
    log("Url text edit found, inputting url {}".format(videoUrl)) 
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
        log("Popup detected, closing popup " + driver.window_handles[1].title)
        driver.switch_to.window(driver.window_handles[1])
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

def clickConvertNext(driver):
    log("Trying to find convert next button")
    convertNextButton = driver.find_element(By.LINK_TEXT, "Convert next")
    log("Convert next button found, clicking convert next")
    convertNextButton.click()



#####################
#   declarations    #
#####################
url = "https://ytmp3.nu/7/youtube-to-mp3"
videoUrlBase = "https://www.youtube.com/watch?v="
enter = u'\ue007'
html = ""
videos = []
wait = 15
directory = r"C:\Users\nathaniel\Downloads\Music\Beethoven Piano Sonatas"

try:
    driver = getDriver(wait, directory)

    html = getHtml()
    if html == "":
        # use the code in ScrapeLinks.py to get the video ids
        playlistUrl = input("Paste the youtube playlist url here: ")

        try:
            driver.get(playlistUrl)
            html = driver.page_source
        except Exception as e:
            errorMessage = "An error of type {} occurred.".format(type(e).__name__)
            html = input("That didn't work. {} \nPlease paste in the html: ".format(errorMessage))

    videos = getVideoIds(html)

    count = len(videos)

    #if count is 0, print "no videos in playlist" and exit
    if count == 0:
        log("No videos in playlist")
        exit()

    log("Number of videos in playlist: " + str(count))

    #check how many files are already in the download directory
    #use the number of files to set the starting index

    driver.get(url)
    
    try:
        #index starts at the number of files in the download directory, so skip downloading them again
        i = len(listdir(directory))
        for video in videos:
            log("Cycle {} of {}".format(i + 1, count))
            inputVideoUrl(videoUrlBase, enter, driver, i)
            i += 1
            #if the error button is found, click it and continue to the next loop
            try:
                ifErrorClickBack(driver)
                #if cannot find download button, check for popup or error
                for j in range(25):
                    try:
                        log("Try {} to download".format(j + 1))
                        clickDownload(driver)
                        closeIfPopUp(driver)
                        break
                    except:
                        log("Could not find download button")
                        closeIfPopUp(driver)
                clickConvertNext(driver)
            except KeyboardInterrupt:
                log("Program has been interrupted.")
                exit()
            except:
                continue
        log("Program has completed successfully.")
    #except keyboard interrupt, print "program has been interrupted"
    except Exception as e:
        print(e)
        log("Program has failed. Error on cycle " + str(i))

except KeyboardInterrupt:
    log("Program has been interrupted.")
except Exception as e:
    print(e)
    log("Program has failed.")
finally:
    log("Closing driver and exiting.")
    #if the driver is not null or closed, close it
    if driver is not None:
        driver.quit()
    exit()