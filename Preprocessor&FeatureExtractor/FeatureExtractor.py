import re
import csv
from MisspellingCorrector import MisspellingCorrector
import enchant

class FeatureExtractor(object):
    def __init__(self, usingCorrection = False, usingNegation = False):
        self.usingCorrection = usingCorrection
        self.usingNegation = usingNegation 
        if usingNegation and usingCorrection:
            self.corrector = MisspellingCorrector('string_pairs_correction_Twitter.txt')
            self.corrector.train()
            self.d = enchant.Dict("en_US")
            self.feature_space = self.get_feature_space('negation_correction_featurespace.txt')
        elif usingNegation and not usingCorrection:
            self.feature_space = self.get_feature_space('negation_featurespace.txt')
        elif not usingNegation and usingCorrection:
            self.corrector = MisspellingCorrector('string_pairs_correction_Twitter.txt')
            self.corrector.train()
            self.d = enchant.Dict("en_US")
            self.feature_space = self.get_feature_space('correction_featurespace.txt')
        else:
            self.feature_space = self.get_feature_space('featurespace.txt')
            
    def get_feature_space(self,fileName):
        self.feature_space = []
        fp = open(fileName)
        line = fp.readline()
        while line:
            word = line.strip()
            self.feature_space.append(word)
            line = fp.readline()
        fp.close()
        return sorted(self.feature_space)

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
            
    # strip punctuations
    def strip_punct(self, words):
        tmp = []
        for w in words:
            # strip symbols in a word
            w = re.sub(r'[\'"?:*,./!]+','',w)
            # w = w.replace("'s", '')
            if w != '':
                tmp.append(w)

        return tmp
        
    def extract_features(self, words):
        if self.usingNegation and self.usingCorrection:
            new_words = []
            words = self.negation(" ".join(words))
            
            # Remove punctuations
            words = re.findall(r"[\w']+[a-zA-Z0-9]", " ".join(words))
            
            for word in words:
                if self.d.check(word):
                    new_words.append(word)
                else:
                    if (word[-3:] == 'neg'):
                        word = self.corrector.correct(word[:-3])
                        new_words.append(word + 'neg')
            return new_words
            # Deal with negation
        
        elif self.usingNegation and not self.usingCorrection:
            words = self.negation(" ".join(words))
            
            # Remove punctuations
            words = re.findall(r"[\w']+[a-zA-Z0-9]", " ".join(words))
            return words
            
        elif not self.usingNegation and self.usingCorrection:
            new_words = []
            
            words = re.findall(r"[\w']+[a-zA-Z0-9]", " ".join(words))
            
            for word in words:
                if self.d.check(word):
                    new_words.append(word)
                else:
                    if (word[-3:] == 'neg'):
                        word = self.corrector.correct(word[:-3])
                        new_words.append(word + 'neg')
            return new_words
            
        else:
            words = re.findall(r"[\w']+[a-zA-Z0-9]", " ".join(words))
            return words
            
    def build_feature_vector(self, words):
        feature_vector = [0] * len(self.feature_space)
        for word in words:
            if word in self.feature_space:
                feature_vector[self.feature_space.index(word)] += 1
            else:
                print word
        return feature_vector