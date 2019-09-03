from Timer import *
from LabelEnums import *
from LegalDoc import *


from collections import OrderedDict
from collections import defaultdict
import re


class Label:

    # ----Constant Static fields----
    # Charge patterns

    # Theft
    CHARGE_1 = re.compile(
                            r".*" +
                            r"(" +
                            r"(?:catchword[s]?|subject[s]?)" +
                            r".*" +
                            r"theft" +
                            r")",
                            re.S | re.M | re.I)

    # Burglary
    CHARGE_2 = re.compile(
                            r".*" +
                            r"(" +
                            r"(?:catchword[s]?|subject[s]?)" +
                            r".*" +
                            r"(?<!aggravated\s)(burglary|burglaries)" +
                            r")",
                            re.S | re.M | re.I)

    # Aggravated Burglary
    CHARGE_3 = re.compile(
                            r".*" +
                            r"(" +
                            r"(?:catchword[s]?|subject[s]?)" +
                            r".*" +
                            r"(?<!attempted\s)aggravated\s(burglary|burglaries)" +
                            r")",
                            re.S | re.M | re.I)

    # Attempted Aggravated Burglary
    CHARGE_4 = re.compile(
                            r".*" +
                            r"(" +
                            r"(?:catchword[s]?|subject[s]?)" +
                            r".*" +
                            r"attempted\saggravated\s(burglary|burglaries)" +
                            r")",
                            re.S | re.M | re.I)

    # Attempted Burglary
    CHARGE_5 = re.compile(
                            r".*" +
                            r"(" +
                            r"(?:catchword[s]?|subject[s]?)" +
                            r".*" +
                            r"attempted\s(?<!aggravated\s)(burglary|burglaries)" +
                            r")",
                            re.S | re.M | re.I)

    # Obtain Property by Deception
    CHARGE_6 = re.compile(
                            r".*" +
                            r"(" +
                            r"(?:catchword[s]?|subject[s]?)" +
                            r".*" +
                            r"obtain\sproperty\sby\sdeception" +
                            r")",
                            re.S | re.M | re.I)

    # Obtain Financial Advantage by Deception
    CHARGE_7 = re.compile(
                            r".*" +
                            r"(" +
                            r"(?:catchword[s]?|subject[s]?)" +
                            r".*" +
                            r"financial\sadvantage\sby\sdeception" +
                            r")",
                            re.S | re.M | re.I)

    # Trafficking in commercial quantity of drug
    CHARGE_8 = re.compile(
                            r".*" +
                            r"(" +
                            r"(?:catchword[s]?|subject[s]?)" +
                            r".*" +
                            r"traffick(?:ing)?" +
                            r".*" +
                            r"(?<!large\s)commercial" +
                            r".*" +
                            r"(?:drug|methylamphetamine|cannabis)" +
                            r"(?:of dependence )?" +
                            r"(?:\(.+\))?" +
                            r")",
                            re.S | re.M | re.I)

    # Trafficking in large commercial quantity of drug
    CHARGE_9 = re.compile(
                            r".*" +
                            r"(" +
                            r"(?:catchword[s]?|subject[s]?)" +
                            r".*" +
                            r"traffick(?:ing)?" +
                            r".*" +
                            r"large\scommercial" +
                            r".*" +
                            r"(?:drug|methylamphetamine|cannabis)" +
                            r"(?:of dependence )?" +
                            r"(?:\(.+\))?" +
                            r")",
                            re.S | re.M | re.I)

    # Trafficking in non commercial quantity of drug
    CHARGE_10 = re.compile(
                            r".*" +
                            r"(" +
                            r"(?:catchword[s]?|subject[s]?)" +
                            r".*" +
                            r"traffick(?:ing)?" +
                            r".*" +
                            r"(?:drug|methylamphetamine|cannabis)" +
                            r"(?:of dependence )?" +
                            r"(?:\(.+\))?" +
                            r")",
                            re.S | re.M | re.I)

    # Aggravating factor patterns
    # Priors
    AGGRAVATING_1 = re.compile(
                            r".*" +
                            r"(" +
                            r"(?:catchword[s]?|subject[s]?)" +
                            r".*" +
                            r"(?<!no)\srelevant\s" +
                            r"(?:prior[s]?|criminal|conviction|record|offen(?:ces|ce|ding))" +
                            r"\s?" +
                            r"(?:criminal|conviction|record)?" +
                            r")",
                            re.S | re.M | re.I)

    # Not guilty plea
    AGGRAVATING_2 = re.compile(
                            r".*" +
                            r"(" +
                            r"(?:catchword[s]?|subject[s]?)" +
                            r".*" +
                            r"(?:plea[s]?\sof\s)?" +
                            r"not\sguilty" +
                            r"(?:\splea[s]?)?" +
                            r")",
                            re.S | re.M | re.I)

    # No remorse
    AGGRAVATING_3 = re.compile(
                            r".*" +
                            r"(" +
                            r"(?:catchword[s]?|subject[s]?)" +
                            r".*" +
                            r"(?:no|lack(?:ed|\sof))\s" +
                            r"(?:sign[s]?\sof)?" +
                            r"\s?remorse" +
                            r")",
                            re.S | re.M | re.I)

    # General deterrence
    AGGRAVATING_4 = re.compile(
                            r".*" +
                            r"(" +
                            r"(?:catchword[s]?|subject[s]?)" +
                            r".*" +
                            r"general\sdeterrence" +
                            r")",
                            re.S | re.M | re.I)

    # Specific deterrence
    AGGRAVATING_5 = re.compile(
                            r".*" +
                            r"(" +
                            r"(?:catchword[s]?|subject[s]?)" +
                            r".*" +
                            r"specific\sdeterrence" +
                            r")",
                            re.S | re.M | re.I)

    # Community protection
    AGGRAVATING_6 = re.compile(
                            r".*" +
                            r"(" +
                            r"(?:catchword[s]?|subject[s]?)" +
                            r".*" +
                            r"community\sprotection" +
                            r")",
                            re.S | re.M | re.I)

    # Mitigating factor patterns
    # No priors
    MITIGATING_1 = re.compile(
                            r".*" +
                            r"(" +
                            r"(?:catchword[s]?|subject[s]?)" +
                            r".*" +
                            r"no\srelevant\s" +
                            r"(?:prior[s]?|criminal|conviction|record|offen(?:ces|ce|ding))" +
                            r"\s?" +
                            r"(?:criminal|conviction|record)?" +
                            r")",
                            re.S | re.M | re.I)

    # Guilty plea
    MITIGATING_2 = re.compile(
                            r".*" +
                            r"(" +
                            r"(?:catchword[s]?|subject[s]?)" +
                            r".*" +
                            r"(?:plea[s]?\sof\s)?" +
                            r"guilty" +
                            r"(?:\splea[s]?)?" +
                            r")",
                            re.S | re.M | re.I)

    # Remorse
    MITIGATING_3 = re.compile(
                            r".*" +
                            r"(" +
                            r"(?:catchword[s]?|subject[s]?)" +
                            r".*" +
                            r"(?<!no)(?<!lack of)(?<!lacked)(?<!lacks)\s" +
                            r"remorse" +
                            r")",
                            re.S | re.M | re.I)

    # Gambling addiction
    MITIGATING_4 = re.compile(
                            r".*" +
                            r"(" +
                            r"(?:catchword[s]?|subject[s]?)" +
                            r".*" +
                            r"(?:" +
                            r"addicted\sto\sgambling" +
                            r"|" +
                            r"gambling\saddiction" +
                            r")" +
                            r")",
                            re.S | re.M | re.I)

    # Sentencing patterns
    # Prison sentence
    SENTENCING_1 = re.compile(
                            r".*" +
                            r"sentence[d]?[:]?[\s]*" +
                            r"(?:to|of|TES[:]?|is)?\s*" +
                            r"(.*?)" +
                            r"imprisonment",
                            re.S | re.M | re.I)

    # Parole
    SENTENCING_2 = re.compile(
                            r".*(?:catchword[s]?|subject[s]?|sentence[s]?|6AAA).*" +
                            r"(" +
                            r"(?:minimum.+parole(?:.+(?:year[s]?|month[s]days))?)" +
                            r"|" +
                            r"(?:non[\s\-]*parole.+(?:year[s]?|month[s]|days))" +
                            r"|" +
                            r"(?:\d\syear[s]?.+?non[\s\-]*parole\speriod)" +
                            r")",
                            re.S | re.M | re.I)

    # CCO
    SENTENCING_3 = re.compile(
                            r".*(?:catchword[s]?|subject[s]?|sentence[s]?|6AAA)" +
                            r".*" +
                            r"((?:(?:one|two|three|four|five|six|\d).{50}(?:community\scorrection[s]?\sorder|CCO)" +
                            r"|" +
                            r"(?:community\scorrection[s]?\sorder|CCO).{0,50}(?:year[s]?|month[s]|days)))",
                            re.S | re.M | re.I)

    # ----Static variables----

    # A dictionary containing all labels in a tree format
    # Useful for iterating over every label of every file
    # i.e. type: subtype: procedure: file_name: (value, location, context)
    s_tree_labels_dict = OrderedDict()

    # A dictionary containing all labels in a flat format
    # Useful for iterating over every label associated with a given file
    # i.e. file_name: ((type, subtype, procedure)(value, location, context))
    s_flat_labels_dict = defaultdict(lambda: [])

    # List containing all label patterns and their associated types
    s_patterns_list = []

    # ----Class methods----
    @classmethod
    def initialise_class(cls):

        """
        Initialises all static label dictionaries
        """

        # Dictionary with keys corresponding to types of charges
        l_charge_dict = {
            Charges.THEFT: cls.create_procedure_dict(),
            Charges.BURGLARY: cls.create_procedure_dict(),
            Charges.AGGRAVATED_BURGLARY: cls.create_procedure_dict(),
            Charges.ATTEMPTED_AGGRAVATED_BURGLARY: cls.create_procedure_dict(),
            Charges.ATTEMPTED_BURGLARY: cls.create_procedure_dict(),
            Charges.PROPERTY_DECEPTION: cls.create_procedure_dict(),
            Charges.FINANCIAL_ADVANTAGE_DECEPTION: cls.create_procedure_dict(),
            Charges.TRAFFICKING_DRUG_COMMERCIAL: cls.create_procedure_dict(),
            Charges.TRAFFICKING_DRUG_LARGE_COMMERCIAL: cls.create_procedure_dict(),
            Charges.TRAFFICKING_DRUG_NON_COMMERCIAL: cls.create_procedure_dict()
        }

        # Dictionary with keys corresponding to types of aggravating factors
        l_aggravating_dict = {
            Aggravating.RELEVANT_PRIORS: cls.create_procedure_dict(),
            Aggravating.PLEA_NOT_GUILTY: cls.create_procedure_dict(),
            Aggravating.NO_REMORSE: cls.create_procedure_dict(),
            Aggravating.GENERAL_DETERRENCE: cls.create_procedure_dict(),
            Aggravating.SPECIFIC_DETERRENCE: cls.create_procedure_dict(),
            Aggravating.COMMUNITY_PROTECTION: cls.create_procedure_dict()
        }

        # Dictionary with keys corresponding to types of mitigating factors
        l_mitigating_dict = {
            Mitigating.NO_RELEVANT_PRIORS: cls.create_procedure_dict(),
            Mitigating.PLEA_GUILTY: cls.create_procedure_dict(),
            Mitigating.REMORSE: cls.create_procedure_dict(),
            Mitigating.GAMBLING_ADDICTION: cls.create_procedure_dict()
        }

        # Dictionary with keys corresponding to types of sentences
        l_sentencing_dict = {
            Sentencing.PRISON: cls.create_procedure_dict(),
            Sentencing.PAROLE: cls.create_procedure_dict(),
            Sentencing.CCO: cls.create_procedure_dict(),

        }

        # Dictionary with keys corresponding to base label types
        cls.s_tree_labels_dict = {
            LabelType.CHARGES_TYPE: l_charge_dict,
            LabelType.AGGRAVATING_TYPE: l_aggravating_dict,
            LabelType.MITIGATING_TYPE: l_mitigating_dict,
            LabelType.SENTENCING_TYPE: l_sentencing_dict,
        }

        # List containing all label patterns and their associated types
        cls.s_patterns_list = [
            (LabelType.CHARGES_TYPE, Charges.THEFT, cls.CHARGE_1),
            (LabelType.CHARGES_TYPE, Charges.BURGLARY, cls.CHARGE_2),
            (LabelType.CHARGES_TYPE, Charges.AGGRAVATED_BURGLARY, cls.CHARGE_3),
            (LabelType.CHARGES_TYPE, Charges.ATTEMPTED_AGGRAVATED_BURGLARY, cls.CHARGE_4),
            (LabelType.CHARGES_TYPE, Charges.ATTEMPTED_BURGLARY, cls.CHARGE_5),
            (LabelType.CHARGES_TYPE, Charges.PROPERTY_DECEPTION, cls.CHARGE_6),
            (LabelType.CHARGES_TYPE, Charges.FINANCIAL_ADVANTAGE_DECEPTION, cls.CHARGE_7),
            (LabelType.CHARGES_TYPE, Charges.TRAFFICKING_DRUG_COMMERCIAL, cls.CHARGE_8),
            (LabelType.CHARGES_TYPE, Charges.TRAFFICKING_DRUG_LARGE_COMMERCIAL, cls.CHARGE_9),
            (LabelType.CHARGES_TYPE, Charges.TRAFFICKING_DRUG_NON_COMMERCIAL, cls.CHARGE_10),

            (LabelType.AGGRAVATING_TYPE, Aggravating.RELEVANT_PRIORS, cls.AGGRAVATING_1),
            (LabelType.AGGRAVATING_TYPE, Aggravating.PLEA_NOT_GUILTY, cls.AGGRAVATING_2),
            (LabelType.AGGRAVATING_TYPE, Aggravating.NO_REMORSE, cls.AGGRAVATING_3),
            (LabelType.AGGRAVATING_TYPE, Aggravating.GENERAL_DETERRENCE, cls.AGGRAVATING_4),
            (LabelType.AGGRAVATING_TYPE, Aggravating.SPECIFIC_DETERRENCE, cls.AGGRAVATING_5),
            (LabelType.AGGRAVATING_TYPE, Aggravating.COMMUNITY_PROTECTION, cls.AGGRAVATING_6),

            (LabelType.MITIGATING_TYPE, Mitigating.NO_RELEVANT_PRIORS, cls.MITIGATING_1),
            (LabelType.MITIGATING_TYPE, Mitigating.PLEA_GUILTY, cls.MITIGATING_2),
            (LabelType.MITIGATING_TYPE, Mitigating.REMORSE, cls.MITIGATING_3),
            (LabelType.MITIGATING_TYPE, Mitigating.GAMBLING_ADDICTION, cls.MITIGATING_4),

            (LabelType.SENTENCING_TYPE, Sentencing.PRISON, cls.SENTENCING_1),
            (LabelType.SENTENCING_TYPE, Sentencing.PAROLE, cls.SENTENCING_2),
            (LabelType.SENTENCING_TYPE, Sentencing.CCO, cls.SENTENCING_3)
        ]

    @classmethod
    def get_label(cls, a_type, a_subtype, a_procedure, a_file_name):

        """
        Label getter
        :param LabelType a_type: The base type of a label
        :param Charges or Aggravating or Mitigating or Sentencing a_subtype: The sub type of a label
        :param Procedure a_procedure: How the label was determined
        :param str a_file_name: The source file's name
        :return: The label data (a_value, a_location, a_context)
        :rtype: (str, str, str)
        """
        return cls.s_tree_labels_dict[a_type][a_subtype][a_procedure][a_file_name]

#----------------------------------------------------------------------

    @classmethod
    def add_label(cls, a_type, a_subtype, a_procedure, a_file_name, a_value, a_location, a_context):

        """
        Adds a label to the static label dictionary
        :param LabelType a_type: The base type of a label
        :param Charges or Aggravating or Mitigating or Sentencing a_subtype: The subtype of a label
        :param Procedure a_procedure: How the label was determined
        :param str a_file_name: The source file's name
        :param str a_value: The value of a label (usually "True" or "False")
        :param str a_location: The part of the document that contained the label ("Head" or "Body" or "Section #")
        :param str or list a_context: The context in which the label value was determined
        """

        # TODO - Timer start
        Timers.s_add_label.start()

        # Verify that parameters are the correct types
        assert isinstance(a_file_name, str)
        assert isinstance(a_procedure, Procedure)
        assert isinstance(a_value, str)
        assert isinstance(a_location, str)
        assert (isinstance(a_context, str)) or (isinstance(a_context, list))
        assert isinstance(a_type, LabelType)

        if a_type is LabelType.CHARGES_TYPE:
            assert isinstance(a_subtype, Charges)

        elif a_type is LabelType.AGGRAVATING_TYPE:
            assert isinstance(a_subtype, Aggravating)

        elif a_type is LabelType.MITIGATING_TYPE:
            assert isinstance(a_subtype, Mitigating)

        elif a_type is LabelType.SENTENCING_TYPE:
            assert isinstance(a_subtype, Sentencing)

        else:
            raise Exception(str(a_subtype) + " is not a subtype of " + str(a_type))

        # Create label data tuple
        l_label_data = (a_value, a_location, a_context)

        # Create a new entry in the static tree labels dictionary
        cls.s_tree_labels_dict[a_type][a_subtype][a_procedure][a_file_name] = l_label_data

        # Create a new entry in the static flat labels dictionary
        cls.s_flat_labels_dict[a_file_name].append(((a_type, a_subtype, a_procedure), l_label_data))

        # TODO - Timer stop
        Timers.s_add_label.stop()

#----------------------------------------------------------------------


    @classmethod
    def auto_regex_label_all_files(cls):

        """
        Labels every LegalDoc using regex
        """

        for l_legal_doc in LegalDoc.s_legal_doc_dict.values():
            Label.auto_regex_label(l_legal_doc.head, l_legal_doc.file_name)

    @classmethod
    def auto_regex_label(cls, a_head, a_file_name):

        """
        Labels a LegalDoc using regex
        :param str a_head: The source file's head
        :param str a_file_name: The source file's name
        """

        # For every label regex
        for l_pattern in cls.s_patterns_list:

            # Check for regex match
            l_match = l_pattern[2].match(a_head)

            # Add a label if the regex matches
            if l_match:
                cls.add_label(l_pattern[0], l_pattern[1], Procedure.REGEX,
                              a_file_name, "True", "Head", [l_match[1]])

    @classmethod
    def __print_type(cls, l_type, l_subtype):

        """
        Service method for "print_type_tree" and "print_all_tree"
        """

        for l_procedure in cls.s_tree_labels_dict[l_type][l_subtype].keys():
            print("\t\t\t" + str(l_procedure))
            for l_name, l_data in cls.s_tree_labels_dict[l_type][l_subtype][l_procedure].items():
                print("\t\t\t\t" + str(l_name) + ": " + str(l_data))

    @classmethod
    def print_type_tree(cls, l_type, l_subtype):

        """
        Prints all label data related to the provided subtype in a tree format
        """

        print("LABELS (Only " + str(l_subtype) + ")")
        print("\t" + str(l_type))
        print("\t\t" + str(l_subtype))
        cls.__print_type(l_type, l_subtype)

    @classmethod
    def print_all_tree(cls):

        """
        Prints all label data in a tree format
        """

        print("LABELS (All)")
        for l_type in cls.s_tree_labels_dict.keys():
            print("\t" + str(l_type))
            for l_subtype in cls.s_tree_labels_dict[l_type].keys():
                cls.__print_type(l_type, l_subtype)

     # TODO FIX LATER
    @classmethod
    def write_labels(cls, a_type, a_subtype):

        l_bool_map = {
            "False": False,
            "True": True,
        }


        # A dict containing the name of every file that has been saved by this method
        l_saved_files = defaultdict(lambda: False)

        for l_procedure in cls.s_tree_labels_dict[a_type][a_subtype].keys():

            # Save target files in target dir
            for l_name, l_value in cls.s_tree_labels_dict[a_type][a_subtype][l_procedure].items():

                # def write_raw_v2(cls, a_subtype, a_value, a_subtype_only, a_procedure, a_file_name):
                # (Tr)(-)(Ma)(Ra)(-) FileName.txt
                # (Tr)(-)(Re)(Ra)(-) FileName.txt
                # (Fa)(Su)(Ma)(Ra)(-) FileName.txt


                cls.write_raw_v2(a_subtype, l_value[0], str(True), l_procedure, l_name)

                #def write_context_v2(cls, a_subtype, a_value, a_subtype_only, a_procedure,  a_context_list, a_file_name):
                # (Tr)(-)(Ma)(Co)(Si) FileName.txt
                # (Tr)(-)(Ma)(Co)(Li) FileName.txt
                # (Tr)(-)(Re)(Co)(Si) FileName.txt
                # (Tr)(-)(Re)(Co)(Li) FileName.txt
                # (Fa)(Su)(Ma)(Co)(Si) FileName.txt
                # (Fa)(Su)(Ma)(Co)(Li) FileName.txt
                cls.write_context_v2(a_subtype, l_value[0], str(True), l_procedure, l_value[2], l_name)

                # Note that this file has been saved
                l_saved_files[l_name] = l_bool_map[l_value[0]]


        print("157.txt")
        print(l_saved_files["157.txt"])
        # Save non target files in non target dir
        for l_legal_doc in LegalDoc.s_legal_doc_dict.values():

            # If this file wasn't already saved
            if not l_saved_files[l_legal_doc.file_name]:

                # def write_raw_v2(cls, a_subtype, a_value, a_subtype_only, a_procedure, a_file_name):
                # (Fa)(Al)(-)(Ra)(-) FileName.txt

                cls.write_raw_v2(a_subtype, str(False), str(False), None, l_legal_doc.file_name)


    # TODO FIX LATER
    @classmethod
    def write_raw_v2(cls, a_subtype, a_value, a_subtype_only, a_procedure, a_file_name):


        l_value_map = {
            "False": "(Fa)",
            "True": "(Tr)",
            None: "(-)"
        }

        l_subtype_only_map = {
            "False": "(Al)",
            "True": "(Su)",
            None: "(-)"
        }

        l_procedure_map = {
            Procedure.MANUAL: "(Ma)",
            Procedure.REGEX: "(Re)",
            Procedure.CLUSTERING: "(Cl)",
            None: "(-)"
        }

        l_raw_only_map = {
            True: "(Ra)",
            False: "(Co)",
            None: "(-)"
        }

        l_single_only_map = {
            True: "(Si)",
            False: "(Li)",
            None: "(-)"
        }

        # Add brackets to prefix if specified
        l_prefixes = l_value_map[a_value] + l_subtype_only_map[a_subtype_only] \
            + l_procedure_map[a_procedure] + l_raw_only_map[True]

        l_path = "Resources/" \
                 "Output/" \
                 "Labelled/" \
                 + str(a_subtype) + "/" \
                 + l_value_map[a_value] + "/" \
                 + l_subtype_only_map[a_subtype_only] + "/" \
                 + l_procedure_map[a_procedure] + "/" \
                 + l_raw_only_map[True] + "/"

        if not os.path.exists(l_path):
            os.makedirs(l_path)

        try:
            l_file = open(
                l_path + "/" + l_prefixes + a_file_name, "w",
                encoding="UTF-8")

            l_legal_doc = LegalDoc.s_legal_doc_dict[a_file_name]
            l_legal_doc.strip_section_identifiers(False)

            # Only write body's contents (unformatted)
            for l_section in l_legal_doc.body:
                for l_sentence in l_section:
                    l_file.write(l_sentence + " \n")

            l_file.close()

        # Handle IO Exception
        except IOError:
            print("ERROR: Unable to save file with path: " + l_file + "..." + a_file_name)
            l_file.close()





    @classmethod
    def write_context_v2(cls, a_subtype, a_value, a_subtype_only, a_procedure,  a_context_list, a_file_name):

        l_value_map = {
            "False": "(Fa)",
            "True": "(Tr)",
            None: "(-)"
        }

        l_subtype_only_map = {
            "False": "(Al)",
            "True": "(Su)",
            None: "(-)"
        }

        l_procedure_map = {
            Procedure.MANUAL: "(Ma)",
            Procedure.REGEX: "(Re)",
            Procedure.CLUSTERING: "(Cl)",
            None: "(-)"
        }

        l_raw_only_map = {
            True: "(Ra)",
            False: "(Co)",
            None: "(-)"
        }

        l_single_only_map = {
            True: "(Si)",
            False: "(Li)",
            None: "(-)"
        }


        # Add brackets to prefix if specified
        l_prefixes = l_value_map[a_value] + l_subtype_only_map[a_subtype_only] \
                     + l_procedure_map[a_procedure] + l_raw_only_map[False]



        l_path = "Resources/" \
                 "Output/" \
                 "Labelled/"\
                 + str(a_subtype) + "/"\
                 + l_value_map[a_value] + "/"\
                 + l_subtype_only_map[a_subtype_only] + "/"\
                 + l_procedure_map[a_procedure] + "/" \
                 + l_raw_only_map[False] + "/"

        l_single_path = l_path + l_single_only_map[True] + "/"
        l_list_path = l_path + l_single_only_map[False] + "/"

        if not os.path.exists(l_single_path):
            os.makedirs(l_single_path)

        if not os.path.exists(l_list_path):
            os.makedirs(l_list_path)

        try:
            l_list_file = open(
                l_list_path + "/" + l_prefixes + " " + a_file_name, "w", encoding="UTF-8")

            for l_index in range(0, len(a_context_list)):

                try:
                    l_single_file = open(
                        l_single_path + "/"  + l_prefixes +  "(" + str(l_index) + ") " + a_file_name, "w", encoding="UTF-8")

                    # Write context as a file
                    l_single_file.write(a_context_list[l_index])
                    l_list_file.write(a_context_list[l_index] + "\n")
                    l_single_file.close()

                # Handle IO Exception
                except IOError:
                    print("ERROR: Unable to save file with path: " + l_single_path + "..." + a_file_name)
                    l_single_file.close()

            l_list_file.close()

        # Handle IO Exception
        except IOError:
            print("ERROR: Unable to save file with path: " + l_list_path + "..." + a_file_name)
            l_list_file.close()


    @classmethod
    def split_and_write(cls, a_type, a_subtype, a_procedure=None, a_subtype_only=False, a_context_only=False):

        """
        - Saves the unformatted body text of labelled files in one of two directories

        - The first (target) directory only contains files that match the given type and subtype

        - The second (non target) directory matches every other file that doesn't have a label for the given
        type and subtype

        - If a procedure is provided as a parameters then only labels with that procedure type will be
        added to the target dir

        - E.g. an input of "LabelType.CHARGES_TYPE" and "Charges.THEFT" would save all
        documents with the "Charges.THEFT" label in the target dir and would save all
        other labelled documents in the non target dir. These two directories can then
        be used to train a classifier on the provided sub type

        :param LabelType a_type: The base type of a label
        :param Charges or Aggravating or Mitigating or Sentencing a_subtype: The sub type of a label
        :param Procedure a_procedure: The procedure used to filter target docs. None implies all procedures
        will be checked
        :param bool a_subtype_only: Whether the non target dir should contain files that do not related to
        the provided subtype (True == only files related to subtype)
         :param bool a_context_only: Whether the target dir should be made up of raw text or label contexts
        """

        # A dict containing the name of every file that has been saved by this method
        l_saved_files = defaultdict(lambda: False)

        # Add labels for all procedures (priority is manual, regex, clustering)
        if a_procedure is None:

            for l_procedure in cls.s_tree_labels_dict[a_type][a_subtype].keys():

                # Save target files in target dir
                for l_name, l_value in cls.s_tree_labels_dict[a_type][a_subtype][l_procedure].items():

                    # If this file wasn't already saved (i.e. multiple procedures for one subtype)
                    if not l_saved_files[l_name]:

                        # Only add labels that identified what they were looking for
                        if str(l_value[0]) == str(True):

                            # Note that this file has been saved
                            l_saved_files[l_name] = True

                            # Save file in target dir as a series of contexts
                            if a_context_only:
                                cls.write_context(True, a_subtype, l_name, l_value[2])

                            # Save file in target dir as raw text
                            else:
                                LegalDoc.s_legal_doc_dict[l_name].write(
                                    True, str(a_subtype), "Resources/Output/Labelled/" + str(a_subtype) + "/")

        # Only add labels for the procedure type provided
        else:

            # Save target files in target dir
            for l_name, l_value in cls.s_tree_labels_dict[a_type][a_subtype][a_procedure].items():

                # Note that this file has been saved
                l_saved_files[l_name] = True

                # Add true labels to target dir
                if str(l_value[0]) == str(True):

                    # Save file in target dir as a series of contexts
                    if a_context_only:
                        cls.write_context(True, a_subtype, l_name, l_value[2])

                    # Save file in target dir as raw text
                    else:
                        LegalDoc.s_legal_doc_dict[l_name].write(
                            True, str(a_subtype), "Resources/Output/Labelled/" + str(a_subtype) + "/")

                # Add false labels to non target dir
                else:

                    # Save file in target dir as a series of contexts
                    if a_context_only:
                        cls.write_context(False, a_subtype, l_name, l_value[2])

                    # Save file in non target dir
                    else:
                        LegalDoc.s_legal_doc_dict[l_name].write(
                            True, "NOT " + str(a_subtype), "Resources/Output/Labelled/NOT " + str(a_subtype) + "/")

        # Add files that don't relate to the target subtype in the non target dir
        if not a_subtype_only:

            # Save non target files in non target dir
            for l_type in cls.s_tree_labels_dict.keys():
                for l_sub_type in cls.s_tree_labels_dict[l_type].keys():
                    for l_procedure in cls.s_tree_labels_dict[l_type][l_sub_type].keys():
                        for l_name in cls.s_tree_labels_dict[l_type][l_sub_type][l_procedure].keys():

                            # If this file wasn't already saved
                            if not l_saved_files[l_name]:

                                # Note that this file has been saved
                                l_saved_files[l_name] = True

                                # Save file in non target dir
                                LegalDoc.s_legal_doc_dict[l_name].write(
                                    True, "NOT " + str(a_subtype), "Resources/Output/Labelled/NOT " + str(a_subtype) + "/")

    # ----Static Methods----
    @staticmethod
    def create_procedure_dict():

        """
        Creates a dict for labelling procedure
        :rtype: dict
        """

        l_procedure_dict = {
            Procedure.MANUAL: dict(),
            Procedure.REGEX: dict(),
            Procedure.CLUSTERING: dict()
        }
        return l_procedure_dict
