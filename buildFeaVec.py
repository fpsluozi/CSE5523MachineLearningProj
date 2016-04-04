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

    # find the substring betweetn Negation word and Clause-level punctuation 
    pattern = re.compile(r"(.*(never|no|nothing|nowhere|noone|none|not|havent|hasnt|hadnt|cant|couldnt|shouldnt|wont|wouldnt|dont|doesnt|didnt|isnt|arent|n't|aint))([^.:;!?]*)([.:;!?])(.*)")
    m = re.search(pattern, tweet)
    if m:

        # add "neg " at the end of a word
        for w in m.group(3).split():
           neg += w + "neg "  

        # restore tweets
        tweet = m.group(1) + neg + m.group(4) + " " + m.group(5)
   
    return tweet.split()
# end

# stemming according to WordNet
def stemWordNet(word):
    wnl = WordNetLemmatizer()

    # obtain the word class
    tag = nltk.pos_tag(nltk.word_tokenize(word))
    
    # word class for verb can be different, but the first two letters must be "VB"
    if len(tag[0][1])>= 2 and (tag[0][1])[0:2] == 'VB':
        return wnl.lemmatize(word, 'v')
        
    else:
        return wnl.lemmatize(word)

# preprocess
def preProcess(words):
    
    tmp = []
    for w in words:
        
        #replace two or more with two occurrences
        w = replaceTwoOrMore(w)

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

        # strip symbols in a word
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

        # the 16th column is about tweet
        processedTweet = processTweet(row[15])
        # featureVector = getFeatureVector(processedTweet)
        featureVector, wordList = getFeatureVectorAndWordlist(processedTweet, wordList)

        # reccord feature vector for each tweet
        results.append(featureVector)

        # recoord category for each vector
        cataM.append(getCategory(row[5]))

    wordList = sorted(wordList)

    for i in range(len(results)):
        # combine feature vector and category together
        dataM.append(dataMatrix(results[i], wordList) + cataM[i])

f.close()

# write feature matrix to the file
with open('featureMatrix.csv', 'wb') as fp:
    writer = csv.writer(fp)
    writer.writerow(sorted(wordList))
    for row in dataM:
        writer.writerow(row)

fp.close()