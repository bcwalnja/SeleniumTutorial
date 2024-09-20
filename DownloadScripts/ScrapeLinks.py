import re

def getVideoIds(html):
    videoIds = re.findall(r"(\?v=)([\w-]+)", html)
    videoIds = [videoId[1] for videoId in videoIds]
    videoIds = list(set(videoIds))

    return videoIds

def getMP3Links(xml):
    mp3Links = re.findall(r'(url="https://aphid.*?mp3")', xml)
    mp3Links = [mp3Link[5:-1] for mp3Link in mp3Links]
    mp3Links = list(set(mp3Links))
    return mp3Links
