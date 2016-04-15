from Preprocessor import Preprocessor
from FeatureExtractor import FeatureExtractor
import csv

def get_category(attribute):
    if attribute == "Positive":
        return ["1", "0", "0"]
    elif attribute == "Negative":
        return ["0", "1", "0"]
    elif attribute == "Neutral":
        return ["0", "0", "1"]
    else:
        # raise ValueError('Attribute is wrong')
        print attribute
        raise ValueError('Attribute is wrong')

fpr = open('Sentiment.csv', 'rb')
reader = csv.reader(fpr)
next(reader, None)

tweets = []
labels = []
for row in reader:
    tweet = row[15]
    tweets.append(tweet)
    label = get_category(row[5])
    labels.append(label)
fpr.close()

preprocessor = Preprocessor('stopWords.txt')
feature_extractor = FeatureExtractor(usingCorrection = False, usingNegation = False)

training_x = []
training_y = []

for tweet in tweets:
    processed_tweet = preprocessor.preprocess(tweet)
    features = feature_extractor.extract_features(processed_tweet)
    feature_vector = feature_extractor.build_feature_vector(features)
    training_x.append(feature_vector)
    
training_y = labels

training_M = []
for i in range(len(training_x)):
    training_M.append(training_x[i] + training_y[i])

print len(training_M)
print len(training_x)
print len(training_y)



'''
fpw = open('featureMatrix.csv', 'wb')
writer = csv.writer(fpw)
for ele in training_M:
    writer.writerow(ele)
fpw.close()
'''