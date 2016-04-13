import re
import csv
import nltk
from nltk.stem import WordNetLemmatizer

class Preprocess(object):
    """docstring for Preprocess"""    
    def __init__(self):
        pass

    # basic process
    def basic_process(self, tweet):
        # process the tweets

        #Convert to lower case
        tweet = tweet.lower()
        #Convert www.* or https?://* to url
        tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','url',tweet)
        #Convert @username to at_user
        tweet = re.sub('@[^\s]+','at_user',tweet)
        #Remove additional white spaces
        tweet = re.sub('[\s]+', ' ', tweet)
        #Replace #word with word
        tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
        #trim
        tweet = tweet.strip('\'"')
        #replace "'s"
        tweet = tweet.replace("'s", '')
        return tweet

    # replace letters which repeated two or more times
    def replace_repeated(self, s):
        # look for 2 or more repetitions of character and replace with the character itself
        pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
        return pattern.sub(r"\1\1", s)

    # get stop word list
    def get_stop_word_list(self, FileName):
        # read the stopwords file and build a list
        stopWords = []

        fp = open(FileName, 'r')
        line = fp.readline()
        while line:
            word = line.strip()
            stopWords.append(word)
            line = fp.readline()
        fp.close()
        return stopWords

    # negation is to add "neg at the end of the word"
    def negation(self, tweet):
        neg = " "

        # find the substring betweetn Negation word and Clause-level punctuation 
        pattern = re.compile(
            r"(.*(never|no|nothing|nowhere|noone|none|not|\
                |havent|hasnt|hadnt|cant|couldnt|shouldnt|\
                |wont|wouldnt|dont|doesnt|didnt|isnt|arent|\
                |n't|aint))([^.:;!?]*)([.:;!?])(.*)")
        m = re.search(pattern, tweet)
        if m:

            # add "neg " at the end of a word
            for w in m.group(3).split():
                neg += w + "neg "

                # restore tweets
            tweet = m.group(1) + neg + m.group(4) + " " + m.group(5)

        return tweet.split()

    # stemming according to WordNet
    def stem_wordnet(self, word):
        wnl = WordNetLemmatizer()

        # obtain the word class
        tag = nltk.pos_tag(nltk.word_tokenize(word))

        # word class for verb can be different, but the first two letters must be "VB"
        if len(tag[0][1]) >= 2 and (tag[0][1])[0:2] == 'VB':
            return wnl.lemmatize(word, 'v')

        else:
            return wnl.lemmatize(word)

    # single word process
    def word_process(self, words, stopWords):
        tmp = []
        for w in words:

            # replace two or more with two occurrences
            w = self.replace_repeated(w)

            # check if the word stats with an alphabet
            val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*", w)

            # ignore if it is a stop word
            if (w in stopWords or val is None):
                continue
            else:
                tmp.append(w)

        return tmp

    # strip punctuations
    def strip_pun(self, words):
        tmp = []
        for w in words:
            # strip symbols in a word
            w = w.strip('\'"?,./')
            # w = w.replace("'s", '')
            if w != '':
                tmp.append(w)

        return tmp

    def strip_tooshort(self, words):
        tmp = []
        for w in words:
            if len(w) > 2:
                tmp.append(w)

        return tmp

    # start getfeatureVector
    def get_fea_vector_and_wordlist(self, tweet, wordlist, stop_words):
        feature_vector = []

        # split tweet into words
        words = tweet.split()

        # preprocess
        words = self.word_process(words, stop_words)

        # stem the word w
        words = [self.stem_wordnet(w) for w in words]

        # negation the tweet
        words = self.negation(" ".join(words))

        # strip punctuations
        words = self.strip_pun(words)

        # strip too short words
        words = self.strip_tooshort(words)

        for w in words:
            feature_vector.append(w)
            if w not in wordlist:
                wordlist.append(w)

        return feature_vector, wordlist