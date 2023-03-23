import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from ScrapeLinks import getVideoIds
from HtmlFile import getHtml

def inputVideoUrl(playlistUrlWithoutIndex, enter, driver, i):
    urlInput = driver.find_element(By.ID, "url")
    videoUrl = playlistUrlWithoutIndex + videos[i]
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

def log(m):
    try:
        #print timestamp and message
        t = time.localtime()
        c = time.strftime("%Y-%m-%d %H:%M:%S", t)
        print(c + " " + m)
    except:
        pass

#declarations
url = "https://ytmp3.nu/7/youtube-to-mp3"
videoUrlBase = "https://www.youtube.com/watch?v="
directory = r"C:\Users\nathaniel\Downloads\Music\Beethoven Piano Sonatas"
enter = u'\ue007'
html = ""
videos = []
wait = 15

options = Options()
options.page_load_strategy = 'normal'
options.add_experimental_option("prefs", { "profile.default_content_settings.popups": 0,\
                                           "download.default_directory":directory,\
                                           "download.prompt_for_download": False,\
                                           "download.directory_upgrade": True })
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(wait)

html = getHtml()
if html == "":
    # use the code in ScrapeLinks.py to get the video ids
    playlistUrl = input("Paste the youtube playlist url here: ")

    try:
        driver.get(playlistUrl)
        html = driver.page_source
    except:
        html = input("That didn't work. Please paste in the html: ")

videos = getVideoIds(html)

count = len(videos)

#if count is 0, print "no videos in playlist" and exit
if count == 0:
    log("No videos in playlist")
    exit()

log("Number of videos in playlist: " + str(count))

driver.get(url)

try:
    i = 0
    for video in videos:
        log("Cycle " + str(i))
        inputVideoUrl(videoUrlBase, enter, driver, i)
        i += 1
        #if the error button is found, click it and continue to the next loop
        try:
            ifErrorClickBack(driver)
            #if cannot find download button, check for popup or error
            for j in range(15):
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

except Exception as e:
    log("Error on cycle " + str(i))
    print(e)
finally:
    log("Closing driver")
    driver.quit()
    exit()