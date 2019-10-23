import nltk
from nltk.corpus import names
from nltk.classify import apply_features
import random


class FeaturesTest:

    @staticmethod
    def gender_features(a_word):
        return {'last_letter': a_word[-1]}

    '''
    Example 6-1. A feature extractor that overfits gender features. The featuresets returned by this feature
    extractor contain a large number of specific features, leading to overfitting for the relatively small
    Names Corpus.
    '''

    @staticmethod
    def gender_features2(l_name):
        l_features = {}

        l_features["firstletter"] = l_name[0].lower()
        l_features["lastletter"] = l_name[-1].lower()
        for letter in 'abcdefghijklmnopqrstuvwxyz':
            l_features["count(%s)" % letter] = l_name.lower().count(letter)
        l_features["has(%s)" % letter] = (letter in l_name.lower())
        return l_features


    @classmethod
    def test(cls):
        l_names = ([(l_name, 'male') for l_name in nltk.corpus.names.words('male.txt')] +
                   [(l_name, 'female') for l_name in nltk.corpus.names.words('female.txt')])

        random.shuffle(l_names)


        '''
        Next, we use the feature extractor to process the names data, and divide the resulting
        list of feature sets into a training set and a test set. The training set is used to train a
        new “naive Bayes” classifier.
        '''

        print(cls.gender_features("John"))

        l_feature_sets = [(cls.gender_features(n), g) for (n, g) in l_names]
        l_train_set, l_test_set = l_feature_sets[500:], l_feature_sets[:500]
        l_classifier = nltk.NaiveBayesClassifier.train(l_train_set)

        print(l_classifier.classify(cls.gender_features('Neo')))
        print(nltk.classify.accuracy(l_classifier, l_test_set))

        '''
        This listing shows that the names in the training set that end in a are female 38 times
        more often than they are male, but names that end in k are male 31 times more often
        than they are female. These ratios are known as likelihood ratios, and can be useful
        for comparing different feature-outcome relationships.
        '''

        l_classifier.show_most_informative_features(5)

        '''
        When working with large corpora, constructing a single list that contains the features
        of every instance can use up a large amount of memory. In these cases, use the function
        nltk.classify.apply_features, which returns an object that acts like a list but does not
        store all the feature sets in memory:
        '''

        # train_set = apply_features(cls.gender_features, names[500:])
        # test_set = apply_features(cls.gender_features, names[:500])
        print("-----------------------------------------------------")
        print(cls.gender_features2("John"))

        l_feature_sets = [(cls.gender_features2(n), g) for (n, g) in l_names]
        l_train_set, l_test_set = l_feature_sets[500:], l_feature_sets[:500]
        l_classifier = nltk.NaiveBayesClassifier.train(l_train_set)

        print(l_classifier.classify(cls.gender_features('Neo')))
        print(nltk.classify.accuracy(l_classifier, l_test_set))
        l_classifier.show_most_informative_features(5)

        print("-----------------------------------------------------")
        '''
        Once an initial set of features has been chosen, a very productive method for refining
        the feature set is error analysis. First, we select a development set, containing the
        corpus data for creating the model. This development set is then subdivided into the
        training set and the dev-test set.
        '''
        l_train_names = l_names[1500:]
        l_dev_test_names = l_names[500:1500]
        l_test_names = l_names[:500]

        '''
        The training set is used to train the model, and the dev-test set is used to perform error
        analysis. The test set serves in our final evaluation of the system. For reasons discussed
        later, it is important that we employ a separate dev-test set for error analysis, rather
        than just using the test set.
        '''
        l_train_set = [(cls.gender_features2(n), g) for (n, g) in l_train_names]
        l_dev_test_set = [(cls.gender_features2(n), g) for (n, g) in l_dev_test_names]
        l_test_set = [(cls.gender_features2(n), g) for (n, g) in l_test_names]
        l_classifier = nltk.NaiveBayesClassifier.train(l_train_set)

        '''
        Using the dev-test set, we can generate a list of the errors that the classifier makes when
        predicting name genders:
        '''
        l_errors = []
        for (l_name, l_tag) in l_dev_test_names:
            l_guess = l_classifier.classify(cls.gender_features2(l_name))
            if l_guess != l_tag:
                l_errors.append((l_tag, l_guess, l_name))

        '''
        We can then examine individual error cases where the model predicted the wrong label,
        and try to determine what additional pieces of information would allow it to make the
        right decision (or which existing pieces of information are tricking it into making the
        wrong decision). The feature set can then be adjusted accordingly. The names classifier
        that we have built generates about 100 errors on the dev-test corpus:
        '''
        print("Error data")
        for (l_tag, l_guess, l_name) in sorted(l_errors):  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
            print('correct=%-8s guess=%-8s name=%-30s' % (l_tag, l_guess, l_name))


# ----Main method----
def main():
    FeaturesTest.test()
    print("Done!")


# Define main method
if __name__ == '__main__':
    main()
