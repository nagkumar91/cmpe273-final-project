import os
import sys
import nltk
import csv
import re
from nltk.corpus import movie_reviews as mr
from textblob.tokenizers import word_tokenize
from django.conf import settings
from nltk.corpus import stopwords

# Some utility functions:
"""
sample input: [ 'what', 'a', 'waste', 'of', 'resources']
output: { 'what':True, 'waste':True, 'resources':True }
"""
def feature_extractor(words):
    sw = stopwords.words('english')
    return dict(((word.lower(), True) for word in words if word.lower() not in sw))

"""
sample input: 'Hey @stonyface, check out http://videogags.org. Might make you *really* laugh'
output: 'Hey AT_USER, check out URL. Might make you really laugh'
"""
def preprocess_tweet(tweet):
    tweet = re.sub('@[^\s]+', 'AT_USER', tweet)
    tweet = re.sub('\*','', tweet)
    tweet = re.sub('\!','', tweet)
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',tweet)
    tweet = tweet.strip('\'"')
    return tweet

"""
process tweets classified into 'pos' or 'neg' by the Stanford guys. The data was obtained from:
    http://help.sentiment140.com/home
"""
def create_training_features_from_stanford_data(nltkdir):
    with open(nltkdir + '/corpora/trainingandtestdata/training.neg_4.csv') as csvfile:
        rdr = csv.reader(csvfile, delimiter=',', quotechar='"')
        my_neg_feats_4 = [(feature_extractor(preprocess_tweet(row[5]).split(" ")), 'neg') for row in rdr]
    with open(nltkdir + '/corpora/trainingandtestdata/training.neg_3.csv') as csvfile:
        rdr = csv.reader(csvfile, delimiter=',', quotechar='"')
        my_neg_feats_3 = [(feature_extractor(preprocess_tweet(row[5]).split(" ")), 'neg') for row in rdr]
    with open(nltkdir + '/corpora/trainingandtestdata/training.neg_2.csv') as csvfile:
        rdr = csv.reader(csvfile, delimiter=',', quotechar='"')
        my_neg_feats_2 = [(feature_extractor(preprocess_tweet(row[5]).split(" ")), 'neg') for row in rdr]
    with open(nltkdir + '/corpora/trainingandtestdata/training.neg_1.csv') as csvfile:
        rdr = csv.reader(csvfile, delimiter=',', quotechar='"')
        my_neg_feats_1 = [(feature_extractor(preprocess_tweet(row[5]).split(" ")), 'neg') for row in rdr]
        my_neg_feats = my_neg_feats_1 + my_neg_feats_2 + my_neg_feats_3 + my_neg_feats_4

    with open(nltkdir + '/corpora/trainingandtestdata/training.pos_4.csv') as csvfile:
        rdr = csv.reader(csvfile, delimiter=',', quotechar='"')
        my_pos_feats_4 = [(feature_extractor(preprocess_tweet(row[5]).split(" ")), 'pos') for row in rdr]
    with open(nltkdir + '/corpora/trainingandtestdata/training.pos_3.csv') as csvfile:
        rdr = csv.reader(csvfile, delimiter=',', quotechar='"')
        my_pos_feats_3 = [(feature_extractor(preprocess_tweet(row[5]).split(" ")), 'pos') for row in rdr]
    with open(nltkdir + '/corpora/trainingandtestdata/training.pos_2.csv') as csvfile:
        rdr = csv.reader(csvfile, delimiter=',', quotechar='"')
        my_pos_feats_2 = [(feature_extractor(preprocess_tweet(row[5]).split(" ")), 'pos') for row in rdr]
    with open(nltkdir + '/corpora/trainingandtestdata/training.pos_1.csv') as csvfile:
        rdr = csv.reader(csvfile, delimiter=',', quotechar='"')
        my_pos_feats_1 = [(feature_extractor(preprocess_tweet(row[5]).split(" ")), 'pos') for row in rdr]
        my_pos_feats = my_pos_feats_1 + my_pos_feats_2 + my_pos_feats_3 + my_pos_feats_4

        my_feats = my_neg_feats + my_pos_feats
        return my_feats


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
        movie_review_feats = neg_feats + pos_feats

        # stanford tweet processing can slow things down to a crawl. Enable it only in production
        if settings.DEBUG == False:
            stanford_feats = create_training_features_from_stanford_data(nltk_data_dir)
            train_feats = movie_review_feats + stanford_feats
        else:
            train_feats = movie_review_feats

        self.classifier = nltk.NaiveBayesClassifier.train(train_feats)
        self.classifier.show_most_informative_features(10)

    def classify(self, intweet):
        """ 
        tweet : The content of the tweet in string format 
        returns : Either "pos" or "neg"
        """
        tweet = preprocess_tweet(intweet)
        tokens = word_tokenize(tweet, include_punc=False)
        filtered = (t.lower() for t in tokens if len(t) >= 3)
        feats = feature_extractor(filtered)
        prob_dist = self.classifier.prob_classify(feats)
        print "For text: %s" % tweet
        print(prob_dist.prob('pos')),
        print(prob_dist.prob("neg")),
        print prob_dist.max()
        print ""
        return (prob_dist.max())


    def print_useful_features(self, count):
        self.classifier.show_most_informative_features(count)


'''
################## UNIT TEST ##################

tw = TweetsClassifier("../nltk_data")
print tw.print_useful_features(10)
tweet = raw_input('Enter your tweet to classify (Type \"exit\" to quit) : ')
while tweet != "exit":
    print tw.classify(tweet)
    tweet = raw_input('Enter your tweet to classify (Type \"exit\" to quit) : ')

###############################################

nltk.data.path.append("../nltk_data")
nltkdir = os.environ.get('NLTK_DATA_DIR')
def create_training_data():
    with open(nltkdir + '/corpora/trainingandtestdata/training.neg_4.csv') as csvfile:
        rdr = csv.reader(csvfile, delimiter=',', quotechar='"')
        my_neg_feats_4 = [(feature_extractor(row[5].split(" ")), 'neg') for row in rdr]
    with open(nltkdir + '/corpora/trainingandtestdata/training.neg_3.csv') as csvfile:
        rdr = csv.reader(csvfile, delimiter=',', quotechar='"')
        my_neg_feats_3 = [(feature_extractor(row[5].split(" ")), 'neg') for row in rdr]
    with open(nltkdir + '/corpora/trainingandtestdata/training.neg_2.csv') as csvfile:
        rdr = csv.reader(csvfile, delimiter=',', quotechar='"')
        my_neg_feats_2 = [(feature_extractor(row[5].split(" ")), 'neg') for row in rdr]
    with open(nltkdir + '/corpora/trainingandtestdata/training.neg_1.csv') as csvfile:
        rdr = csv.reader(csvfile, delimiter=',', quotechar='"')
        my_neg_feats_1 = [(feature_extractor(row[5].split(" ")), 'neg') for row in rdr]
        my_neg_feats = my_neg_feats_1 + my_neg_feats_2 + my_neg_feats_3 + my_neg_feats_4

    with open(nltkdir + '/corpora/trainingandtestdata/training.pos_4.csv') as csvfile:
        rdr = csv.reader(csvfile, delimiter=',', quotechar='"')
        my_pos_feats_4 = [(feature_extractor(row[5].split(" ")), 'pos') for row in rdr]
    with open(nltkdir + '/corpora/trainingandtestdata/training.pos_3.csv') as csvfile:
        rdr = csv.reader(csvfile, delimiter=',', quotechar='"')
        my_pos_feats_3 = [(feature_extractor(row[5].split(" ")), 'pos') for row in rdr]
    with open(nltkdir + '/corpora/trainingandtestdata/training.pos_2.csv') as csvfile:
        rdr = csv.reader(csvfile, delimiter=',', quotechar='"')
        my_pos_feats_2 = [(feature_extractor(row[5].split(" ")), 'pos') for row in rdr]
    with open(nltkdir + '/corpora/trainingandtestdata/training.pos_1.csv') as csvfile:
        rdr = csv.reader(csvfile, delimiter=',', quotechar='"')
        my_pos_feats_1 = [(feature_extractor(row[5].split(" ")), 'pos') for row in rdr]
        my_pos_feats = my_pos_feats_1 + my_pos_feats_2 + my_pos_feats_3 + my_pos_feats_4

        my_feats = my_neg_feats + my_pos_feats
        return my_feats

def my_classify(tweet):
   tokens = word_tokenize(tweet, include_punc=False)
   filtered = (t.lower() for t in tokens if len(t) >= 3)
   feats = feature_extractor(filtered)
   prob_dist = my_classifier.prob_classify(feats)
   print(prob_dist.prob('pos')),
   print(prob_dist.prob('neg')),
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
