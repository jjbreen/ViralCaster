import TitleParser
import youtubesearch as youtube











def main():
    stats = youtube.grabYouTubeSample(10000)
    #print len(videos)
    print len(stats)
    #print videos
    print stats
    print "FINISHED COLLECTION"
    print "STARTING PARSING"
    TitleParser.parse_videos(stats)
    print "COMPUTING AVERAGES"
    TitleParser.compute_average_views()
    print "COMPLETE"












if __name__ == "__main__":
    main()