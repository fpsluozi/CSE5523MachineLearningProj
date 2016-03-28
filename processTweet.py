import re
import csv

#start process_tweet
def processTweet(tweet):
    # process the tweets

    #Convert to lower case
    tweet = tweet.lower()
    #Convert www.* or https?://* to URL
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',tweet)
    #Convert @username to AT_USER
    tweet = re.sub('@[^\s]+','AT_USER',tweet)
    #Remove additional white spaces
    tweet = re.sub('[\s]+', ' ', tweet)
    #Replace #word with word
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    #trim
    tweet = tweet.strip('\'"')
    return tweet

results = []

with open('Sentiment.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        processedTweet = processTweet(row[15])
        results.append(processedTweet)

f.close()

tmp = []

with open('result.csv', 'wb') as fp:
    writer = csv.writer(fp)
    for i in range(len(results)):
        writer.writerow([results[i]])

fp.close()

