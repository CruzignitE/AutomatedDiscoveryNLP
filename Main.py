
# from numpy import *
# from PyRTF import *
# from os import *
# from pandoc import *
# import re
# from array import *

from treelib import Node, Tree

from sklearn.feature_extraction.text import TfidfVectorizer
import string
import nltk
import sklearn
import os
from LegalDoc import LegalDoc
from Judge import Judge
from Timer import Timer, Timers


class Main:

    # ----Constant Static fields----
    # Settings
    UNFORMATTED_PATH = "Resources/Input/txt all/"
    FORMATTED_PATH = "Resources/Output/Formatted/"
    LOAD_FORMATTED = False           # Load formatted files (Fast!) (~16 seconds)
    LOAD_UNFORMATTED = True        # Load unformatted files (Slow!) (~150 seconds)
    SAVE_FORMATTED = True           # Save LegalDoc instances as .TXT files after formatting
    PRINT_JUDGE_DATA = True         # Print the list of judges and their associated cases
    PRINT_EXCEPTION_DATA = True     # Print exception data
    RUN_TEST_CODE = True            # Runs the test method
    RUN_LEGAL_DOC_TEST_CODE = True  # Runs the test method
    ENABLE_TIMERS = True




    @classmethod
    def test(cls):
        tree = Tree()

        l_corpus = ["Cat", "Dog", "meow", "woof"]
        # print(Main.index(l_corpus, "meow"))


        # l_filtered_corpus = [w for w in l_corpus if w[0].isupper()]
        # print(l_filtered_corpus)

        # print("Starting test...")
        # x1 = ["C J RYAN", "C J Ryan", "C RYAN", "C.J.Ryan", "C. Ryan"]
        # x2 = "C Jack RYAN C J Ryan C RYAN C.J.Ryan C. Ryan"

        print("Ending test...")

    @classmethod
    def test_legal_doc(cls):
        legal_doc = next(iter(LegalDoc.s_legal_doc_dict.values()))
        assert isinstance(legal_doc, LegalDoc)
        # print(legal_doc)

    # Load all formatted files in the specified directory
    @classmethod
    def load_formatted_files(cls):
        for filename in os.listdir(cls.FORMATTED_PATH):
            l_legal_doc = LegalDoc()

            # TODO - Timer start
            Timers.s_init_timer.start()

            l_succeeded = l_legal_doc.initialise(cls.FORMATTED_PATH + filename, True)

            # TODO - Timer stop
            Timers.s_init_timer.stop()

            # If LegalDoc instance throws one or more errors whilst initialising
            if not l_succeeded:
                del l_legal_doc

    # Load all unformatted files in the specified directory
    @classmethod
    def load_unformatted_files(cls):

        for filename in os.listdir(cls.UNFORMATTED_PATH):
            l_legal_doc = LegalDoc()

            # TODO - Timer start
            Timers.s_init_timer.start()

            l_succeeded = l_legal_doc.initialise(cls.UNFORMATTED_PATH + filename, False)

            # TODO - Timer stop
            Timers.s_init_timer.stop()

            # If LegalDoc instance throws one or more errors whilst initialising
            if not l_succeeded:
                del l_legal_doc

            else:
                # Write LegalDoc to .txt
                if cls.SAVE_FORMATTED:
                    l_legal_doc.write(True)


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

    if Main.RUN_LEGAL_DOC_TEST_CODE:
        Main.test_legal_doc()

    print("File errors: " + str(LegalDoc.s_file_error))
    print("Case errors: " + str(LegalDoc.s_case_error))
    print("Judge errors: " + str(LegalDoc.s_judge_error))
    print("Defendant errors: " + str(LegalDoc.s_defendant_error))
    print("Sentencing errors: " + str(LegalDoc.s_sentencing_error))
    print("Section errors: " + str(LegalDoc.s_section_error))
    print("Body errors: " + str(LegalDoc.s_body_error))
    print("Unknown errors: " + str(LegalDoc.s_unknown_error))

    if Main.PRINT_JUDGE_DATA:
        Judge.print_all()

    if Main.ENABLE_TIMERS:
        Timer.print_all()

    print("Done!")


# Define main method
if __name__ == '__main__':
    main()
