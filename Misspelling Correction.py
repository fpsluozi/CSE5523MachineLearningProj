
# coding: utf-8

# In[65]:

import numpy as np
lines = open('string_pairs_correction_Twitter.txt', 'r').readlines()

# Generate Positive Correction Pair
ppairs = []
ppairs = [line.split('\t')[1].strip().split(' | ') for line in lines]
ppairs = [(pair[0], pair[i]) for pair in ppairs for i in xrange(1, len(pair))]
dictionary = [pair[i] for pair in ppairs for i in xrange(1, len(pair))]


# Generate Positive Training Correction Pairs and Testing Correction Pairs
from sklearn.cross_validation import train_test_split
ppairs_train, ppairs_test = train_test_split(ppairs, test_size=100, random_state=1)
ppairs_train = [tuple(ppair_train) for ppair_train in ppairs_train]
ppairs_test = [tuple(ppair_test) for ppair_test in ppairs_test]


# Generate Negative Training Correction Pairs
from numpy.random import shuffle 
incorrect = list(zip(*ppairs_train)[0])
shuffle(incorrect)
correct = list(zip(*ppairs_train)[1])
npairs_train = zip(incorrect, correct)


# Raw training set
x_raw = ppairs_train + npairs_train
# Label of the training set
y_orig = [0] * len(ppairs_train) + [1] * len(npairs_train)

# Extract Features from the raw training set
from pyhacrf import StringPairFeatureExtractor
fe = StringPairFeatureExtractor(match=True, numeric=True, transition=True)
x_orig = fe.fit_transform(x_raw)


from sklearn.cross_validation import train_test_split
from sklearn.metrics import accuracy_score
#x_train, x_test, y_train, y_test = train_test_split(x_orig, y_orig, test_size=0.2, random_state=42)
x_train = x_orig
y_train = y_orig

# Training
from pyhacrf import Hacrf
from scipy.optimize import fmin_l_bfgs_b
m = Hacrf(l2_regularization=10.0, optimizer=fmin_l_bfgs_b, optimizer_kwargs={'maxfun': 45}, state_machine=None)
m.fit(x_train, y_train, verbosity=20)


# Testing on the testing data set
import random
import levenshtein
import heapq

count = 0
for incorrect, correct in ppairs_test:
    # Get the top 100 candidats with smallest levenshtein distance
    test_pairs = [(incorrect, candidate) for candidate in 
                  heapq.nsmallest(100, dictionary, key=lambda x: levenshtein.levenshtein(incorrect, x))]
    gx_test = fe.transform(test_pairs)
    # Pr is a list of probability, corresponding to each correction pair in test_pairs 
    pr = m.predict_proba(gx_test)
    cr = zip(pr, test_pairs)
    # We use the one with largest probability as the correction of the incorrect word
    cr = max(cr, key=lambda x: x[0][0])
    if cr[1][1] == correct:
        count += 1
    else:
        print (incorrect, correct),
        print cr[1][1]
    print
print count/float(len(ppairs_test))



