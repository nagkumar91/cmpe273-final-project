import os
import sys
import nltk
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


# ################# UNIT TEST ##################

tw = TweetsClassifier("../nltk_data")
print tw.print_useful_features(10)
tweet = raw_input('Enter your tweet to classify (Type \"exit\" to quit) : ')
while tweet != "exit":
    print tw.classify(tweet)
    tweet = raw_input('Enter your tweet to classify (Type \"exit\" to quit) : ')

