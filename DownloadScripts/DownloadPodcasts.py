from os import makedirs
from os import path
from os import rename
import re
from Logger import log
import requests
import eyed3

from HtmlFile import getXml
from ScrapeLinks import getMP3Links

def getDirectory():
    #get environment downloads directory
    downloadsFolder = path.expanduser("~\\Downloads")
    #if downloads folder does not contain a Podcasts folder, create one
    podcastsFolder = downloadsFolder + "\\Podcasts"
    if not path.exists(podcastsFolder):
        log("Creating directory {}".format(downloadsFolder + "\\Podcasts"))
        makedirs(downloadsFolder + "\\Podcasts")

    log("returning directory {}".format(podcastsFolder))
    return podcastsFolder

def cleanTitle(title):
    title = padNumbers(title)
    title = removeIllegalCharacters(title)
    title = title.replace("The BEMA Podcast", "BEMA")

    return title

def padNumbers(title):
    if re.search(r"(\d{1,2})", title) and not re.search(r"(\d{3})", title):
        log("title: {}".format(title))
        test = True

    
    # pad the episode number to three digits
    title = re.sub(r"(\d{1,3}):?", lambda x: x.group(1).zfill(3) + ":", title)

    # if the title ends up with duplicate episode numbers, remove all but one
    title = re.sub(r"(\d{3}): ?(\d{3})", lambda x: x.group(1), title)

    return title

def removeIllegalCharacters(title):
    invalid_chars = [":", "/", "\\", "*", "|", "<", ">", "\"", "?", "\\xa0"]
    for char in invalid_chars:
        title = title.replace(char, "")
    title = title.replace("  ", " ")
    title = title.replace("—", "-")
    return title

def download_podcast(url, folder):
    log("Downloading...")
    response = requests.get(url)

    # filename = first six digits of hash of url
    filename = str(hash(url))[:6]
    filename = cleanTitle(filename)
    
    filepath = path.join(folder, filename + '.mp3')
    with open(filepath, 'wb') as f:
        log("Writing...")
        f.write(response.content)
    
    tag = eyed3.load(filepath).tag
    log("title: {}".format(tag))
    filename = cleanTitle(tag.title)

    # if the filename is reduced to "BEMA ###", add the episode title
    # by searching the xml for the episode title
    episode = re.search(r"(\d{1,3})", filename).group(1)
    missingTitle = "BEMA " + episode
    if filename == missingTitle:
        log("Searching for episode title")
        xml = getXml()
        start = xml.find("<title>" + str(int(episode)) + ": ")
        if start > -1:
            end = xml.find("</title>", start)
            episodeTitle = xml[start + 7:end]
            episodeTitle = episodeTitle.replace(str(int(episode)) + ":", "")
            filename = filename + episodeTitle
            filename = cleanTitle(filename)

    if filename != "":
        log("Renaming file to {}".format(filename))
        rename(filepath, path.join(folder, filename + '.mp3'))
    log("Loop finished")
        
if __name__ == '__main__':
    log("Getting xml")
    xml = getXml()
    log("Getting mp3 links")
    mp3s = getMP3Links(xml)
    folder = getDirectory()

    for i, mp3 in enumerate(mp3s):
        log("Downloading podcast {} of {}".format(i + 1, len(mp3s)))
        download_podcast(mp3, folder)