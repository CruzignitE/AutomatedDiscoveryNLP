
# from numpy import *
# from PyRTF import *
# from os import *
# from pandoc import *
# import re
# from array import *
from Label import *

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

    # Utility regex
    REGEX = re.compile(
        r".*" +
        r"(" +
        r"(?:sexual|indecent act)" +
        r".*" +
        r"(?:child|minor)" +
        r")",
        re.S | re.M | re.I)

    # Paths
    UNFORMATTED_FILE_PATH = "Resources/Input/txt/"
    FORMATTED_FILE_PATH = "Resources/Output/Formatted/"

    # Outputs labelled files split by a given subtype (For further info check method)
    SPLIT_AND_WRITE = (True, LabelType.CHARGES_TYPE, Charges.SEXUAL_ASSAULT_OF_MINOR)

    # Print docs using utility regex
    PRINT_DOCS_BY_REGEX = True

    # Settings
    LOAD_FORMATTED_FILES = False        # Load formatted files (Fast!) (Speed depends on LegalDoc settings)
    LOAD_UNFORMATTED_FILES = True       # Load unformatted files (Slow!) (Speed depends on LegalDoc settings)
    SAVE_FILES = True                   # Save LegalDoc instances as .TXT files after formatting
    SAVE_FORMATTED_AS_RAW = True        # Saved files will be unformatted
    AUTO_REGEX_LABEL_FILES = True       # Label all files with regex

    PRINT_EXCEPTION_DATA = False        # Print detailed exception data
    PRINT_JUDGE_DATA = False            # Print the list of judges and their associated cases
    PRINT_LABELS = False                # Print the list of labels in tree format
    PRINT_TIMERS = True                 # Print timer data as a table

    RUN_TEST = True                # Runs "test" method after files have been read
    RUN_TEST_A_LEGAL_DOC = False        # Runs "test_a_legal_doc" method after files have been read
    RUN_TEST_ALL_LEGAL_DOCS = True      # Runs "test_all_legal_docs" method after files have been read




    @classmethod
    def test(cls):

        print("Starting test...")

        print("Ending test...")

    @classmethod
    def test_all_legal_docs(cls):

        print("Starting test_all_legal_docs...")

        print("Ending test_all_legal_docs...")

    @classmethod
    def test_a_legal_doc(cls, a_name=""):

        print("Starting test_a_legal_doc...")

        if a_name:
            legal_doc = LegalDoc.s_legal_doc_dict[a_name]
        else:
            legal_doc = next(iter(LegalDoc.s_legal_doc_dict.values()))

        # Label.auto_regex_label(legal_doc.head, legal_doc.file_name)
        # print(legal_doc)

        print("Ending test_a_legal_doc...")

    # Load all formatted files in the specified directory
    @classmethod
    def load_formatted_files(cls):
        for filename in os.listdir(cls.FORMATTED_FILE_PATH):
            l_legal_doc = LegalDoc()

            # TODO - Timer start
            Timers.s_init_timer.start()

            l_succeeded = l_legal_doc.initialise(cls.FORMATTED_FILE_PATH + filename, True)

            # TODO - Timer stop
            Timers.s_init_timer.stop()

            # If LegalDoc instance throws one or more errors whilst initialising
            if not l_succeeded:
                del l_legal_doc

    # Load all unformatted files in the specified directory
    @classmethod
    def load_unformatted_files(cls):

        for filename in os.listdir(cls.UNFORMATTED_FILE_PATH):
            l_legal_doc = LegalDoc()

            # TODO - Timer start
            Timers.s_init_timer.start()

            l_succeeded = l_legal_doc.initialise(cls.UNFORMATTED_FILE_PATH + filename, False)

            # TODO - Timer stop
            Timers.s_init_timer.stop()

            # If LegalDoc instance throws one or more errors whilst initialising
            if not l_succeeded:
                del l_legal_doc

            else:
                # Write LegalDoc to .txt
                if cls.SAVE_FILES:
                    l_legal_doc.write(Main.SAVE_FORMATTED_AS_RAW)


# ----Main method----
def main():

    # Print versions
    print('The nltk version is {}.'.format(nltk.__version__))
    print('The scikit-learn version is {}.'.format(sklearn.__version__))

    # Initialise label class
    Label.initialise_class()

    # Functionality based on settings in Main class

    if Main.LOAD_FORMATTED_FILES:
        Main.load_formatted_files()

    elif Main.LOAD_UNFORMATTED_FILES:
        Main.load_unformatted_files()

    # Print info
    if Main.PRINT_EXCEPTION_DATA:
        LegalDoc.print_exception_data()

    if Main.PRINT_JUDGE_DATA:
        Judge.print_all()

    # Labels
    if Main.AUTO_REGEX_LABEL_FILES:
        Label.auto_regex_label_all_files()

    if Main.SPLIT_AND_WRITE[0]:
        Label.split_and_write(Main.SPLIT_AND_WRITE[1], Main.SPLIT_AND_WRITE[2])

    if Main.PRINT_DOCS_BY_REGEX:
        LegalDoc.get_docs_by_regex(Main.REGEX)

    if Main.PRINT_LABELS:
        Label.print_all()

    # Test code
    if Main.RUN_TEST:
        Main.test()

    if Main.RUN_TEST_A_LEGAL_DOC:
        Main.test_a_legal_doc()

    if Main.RUN_TEST_ALL_LEGAL_DOCS:
        Main.test_all_legal_docs()

    # Print timers
    if Main.PRINT_TIMERS:
        Timer.print_all()

    print("Done!")


# Define main method
if __name__ == '__main__':
    main()
