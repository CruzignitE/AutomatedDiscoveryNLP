'''
pip install regex
pip install nltk
pip install scikit-learn
pip install sacremoses
'''
import os
import re
import random
import ntpath
import string
import contextlib
import timeit
from typing import List

from Judge import Judge
from Timer import Timer, Timers

import Label

from sacremoses import MosesDetokenizer
import nltk.data
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
import bisect
from sklearn.feature_extraction.text import TfidfVectorizer
import ast

import math

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')


class LegalDoc:

    # ----Constant Static fields----
    # Patterns
    __SENTENCING_IDENTIFIER_PATTERN = re.compile(r".+(DATE OF SENTENCE:)", re.S | re.M)
    __EMPTY_LINE_PATTERN = re.compile(r"^[\s\t\n\r]*$")
    __FILE_SECTION_PATTERN = re.compile(r"Section:[0-9]+")
    __SECTION_PATTERN = re.compile(r"([0-9]+)[.(\s\t]*([A-Z].+)")
    __DOCUMENT_PATTERN = re.compile(
        r"(.+?)" +  # Head
        r"("  # Capture Body start
        r"(?:^1[.\t\s]*[A-Z])" +  # 1st section number and 1st capital letter
        r"(?:.+)"  # Body sans above capture
        r")",  # Capture Body End
        re.S | re.M)

    __CASE_NUMBER_PATTERN = re.compile(
        r"^.+" +
        r"(?:" +
        r"(?:AP|CR)" +  # E.g. "CR"
        r"|" +
        r"(?:Case No(?:[.\s\tA-Za-z]*))" +  # E.g. "Case No. X"
        r")" +
        r"([0-9\s-]+[0-9])" +  # E.g. "-12-34567"
        r"[\s\t]*$", +
        re.S | re.M)
    __DEFENDANT_NAME_PATTERN = re.compile(
        r".+" +
        r"(?:^\|[\s]+[vV][\s]+\|$)" +  # E.g. "| v |"
        r"(?:[-\s]+)" +  # E.g. "------"
        r"^\|[\s]+"  # E.g. "|  "
        r"([A-Za-z\s-]+)",  # E.g. "John Smith"
        re.S | re.M)

    __JUDGE_NAME_PATTERN = re.compile(
        r".+JUDGE:[\s|]+" +  # E.g. "JUDGE: |:
        r"(?:(?:HIS|HER)[\s].+[\s]+JUDGE?)?" +  # E.g. "HIS HONOUR CHIEF JUDGE"
        r"([a-zA-Z\s.']+)\|",  # E.g. "J. Smith"
        re.S | re.M | re.I)

    NAME_SIMPLIFIER_PATTERN = re.compile(r"([A-Z][A-Za-z]+)")
    SECTION_IDENTIFIER_PATTERN = re.compile(r"(SECTIONSTART[0-9]+:?\s?)")

    # Settings
    ANONYMIZE_NAMES: bool = False
    CLEAN_DATA: bool = False
    REMOVE_PUNCTUATION: bool = False
    REMOVE_STOP_WORDS: bool = False
    APPLY_STEMMING: bool = False
    APPLY_LEMMATIZATION: bool = False
    TO_LOWER_CASE: bool = False

    # ~95% success rate if False but ~20% of LegalDocs will have
    # a generated case number and/or the sections will lack structure.
    # Otherwise, ~75% success rate if True

    EXIT_IF_ERRORS: bool = True

    # Singletons
    MONTHS = ["January", "February", "March", "April", "May"
              "June", "July", "August", "September",
              "October", "November", "December"]
    SENTENCE_TOKENIZER = nltk.data.load('tokenizers/punkt/english.pickle')
    STOP_WORDS = set(stopwords.words("english"))
    STEMMER = PorterStemmer()
    LEMMATIZER = WordNetLemmatizer()
    DETOKENIZER = MosesDetokenizer()
    TFIDF_VECTORIZER = TfidfVectorizer()
    NAMES = sorted(list(set(nltk.corpus.names.words('male.txt') + nltk.corpus.names.words('female.txt'))))

    # ---- Static fields----
    s_successful_init_count: int = 0
    s_failed_init_count: int = 0
    s_exception_data_dict: dict = dict()
    s_legal_doc_dict:  dict = dict()

    s_file_error: int = 0
    s_case_error: int = 0
    s_judge_error: int = 0
    s_defendant_error: int = 0
    s_sentencing_error: int = 0
    s_section_error: int = 0
    s_body_error: int = 0
    s_parsing_error: int = 0
    s_unknown_error: int = 0

    # ----Constructor----
    def __init__(self):

            # Initialise fields
            self.__f_path = "NULL"
            self.__f_file_name = "NULL"
            self.__f_head = "NULL"
            self.__f_body = []
            self.__f_case_number = "NULL"
            self.__f_judge_name = "NULL"
            self.__f_defendant_name = "NULL"

            self.__f_corpus = []

            self.__f_sentencing_document = False
            self.__f_parsing_error = False
            self.__f_punctuation_removed = False
            self.__f_lower_case = False
            self.__f_stop_words_removed = False
            self.__f_stemmed = False
            self.__f_lemmatized = False
            self.__f_contains_errors = False
            self.__f_tokenized_sentences = False

    # ----Instance methods----
    # Initialise
    def initialise(self, a_path, load_state):

        """"
        Initialises a LegalDoc instance from a file
        Separated from __init__ to avoid exceptions in the constructor
        This method must be executed after construction
        :param str a_path: The path to a legal document
        :param bool load_state: Whether the provided path points to a formatted file (true) or an unformatted file (false)
        :rtype: bool
        :return: Whether an instance was successfully generated from file at the provided path
        """

        # Initialise path
        self.__f_path = a_path

        # Get file name
        head, tail = ntpath.split(self.path)
        self.__f_file_name = (tail or ntpath.basename(head))

        # Read in file
        l_file = None
        try:
            l_file = open(self.path)
            l_file_content = l_file.read()
            l_file.close()

        # Handle file error
        except IOError:
            LegalDoc.__note_exception(self.path, "MAJOR ERROR: Unable to read file", True)
            l_file.close()
            return False

        # Load state from a formatted file
        if load_state:

            # TODO - Timer start
            Timers.s_init_load_state_timer.start()

            l_succeeded = self.__initialise_load_state(l_file_content)

            # TODO - Timer stop
            Timers.s_init_load_state_timer.stop()

            if not l_succeeded:
                LegalDoc.s_file_error += 1
                return False

        # Generate state from an unformatted file
        else:

            # TODO - Timer start
            Timers.s_init_gen_state_timer.start()

            l_succeeded = self.__initialise_generate_state(l_file_content)

            # TODO - Timer stop
            Timers.s_init_gen_state_timer.stop()

            if not l_succeeded:
                return False
            self.__f_punctuation_removed = LegalDoc.REMOVE_PUNCTUATION
            self.__f_lower_case = LegalDoc.TO_LOWER_CASE
            self.__f_stop_words_removed = LegalDoc.REMOVE_STOP_WORDS
            self.__f_stemmed = LegalDoc.APPLY_STEMMING
            self.__f_lemmatized = LegalDoc.APPLY_LEMMATIZATION

        # Note successful initialisation
        LegalDoc.s_successful_init_count += 1

        # Add current LegalDoc to static dictionary of LegalDocs
        LegalDoc.s_legal_doc_dict[self.file_name] = self

        # Create judge and add it to static dictionary of judges
        Judge.add_legal_doc(self)

        return True

    # Load state from a formatted file
    def __initialise_load_state(self, a_file_content):

        """"
        Initialises a LegalDoc instance from a formatted file
        :type a_file_content: str
        :rtype: bool
        :return: Whether an instance was successfully generated from the source file content
        """

        try:
            l_lines = a_file_content.splitlines()
            i = 0

            # Verify this is a formatted LegalDOc
            if l_lines[0] == "FIELD DATA:":
                i += 1

                # Read in field data
                while l_lines[i] != "SECTIONS:":
                    l_line = l_lines[i].strip()

                    # File name
                    if l_line == "FILE NAME:":
                        self.__f_file_name = l_lines[i+1].strip()
                        i += 2
                        continue

                    # Case number
                    if l_line == "CASE NUMBER:":
                        self.__f_case_number = l_lines[i + 1].strip()
                        i += 2
                        continue

                    # Judge name
                    if l_line == "JUDGE NAME:":
                        self.__f_judge_name = l_lines[i + 1].strip()
                        i += 2
                        continue

                    # Defendant name
                    if l_line == "DEFENDANT NAME:":
                        self.__f_defendant_name = l_lines[i + 1].strip()
                        i += 2
                        continue

                    # Sentencing document
                    if l_line == "PRISON DOCUMENT:":
                        self.__f_sentencing_document = ast.literal_eval(l_lines[i + 1].strip())
                        i += 2
                        continue

                    # Punctuation removed
                    if l_line == "PUNCTUATION REMOVED:":
                        self.__f_punctuation_removed = ast.literal_eval(l_lines[i + 1].strip())
                        i += 2
                        continue

                    # Stop words removed
                    if l_line == "STOP WORDS REMOVED:":
                        self.__f_stop_words_removed = ast.literal_eval(l_lines[i + 1].strip())
                        i += 2
                        continue

                    # Lower case
                    if l_line == "LOWER CASE:":
                        self.__f_lower_case = ast.literal_eval(l_lines[i + 1].strip())
                        i += 2
                        continue

                    # Stemmed
                    if l_line == "STEMMED:":
                        self.__f_stemmed = ast.literal_eval(l_lines[i + 1].strip())
                        i += 2
                        continue

                    # Lemmatized
                    if l_line == "LEMMATIZED:":
                        self.__f_lemmatized = ast.literal_eval(l_lines[i + 1].strip())
                        i += 2
                        continue

                    # Contains errors
                    if l_line == "CONTAINS ERRORS:":
                        self.__f_contains_errors = ast.literal_eval(l_lines[i + 1].strip())
                        i += 2
                        continue

                    # Skip line
                    i += 1

                # Read in section data
                l_section_index = -1
                i += 1
                while i < len(l_lines):
                    l_line = l_lines[i].strip()

                    # Reading a section heading
                    if LegalDoc.__FILE_SECTION_PATTERN.match(l_line):
                        l_section_index += 1
                        self.__f_body.append([])

                    # Reading a section's contents
                    else:
                        self.__f_body[l_section_index].append(l_line)
                    i += 1

            # Create corpora
            for l_section in self.body:
                for l_sentence in l_section:
                    self.__f_corpus += word_tokenize(l_sentence)

            return True
        except IndexError:
            LegalDoc.__note_exception(self.path,
                                      "MAJOR ERROR: Failed to import formatted file, index out of bounds", True)
            return False

    # Generate state from an unformatted file
    def __initialise_generate_state(self, a_file_content):

        """"
        Initialises a LegalDoc instance from an unformatted file
        :type a_file_content: str
        :rtype: bool
        :return: Whether an instance was successfully generated from the source file content
        """

        try:

            # Break up document into base components
            l_document_match = LegalDoc.__DOCUMENT_PATTERN.match(a_file_content)
            if l_document_match:
                l_document_groups = l_document_match.groups()

            # Handle document parsing error
            else:
                LegalDoc.__note_exception(self.path, "MAJOR ERROR: Regex cannot parse document", True)
                LegalDoc.s_parsing_error += 1
                return False

            # Extract head
            self.__f_head = l_document_groups[0]

            # Extract sentencing identifier
            if not self.__extract_sentencing_identifier():
                return False

            # Extract case number
            if not self.__extract_case_number():
                return False

            # Extract defendant's name
            if not self.__extract_defendant_name():
                return False

            # Extract judge's name
            if not self.__extract_judge_name():
                return False

            # Group lines into sections
            l_lines = l_document_groups[1].splitlines()  # Body broken down by line
            if not self.__group_lines_into_sections(l_lines):
                return False

            # Anonymize names
            self.__anonymize_names()

            # Clean sections
            self.__clean_sections()

            # Initialisation completed with no errors
            return True

        # Handle miscellaneous errors
        except Exception:
            LegalDoc.__note_exception(self.path, "MAJOR ERROR: Unspecified error occurred", True)
            LegalDoc.s_unknown_error += 1
            raise
            return False

    # Anonymize names
    def __anonymize_names(self):

        """"
        Change's every instance of the defendant's name to "Defandant"
        Encrypts the judge's name
        Assigns a random name to everybody else
        """

        if LegalDoc.ANONYMIZE_NAMES:
            # TODO - Timer start
            Timers.s_anonymize_names_timer.start()

            # Generate corpus
            self.generate_corpus_from_sections()

            # TODO - Timer start
            Timers.s_anonymization_timer.start()

            # Get list of names
            l_filtered_corpus = [w for w in self.corpus if w[0].isupper()]
            # print(l_filtered_corpus)

            # print(l_filtered_corpus)
            # l_names = [w for w in LegalDoc.NAMES if w in l_filtered_corpus]

            l_names = []
            for w in l_filtered_corpus:
                i = LegalDoc.index(LegalDoc.NAMES, w)
                if i is not None:
                    l_names.append(LegalDoc.NAMES[i])

            # TODO - Timer stop
            Timers.s_anonymization_timer.stop()

            # print("Namesxxx: " + str(l_names))
            # print("All Names: " + str(sorted(LegalDoc.NAMES)))

            # Create a random name dictionary
            l_random_names = dict()
            for l_name in l_names:
                l_random_index = random.randint(0, len(LegalDoc.NAMES) - 1)
                l_random_names[l_name] = LegalDoc.NAMES[l_random_index]

            # Anonymize names
            for i, l_word in enumerate(self.corpus):
                try:
                    if l_word in self.defendant_name:
                        if self.corpus[i-1] == "Defendant":
                            del self.corpus[i]
                        else:
                            self.corpus[i] = "Defendant"
                    elif l_word in self.judge_name:
                        if self.corpus[i - 1] == "Judge":
                            del self.corpus[i]
                        else:
                            self.corpus[i] = "Judge"
                    elif l_word in l_names and l_word not in LegalDoc.MONTHS:
                        self.corpus[i] = l_random_names[l_word]

                except IndexError:
                    print("FAIL")
                    continue

            self.generate_sections_from_corpus()

            # TODO - Timer stop
            Timers.s_anonymize_names_timer.stop()

    def __extract_sentencing_identifier(self):

        """"
        Extracts the sentencing identifier from this legal document's head
        sets the value of "__f_sentencing_document" as a bool
        :rtype: bool
        :return: Whether the sentencing identifier was successfully extracted and set
        """

        # Extract sentencing identifier
        l_sentencing_identifier_match = LegalDoc.__SENTENCING_IDENTIFIER_PATTERN.match(self.__f_head)
        if l_sentencing_identifier_match:
            self.__f_sentencing_document = True
            return True

        # Handle non sentencing document
        else:
            LegalDoc.__note_exception(self.path, "MAJOR ERROR: This is not a sentencing document", True)
            LegalDoc.s_sentencing_error += 1
            return False

    # Extract case number
    def __extract_case_number(self):
        """"
        Extracts the case number from this legal document's head and cleans it
        sets the value of "l_case_num_match" as a string
        :rtype: bool
        :return: Whether the case number was successfully extracted and set
        """

        # Extract case number
        l_case_num_match = LegalDoc.__CASE_NUMBER_PATTERN.match(self.__f_head)
        if l_case_num_match:

            # Extract case number whilst removing dashes, spaces and tabs
            self.__f_case_number = (l_case_num_match.groups())[0].translate({ord(c): None for c in r'-    '})
            return True

        # Handle failure to find a case number
        else:
            LegalDoc.__note_exception(
                self.path, "ERROR: Unable to find case number", LegalDoc.EXIT_IF_ERRORS)
            LegalDoc.s_case_error += 1

            if LegalDoc.EXIT_IF_ERRORS:
                return False

    # Extract defendant's name
    def __extract_defendant_name(self):

        """"
        Extracts the defendant's name from this legal document's head
        Removes initials from the defendant's name
        Ensure the defendant's name is all lower case with the exception of the first letter
        sets the value of "__f_defendant_name" as a set of strings
        (e.g. "John Smith" becomes {"John", "Smith"})
        :rtype: bool
        :return: Whether the defendant's name was successfully extracted and set
        """

        l_defendant_name_match = LegalDoc.__DEFENDANT_NAME_PATTERN.match(self.head)

        # Check for regex match
        if l_defendant_name_match:

            # Clean name and set value of "__f_defendant_name"
            self.__f_defendant_name = (l_defendant_name_match.groups())[0].strip()
            self.__f_defendant_name = LegalDoc.NAME_SIMPLIFIER_PATTERN.findall(self.defendant_name)
            self.__f_defendant_name = set([x.lower().capitalize() for x in self.defendant_name])
            return True

        # Handle inability to determine defendant's name
        else:
            LegalDoc.__note_exception(self.path, "MAJOR ERROR: Unable to find defendant's name", True)
            LegalDoc.s_defendant_error += 1
            return False

    # Extract judge's name
    def __extract_judge_name(self):

        """"
        Extracts the judge's name from this legal document's head
        Removes initials from the judge's name
        Ensure the judge's name is all lower case with the exception of the first letter
        sets the value of "__f_judge_name" as a set of strings
        (e.g. "John Smith" becomes {"John", "Smith"})
        :rtype: bool
        :return: Whether the judge's name was successfully extracted and set
        """

        # Check for regex match
        l_judge_name_match = LegalDoc.__JUDGE_NAME_PATTERN.match(self.head)
        if l_judge_name_match:

            # Clean name and set value of "__f_judge_name"
            self.__f_judge_name = (l_judge_name_match.groups())[0].strip()
            self.__f_judge_name = LegalDoc.NAME_SIMPLIFIER_PATTERN.findall(self.judge_name)
            self.__f_judge_name = set([x.lower().capitalize() for x in self.judge_name])
            return True

        # Handle inability to determine judge's name
        else:
            LegalDoc.__note_exception(self.path, "MAJOR ERROR: Unable to find judge's name", True)
            LegalDoc.s_judge_error += 1
            return False

    # Tokenize each sentence in each section in the body
    def __group_lines_into_sections(self, a_lines):

        """"
        Groups the provided list of lines into sections comprised of sentences
        :type a_lines: list
        :rtype: bool
        :return: Whether the lines were successfully grouped into sections
        """

        l_sections = []

        # Group lines into sections
        try:
            l_section_index = 0  # Used to check whether sections are being missed
            l_sections.append("")  # l_sections[0] catches any lines prior to the first section
            l_bad_sections = False  # True if any problems are encountered whilst parsing sections

            # For each line in l_lines...
            for l_line in a_lines:
                l_section_match = LegalDoc.__SECTION_PATTERN.match(l_line)

                # Check if the line contains the start of a section
                if l_section_match:

                    # Remove the section number from the line
                    l_line = LegalDoc.__SECTION_PATTERN.sub(r"\g<2>", l_line, 1)

                    # If the section number in the line matches the l_section_index
                    if l_section_match[1] == str(l_section_index + 1):
                        l_section_index += 1
                        l_section = "SECTIONSTART" + str(l_section_index) + ":\t" + l_line
                        l_sections.append(l_section)

                    # A parsing error has occurred
                    else:
                        l_bad_sections = True
                        l_sections[l_section_index] += l_line

                # Check if the line is empty
                elif LegalDoc.__EMPTY_LINE_PATTERN.match(l_line):
                    continue

                # This line is not the start of a section nor is it empty
                else:

                    # The line is part of a section
                    if l_section_index > 0:
                        l_sections[l_section_index] += l_line

                    # This line is prior to all sections. Add it to section 0
                    else:
                        l_bad_sections = True
                        l_sections[l_section_index] += l_line

            # Handle section parsing errors
            if l_bad_sections:
                self.__f_contains_errors = True
                LegalDoc.__note_exception(
                    self.path, "ERROR: Bad section(s)", LegalDoc.EXIT_IF_ERRORS)
                LegalDoc.s_section_error += 1
                if LegalDoc.EXIT_IF_ERRORS:
                    return False

            # Break up sections into sentences
            # Add N sentence arrays to body, where N is the number of sections
            for l_section in l_sections:
                self.body.append(LegalDoc.SENTENCE_TOKENIZER.tokenize(l_section))

            return True

        # Handle failure to parse document's body
        except (TypeError, AttributeError, IndexError):
            LegalDoc.__note_exception(self.path, "MAJOR ERROR: Unable to break down body", True)
            LegalDoc.s_body_error += 1
            return False

    # Tokenize each sentence in each section in the body
    def tokenize_sentences(self):

        # Check if sentences are already tokenized
        if not self.tokenized_sentences:
            l_tokenized_sections = []

            # By section
            for l_section in self.body:
                l_tokenized_sentences = []

                # By sentence
                for l_sentence in l_section:

                    # Add tokenized sentences to section
                    l_tokenized_sentences.append(word_tokenize(l_sentence))

                # Add tokenized sections to sections list
                l_tokenized_sections.append(l_tokenized_sentences)

            # Update body
            self.__f_body = l_tokenized_sections

            self.__f_tokenized_sentences = True

    # Detokenize each sentence in each section in the body
    def detokenize_sentences(self):

        # Check if sentences are already tokenized
        if self.tokenized_sentences:
            l_detokenized_sections = []

            # By section
            for l_section in self.body:
                l_detokenized_sentences = []

                # By sentence
                for l_sentence in l_section:

                    # Add detokenized sentences to section
                    l_detokenized_sentences.append(LegalDoc.DETOKENIZER.detokenize(l_sentence, return_str=True))

                # Add detokenized sections to sections list
                l_detokenized_sections.append(l_detokenized_sentences)

            # Update body
            self.__f_body = l_detokenized_sections

            self.__f_tokenized_sentences = False

    # Generates untokenized sections from the words in the corpus
    def generate_sections_from_corpus(self):

        """"
        This method will not work properly if punctuation has been removed
        or if all words have been lower cased
        """

        # TODO - Timer start
        Timers.s_gen_secs_from_corpus_timer.start()

        self.__f_body = []
        l_section_words = []

        for l_word in self.corpus:
            if LegalDoc.SECTION_IDENTIFIER_PATTERN.match(l_word):

                # Detokenize section words list into a string
                l_detokenized_section = LegalDoc.DETOKENIZER.detokenize(l_section_words, return_str=True)

                # Tokenize section string into sentences (a list of strings)
                self.body.append(LegalDoc.SENTENCE_TOKENIZER.tokenize(l_detokenized_section))

                # New section
                l_section_words = [l_word]
            else:
                # Add word to section words list
                l_section_words.append(l_word)

        # TODO - Timer stop
        Timers.s_gen_secs_from_corpus_timer.stop()

    # Creates a corpus from the sentences in the body's sections
    def generate_corpus_from_sections(self):

        """"
        This method will not work properly if punctuation has been removed
        or if all words have been lower cased
        """

        # TODO - Timer start
        Timers.s_gen_corpus_from_secs_timer.start()

        # Check whether sentences are tokenized already
        if self.tokenized_sentences:

            # Create corpus from tokenized sentences
            for l_section in self.body:
                for l_sentence in l_section:
                    for l_word in l_sentence:
                        self.corpus.append(l_word)

        else:

            # Create corpus from untokenized sentences
            for l_section in self.body:
                for l_sentence in l_section:
                    for l_word in word_tokenize(l_sentence):
                        self.corpus.append(l_word)

        # TODO - Timer stop
        Timers.s_gen_corpus_from_secs_timer.stop()

    # Creates a corpus from the sentences in the body's sections
    def __clean_sections(self):
        if LegalDoc.CLEAN_DATA:

            # TODO - Timer start
            Timers.s_clean_sections_timer.start()

            # Tokenize sections
            self.tokenize_sentences()

            # Clean data
            l_filtered_sections = []

            # By section
            for l_section in self.body:
                l_filtered_sentences = []

                # By sentence
                for l_sentence in l_section:
                    l_filtered_words = []

                    # By word
                    for l_word in l_sentence:

                        # Remove stopwords
                        if l_word in LegalDoc.STOP_WORDS and LegalDoc.REMOVE_STOP_WORDS:
                            continue

                        # Stemming
                        if LegalDoc.APPLY_STEMMING:
                            l_word = LegalDoc.STEMMER.stem(l_word)

                        # Lemmatization
                        if LegalDoc.APPLY_LEMMATIZATION:
                            l_word = LegalDoc.LEMMATIZER.lemmatize(l_word)

                        # Remove punctuation
                        if LegalDoc.REMOVE_PUNCTUATION:
                            l_word = l_word.translate(str.maketrans('', '', string.punctuation))

                        # To lower case
                        if LegalDoc.TO_LOWER_CASE:
                            l_word = l_word.lower()

                        # Add filtered word to sentence
                        l_filtered_words.append(l_word)

                    # Add filtered sentence to section
                    l_filtered_sentences.append(l_filtered_words)

                # Add filtered section to section list
                l_filtered_sections.append(l_filtered_sentences)

            # Update body
            self.__f_body = l_filtered_sections

            # Create corpus from sections
            self.generate_corpus_from_sections()

            # Detokenize sentences
            self.detokenize_sentences()

            # TODO - Timer stop
            Timers.s_clean_sections_timer.stop()

    # Strip section identifiers
    def strip_section_identifiers(self, a_generate_corpus=True):
        for l_section in self.body:
            for i, l_sentence in enumerate(l_section):
                l_section[i] = LegalDoc.SECTION_IDENTIFIER_PATTERN.sub("", l_sentence, 1)

        if a_generate_corpus:
            self.generate_corpus_from_sections()

    # Save formatting as a txt file
    def write(self, a_raw_text=False, a_prefix="", a_new_path=""):

        """"
        Writes the data in this instance to a .TXT file
        The case name and number are used to name the file
        """

        # TODO - Timer start
        Timers.s_write_timer.start()

        # Make sure that "CaseName" and  "CaseNumber" do not contain illegal values and are not excessively long
        l_safe_file_name = re.sub(r'[\\/:"*?<>|]+', "", self.file_name)
        l_safe_file_name = (l_safe_file_name[:25] + '..') if len(l_safe_file_name) > 25 else l_safe_file_name

        # l_safe_case_number = re.sub(r'[\\/:"*?<>|]+', "", self.case_number)
        # l_safe_case_number = (l_safe_case_number[:25] + '..') if len(l_safe_case_number) > 25 else l_safe_case_number

        # Add brackets to prefix if specified
        if a_prefix:
            a_prefix = "(" + a_prefix + ")"

        # Select path string based on input
        if a_new_path:
            l_path = a_new_path
        else:
            l_path = "Resources/Output/Formatted/"

        # Make path if it doesn't exist
        if not os.path.exists(l_path):
            os.makedirs(l_path)

        # Save file
        l_save_file = None
        try:
            l_save_file = open(
                l_path + a_prefix + "(F) " + l_safe_file_name, "w", encoding="UTF-8")

            # Remove section identifiers
            self.strip_section_identifiers(False)

            # Write formatted LegalDoc
            if not a_raw_text:
                l_save_file.write(self.__str__())

            # Only write body's contents (unformatted)
            else:
                for l_section in self.body:
                    for l_sentence in l_section:
                        l_save_file.write(l_sentence + " \n")

            l_save_file.close()

            # TODO - Timer start
            Timers.s_write_timer.stop()

        # Handle IO Exception
        except IOError:
            print("ERROR: Unable to save file with path: " + self.path)
            l_save_file.close()

            # TODO - Timer start
            Timers.s_write_timer.stop()

    # ----Method Overrides----
    # Override str(self) with formatted body output
    def __str__(self):

        # Write field data
        l_info = "FIELD DATA:\n"
        l_info += "\tFILE NAME:\n\t\t" + self.file_name + "\n"
        l_info += "\tCASE NUMBER:\n\t\t" + self.case_number + '\n'
        l_info += "\tJUDGE NAME:\n\t\t" + str(self.judge_name) + '\n'
        l_info += "\tDEFENDANT NAME:\n\t\t" + str(self.defendant_name) + '\n'

        l_info += "\tPRISON DOCUMENT:\n\t\t" + str(self.sentencing_document) + '\n'
        l_info += "\tPUNCTUATION REMOVED:\n\t\t" + str(self.punctuation_removed) + '\n'
        l_info += "\tLOWER CASE:\n\t\t" + str(self.lower_case) + '\n'
        l_info += "\tSTOP WORDS REMOVED:\n\t\t" + str(self.stop_words_removed) + '\n'
        l_info += "\tSTEMMED:\n\t\t" + str(self.stemmed) + '\n'
        l_info += "\tLEMMATIZED:\n\t\t" + str(self.lemmatized) + '\n'
        l_info += "\tCONTAINS ERRORS:\n\t\t" + str(self.contains_errors) + '\n'

        l_info += "SECTIONS:" + '\n'

        # Write the section headers
        for i in range(0, len(self.body)):
            l_section = self.body[i]
            l_info += '\t' "Section:" + str(i) + '\n'

            # Write the sentences corresponding to the above section
            for l_sentence in l_section:
                l_info += "\t\t" + l_sentence + '\n'

        return l_info

    # ----Class Methods----
    # Prints all the exception data in the exception dict as well as some basic summary statistics
    @classmethod
    def print_exception_data(cls):

        # Write general error data
        l_error_data = "Successful initialisations: " + str(cls.s_successful_init_count) + '\n'
        l_error_data += "Failed initialisations: " + str(cls.s_failed_init_count) + '\n'
        l_error_data += "Success rate: " + \
                        str((cls.s_successful_init_count * 1.0) /
                            ((cls.s_failed_init_count * 1.0) + (cls.s_successful_init_count * 1.0))) + '\n'

        l_error_data += (
                        "File errors: " + str(LegalDoc.s_file_error) +
                        "Case errors: " + str(LegalDoc.s_case_error) +
                        "Judge errors: " + str(LegalDoc.s_judge_error) +
                        "Defendant errors: " + str(LegalDoc.s_defendant_error) +
                        "Sentencing errors: " + str(LegalDoc.s_sentencing_error) +
                        "Section errors: " + str(LegalDoc.s_section_error) +
                        "Body errors: " + str(LegalDoc.s_body_error) +
                        "Unknown errors: " + str(LegalDoc.s_unknown_error)
                        )

        l_error_data += "Exceptions: " + '\n'

        # For each LegalDoc containing one or more errors
        # l_path is the key, l_errors is the value
        for l_path, l_errors in cls.s_exception_data_dict.items():

            # Write the path of the LegalDoc
            l_error_data += "\t" + l_path + '\n'

            # Write the errors associated with the above LegalDoc
            for l_error in l_errors:
                l_error_data += "\t\t" + l_error + '\n'

        print(l_error_data)

    # Notes an exception
    @classmethod
    def __note_exception(cls, a_path: str, a_exception: str, a_failed_init: bool):

        """"
        Adds the provided exception data to the exception dict using the provided path.
        Also increments the classes failed init count
        :type a_path: str
        :type a_exception: str
        :type a_failed_init: bool
        """

        # If the path already exists in the exception dictionary
        if a_path in cls.s_exception_data_dict:
            cls.s_exception_data_dict[a_path].append(a_exception)

        # Add the path to the exception dictionary
        else:
            cls.s_exception_data_dict[a_path] = [a_exception]

        if a_failed_init:
            # Increment static counter for failed initialisation
            cls.s_failed_init_count += 1

    # TODO Work on this method
    @classmethod
    def get_docs_by_regex(cls, a_regex):

        """
        Gets a list of LegalDocs whose bodies' match the provided pattern
        :param str a_regex: A pattern used to get LegalDocs
        :return: A list of LegalDocs
        :rtype: list

        """
        assert (isinstance(a_regex, re.Pattern))

        l_matching_docs = []
        l_break = False

        for l_legal_doc in LegalDoc.s_legal_doc_dict.values():
            l_break = False

            for l_section in l_legal_doc.body:
                if l_break:
                    break

                for l_sentence in l_section:

                    # Look for match
                    l_match = a_regex.match(l_sentence)

                    if l_match:
                        # TODO Annoying import bug, fix later
                        if not Label.Label.s_flat_labels_dict[l_legal_doc.file_name]:
                            l_matching_docs.append(l_legal_doc.file_name)
                        l_break = True
                        break

        print(l_matching_docs)
        print(len(l_matching_docs))

    # ----Properties (Read only getters)----
    # Origin path
    @property
    def path(self):

        """"
        :rtype: str
        :return: The path of the file that originally generated this LegalDoc instance
        """

        return self.__f_path

    # File name
    @property
    def file_name(self):

        """"
        :rtype: str
        :return: The name of the file that originally generated this LegalDoc instance
        """

        return self.__f_file_name

    # Head
    @property
    def head(self):

        """"
        :rtype: str
        :return: Summary information of the court proceeding
        """

        return self.__f_head

    # Body
    @property
    def body(self):

        """"
        :rtype: list
        :return: The transcript of the court proceeding. Broken down into sections (list) comprised of sentences (str)
        """

        return self.__f_body

    # Case number
    @property
    def case_number(self):

        """"
        :rtype: str
        :return: The document's case number
        """

        return self.__f_case_number

    # Judge's name
    @property
    def judge_name(self):

        """"
        :rtype: str
        :return: The judge's name
        """

        return self.__f_judge_name

    # Defendant name
    @property
    def defendant_name(self):

        """"
        :rtype: str
        :return: The defendant's name
        """

        return self.__f_defendant_name

    # Sentencing document
    @property
    def sentencing_document(self):

        """"
        :rtype: bool
        :return: Whether the document pertains to the sentencing of an individual
        """

        return self.__f_sentencing_document

    # Punctuation Removed
    @property
    def punctuation_removed(self):

        """"
        :rtype: bool
        :return: Whether the document's contents have had punctuation removed
        """

        return self.__f_punctuation_removed

    # Lower case
    @property
    def lower_case(self):

        """"
        :rtype: bool
        :return: Whether the document's contents have been converted to lower case
        """

        return self.__f_lower_case

    # Stop words removed
    @property
    def stop_words_removed(self):

        """"
        :rtype: bool
        :return: Whether the document's contents have been stripped of stop words
        """

        return self.__f_stop_words_removed

    # Stemmed
    @property
    def stemmed(self):

        """"
        :rtype: bool
        :return: Whether the document's contents have been stemmed
        """

        return self.__f_stemmed

    # Lemmatized
    @property
    def lemmatized(self):

        """"
        :rtype: bool
        :return: Whether the document's contents have been lemmatized
        """

        return self.__f_lemmatized

    # Contains errors
    @property
    def contains_errors(self):

        """"
        :rtype: bool
        :return: Whether the document contains broken sections or a missing case number or both
        """

        return self.__f_contains_errors

    # Tokenized sentences
    @property
    def tokenized_sentences(self):

        """"
        :rtype: bool
        :return: Whether the document's sections contain tokenized sentences
        """

        return self.__f_tokenized_sentences

    # Corpus
    @property
    def corpus(self):

        """"
        :rtype: list
        :return: Corpus with each index corresponding to a single word
        """

        return self.__f_corpus

    # ----Static Methods----
    @staticmethod
    def index(a_list, a_value):

        """Locate the leftmost value exactly equal to x"""

        i = bisect.bisect_left(a_list, a_value)
        if i != len(a_list) and a_list[i] == a_value:
            return i
        return None

    @contextlib.contextmanager
    def escapable(self):
        class Escape(RuntimeError): pass
        class Unblock(object):
            def escape(self):
                raise Escape()

        try:
            yield Unblock()
        except Escape:
            pass