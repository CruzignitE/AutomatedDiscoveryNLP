# from nltk import *
# from numpy import *
# from PyRTF import *
# from os import *
# from pandoc import *

# import regex as re

from LegalDoc import LegalDoc


# ----Main method----
def main():
    testAll(True)
    testSingle()
    print(LegalDoc.GetExceptionData())
    print("Done!")


# Test all legal docs
def testAll(aSaveFormattedFiles):
    # Very slow when files throw exception due to bad formatting
    try:
        lPathList = [
            "ERRORS1",
            "ERRORS2",
            # "ERRORS3",

            "DPP v Blum",
            "DPP v Bowden",
            "DPP v Bux",
            "DPP v Shaw",
            "DPP v Skonis",
            "DPP v Spokes",
            "DPP v Taha",
            "DPP v Tomuli"  # Needs additional work
        ]

        lLegalDocList = []
        for i in range(0, len(lPathList)):
            lLegalDoc = LegalDoc("Resources/Input/txt/" + lPathList[i] + ".txt")

            if lLegalDoc.FailedInit:
                del lLegalDoc
                continue

            else:
                lLegalDocList.append(lLegalDoc)

                if aSaveFormattedFiles:
                    lLegalDoc.Write()

    except Exception:
        raise


# Test a selection of legal docs
def testSingle():
    try:
        # lLegalDoc = "No Document specified"
        lLegalDoc = LegalDoc("Resources/Input/txt/DPP v Blum.txt")    # Works
        # lLegalDoc = LegalDoc("Resources/Input/txt/DPP v Bowden.txt")  # Works
        # lLegalDoc = LegalDoc("Resources/Input/txt/DPP v Bux.txt")     # Works
        # lLegalDoc = LegalDoc("Resources/Input/txt/DPP v Shaw.txt")    # Works
        # lLegalDoc = LegalDoc("Resources/Input/txt/DPP v Skonis.txt")  # Works
        # lLegalDoc = LegalDoc("Resources/Input/txt/DPP v Spokes.txt")  # Works
        # lLegalDoc = LegalDoc("Resources/Input/txt/DPP v Taha.txt")    # Works
        # lLegalDoc = LegalDoc("Resources/Input/txt/DPP v Tomuli.txt")    # Works

        # lLegalDoc = LegalDoc("Resources/Input/txt/ERRORS1.txt")       # Works
        # lLegalDoc = LegalDoc("Resources/Input/txt/ERRORS2.txt")       # Works
        # lLegalDoc = LegalDoc("Resources/Input/txt/ERRORS3.txt")       # Works

        print(lLegalDoc)

    except Exception:
        raise


# Define main method
if __name__ == '__main__':
    main()


