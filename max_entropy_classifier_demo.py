
import classifier_helper
from classifier_helper import *

pos_tweets = [('I love this car', 'positive'),
              ('This view is amazing', 'positive'),
              ('I feel great this morning', 'positive'),
              ('I am so excited about the concert', 'positive'),
              ('He is my best friend', 'positive')]

neg_tweets = [('I do not like this car', 'negative'),
              ('This view is horrible', 'negative'),
              ('I feel tired this morning', 'negative'),
              ('I am not looking forward to the concert', 'negative'),
              ('He is my enemy', 'negative')]

helper = ClassifierHelper('data/feature_list/feature_list.txt')
tweets = []
for (words, sentiment) in pos_tweets + neg_tweets:
    words_filtered = [e.lower() for e in words.split() if len(e) >= 3]
    tweets.append((words_filtered, sentiment))

#word_features = get_word_features(get_words_in_tweets(tweets))
#set_word_features(word_features)
training_set = nltk.classify.apply_features(helper.extract_features, tweets)
print type(training_set)

classifier = nltk.classify.maxent.MaxentClassifier.train(training_set,'GIS',trace=3,encoding=None,labels=None,gaussian_prior_sigma=0, max_iter = 5) 
print 'Finish Training'
tweet = 'Im tired and enemy'
print classifier.classify(helper.extract_features(tweet.split()))
print nltk.classify.accuracy(classifier, training_set)
classifier.show_most_informative_features(10)