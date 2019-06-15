
# from numpy import *
# from PyRTF import *
# from os import *
# from pandoc import *
# import re
# from array import *
import nltk
import sklearn
import os
from LegalDoc import LegalDoc
from Judge import Judge


# ----Main method----
def main():
    print('The nltk version is {}.'.format(nltk.__version__))
    print('The scikit-learn version is {}.'.format(sklearn.__version__))

    test_all(True)
    print(LegalDoc.get_exception_data())
    Judge.print_all()
    print("Done!")


# Test all legal docs
def test_all(a_save_formatted_files: bool):
    l_legal_doc_list = []

    for filename in os.listdir("Resources/Input/txt/"):
        l_legal_doc = LegalDoc("Resources/Input/txt/" + filename)

        if l_legal_doc.failed_init:
            del l_legal_doc
            continue

        else:
            l_legal_doc_list.append(l_legal_doc)

            # Write LegalDoc to .txt
            if a_save_formatted_files:
                l_legal_doc.write()


# Define main method
if __name__ == '__main__':
    main()
