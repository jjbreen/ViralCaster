import itertools

view_count_dict = {
1: {},
2: {},
3: {},
4: {}
}

def parse_videos(videos):
    print "test"

    #iterate through the list of videos
    for video in videos:

        #parse out the title into a list
        title = video["snippet"]["title"].lower()
        title_words = list(set(title.split())) 
        title_words.sort()
    
        #create tuples with 1-4 words and add them and the view count to the
        #dictionary
        for s in title_words:
            add_to_dict(1, video, s)
        for i in range(2, 5):
            print i
            combos = itertools.combinations(title_words, i)
            for s in combos:
                add_to_dict(i, video, s)
        print view_count_dict
            
def add_to_dict(i, video, s):
    print s
    if s in view_count_dict[i]:
        print "exists"
        view_count_dict[i][s].append(video["statistics"]["viewCount"])
    else:
        print "not exists"
        view_count_dict[i][s] = [video["statistics"]["viewCount"]]

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

    """
    global STRATEGY_CLASS, TRAINING_TIME, BACKTEST_TIME, EPOCHS, IS_NORMALIZE
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--strategy_num", default=1, type=int, choices=[key for key in strategy_dict])
    parser.add_argument("-t", "--training_time", default=1, type=int, choices=[year for year in range(0,14)])
    parser.add_argument("-b", "--backtest_time", default=1, type=int, choices=[year for year in range(0,14)])
    parser.add_argument("-e", "--epochs", default=2000, type=int)
    parser.add_argument("-z", "--normalize", action='store_false', help='Turn normalization off.')
    parser.add_argument("-o", "--overfit", action='store_false', help='Perform test with overfitting.')
    args = parser.parse_args()
    STRATEGY_CLASS = strategy_dict[args.strategy_num]
    TRAINING_TIME = args.training_time
    BACKTEST_TIME = args.backtest_time
    EPOCHS = args.epochs
    IS_NORMALIZE = args.normalize
    IS_OVERFIT = args.overfit
    if not IS_OVERFIT: #or not IS_NORMALIZE
        print "ERROR: not implemented"; return
    print "Using:", str(STRATEGY_CLASS)
    print "Train", TRAINING_TIME, "year,", "Test", BACKTEST_TIME, "year."
    runMaster()"""

if __name__ == "__main__":
    main()