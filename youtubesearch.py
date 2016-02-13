from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import random
import collections
import math
import types
try:
    unicode = unicode
except NameError:
    # 'unicode' is undefined, must be Python 3
    str = str
    unicode = str
    bytes = bytes
    basestring = (str,bytes)
else:
    # 'unicode' exists, must be Python 2
    str = str
    unicode = unicode
    bytes = str
    basestring = basestring
##
import pandas as pd


# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "AIzaSyA88bWmeLWQg5x4axkN-Um_BSPdqzxh5DY"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"



def youtube_search(q,max_videos):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)
    
    # Call the search.list method to retrieve results matching the specified
    search_response = youtube.search().list(q=q,part="id,snippet",maxResults=max_videos).execute()
    videos = {}
    
    nextPageToken = search_response.get('nextPageToken')
    while ('nextPageToken' in search_response):
        nextPage = youtube.search().list(
        q=q,
        part="id,snippet",
        maxResults=max_videos,
        pageToken=nextPageToken
        ).execute()
        search_response['items'] = search_response['items'] + nextPage['items']

        if 'nextPageToken' not in nextPage:
            search_response.pop('nextPageToken', None)
        else:
            nextPageToken = nextPage['nextPageToken']
    
    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videos[search_result["id"]["videoId"]] = search_result["snippet"]["title"]
            #videos.append("%s (%s)" % (search_result["snippet"]["title"],search_result["id"]["videoId"]))
    
    print ("Videos:\n", "\n".join(videos), "\n")

    stats = []
    for x in range(int(math.ceil(len(videos.keys()) / max_videos))):
        maxLength = max_videos*(x+1)
        if maxLength > len(videos.keys()):
            s=",".join(list(videos.keys())[max_videos*x:])
        else:
            s=",".join(list(videos.keys())[max_videos*x:maxLength])
        
    
        #return search_response.get("items", [])
        videos_list_response = youtube.videos().list(id=s,part='id,statistics').execute()
        for i in videos_list_response['items']:
            temp_res = dict(v_id = i['id'], v_title = videos[i['id']])
            temp_res.update(i['statistics'])
            stats.append(temp_res)

    return search_response.get("items", []), stats
    

def generateRandomPrefix(psize=5):
    cset = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'

    rstr = ''
    for x in range(psize):
        rstr += random.choice(cset)

    print("Generated Random String: %s" % rstr)
    return rstr

def grabYouTubeSample(total_videos):
    vidSamples = []
    vidStats = []
    vidPrefix = []
    while len(vidStats) < total_videos:
        rPrefix = generateRandomPrefix()
        vidPrefix.append(rPrefix)
        x = 'watch?v='+ rPrefix 
        max_videos=50

        #try:
        data, stats = youtube_search(x,max_videos)
        #except HttpError as e:
            #print ("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))

        print "Stats Length: " + str(len(stats))
        #data = convertEncoding(data)
        stats = convertEncoding(stats)
        #print (stats)
        vidSamples += data
        vidStats += stats
        print("Collected %s Videos!" % (len(vidStats)))
        print "OF " + str(total_videos)
    
    return vidSamples, vidStats


def convertEncoding(data):
    if isinstance(data, basestring):
        return data.encode('utf-8')
    elif isinstance(data, collections.Mapping):
        return dict(map(convertEncoding, data.items()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convertEncoding, data))
    else:
        return data