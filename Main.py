
# from numpy import *
# from PyRTF import *
# from os import *
# from pandoc import *
# import re
# from array import *
from sklearn.feature_extraction.text import TfidfVectorizer
import string
import nltk
import sklearn
import os
from LegalDoc import LegalDoc
from Judge import Judge


class Main:

    # ----Constant Static fields----
    # Settings
    UNFORMATTED_PATH = "Resources/Input/txt/"
    FORMATTED_PATH = "Resources/Output/Formatted/"
    LOAD_FORMATTED = False          # Load formatted files (Fast!)
    LOAD_UNFORMATTED = True         # Load unformatted files (Slow!)
    SAVE_FORMATTED = True           # Save LegalDoc instances as .TXT files after formatting
    PRINT_JUDGE_DATA = True         # Print the list of judges and their associated cases
    PRINT_EXCEPTION_DATA = True     # Print exception data
    RUN_TEST_CODE = True            # Runs the test method

    # ----Class Methods----
    @classmethod
    def test(cls):
        print("Hello World")

    # Load all formatted files in the specified directory
    @classmethod
    def load_formatted_files(cls):
        for filename in os.listdir(cls.FORMATTED_PATH):
            l_legal_doc = LegalDoc()

            # If LegalDoc instance throws one or more errors whilst initialising
            if not l_legal_doc.initialise(cls.FORMATTED_PATH + filename, True):
                del l_legal_doc
                continue

    # Load all unformatted files in the specified directory
    @classmethod
    def load_unformatted_files(cls):

        for filename in os.listdir(cls.UNFORMATTED_PATH):
            l_legal_doc = LegalDoc()

            # If LegalDoc instance throws one or more errors whilst initialising
            if not l_legal_doc.initialise(cls.UNFORMATTED_PATH + filename, False):
                del l_legal_doc
                continue

            else:
                # Write LegalDoc to .txt
                if cls.SAVE_FORMATTED:
                    l_legal_doc.write()


# ----Main method----
def main():
    # Print versions
    print('The nltk version is {}.'.format(nltk.__version__))
    print('The scikit-learn version is {}.'.format(sklearn.__version__))

    # Functionality based on settings in Main class
    if Main.RUN_TEST_CODE:
        Main.test()

    if Main.LOAD_FORMATTED:
        Main.load_formatted_files()

    elif Main.LOAD_UNFORMATTED:
        Main.load_unformatted_files()

    if Main.PRINT_EXCEPTION_DATA:
        LegalDoc.print_exception_data()

    if Main.PRINT_JUDGE_DATA:
        Judge.print_all()

    print("Done!")


# Define main method
if __name__ == '__main__':
    main()
