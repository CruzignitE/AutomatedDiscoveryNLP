
from nltk.corpus import movie_reviews as mr
from collections import defaultdict
import string
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import itertools
import nltk
from nltk.classify import NaiveBayesClassifier as nbc



import random

class ClassifierTest:




    @classmethod
    def test(cls):

        stop = stopwords.words('english')
        documents = defaultdict(list)

        for i in mr.fileids():
            documents[i.split('/')[0]].append(i)

        print(documents['pos'][:10])  # first ten pos reviews.
        print(documents['neg'][:10])  # first ten neg reviews.

        documents = [
            ([w for w in mr.words(i) if w.lower() not in stop and w.lower() not in string.punctuation], i.split('/')[0])
            for i in mr.fileids()]

        all_words = FreqDist(
            w.lower() for w in mr.words() if w.lower() not in stop and w.lower() not in string.punctuation)

        print(all_words)

        word_features = FreqDist(itertools.chain(*[i for i, j in documents]))
        word_features = list(word_features.keys())[:100]

        numtrain = int(len(documents) * 90 / 100)

        train_set = [({i: (i in tokens) for i in word_features}, tag) for tokens, tag in documents[:numtrain]]
        print(train_set)
        print(type(train_set))

        test_set = [({i: (i in tokens) for i in word_features}, tag) for tokens, tag in documents[numtrain:]]
        print(test_set)
        print(type(test_set))

        classifier = nbc.train(train_set)
        print(nltk.classify.accuracy(classifier, test_set))
        classifier.show_most_informative_features(5)

# ----Main method----
def main():
    ClassifierTest.test()
    print("Done!")

# Define main method
if __name__ == '__main__':
    main()