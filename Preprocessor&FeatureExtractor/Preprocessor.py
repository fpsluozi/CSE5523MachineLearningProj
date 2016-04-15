import re
import csv
import nltk
from nltk.stem import WordNetLemmatizer

class Preprocessor(object):
    def __init__(self, file):
        self.get_stop_word_list(file)
        
    def get_stop_word_list(self, fileName):
        # read the stopwords file and build a list
        self.stopWords = []

        fp = open(fileName, 'r')
        line = fp.readline()
        while line:
            word = line.strip()
            self.stopWords.append(word)
            line = fp.readline()
        fp.close()

    # replace letters which repeated two or more times
    def replace_repeated(self, word):
        # look for 2 or more repetitions of character and replace with the character itself
        pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
        return pattern.sub(r"\1\1", word)
    
    def basic_process(self, tweet):

        #Convert to lower case
        tweet = tweet.lower()
        #Convert www.* or https?://* to url
        tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','url',tweet)
        #Remove non_Unicode characters
        tweet = re.sub(r'[^\x00-\x7F]+','', tweet)
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
        
    # single word level advanced process
    def advanced_process(self, words):
        new_words = []
        for w in words:
            # replace two or more with two occurrences
            w = self.replace_repeated(w)

            # check if the word stats with an alphabet
            val = re.search(r"^[a-zA-Z][a-zA-Z0-9]+", w)

            # ignore if it is a stop word
            if (w in self.stopWords or val is None):
                continue
            else:
                # partially strip punctuations, keep those punctuations useful for negation
                w = w.strip('\'",/')
                #strip too short word (len(w)) <= 2
                if w != '':
                    new_words.append(w)
        return new_words
    
    # tweet level basic process
    def preprocess(self, tweet):
        # process the tweets
        tweet = self.basic_process(tweet)
        
        # split tweet into words
        words = tweet.split()
        
        # preprocess
        words = self.advanced_process(words)
        
        return words