import nltk
import os, os.path
import sys
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews

# README.1st:
# Needs the NLTK_DATA env variable to point to ../nltk_data
class Splitter(object):
    def __init__(self):
        nltk.data.path.append("../nltk_data")
        print nltk.data.path
        self.nltk_splitter = nltk.data.load('tokenizers/punkt/english.pickle')
        self.nltk_tokenizer = nltk.tokenize.TreebankWordTokenizer()

    def split(self, text):
        """
        input format: a paragraph of text
        output format: a list of lists of words.
            e.g.: [['this', 'is', 'a', 'sentence'], ['this', 'is', 'another', 'one']]
        """
        sentences = self.nltk_splitter.tokenize(text)
        tokenized_sentences = [self.nltk_tokenizer.tokenize(sent) for sent in sentences]
        return tokenized_sentences


class POSTagger(object):
    def __init__(self):
        pass

    def pos_tag(self, sentences):
        """
        input format: list of lists of words
            e.g.: [['this', 'is', 'a', 'sentence'], ['this', 'is', 'another', 'one']]
        output format: list of lists of tagged tokens. Each tagged tokens has a
        form, a lemma, and a list of tags
            e.g: [[('this', 'this', ['DT']), ('is', 'be', ['VB']), ('a', 'a', ['DT']), ('sentence', 'sentence', ['NN'])],
                    [('this', 'this', ['DT']), ('is', 'be', ['VB']), ('another', 'another', ['DT']), ('one', 'one', ['CARD'])]]
        """

        pos = [nltk.pos_tag(sentence) for sentence in sentences]
        # adapt format
        pos = [[(word, word, [postag]) for (word, postag) in sentence] for sentence in pos]
        return pos

# class Splitter(object):
#    def __init__(self):
#        nltk.data.path.append("../nltk_data")
#        print nltk.data.path
#        self.nltk_splitter = nltk.data.load('tokenizers/punkt/english.pickle')
#        self.nltk_tokenizer = nltk.tokenize.TreebankWordTokenizer()
# 
#    def split(self, text):
#        """
#        input format: a paragraph of text
#        output format: a list of lists of words.
#            e.g.: [['this', 'is', 'a', 'sentence'], ['this', 'is', 'another', 'one']]
#        """
#        sentences = self.nltk_splitter.tokenize(text)
#        tokenized_sentences = [self.nltk_tokenizer.tokenize(sent) for sent in sentences]
#        return tokenized_sentences
# 
#class POSTagger(object):
#    def __init__(self):
#        pass
#        
#    def pos_tag(self, sentences):
#        """
#        input format: list of lists of words
#            e.g.: [['this', 'is', 'a', 'sentence'], ['this', 'is', 'another', 'one']]
#        output format: list of lists of tagged tokens. Each tagged tokens has a
#        form, a lemma, and a list of tags
#            e.g: [[('this', 'this', ['DT']), ('is', 'be', ['VB']), ('a', 'a', ['DT']), ('sentence', 'sentence', ['NN'])],
#                    [('this', 'this', ['DT']), ('is', 'be', ['VB']), ('another', 'another', ['DT']), ('one', 'one', ['CARD'])]]
#        """
# 
#        pos = [nltk.pos_tag(sentence) for sentence in sentences]
#        #adapt format
#        pos = [[(word, word, [postag]) for (word, postag) in sentence] for sentence in pos]
#        return pos
#
###############################################################################

text = """What can I say about this place. The staff of the restaurant is nice and the eggplant is not bad. Apart from that, very uninspired food, lack of atmosphere and too expensive. I am a staunch vegetarian and was sorely dissapointed with the veggie options on the menu. Will be the last time I visit, I recommend others to avoid."""

splitter = Splitter()
postagger = POSTagger()
splitted_sentences = splitter.split(text)
print splitted_sentences
pos_tagged_sentences = postagger.pos_tag(splitted_sentences)
print pos_tagged_sentences

#splitter = Splitter()
#postagger = POSTagger()
#splitted_sentences = splitter.split(text)
#print splitted_sentences
#pos_tagged_sentences = postagger.pos_tag(splitted_sentences)
#print pos_tagged_sentences

###############################################################################

def word_feats(words):
    return dict([(word, True) for word in words])


negids = movie_reviews.fileids('neg')
posids = movie_reviews.fileids('pos')

negfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in negids]
posfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'pos') for f in posids]

negcutoff = len(negfeats)
poscutoff = len(posfeats)

trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]

classifier = NaiveBayesClassifier.train(trainfeats)
feat = word_feats(['Your song is annoying'])
print classifier.classify(feat)

