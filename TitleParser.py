import itertools

view_count_dict = {
1: {},
2: {},
3: {},
4: {}
}

def parse_videos(videos):
    print "test"
    i = 0
    #iterate through the list of videos
    for video in videos:
        print "Parsing video " + str(++i)
        #parse out the title into a list
        title = video["v_title"].lower()
        title_words = list(set(title.split())) 
        title_words.sort()
    
        #create tuples with 1-4 words and add them and the view count to the
        #dictionary
        for s in title_words:
            add_to_dict(1, video, s)
        for i in range(2, 5):
            combos = itertools.combinations(title_words, i)
            for s in combos:
                add_to_dict(i, video, s)
        #print view_count_dict
            
def add_to_dict(i, video, s):
    print s
    if s in view_count_dict[i]:
        print "exists"
        view_count_dict[i][s].append(video["viewCount"])
    else:
        print "not exists"
        view_count_dict[i][s] = [video["viewCount"]]

def main():

    test_data = [{
  "kind": "youtube#searchResult",
  "etag": "",
  "id": {
    "kind": "video",
    "videoId": "369"
  },
  "snippet": {
    "publishedAt": "",
    "channelId": "985",
    "title": "epic video title",
    "description": "",
    "thumbnails": {
    },
    "channelTitle": "",
    "liveBroadcastContent": ""
  },
  "statistics": {
      "viewCount": 888
      }
},
                 {
  "kind": "youtube#searchResult",
  "etag": "",
  "id": {
    "kind": "video",
    "videoId": "1234"
  },
  "snippet": {
    "publishedAt": "",
    "channelId": "5678",
    "title": "This is a title IT IS EPIC",
    "description": "",
    "thumbnails": {
    },
    "channelTitle": "",
    "liveBroadcastContent": ""
  },
  "statistics": {
      "viewCount": 4839
      }
}]
    print "test"
    parse_videos(test_data)

if __name__ == "__main__":
    main()