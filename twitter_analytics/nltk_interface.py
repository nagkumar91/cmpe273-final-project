import os
import sys
import nltk
import csv
from nltk.corpus import movie_reviews as mr
from textblob.tokenizers import word_tokenize
from django.conf import settings


def feature_extractor(words):
    return dict(((word, True) for word in words))


class TweetsClassifier(object):
    def __init__(self, nltk_data_dir=None):
        """
        nltk_data_dir points to the directory that contains the 
        copora/movie_reviews corpus data.
        """

        # TODO: Using NLTK_DATA_DIR for the moment. Need to come up with a better
        # scheme to point the nltk_data directory to the nltk library
        if nltk_data_dir is None:
            nltk_data_dir = os.environ.get('NLTK_DATA_DIR')

        if nltk_data_dir is None:
            nltk_data_dir = settings.NLTK_DATA_DIR

        if nltk_data_dir is None:
            print "This feature needs nltk_data. Either download the corpora "
            print "to default location or point environment variable "
            print "NLTK_DATA_DIR to the appropriate directory where you have "
            print "the data downloaded"
            sys.exit(0)

        nltk.data.path.append(nltk_data_dir)
        neg_fds = mr.fileids('neg')
        pos_fds = mr.fileids('pos')
        neg_feats = [(feature_extractor(mr.words(fileids=[f])), 'neg') for f in neg_fds]
        pos_feats = [(feature_extractor(mr.words(fileids=[f])), 'pos') for f in pos_fds]
        train_feats = neg_feats + pos_feats
        self.classifier = nltk.NaiveBayesClassifier.train(train_feats)


    def classify(self, tweet):
        """ 
        tweet : The content of the tweet in string format 
        returns : Either "pos" or "neg"
        """
        tokens = word_tokenize(tweet, include_punc=False)
        filtered = (t.lower() for t in tokens if len(t) >= 3)
        feats = feature_extractor(filtered)
        prob_dist = self.classifier.prob_classify(feats)
        # print "For text: %s" % tweet
        # print ""
        #print prob_dist.max()
        #print prob_dist.prob('pos')
        #print prob_dist.prob("neg")
        return (prob_dist.max())


    def print_useful_features(self, count):
        self.classifier.show_most_informative_features(count)


################## UNIT TEST ##################

'''
tw = TweetsClassifier("../nltk_data")
print tw.print_useful_features(10)
tweet = raw_input('Enter your tweet to classify (Type \"exit\" to quit) : ')
while tweet != "exit":
    print tw.classify(tweet)
    tweet = raw_input('Enter your tweet to classify (Type \"exit\" to quit) : ')


###############################################

nltk.data.path.append("../nltk_data")
def create_training_data():
    with open('/Users/rprakash/cmpe273-final-project/nltk_data/corpora/trainingandtestdata/training.neg_4.csv') as csvfile:
        rdr = csv.reader(csvfile, delimiter=',', quotechar='"')
        my_neg_feats_4 = [(feature_extractor(row[5].split(" ")), 'neg') for row in rdr]
    with open('/Users/rprakash/cmpe273-final-project/nltk_data/corpora/trainingandtestdata/training.neg_3.csv') as csvfile:
        rdr = csv.reader(csvfile, delimiter=',', quotechar='"')
        my_neg_feats_3 = [(feature_extractor(row[5].split(" ")), 'neg') for row in rdr]
    with open('/Users/rprakash/cmpe273-final-project/nltk_data/corpora/trainingandtestdata/training.neg_2.csv') as csvfile:
        rdr = csv.reader(csvfile, delimiter=',', quotechar='"')
        my_neg_feats_2 = [(feature_extractor(row[5].split(" ")), 'neg') for row in rdr]
    with open('/Users/rprakash/cmpe273-final-project/nltk_data/corpora/trainingandtestdata/training.neg_1.csv') as csvfile:
        rdr = csv.reader(csvfile, delimiter=',', quotechar='"')
        my_neg_feats_1 = [(feature_extractor(row[5].split(" ")), 'neg') for row in rdr]
        my_neg_feats = my_neg_feats_1 + my_neg_feats_2 + my_neg_feats_3 + my_neg_feats_4

    with open('/Users/rprakash/cmpe273-final-project/nltk_data/corpora/trainingandtestdata/training.pos_4.csv') as csvfile:
        rdr = csv.reader(csvfile, delimiter=',', quotechar='"')
        my_pos_feats_4 = [(feature_extractor(row[5].split(" ")), 'pos') for row in rdr]
    with open('/Users/rprakash/cmpe273-final-project/nltk_data/corpora/trainingandtestdata/training.pos_3.csv') as csvfile:
        rdr = csv.reader(csvfile, delimiter=',', quotechar='"')
        my_pos_feats_3 = [(feature_extractor(row[5].split(" ")), 'pos') for row in rdr]
    with open('/Users/rprakash/cmpe273-final-project/nltk_data/corpora/trainingandtestdata/training.pos_2.csv') as csvfile:
        rdr = csv.reader(csvfile, delimiter=',', quotechar='"')
        my_pos_feats_2 = [(feature_extractor(row[5].split(" ")), 'pos') for row in rdr]
    with open('/Users/rprakash/cmpe273-final-project/nltk_data/corpora/trainingandtestdata/training.pos_1.csv') as csvfile:
        rdr = csv.reader(csvfile, delimiter=',', quotechar='"')
        my_pos_feats_1 = [(feature_extractor(row[5].split(" ")), 'pos') for row in rdr]
        my_pos_feats = my_pos_feats_1 + my_pos_feats_2 + my_pos_feats_3 + my_pos_feats_4

        my_feats = my_neg_feats + my_pos_feats
        return my_feats

"""
    with open('/Users/rprakash/cmpe273-final-project/nltk_data/corpora/trainingandtestdata/training.neg_2.test.csv') as csvfile:
        rdr = csv.reader(csvfile, delimiter=',', quotechar='"')
        count = 0
        for row in rdr:
            count = count + 1
            if (count % 1000 == 0):
                print ""
                print "Processed %s tweets for training. %s more to go" % (count, 1600000 - count)
            if row[0] == "0":
                print("-"),
                my_neg_feats = my_neg_feats + [(feature_extractor(row[5].split(" ")), 'neg')]


    with open('/Users/rprakash/cmpe273-final-project/nltk_data/corpora/trainingandtestdata/training.neg_3.test.csv') as csvfile:
        rdr = csv.reader(csvfile, delimiter=',', quotechar='"')
        count = 0
        for row in rdr:
            count = count + 1
            if (count % 1000 == 0):
                print ""
                print "Processed %s tweets for training. %s more to go" % (count, 1600000 - count)
            if row[0] == "0":
                print("-"),
                my_neg_feats = my_neg_feats + [(feature_extractor(row[5].split(" ")), 'neg')]

    with open('/Users/rprakash/cmpe273-final-project/nltk_data/corpora/trainingandtestdata/training.neg_4.test.csv') as csvfile:
        rdr = csv.reader(csvfile, delimiter=',', quotechar='"')
        count = 0
        for row in rdr:
            count = count + 1
            if (count % 1000 == 0):
                print ""
                print "Processed %s tweets for training. %s more to go" % (count, 1600000 - count)
            if row[0] == "0":
                print("-"),
                my_neg_feats = my_neg_feats + [(feature_extractor(row[5].split(" ")), 'neg')]

    my_pos_feats = []
    with open('/Users/rprakash/cmpe273-final-project/nltk_data/corpora/trainingandtestdata/training.pos_1.test.csv') as csvfile:
        rdr = csv.reader(csvfile, delimiter=',', quotechar='"')
        count = 0
        for row in rdr:
            count = count + 1
            if (count % 1000 == 0):
                print ""
                print "Processed %s tweets for training. %s more to go" % (count, 1600000 - count)
            if row[0] == "4":
                print("+"),
                my_pos_feats = my_pos_feats + [(feature_extractor(row[5].split(" ")), 'pos')]

    with open('/Users/rprakash/cmpe273-final-project/nltk_data/corpora/trainingandtestdata/training.pos_2.test.csv') as csvfile:
        rdr = csv.reader(csvfile, delimiter=',', quotechar='"')
        count = 0
        for row in rdr:
            count = count + 1
            if (count % 1000 == 0):
                print ""
                print "Processed %s tweets for training. %s more to go" % (count, 1600000 - count)
            if row[0] == "4":
                print("+"),
                my_pos_feats = my_pos_feats + [(feature_extractor(row[5].split(" ")), 'pos')]

    with open('/Users/rprakash/cmpe273-final-project/nltk_data/corpora/trainingandtestdata/training.pos_3.test.csv') as csvfile:
        rdr = csv.reader(csvfile, delimiter=',', quotechar='"')
        count = 0
        for row in rdr:
            count = count + 1
            if (count % 1000 == 0):
                print ""
                print "Processed %s tweets for training. %s more to go" % (count, 1600000 - count)
            if row[0] == "4":
                print("+"),
                my_pos_feats = my_pos_feats + [(feature_extractor(row[5].split(" ")), 'pos')]

    with open('/Users/rprakash/cmpe273-final-project/nltk_data/corpora/trainingandtestdata/training.pos_4.test.csv') as csvfile:
        rdr = csv.reader(csvfile, delimiter=',', quotechar='"')
        count = 0
        for row in rdr:
            count = count + 1
            if (count % 1000 == 0):
                print ""
                print "Processed %s tweets for training. %s more to go" % (count, 1600000 - count)
            if row[0] == "4":
                print("+"),
                my_pos_feats = my_pos_feats + [(feature_extractor(row[5].split(" ")), 'pos')]

        #my_neg_feats = [(feature_extractor(row[5].split(" ")), 'neg') for row in rdr if row[0] == "0"]
        #my_pos_feats = [(feature_extractor(row[5].split(" ")), 'pos') for row in rdr if row[0] == "4"]

    return (my_neg_feats + my_pos_feats)
"""

def my_classify(tweet):
   tokens = word_tokenize(tweet, include_punc=False)
   filtered = (t.lower() for t in tokens if len(t) >= 3)
   feats = feature_extractor(filtered)
   prob_dist = my_classifier.prob_classify(feats)
   return(prob_dist.max())

my_train_feats = create_training_data()
my_classifier = nltk.NaiveBayesClassifier.train(my_train_feats)
print "New Classifier:"
my_classifier.show_most_informative_features(10)
print "Old Classifier:"
tw = TweetsClassifier("../nltk_data")
print tw.print_useful_features(10)
mytweet = raw_input('Enter your tweet to classify (Type \"exit\" to quit) : ')
while mytweet != "exit":
    print("New Classifier says :"),
    print my_classify(mytweet)
    print("Old Classifier says :"),
    print tw.classify(mytweet)
    mytweet = raw_input('Enter your tweet to classify (Type \"exit\" to quit) : ')

'''