import itertools
import time
import io
import csv

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
        print "Parsing video " + video["v_id"]
        #parse out the title into a list
        title = video["v_title"].lower()
        title_words = list(set(title.split())) 
        title_words.sort()
    
        #create tuples with 1-4 words and add them and the view count to the
        #dictionary
        for s in title_words:
            add_to_dict(1, video, s)
        for i in range(2, 4):
            combos = itertools.combinations(title_words, i)
            for s in combos:
                add_to_dict(i, video, s)
        #print view_count_dict
            
def add_to_dict(i, video, s):
    #print s
    if s in view_count_dict[i]:
        #print "exists"
        view_count_dict[i][s].append(video["viewCount"])
    else:
        #print "not exists"
        view_count_dict[i][s] = [video["viewCount"]]


def compute_average_views():
    summarized_views_dict = {}
    max_avg_views = 0
    max_avg_views_words = ""

    for size in view_count_dict:
        dict = view_count_dict[size]   
        for words in dict:
            summarized_views_dict[words] = {}
            views = [int(x) for x in dict[words]]
            summarized_views_dict[words]["words"] = words
            summarized_views_dict[words]["average"] = str(sum(views) / len(views))
            summarized_views_dict[words]["max"] = str(max(views))
            summarized_views_dict[words]["min"] = str(min(views))
            if str(sum(views) / len(views)) > max_avg_views:
                max_avg_views =  str(sum(views) / len(views))
                max_avg_views_words = words

    print "BEST AVERAGE: " + str(max_avg_views) + " with: " + str(max_avg_views_words)
    print summarized_views_dict[max_avg_views_words]
    write_summary(summarized_views_dict)
    create_metric()

def write_summary(summarized_views_dict):
    print "OPENING"
    with open('titleData.csv', 'w') as output_file:
        print "OPEN"
        keys = ['words', 'average', 'max', 'min']
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        for summary in summarized_views_dict:
            #print "Writing Line"
            #print summarized_views_dict[summary]
            dict_writer.writerow(summarized_views_dict[summary])

def create_metric():
    dict = view_count_dict[1]
    max_avg = 0

    for words in dict:
        views = [int(x) for x in dict[words]]
        avg = sum(views) / float(len(views))
        if avg > max_avg:
            max_avg = avg

    with open('metricData.csv', 'w') as output_file:
        print "OPEN"
        keys = ['word', 'value']
        dict_writer = csv.DictWriter(output_file, keys, lineterminator='\n',)
        dict_writer.writeheader() 

        for words in dict:
            views = [int(x) for x in dict[words]]
            avg = sum(views) / float(len(views))
            value = avg/max_avg
            out = {"word": words, "value": value}
            dict_writer.writerow(out)


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