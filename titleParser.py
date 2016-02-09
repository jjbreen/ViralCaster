import itertools

def parse_videos(videos):
	print "test"
	video = videos[0]

	title = video["snippet"]["title"].lower()
	print title
	singles = itertools.combinations(title.split(), 1);
	doubles = itertools.combinations(title.split(), 2);
	triples = itertools.combinations(title.split(), 3);
	quads = itertools.combinations(title.split(), 4);

	for s in singles: print s
	for s in doubles: print s
	for s in triples: print s
	for s in quads: print s

def main():

	test_data = [{
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