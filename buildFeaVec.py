from processTweet import processTweet

import re
import csv

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
def getFeatureVector(tweet):
    featureVector = []
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
            featureVector.append(w.lower())
    return featureVector
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

with open('dataset/Sentiment.csv', 'rb') as f:
    reader = csv.reader(f)
    first = True
    st = open('stopWords.txt', 'r')
    stopWords = getStopWordList('stopWords.txt')
    for row in reader:
        if first:
            first = False
            continue
        processedTweet = processTweet(row[15])
        featureVector = getFeatureVector(processedTweet)
        results.append(getCategory(row[5]) + featureVector)

f.close()

with open('featureVector.csv', 'wb') as fp:
    writer = csv.writer(fp)
    for i in range(1,len(results)):
        writer.writerow(results[i])

fp.close()