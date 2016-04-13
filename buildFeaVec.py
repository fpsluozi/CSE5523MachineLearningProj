
import re
import csv

from preprocess import Preprocess 

class BuildFeaVec(object):
    """docstring for BuildFeaVec"""
    def __init__(self):
        pass


    def get_category(self, attribute):
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


    def data_matrix(self, tweet, word_list):
        data = [0 for i in range(len(word_list))]

        # calculate how many times a word repeats
        for w in tweet:
            data[word_list.index(w)] += 1

        return data


    def build_feature_matrix(self, file_name):
        # with open('dataset/test.csv', 'rb') as f:
        with open(file_name, 'rb') as f:
            p = Preprocess()

            # "results" contains preprocessed tweet
            # word list contains all distinct words in training data
            results = []; word_list = []

            # dataM contains every tweet's feature vector
            # cataM contains every tweet's catagory vector
            dataM = []; cataM = []

            # read training data
            reader = csv.reader(f)
            first = True
            
            # read stop words from file
            stop_words = p.get_stop_word_list('stopWords.txt')

            for row in reader:
                if first:
                    first = False
                    continue

                # the 16th column is about tweet
                processed_tweet = p.basic_process(row[15])

                # feature_vector = getFeatureVector(processed_tweet)
                feature_vector, word_list = p.get_fea_vector_and_wordlist(processed_tweet, word_list, stop_words)

                # record feature vector for each tweet
                results.append(feature_vector)

                # record category for each vector
                cataM.append(self.get_category(row[5]))

            word_list = sorted(word_list)

            for i in range(len(results)):
                # combine feature vector and category together
                dataM.append(self.data_matrix(results[i], word_list) + cataM[i])

        f.close()

        # write feature matrix to the file
        with open('featureMatrix.csv', 'wb') as fp:
            writer = csv.writer(fp)
            # write world list into '.csv' file
            writer.writerow(word_list)

            # write feature number matrix into '.csv' file
            for row in dataM:
                writer.writerow(row)

        fp.close()
