# from processTweet import processTweet

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


#initialize stopWords
stopWords = []

#start replaceTwoOrMore
def replaceTwoOrMore(s):
    #look for 2 or more repetitions of character and replace with the character itself
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", s)
#end

#start getStopWordList
def getStopWordList(stopWordListFileName):
    #read the stopwords file and build a list
    stopWords = []
    stopWords.append('AT_USER')
    stopWords.append('URL')

    fp = open("stopWords.txt", 'r')
    line = fp.readline()
    while line:
        word = line.strip()
        stopWords.append(word)
        line = fp.readline()
    fp.close()
    return stopWords
#end

#start getfeatureVector
def getFeatureVectorAndFrequency(tweet,frequency):
    featureVector = []
    # frequency = {}
    # fre = []
    #split tweet into words
    words = tweet.split()
    for w in words:
        #replace two or more with two occurrences
        w = replaceTwoOrMore(w)
        #strip punctuation
        w = w.strip('\'"?,.')
        #check if the word stats with an alphabet
        val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*$", w)
        #ignore if it is a stop word
        if(w in stopWords or val is None):
            continue
        else:
            # print w
            featureVector.append(w.lower())
            if w not in frequency:
                frequency[w] = 1
                # fre.append(w)
            else:
                frequency[w] += 1

    return featureVector, frequency
#end

def getCategory(attribute):
    if attribute == "Positive":
        return ["1","0","0"]
    elif attribute == "Negative":
        return ["0","1","0"]
    elif attribute == "Neutral":
        return ["0","0","1"]
    else:
        # raise ValueError('Attribute is wrong')
        raise ValueError('Attribute is wrong')

results = []
frequency = {}

with open('Sentiment.csv', 'rb') as f:
    reader = csv.reader(f)
    first = True
    st = open('stopWords.txt', 'r')
    stopWords = getStopWordList('stopWords.txt')
    for row in reader:
        if first:
            first = False
            continue
        processedTweet = processTweet(row[15])
        featureVector, frequency = getFeatureVectorAndFrequency(processedTweet, frequency)

f.close()

with open('frequency.csv', 'wb') as fp:
    writer = csv.writer(fp)
    writer.writerows(sorted(frequency.items()))

fp.close()




