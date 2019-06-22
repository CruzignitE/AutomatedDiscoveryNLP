
from nltk.corpus import movie_reviews
from collections import defaultdict
import string
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import itertools
import nltk
from nltk.classify import NaiveBayesClassifier as nbc



import random

class ClassifierTest2:

    @staticmethod
    def document_features(document, word_features):
        document_words = set(document)

        features = {}
        for word in word_features:
            features['contains(%s)' % word] = (word in document_words)
        return features


    @classmethod
    def test(cls):
        documents = [(list(movie_reviews.words(fileid)), category)
            for category in movie_reviews.categories()
            for fileid in movie_reviews.fileids(category)]
        random.shuffle(documents)

        all_words = nltk.FreqDist(w.lower() for w in movie_reviews.words())
        word_features = list(all_words.keys())[:2000]

        print(cls.document_features(movie_reviews.words('pos/cv957_8737.txt'), word_features))

        featuresets = [(cls.document_features(d, word_features), c) for (d, c) in documents]
        train_set, test_set = featuresets[100:], featuresets[:100]

        classifier = nltk.NaiveBayesClassifier.train(train_set)
        print(nltk.classify.accuracy(classifier, test_set))
        classifier.show_most_informative_features(5)

        '''
        Not applicable in this case
        
        classifier = nltk.DecisionTreeClassifier.train(train_set)
        print(nltk.classify.accuracy(classifier, test_set))
        print(classifier.pseudocode(depth=4))
        classifier.show_most_informative_features(5)
        '''


# ----Main method----
def main():
    ClassifierTest2.test()
    print("Done!")

# Define main method
if __name__ == '__main__':
    main()