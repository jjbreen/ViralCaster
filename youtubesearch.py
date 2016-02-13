from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import random
import collections
import math
import types
import datetime
import csv
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
    for x in range(math.ceil(len(videos.keys()) / max_videos)):
        maxLength = max_videos*(x+1)
        if maxLength > len(videos.keys()):
            s=",".join(list(videos.keys())[max_videos*x:])
        else:
            s=",".join(list(videos.keys())[max_videos*x:maxLength])
        
    
        #return search_response.get("items", [])
        videos_list_response = youtube.videos().list(id=s,part='id,statistics,localizations,snippet,contentDetails,projectDetails').execute()
        for i in videos_list_response['items']:
            print(i.keys())
            temp_res = dict(v_id = i['id'], v_title = videos[i['id']])
            temp_res.update(i['statistics'])
            temp_res.update(i['contentDetails'])
            temp_res.update(i['snippet'])
            del temp_res['thumbnails']
            temp_res.update(temp_res['localized'])
            del temp_res['localized']
            temp_res['publishedAt'] = datetime.datetime.strptime(temp_res['publishedAt'][:19], "%Y-%m-%dT%H:%M:%S")
            temp_res['publishYear'] = temp_res['publishedAt'].year
            temp_res['publishDay'] = temp_res['publishedAt'].day
            temp_res['publishMonth'] = temp_res['publishedAt'].month
            temp_res['publishHour'] = temp_res['publishedAt'].hour
            temp_res['publishMinute'] = temp_res['publishedAt'].minute
            temp_res['publishSecond'] = temp_res['publishedAt'].second
            del temp_res['publishedAt']

            durationFormat = "P"
            if 'D' in temp_res['duration']:
                durationFormat+= "%dD"
            durationFormat+="T"
            if 'H' in temp_res['duration']:
                durationFormat+= "%HH"
            if 'M' in temp_res['duration']:
                durationFormat+= "%MM"
            if 'S' in temp_res['duration']:
                durationFormat+= "%SS"
            temp_res['duration'] = datetime.datetime.strptime(temp_res['duration'], durationFormat) 
            temp_res['durationDay'] = temp_res['duration'].day
            temp_res['durationHour'] = temp_res['duration'].hour
            temp_res['durationMinute'] = temp_res['duration'].minute
            temp_res['durationSecond'] = temp_res['duration'].second
            del temp_res['duration']
            if 'tags' in temp_res.keys():
                temp_res['tagLength'] = len(temp_res['tags'])
                del temp_res['tags']
            else:
                temp_res['tagLength'] = 0
            if 'regionRestriction' in temp_res.keys():
                del temp_res['regionRestriction']
            if 'defaultAudioLanguage' in temp_res.keys():
                del temp_res['defaultAudioLanguage']
            stats.append(temp_res)

    return search_response.get("items", []), stats
    

def generateRandomPrefix(psize=5):
    cset = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'

    rstr = ''
    for x in range(psize):
        rstr += random.choice(cset)

    print("Generated Random String: %s" % rstr)
    return rstr

def grabYouTubeSample():
    vidSamples = []
    vidStats = []
    vidPrefix = []
    while len(vidStats) < 10000:
        rPrefix = generateRandomPrefix()
        vidPrefix.append(rPrefix)
        x = 'watch?v='+ rPrefix 
        max_videos=50

        try:
            data, stats = youtube_search(x,max_videos)
        except HttpError as e:
            print ("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))

        data = convertEncoding(data)
        stats = convertEncoding(stats)
        vidSamples += data
        vidStats += stats

        print("Collected %s Videos!" % (len(vidStats)))
        #if (len(stats) >= 1):
        #    generateCSVfromSamples(stats)
    return vidStats

def generateCSVfromSamples(samples):
    keys = samples[0].keys()
    print (samples)
    with open('YouTubeData.csv', 'w', encoding='utf8',newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(samples)

def convertEncoding(data):
    if isinstance(data, basestring):
        return data.encode('utf-8')
    elif isinstance(data, collections.Mapping):
        return dict(map(convertEncoding, data.items()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convertEncoding, data))
    else:
        return data


generateCSVfromSamples(grabYouTubeSample())