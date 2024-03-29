from os import listdir, mkdir, path as p
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
directory = r"Music"
headless = False

if __name__ == "__main__":
    try:
        
        #get path by finding local environment download folder and appending "directory" to it
        path = r"C:\Users\{}\Downloads\{}".format(listdir(r"C:\Users")[1], directory)
        #if folder doesn't exist, create it
        if not p.exists(path):
            log("Creating directory: " + path)
            mkdir(path)
        #if user inputs "y", add headless option
        driver = getDriver(wait, path, True)
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
        headless = input("Headless? (y/n): ") == "y"

        try:
            #index starts at the number of files in the download directory, so skip downloading them again
            i = len(listdir(path))
            processes = []
            for video in videos:
                try:
                    log("Cycle {} of {}".format(i + 1, count))
                    #use Process to start openNewDriverAndDownload(url, video) in a new process
                    openNewDriverAndDownload(url, video, wait, path, headless)
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
        try:
            if driver is not None:
                driver.quit()
        except:
            pass
        exit()