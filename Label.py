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

    # Drug trafficking
    CHARGE_2 = re.compile(
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

    # Burglary
    CHARGE_3 = re.compile(
                            r".*" +
                            r"(" +
                            r"(?:catchword[s]?|subject[s]?)" +
                            r".*" +
                            r"burglary" +
                            r")",
                            re.S | re.M | re.I)

    # (Non sexual) Assault
    CHARGE_4 = re.compile(
                            r".*" +
                            r"(" +
                            r"(?:catchword[s]?|subject[s]?)" +
                            r".*" +
                            r"(?<!sexual )assault" +
                            r")",
                            re.S | re.M | re.I)

    # Sex with minor
    CHARGE_5 = re.compile(
                            r".*" +
                            r"(" +
                            r"(?:catchword[s]?|subject[s]?)" +
                            r".*" +
                            r"(?:sexual|indecent act)" +
                            r".*" +
                            r"(?:child|minor)" +
                            r")",
                            re.S | re.M | re.I)

    # Causing injury
    CHARGE_6 = re.compile(
                            r".*" +
                            r"(" +
                            r"(?:catchword[s]?|subject[s]?)" +
                            r".*" +
                            r"(?:cause|causing|caused)" +
                            r".*" +
                            r"(?:injury|injuries)" +
                            r")",
                            re.S | re.M | re.I)

    # Robbery
    CHARGE_7 = re.compile(
                            r".*" +
                            r"(" +
                            r"(?:catchword[s]?|subject[s]?)" +
                            r".*" +
                            r"robbery" +
                            r")",
                            re.S | re.M | re.I)

    # Prohibited person possessing firearm
    CHARGE_8 = re.compile(
                            r".*" +
                            r"(" +
                            r"(?:catchword[s]?|subject[s]?)" +
                            r".*" +
                            r"(?:" +
                            r"possession.*firearm.*prohibited.*person" +
                            r"|" +
                            r"prohibited.*person.*firearm" +
                            r")" +
                            r")",
                            re.S | re.M | re.I)

    # Obtaining X by deception
    CHARGE_9 = re.compile(
                            r".*" +
                            r"(" +
                            r"(?:catchword[s]?|subject[s]?)" +
                            r".*" +
                            r"(?:" +
                            r"obtain.*by\sdeception" +
                            r"|" +
                            r"charge(?:s|d)\s(?:of|with)\sdeception" +
                            r")" +
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
            Charges.TRAFFICKING_DRUG: cls.create_procedure_dict(),
            Charges.BURGLARY: cls.create_procedure_dict(),
            Charges.ASSAULT: cls.create_procedure_dict(),
            Charges.SEXUAL_ASSAULT_OF_MINOR: cls.create_procedure_dict(),
            Charges.CAUSING_INJURY: cls.create_procedure_dict(),
            Charges.ROBBERY: cls.create_procedure_dict(),
            Charges.PROHIBITED_FIREARM: cls.create_procedure_dict(),
            Charges.OBTAIN_BY_DECEPTION: cls.create_procedure_dict()
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
            (LabelType.CHARGES_TYPE, Charges.TRAFFICKING_DRUG, cls.CHARGE_2),
            (LabelType.CHARGES_TYPE, Charges.BURGLARY, cls.CHARGE_3),
            (LabelType.CHARGES_TYPE, Charges.ASSAULT, cls.CHARGE_4),
            (LabelType.CHARGES_TYPE, Charges.SEXUAL_ASSAULT_OF_MINOR, cls.CHARGE_5),
            (LabelType.CHARGES_TYPE, Charges.CAUSING_INJURY, cls.CHARGE_6),
            (LabelType.CHARGES_TYPE, Charges.ROBBERY, cls.CHARGE_7),
            (LabelType.CHARGES_TYPE, Charges.PROHIBITED_FIREARM, cls.CHARGE_8),
            (LabelType.CHARGES_TYPE, Charges.OBTAIN_BY_DECEPTION, cls.CHARGE_9),

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
        :param str a_context: The context in which the label value was determined
        """

        # TODO - Timer start
        Timers.s_add_label.start()

        # Verify that parameters are the correct types
        assert isinstance(a_file_name, str)
        assert isinstance(a_procedure, Procedure)
        assert isinstance(a_value, str)
        assert isinstance(a_location, str)
        assert isinstance(a_context, str)
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
                              a_file_name, "True", "Head", l_match[1])

    @classmethod
    def print_all(cls):

        """
        Prints all label data in a tree format
        """

        print("LABELS")
        for l_type in cls.s_tree_labels_dict.keys():
            print("\t" + str(l_type))
            for l_sub_type in cls.s_tree_labels_dict[l_type].keys():
                print("\t\t" + str(l_sub_type))
                for l_procedure in cls.s_tree_labels_dict[l_type][l_sub_type].keys():
                    print("\t\t\t" + str(l_procedure))
                    for l_name, l_data in cls.s_tree_labels_dict[l_type][l_sub_type][l_procedure].items():
                        print("\t\t\t\t" + str(l_name) + ": " + str(l_data))

    @classmethod
    def split_and_write(cls, a_type, a_subtype):

        """
        Saves the unformatted body text of labelled files in one of two directories
        E.g. an input of "LabelType.CHARGES_TYPE" and "Charges.THEFT" would save all
        documents with the "Charges.THEFT" label in the target dir and would save all
        other labelled documents in the non target dir. These two directories can then
        be used to train a classifier on the provided sub type
        :param LabelType a_type: The base type of a label
        :param Charges or Aggravating or Mitigating or Sentencing a_subtype: The sub type of a label
        """

        # A dict containing the name of every file that has been saved by this method
        l_saved_files = defaultdict(lambda: False)

        # Save target files in target dir
        for l_name in cls.s_tree_labels_dict[a_type][a_subtype][Procedure.REGEX].keys():

            # Note that this file has been saved
            l_saved_files[l_name] = True

            # Save file in target dir
            LegalDoc.s_legal_doc_dict[l_name].write\
                (True, str(a_subtype), "Resources/Output/Labelled/" + str(a_subtype) + "/")

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
