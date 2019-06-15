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

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')


class LegalDoc:

    # ----Constant Static fields----
    # Patterns
    __SENTENCING_IDENTIFIER_PATTERN = re.compile(r".+(DATE OF SENTENCE:)", re.S | re.M)
    __EMPTY_LINE_PATTERN = re.compile(r"^[\s\t\n\r]*$")
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
    __s_exception_data: dict = dict()

    # ~95% success rate if False but ~20% of LegalDocs will have
    # a generated case number and/or the sections will lack structure.
    # Otherwise, ~75% success rate if True
    __f_exit_if_minor_errors: bool = True

    # ----Private fields----
    __f_path: str
    __f_file_name: str
    __f_head: str
    __f_body: List[List[str]]
    __f_judge_name: str
    __f_defendant_name: str
    __f_case_number: str
    __f_sentencing_document: bool
    __f_failed_init: bool
    __f_corpora: List[str]

    # __f_text_tfidf: TF-IDF

    # ----Constructor----
    def __init__(self, a_path: str):
        try:
            # Initialise fields
            self.__f_path = a_path
            self.__f_file_name = "NULL"
            self.__f_head = "NULL"
            self.__f_body = []
            self.__f_judge_name = "NULL"
            self.__f_defendant_name = "NULL"
            self.__f_case_name = "NULL"
            self.__f_case_number = "NULL"
            self.__f_sentencing_document = False
            self.__f_failed_init = True
            self.__f_corpora = []
            self.__f_text_tfidf = None

            # Get file name
            head, tail = ntpath.split(a_path)
            self.__f_file_name = (tail or ntpath.basename(head)).replace('.txt', '')

            # Read in file
            l_file = None
            try:
                l_file = open(a_path)
                l_content = l_file.read()
                l_file.close()

            # Handle file error
            except IOError:
                LegalDoc.__note_exception(a_path, "MAJOR ERROR: Unable to read file", True)
                l_file.close()
                return

            # Break up document into base components
            l_document_match = LegalDoc.__DOCUMENT_PATTERN.match(l_content)
            if l_document_match:
                l_document_groups = l_document_match.groups()

            # Handle document parsing error
            else:
                LegalDoc.__note_exception(a_path, "MAJOR ERROR: Regex cannot parse document", True)
                return

            # Extract head
            self.__f_head = l_document_groups[0]

            # Extract sentencing identifier
            l_sentencing_identifier_match = LegalDoc.__SENTENCING_IDENTIFIER_PATTERN.match(self.__f_head)
            if l_sentencing_identifier_match:
                __f_sentencing_document = True

            # Handle non sentencing document
            else:
                LegalDoc.__note_exception(a_path, "MAJOR ERROR: This is not a sentencing document", True)
                return

            # Extract case number
            l_case_num_match = LegalDoc.__CASE_NUMBER_PATTERN.match(self.__f_head)
            if l_case_num_match:
                # Extract case number whilst removing dashes, spaces and tabs
                self.__f_case_number = (l_case_num_match.groups())[0].translate({ord(c): None for c in r'-    '})

            # Generate case number randomly using the path as a seed
            else:
                l_seed = 0
                for l_char in a_path:
                    l_seed += ord(l_char)
                random.seed(l_seed)
                self.__f_case_number = str(random.randint(1, 9999999))

                # Handle failure to find a case number
                LegalDoc.__note_exception(
                    a_path, "ERROR: Unable to find case number", LegalDoc.__f_exit_if_minor_errors)
                if LegalDoc.__f_exit_if_minor_errors:
                    return

            # Extract defendant's name
            l_defendant_name_match = LegalDoc.__DEFENDANT_NAME_PATTERN.match(self.__f_head)
            if l_defendant_name_match:
                self.__f_defendant_name = (l_defendant_name_match.groups())[0].strip().upper()

            # Handle inability to determine defendant's name
            else:
                LegalDoc.__note_exception(a_path, "MAJOR ERROR: Unable to find defendant's name", True)
                return

            # Extract judge's name
            l_judge_name_match = LegalDoc.__JUDGE_NAME_PATTERN.match(self.__f_head)
            if l_judge_name_match:
                self.__f_judge_name = (l_judge_name_match.groups())[0].strip().upper()

            # Handle inability to determine judge's name
            else:
                LegalDoc.__note_exception(a_path, "MAJOR ERROR: Unable to find judge's name", True)
                return

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
                    LegalDoc.__note_exception(
                        a_path, "ERROR: Bad section(s)", LegalDoc.__f_exit_if_minor_errors)
                    if LegalDoc.__f_exit_if_minor_errors:
                        return

            # Handle failure to parse document's body
            except (TypeError, AttributeError, IndexError):
                LegalDoc.__note_exception(a_path, "MAJOR ERROR: Unable to break down body", True)
                return

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

            # Note successful initialisation
            LegalDoc.__s_successful_init_count += 1
            self.__f_failed_init = False

            # Create judge
            Judge(self)

        # Handle miscellaneous errors
        except Exception:
            LegalDoc.__note_exception(a_path, "MAJOR ERROR: Unspecified error occurred", True)
            raise

    # ----Method Overrides----
    # Override str(self) with formatted body output
    def __str__(self):

        # Write field data
        l_info = "FILE NAME:\n\t" + self.__f_file_name + ".txt\n"
        l_info += "CASE NUMBER:\n\t" + self.__f_case_number + '\n'
        l_info += "JUDGE NAME:\n\t" + self.__f_judge_name + '\n'
        l_info += "DEFENDANT NAME:\n\t" + self.__f_defendant_name + '\n'
        l_info += "SECTIONS:" + '\n'

        # Write the section headers
        for i in range(0, len(self.body)):
            l_section = self.body[i]
            l_info += '\t' "Section:" + str(i) + '\n'

            # Write the sentences corresponding to the above section
            for l_sentence in l_section:
                l_info += "\t\t" + l_sentence + '\n'

        return l_info

    # ----Instance methods----
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

    # ----Class Methods----
    @classmethod
    def get_exception_data(cls):

        # Write general error data
        l_error_data = "Successful initialisations: " + str(cls.__s_successful_init_count) + '\n'
        l_error_data += "Failed initialisations: " + str(cls.__s_failed_init_count) + '\n'
        l_error_data += "Success rate: " + \
                        str((cls.__s_successful_init_count * 1.0) /
                            ((cls.__s_failed_init_count * 1.0) + (cls.__s_successful_init_count * 1.0))) + '\n'
        l_error_data += "Exceptions: " + '\n'

        # For each LegalDoc containing one or more errors
        # l_path is the key, l_errors is the value
        for l_path, l_errors in cls.__s_exception_data.items():

            # Write the path of the LegalDoc
            l_error_data += "\t" + l_path + '\n'

            # Write the errors associated with the above LegalDoc
            for l_error in l_errors:
                l_error_data += "\t\t" + l_error + '\n'

        return l_error_data

    @classmethod
    def __note_exception(cls, a_path: str, a_exception: str, a_failed_init: bool):

        # If the path already exists in the exception dictionary
        if a_path in cls.__s_exception_data:
            cls.__s_exception_data[a_path].append(a_exception)

        # Add the path to the exception dictionary
        else:
            cls.__s_exception_data[a_path] = [a_exception]

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

    # Defendant name
    @property
    def defendant_name(self):
        return self.__f_defendant_name

    # Judge's name
    @property
    def judge_name(self):
        return self.__f_judge_name

    # Case number
    @property
    def case_number(self):
        return self.__f_case_number

    # Failed initialisation
    @property
    def failed_init(self):
        return self.__f_failed_init

    # Sentencing Document
    @property
    def sentencing_document(self):
        return self.__f_sentencing_document

    # Corpora
    @property
    def corpora(self):
        return self.__f_corpora

    # Text TF-IDF
    @property
    def text_tfidf(self):
        return self.__f_text_tfidf
