from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import random
import collections
import math
import os
import types
import datetime
import csv
import TitleParser
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
            if 'W' in temp_res['duration']:
                durationFormat+= "%WW"
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
                #temp_res['tags']
            else:
                temp_res['tagLength'] = 0
                temp_res['tags'] = []
            if 'regionRestriction' not in temp_res.keys():
                temp_res['regionRestriction'] = None
            if 'defaultAudioLanguage' not in temp_res.keys():
                temp_res['defaultAudioLanguage'] = None
            if 'defaultLanguage' not in temp_res.keys():
                temp_res['defaultLanguage'] = None
            if 'contentRating' not in  temp_res.keys():
                temp_res['contentRating'] = None
            if 'title' in temp_res.keys():
                temp_res['titleLength'] = len(temp_res['title'])
                #temp_res['title']
                #temp_res['v_title']
            if 'description' in temp_res.keys():
                temp_res['descriptionLength'] = len(temp_res['description'])
                #temp_res['description']
            if 'channelTitle' in temp_res.keys():
                temp_res['channelTitleLength'] = len(temp_res['channelTitle'])
                #temp_res['channelTitle']

            #temp_res['channelId']
            #temp_res['v_id']
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
    
    fileName = 'StringDataForConversion.csv'
    first = False
    writeKeys = True
    fileattr = 'w'
    if os.path.exists(fileName):
        writeKeys = False
        fileattr = 'a'

    with open(fileName, fileattr, encoding='utf8',newline='') as output_file:
        output_file.seek(2)
        while len(vidStats) < 20000:

            rPrefix = generateRandomPrefix()
            rcount = 0
            while rPrefix in vidPrefix:
                rPrefix = generateRandomPrefix()
                rcount +=1
                if (rcount >= 10000):
                    return vidStats
            vidPrefix.append(rPrefix)
            x = 'watch?v='+ rPrefix 
            max_videos=50

            try:
                data, stats = youtube_search(x,max_videos)
            except HttpError as e:
                print ("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))

            #data = convertEncoding(data)
            #stats = convertEncoding(stats)
            vidSamples += data
            vidStats += stats

            print("Collected %s Videos!" % (len(vidStats)))
            if (len(stats) >= 1):
                if first == False:
                    first = True
                    keys = sorted(stats[0].keys())
                    dict_writer = csv.DictWriter(output_file, keys, delimiter="|")
                    if writeKeys:
                        dict_writer.writeheader()
                else:
                    generateCSVfromSamples(stats, dict_writer)
    return vidStats

def generateCSVfromSamples(samples, dict_writer):
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

def fixViewCount():
    readFile = 'NoNullYouTubeData5.csv'
    data = []

    with open(readFile, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row['viewCount'] = int(row['viewCount'])
            if row['viewCount'] <= 10:
                row['viewCount'] = '0-10'
            elif row['viewCount'] <= 100:
                row['viewCount'] = '11-100'
            elif row['viewCount'] <= 1000:
                row['viewCount'] = '101-1,000'
            elif row['viewCount'] <= 10000:
                row['viewCount'] = '1,001-10,000'
            elif row['viewCount'] <= 100000:
                row['viewCount'] = '10,001-100,000'
            elif row['viewCount'] <= 1000000:
                row['viewCount'] = '100,001-1,000,000'
            else:
                row['viewCount'] = '1,000,000+'
            data.append(row)

    with open("Fixed"+readFile,'w',encoding='utf8',newline='') as output_file:
        keys = data[0].keys()
        writer = csv.DictWriter(output_file, keys)
        writer.writeheader()
        writer.writerows(data)

def fixNullByte():
    readFile = 'YouTubeData5.csv'
    data = ''

    with open(readFile) as fd:
        data = fd.read()

    with open("NoNull"+readFile, 'w') as fo:
        fo.write(data.replace('\x00', ''))

#fixNullByte()
#fixViewCount()
s = grabYouTubeSample()
TitleParser.parse_videos(s)
TitleParser.compute_average_views()
TitleParser.gen_compute_average_views(TitleParser.description_dict, 'DescriptionData.csv')
TitleParser.gen_compute_average_views(TitleParser.tag_dict, 'TagData.csv')
