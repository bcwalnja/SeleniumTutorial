#prompt the user in the console to paste in the entire html from the youtube playlist page
import re

def getVideoIds(html):
    #capture the video ids from the html using the regex pattern
    #(\/(?:[\w\-]+\?v=|embed\/|v\/)?)$
    #the video ids are the second group captured
    videoIds = re.findall(r"(\?v=)(\w+)", html)
    videoIds = [videoId[1] for videoId in videoIds]
    videoIds = list(set(videoIds))

    return videoIds