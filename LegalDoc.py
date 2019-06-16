'''
pip install regex
pip install nltk
pip install scikit-learn
pip install sacremoses
'''

import re
import random
import ntpath
from typing import List

from Judge import Judge

from sacremoses import MosesDetokenizer
import nltk.data
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
import ast

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

    # Settings
    CLEAN_DATA = True
    REMOVE_STOP_WORDS = True
    APPLY_STEMMING = False
    APPLY_LEMMATIZATION = True

    # Singletons
    STOP_WORDS = set(stopwords.words("english"))
    STEMMER = PorterStemmer()
    LEMMATIZER = WordNetLemmatizer()
    DETOKENIZER = MosesDetokenizer()
    TFIDF_VECTORIZER = TfidfVectorizer()

    # ---- Static fields----
    __s_successful_init_count: int = 0
    __s_failed_init_count: int = 0
    __s_exception_data_dict: dict = dict()
    __s_legal_doc_dict:  dict = dict()

    # ~95% success rate if False but ~20% of LegalDocs will have
    # a generated case number and/or the sections will lack structure.
    # Otherwise, ~75% success rate if True
    __f_exit_if_minor_errors: bool = True

    # ----Private fields----
    __f_path: str
    __f_file_name: str
    __f_head: str
    __f_body: List[List[str]]
    __f_case_number: str
    __f_judge_name: str
    __f_defendant_name: str


    __f_corpora: List[str]
    # __f_text_tfidf: TF-IDF

    __f_sentencing_document: bool
    __f_stop_words_removed: bool
    __f_stemmed: bool
    __f_lemmatized: bool
    __f_contains_errors: bool

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

            self.__f_corpora = []
            self.__f_text_tfidf = None

            self.__f_sentencing_document = False
            self.__f_stop_words_removed = False
            self.__f_stemmed = False
            self.__f_lemmatized = False
            self.__f_contains_errors = False

    # ----Instance methods----

    # Initialise
    def initialise(self, a_path: str, load_state: bool):
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
            if not self.initialise_load_state(l_file_content):
                return False

        # Generate state from an unformatted file
        else:
            if not self.initialise_generate_state(l_file_content):
                return False

        # Note successful initialisation
        LegalDoc.__s_successful_init_count += 1

        # Add current LegalDoc to static dictionary of LegalDocs
        LegalDoc.__s_legal_doc_dict[self.file_name] = self

        # Create judge and add it to static dictionary of judges
        Judge(self)

        return True

    # Load state from formatted file
    def initialise_load_state(self, a_file_content):
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
                    if l_line == "SENTENCING DOCUMENT:":
                        self.__f_sentencing_document = ast.literal_eval(l_lines[i + 1].strip())
                        i += 2
                        continue

                    # Stop words removed
                    if l_line == "STOP WORDS REMOVED:":
                        self.__f_sentencing_document = ast.literal_eval(l_lines[i + 1].strip())
                        i += 2
                        continue

                    # Stemmed
                    if l_line == "STEMMED:":
                        self.__f_sentencing_document = ast.literal_eval(l_lines[i + 1].strip())
                        i += 2
                        continue

                    # Stemmed
                    if l_line == "LEMMATIZED:":
                        self.__f_sentencing_document = ast.literal_eval(l_lines[i + 1].strip())
                        i += 2
                        continue

                    # Contains errors
                    if l_line == "CONTAINS ERRORS:":
                        self.__f_sentencing_document = ast.literal_eval(l_lines[i + 1].strip())
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
                    self.__f_corpora += word_tokenize(l_sentence)

            return True
        except IndexError:
            LegalDoc.__note_exception(self.path,
                                      "MAJOR ERROR: Failed to import formatted file, index out of bounds", True)
            return False

    # Generate state from unformatted file
    def initialise_generate_state(self, a_file_content):
        try:
            # Break up document into base components
            l_document_match = LegalDoc.__DOCUMENT_PATTERN.match(a_file_content)
            if l_document_match:
                l_document_groups = l_document_match.groups()

            # Handle document parsing error
            else:
                LegalDoc.__note_exception(self.path, "MAJOR ERROR: Regex cannot parse document", True)
                return False

            # Extract head
            self.__f_head = l_document_groups[0]

            # Extract sentencing identifier
            l_sentencing_identifier_match = LegalDoc.__SENTENCING_IDENTIFIER_PATTERN.match(self.__f_head)
            if l_sentencing_identifier_match:
                self.__f_sentencing_document = True

            # Handle non sentencing document
            else:
                LegalDoc.__note_exception(self.path, "MAJOR ERROR: This is not a sentencing document", True)
                return False

            # Extract case number
            l_case_num_match = LegalDoc.__CASE_NUMBER_PATTERN.match(self.__f_head)
            if l_case_num_match:
                # Extract case number whilst removing dashes, spaces and tabs
                self.__f_case_number = (l_case_num_match.groups())[0].translate({ord(c): None for c in r'-    '})

            # Generate case number randomly using the path as a seed
            else:
                self.__f_contains_errors = True
                l_seed = 0
                for l_char in self.path:
                    l_seed += ord(l_char)
                random.seed(l_seed)
                self.__f_case_number = str(random.randint(1, 9999999))

                # Handle failure to find a case number
                LegalDoc.__note_exception(
                    self.path, "ERROR: Unable to find case number", LegalDoc.__f_exit_if_minor_errors)

                if LegalDoc.__f_exit_if_minor_errors:
                    return False

            # Extract defendant's name
            l_defendant_name_match = LegalDoc.__DEFENDANT_NAME_PATTERN.match(self.__f_head)
            if l_defendant_name_match:
                self.__f_defendant_name = (l_defendant_name_match.groups())[0].strip().upper()

            # Handle inability to determine defendant's name
            else:
                LegalDoc.__note_exception(self.path, "MAJOR ERROR: Unable to find defendant's name", True)
                return False

            # Extract judge's name
            l_judge_name_match = LegalDoc.__JUDGE_NAME_PATTERN.match(self.__f_head)
            if l_judge_name_match:
                self.__f_judge_name = (l_judge_name_match.groups())[0].strip().upper()

            # Handle inability to determine judge's name
            else:
                LegalDoc.__note_exception(self.path, "MAJOR ERROR: Unable to find judge's name", True)
                return False

            # Extract body
            l_lines = l_document_groups[1].splitlines()  # Body broken down by line
            l_sections = []

            # Break up body into sections
            try:
                l_section_index = 0  # Used to check whether sections are being missed
                l_sections.append("")  # l_sections[0] catches any lines prior to the first section
                l_bad_sections = False  # True if any problems are encountered whilst parsing sections

                # For each line in l_lines...
                for l_line in l_lines:
                    l_section_match = LegalDoc.__SECTION_PATTERN.match(l_line)

                    # Check if the line contains the start of a section
                    if l_section_match:

                        # Remove the section number from the line
                        l_line = LegalDoc.__SECTION_PATTERN.sub(r"\g<2>", l_line, 1)

                        # If the section number in the line matches the l_section_index
                        if l_section_match[1] == str(l_section_index + 1):
                            l_section_index += 1
                            l_sections.append(l_line)

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

                        # This line is prior to all sections
                        else:
                            l_bad_sections = True
                            l_sections[l_section_index] += l_line

                # Handle section parsing errors
                if l_bad_sections:
                    self.__f_contains_errors = True
                    LegalDoc.__note_exception(
                        self.path, "ERROR: Bad section(s)", LegalDoc.__f_exit_if_minor_errors)
                    if LegalDoc.__f_exit_if_minor_errors:
                        return False

            # Handle failure to parse document's body
            except (TypeError, AttributeError, IndexError):
                LegalDoc.__note_exception(self.path, "MAJOR ERROR: Unable to break down body", True)
                return False

            # Break up sections into sentences
            tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

            # Add N sentence arrays to body, where N is the number of sections
            for l_section in l_sections:
                self.body.append(tokenizer.tokenize(l_section))

            # Clean Data
            if LegalDoc.CLEAN_DATA:

                # Tokenize sentences
                l_tokenized_sections = []
                for l_section in self.body:
                    l_tokenized_sentences = []
                    for l_sentence in l_section:
                        l_tokenized_sentences.append(word_tokenize(l_sentence))
                    l_tokenized_sections.append(l_tokenized_sentences)
                self.__f_body = l_tokenized_sections

                # Remove stopwords
                if LegalDoc.REMOVE_STOP_WORDS:
                    l_filtered_sections = []
                    for l_section in self.body:
                        l_filtered_sentences = []
                        for l_sentence in l_section:
                            l_filtered_words = []
                            for l_word in l_sentence:
                                if l_word not in LegalDoc.STOP_WORDS:
                                    l_filtered_words.append(l_word)
                            l_filtered_sentences.append(l_filtered_words)
                        l_filtered_sections.append(l_filtered_sentences)
                    self.__f_body = l_filtered_sections
                    self.__f_stop_words_removed = True

                # Stemming
                if LegalDoc.APPLY_STEMMING:
                    l_stemmed_sections = []
                    for l_section in self.body:
                        l_stemmed_sentences = []
                        for l_sentence in l_section:
                            l_stemmed_words = []
                            for l_word in l_sentence:
                                l_stemmed_words.append(LegalDoc.STEMMER.stem(l_word))
                            l_stemmed_sentences.append(l_stemmed_words)
                        l_stemmed_sections.append(l_stemmed_sentences)
                    self.__f_body = l_stemmed_sections
                    self.__f_stemmed = True

                # Lemmatization
                if LegalDoc.APPLY_LEMMATIZATION:
                    l_lemmatized_sections = []
                    for l_section in self.body:
                        l_lemmatized_sentences = []
                        for l_sentence in l_section:
                            l_lemmatized_words = []
                            for l_word in l_sentence:
                                l_lemmatized_words.append(LegalDoc.LEMMATIZER.lemmatize(l_word))
                            l_lemmatized_sentences.append(l_lemmatized_words)
                        l_lemmatized_sections.append(l_lemmatized_sentences)
                    self.__f_body = l_lemmatized_sections
                    self.__f_lemmatized = True

                # Create corpora
                for l_section in self.body:
                    for l_sentence in l_section:
                        for l_word in l_sentence:
                            self.corpora.append(l_word)

                # Create TF-IDF
                # Not sure how i'm supposed to use this...
                self.__f_text_tfidf = LegalDoc.TFIDF_VECTORIZER.fit_transform(self.__f_corpora)
                # print(LegalDoc.TFIDF_VECTORIZER.get_feature_names())
                # print(self.__f_text_tfidf.shape)

                # Detokenize sections
                l_detokenized_sections = []
                for l_section in self.body:
                    l_detokenized_sentences = []
                    for l_sentence in l_section:
                        l_detokenized_sentences.append(LegalDoc.DETOKENIZER.detokenize(l_sentence, return_str=True))
                    l_detokenized_sections.append(l_detokenized_sentences)
                self.__f_body = l_detokenized_sections

            return True

        # Handle miscellaneous errors
        except Exception:
            LegalDoc.__note_exception(self.path, "MAJOR ERROR: Unspecified error occurred", True)
            return False

    # Save formatting as a txt file
    def write(self):

        # Make sure that "CaseName" and  "CaseNumber" do not contain illegal values or are not excessively long
        l_safe_file_name = re.sub(r'[\\/:"*?<>|]+', "", self.file_name)
        l_safe_file_name = (l_safe_file_name[:25] + '..') if len(l_safe_file_name) > 25 else l_safe_file_name
        l_safe_case_number = re.sub(r'[\\/:"*?<>|]+', "", self.case_number)
        l_safe_case_number = (l_safe_case_number[:25] + '..') if len(l_safe_case_number) > 25 else l_safe_case_number

        # Save file
        l_save_file = None
        try:
            l_save_file = open(
                "Resources/Output/Formatted/"
                "(FN-" + l_safe_file_name + ") (CR-" + l_safe_case_number + ").txt",
                "w", encoding="UTF-8")
            l_save_file.write(self.__str__())
            l_save_file.close()

        # Handle IO Exception
        except IOError:
            print("ERROR: Unable to save file with path: " + self.path)
            l_save_file.close()
            return


    # ----Method Overrides----
    # Override str(self) with formatted body output
    def __str__(self):

        # Write field data
        l_info = "FIELD DATA:\n"
        l_info += "\tFILE NAME:\n\t\t" + self.file_name + "\n"
        l_info += "\tCASE NUMBER:\n\t\t" + self.case_number + '\n'
        l_info += "\tJUDGE NAME:\n\t\t" + self.judge_name + '\n'
        l_info += "\tDEFENDANT NAME:\n\t\t" + self.defendant_name + '\n'

        l_info += "\tSENTENCING DOCUMENT:\n\t\t" + str(self.sentencing_document) + '\n'
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
    @classmethod
    def print_exception_data(cls):

        # Write general error data
        l_error_data = "Successful initialisations: " + str(cls.__s_successful_init_count) + '\n'
        l_error_data += "Failed initialisations: " + str(cls.__s_failed_init_count) + '\n'
        l_error_data += "Success rate: " + \
                        str((cls.__s_successful_init_count * 1.0) /
                            ((cls.__s_failed_init_count * 1.0) + (cls.__s_successful_init_count * 1.0))) + '\n'
        l_error_data += "Exceptions: " + '\n'

        # For each LegalDoc containing one or more errors
        # l_path is the key, l_errors is the value
        for l_path, l_errors in cls.__s_exception_data_dict.items():

            # Write the path of the LegalDoc
            l_error_data += "\t" + l_path + '\n'

            # Write the errors associated with the above LegalDoc
            for l_error in l_errors:
                l_error_data += "\t\t" + l_error + '\n'

        print(l_error_data)

    @classmethod
    def __note_exception(cls, a_path: str, a_exception: str, a_failed_init: bool):

        # If the path already exists in the exception dictionary
        if a_path in cls.__s_exception_data_dict:
            cls.__s_exception_data_dict[a_path].append(a_exception)

        # Add the path to the exception dictionary
        else:
            cls.__s_exception_data_dict[a_path] = [a_exception]

        if a_failed_init:
            # Increment static counter for failed initialisation
            cls.__s_failed_init_count += 1

    # ----Static Methods----
    # Static method (don't access instance or class)
    @staticmethod
    def a_static_method(a_number: int):
        return 2 * a_number

    # ----Properties (Read only getters)----
    # Origin path
    @property
    def path(self):
        return self.__f_path

    # File name
    @property
    def file_name(self):
        return self.__f_file_name

    # Head
    @property
    def head(self):
        return self.__f_head

    # Body
    @property
    def body(self):
        return self.__f_body

    # Case number
    @property
    def case_number(self):
        return self.__f_case_number

    # Judge's name
    @property
    def judge_name(self):
        return self.__f_judge_name

    # Defendant name
    @property
    def defendant_name(self):
        return self.__f_defendant_name

    # Sentencing document
    @property
    def sentencing_document(self):
        return self.__f_sentencing_document

    # Stop words removed
    @property
    def stop_words_removed(self):
        return self.__f_stop_words_removed

    # Stemmed
    @property
    def stemmed(self):
        return self.__f_stemmed

    # Lemmatized
    @property
    def lemmatized(self):
        return self.__f_lemmatized

    # Contains errors
    @property
    def contains_errors(self):
        return self.__f_contains_errors

    # Corpora
    @property
    def corpora(self):
        return self.__f_corpora

    # Text TF-IDF
    @property
    def text_tfidf(self):
        return self.__f_text_tfidf
