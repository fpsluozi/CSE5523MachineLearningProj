# coding: utf-8

import numpy as np
from sklearn.cross_validation import train_test_split
from numpy.random import shuffle 
from sklearn.metrics import accuracy_score
from pyhacrf import StringPairFeatureExtractor
from pyhacrf import Hacrf
from scipy.optimize import fmin_l_bfgs_b
import random
import levenshtein
import heapq

class MisspellingCorrection:
    def __init__(self, infile):
        lines = open(infile, 'r').readlines()
        # Generate Positive Correction Pair
        ppairs = []
        ppairs = [line.split('\t')[1].strip().split(' | ') for line in lines]
        ppairs = [(pair[0], pair[i]) for pair in ppairs for i in xrange(1, len(pair))]
        self.dictionary = [pair[i] for pair in ppairs for i in xrange(1, len(pair))]
        
        # Generate Positive Training Correction Pairs and Testing Correction Pairs
        ppairs_train, ppairs_test = train_test_split(ppairs, test_size=200, random_state=1)
        self.ppairs_train = [tuple(ppair_train) for ppair_train in ppairs_train]
        self.ppairs_test = [tuple(ppair_test) for ppair_test in ppairs_test]


        # Generate Negative Training Correction Pairs
        incorrect = list(zip(*ppairs_train)[0])
        shuffle(incorrect)
        correct = list(zip(*ppairs_train)[1])
        npairs_train = zip(incorrect, correct)
        
        # Raw training set
        x_raw = ppairs_train + npairs_train
        # Label of the training set
        self.y_train = [0] * len(ppairs_train) + [1] * len(npairs_train)

        # Extract Features from the raw training set
        self.fe = StringPairFeatureExtractor(match=True, numeric=True, transition=True)
        self.x_train = x_orig = self.fe.fit_transform(x_raw)
        #x_train, x_test, y_train, y_test = train_test_split(x_orig, y_orig, test_size=0.2, random_state=42)
        self.train()
        
    def train(self):
        # Training
        self.m = Hacrf(l2_regularization=10.0, optimizer=fmin_l_bfgs_b, optimizer_kwargs={'maxfun': 45}, state_machine=None)
        self.m.fit(self.x_train, self.y_train, verbosity=20)
    
    def test(self):
        count = 0
        for incorrect, correct in self.ppairs_test:
            # Get the top 100 candidats with smallest levenshtein distance
            test_pairs = [(incorrect, candidate) for candidate in 
                          heapq.nsmallest(100, self.dictionary, key=lambda x: levenshtein.levenshtein(incorrect, x))]
            gx_test = self.fe.transform(test_pairs)
            # Pr is a list of probability, corresponding to each correction pair in test_pairs 
            pr = self.m.predict_proba(gx_test)
            cr = zip(pr, test_pairs)
            # We use the one with largest probability as the correction of the incorrect word
            cr = max(cr, key=lambda x: x[0][0])
            if cr[1][1] == correct:
                count += 1
            else:
                print (incorrect, correct),
                print cr[1][1]
            print
        print count/float(len(self.ppairs_test))
        
    def correct(self, incorrect):
        test_pairs = [(incorrect, candidate) for candidate in 
                      heapq.nsmallest(100, self.dictionary, key=lambda x: levenshtein.levenshtein(incorrect, x))]
        gx_test = self.fe.transform(test_pairs)
        # Pr is a list of probability, corresponding to each correction pair in test_pairs 
        pr = self.m.predict_proba(gx_test)
        cr = zip(pr, test_pairs)
        # We use the one with largest probability as the correction of the incorrect word
        cr = max(cr, key=lambda x: x[0][0])
        return cr[1][1]
        
if __name__ == '__main__':
    correcter = MisspellingCorrection('string_pairs_correction_Twitter.txt')
    print correcter.correct('hapy')
