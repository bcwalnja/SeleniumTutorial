from os import listdir
from selenium.webdriver.common.by import By
from ScrapeLinks import getVideoIds
from HtmlFile import getHtml
from Logger import log
from DriverBuilder import getDriver
from Downloader import openNewDriverAndDownload
from multiprocessing import Process

#####################
#   declarations    #
#####################
url = "https://ytmp3.nu/7/youtube-to-mp3"
videoUrlBase = "https://www.youtube.com/watch?v="
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
            try:
                log("Cycle {} of {}".format(i + 1, count))
                #use Process to start openNewDriverAndDownload(url, video) in a new process
                p = Process(target=openNewDriverAndDownload, args=(url, video, wait, directory))
                p.start()
                p.join()
                i += 1
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