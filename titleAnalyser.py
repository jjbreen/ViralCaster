import csv

metrics = {}

def readMetric():
    with open('metricData.csv', 'r') as csvfile:
       reader = csv.DictReader(csvfile)
       for row in reader:
           metrics[row["word"]] = row["value"]

def calculateValue(title):
    words = title.split()
    values = []
    for word in words:
        if metrics.has_key(word):
            values.append(float(metrics[word]))
        else:
            values.append(0.5)
    
    #print "title values: " + str(values)
    #print "title value: " + str(sum(values) / len(values))
    return sum(values) / len(values)

def main():
    readMetric()
    values = []
    with open('YouTubeData.csv', 'r') as csvfile:
           reader = csv.DictReader(csvfile)

           for row in reader:
              title = row["b'v_title'"][2:-1]
              value = calculateValue(title)
              values.append(value)
               
    with open('YouTubeData.csv', 'r') as csvfile:
       with open('YouTubeData_WithTitleMetric.csv', 'w') as csvOut:
           #write the header out
           header = csvfile.readline().replace('\n', '').replace('\r', '')
           #print header
           csvOut.write(header + ", titleMetric\n")
           for line, value in zip(csvfile, values):
               line = line.replace('\n', '').replace('\r', '')
               csvOut.write(line + ", " + str(value) + '\n')




if __name__ == "__main__":
    main()