from processTweet import processTweet

import re
import csv
import nltk
from nltk.stem import WordNetLemmatizer

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

# negation is to add "neg at the end of the word"
def negation(tweet):
    neg = " "

    # pay attention to "n't"
    pattern = re.compile(r"(.*(never|no|nothing|nowhere|noone|none|not|havent|hasnt|hadnt|cant|couldnt|shouldnt|wont|wouldnt|dont|doesnt|didnt|isnt|arent|n't|aint))([^.:;!?]*)([.:;!?])(.*)")
    m = re.search(pattern, tweet)
    if m:
        for w in m.group(3).split():
           neg += w + "neg "  

        tweet = m.group(1) + neg + m.group(4) + " " + m.group(5)
   
    return tweet.split()

# stemming according to WordNet
def stemWordNet(word):
    wnl = WordNetLemmatizer()
    tag = nltk.pos_tag(nltk.word_tokenize(word))
    
    if len(tag[0][1])>= 2 and (tag[0][1])[0:2] == 'VB':
        return wnl.lemmatize(word, 'v')
        
    else:
        return wnl.lemmatize(word)

# preprocess
def preProcess(words):
    
    tmp = []
    for w in words:
        # w = w.lower() 
        #replace two or more with two occurrences
        w = replaceTwoOrMore(w)
        #strip punctuation
        # w = w.strip('\'"?,.')
        #check if the word stats with an alphabet
        val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*", w)
        #ignore if it is a stop word
        if(w in stopWords or val is None):
            continue
        else:
            tmp.append(w)
        
    return tmp

def stripPun(words):
    tmp = []
    for w in words:
        w = w.strip('\'"?,./')
        tmp.append(w)
        
    return tmp

#start getfeatureVector
def getFeatureVectorAndWordlist(tweet,wordList):
    featureVector = []

    #split tweet into words
    words = (tweet.lower()).split()
    # print words

    # preprocess
    words = preProcess(words)
    # print words

    # stem the word w
    words = [stemWordNet(w) for w in words]
    # print words

    # negation the tweet
    words = negation(" ".join(words))
    
    # strip punctuations
    words = stripPun(words)
    # print words

    for w in words:
        featureVector.append(w)
        if w not in wordList:
            wordList.append(w) 

    return featureVector, wordList
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
        print attribute
        raise ValueError('Attribute is wrong')

def dataMatrix(tweet, wordList):
    data = [0 for i in range(len(wordList))]
    # words = tweet.split()
    for w in tweet:
        data[wordList.index(w)] += 1

    # print data
    return data

results = []
wordList = []
dataM = []
cataM = []

with open('dataset/test.csv', 'rb') as f:
    reader = csv.reader(f)
    first = True
    st = open('stopWords.txt', 'r')
    stopWords = getStopWordList('stopWords.txt')
    for row in reader:
        if first:
            first = False
            continue
        processedTweet = processTweet(row[15])
        # featureVector = getFeatureVector(processedTweet)
        featureVector, wordList = getFeatureVectorAndWordlist(processedTweet, wordList)
        # print featureVector, '\n'

        results.append(featureVector)
        cataM.append(getCategory(row[5]))

    wordList = sorted(wordList)

    for i in range(len(results)):
        dataM.append(dataMatrix(results[i], wordList) + cataM[i])

f.close()

with open('featureMatrix.csv', 'wb') as fp:
    writer = csv.writer(fp)
    writer.writerow(sorted(wordList))
    for row in dataM:
        writer.writerow(row)

fp.close()