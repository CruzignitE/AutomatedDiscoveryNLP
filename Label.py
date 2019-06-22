from Timer import *
from LabelEnums import *
import re

class Label:

    # ----Constant Static fields----
    # Charge patterns
    CHARGE_1 = re.compile(
                            r".*" +
                            r"(" +
                            r"(?:catchword[s]?|subject[s]?)" +
                            r".*" +
                            r"theft" +
                            r")",
                            re.S | re.M | re.I)

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

    CHARGE_3 = re.compile(
                            r".*" +
                            r"(" +
                            r"(?:catchword[s]?|subject[s]?)" +
                            r".*" +
                            r"burglary" +
                            r")",
                            re.S | re.M | re.I)

    CHARGE_4 = re.compile(
                            r".*" +
                            r"(" +
                            r"(?:catchword[s]?|subject[s]?)" +
                            r".*" +
                            r"(?<!sexual )assault" +
                            r")",
                            re.S | re.M | re.I)

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

    CHARGE_7 = re.compile(
                            r".*" +
                            r"(" +
                            r"(?:catchword[s]?|subject[s]?)" +
                            r".*" +
                            r"robbery" +
                            r")",
                            re.S | re.M | re.I)

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

    AGGRAVATING_4 = re.compile(
                            r".*" +
                            r"(" +
                            r"(?:catchword[s]?|subject[s]?)" +
                            r".*" +
                            r"general\sdeterrence" +
                            r")",
                            re.S | re.M | re.I)

    AGGRAVATING_5 = re.compile(
                            r".*" +
                            r"(" +
                            r"(?:catchword[s]?|subject[s]?)" +
                            r".*" +
                            r"specific\sdeterrence" +
                            r")",
                            re.S | re.M | re.I)

    AGGRAVATING_6 = re.compile(
                            r".*" +
                            r"(" +
                            r"(?:catchword[s]?|subject[s]?)" +
                            r".*" +
                            r"community\sprotection" +
                            r")",
                            re.S | re.M | re.I)

    # Aggravating factor patterns
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

    MITIGATING_3 = re.compile(
                            r".*" +
                            r"(" +
                            r"(?:catchword[s]?|subject[s]?)" +
                            r".*" +
                            r"(?<!no)(?<!lack of)(?<!lacked)(?<!lacks)\s" +
                            r"remorse" +
                            r")",
                            re.S | re.M | re.I)

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

    SENTENCING_1 = re.compile(
                            r".*" +
                            r"sentence[d]?[:]?[\s]*" +
                            r"(?:to|of|TES[:]?|is)?\s*" +
                            r"(.*?)" +
                            r"imprisonment",
                            re.S | re.M | re.I)

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

    SENTENCING_3 = re.compile(
                            r".*(?:catchword[s]?|subject[s]?|sentence[s]?|6AAA)" +
                            r".*" +
                            r"((?:(?:one|two|three|four|five|six|\d).{50}(?:community\scorrection[s]?\sorder|CCO)" +
                            r"|" +
                            r"(?:community\scorrection[s]?\sorder|CCO).{0,50}(?:year[s]?|month[s]|days)))",
                            re.S | re.M | re.I)

    # ----Static variables----
    s_type_dict = {}

    # ----Class methods----
    @classmethod
    def initialise_class(cls):
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

        l_aggravating_dict = {
            Aggravating.RELEVANT_PRIORS: cls.create_procedure_dict(),
            Aggravating.PLEA_NOT_GUILTY: cls.create_procedure_dict(),
            Aggravating.NO_REMORSE: cls.create_procedure_dict(),
            Aggravating.GENERAL_DETERRENCE: cls.create_procedure_dict(),
            Aggravating.SPECIFIC_DETERRENCE: cls.create_procedure_dict(),
            Aggravating.COMMUNITY_PROTECTION: cls.create_procedure_dict()
        }

        l_mitigating_dict = {
            Mitigating.NO_RELEVANT_PRIORS: cls.create_procedure_dict(),
            Mitigating.PLEA_GUILTY: cls.create_procedure_dict(),
            Mitigating.REMORSE: cls.create_procedure_dict(),
            Mitigating.GAMBLING_ADDICTION: cls.create_procedure_dict()
        }

        cls.s_type_dict = {
            Type.CHARGES_TYPE: l_charge_dict,
            Type.AGGRAVATING_TYPE: l_aggravating_dict,
            Type.MITIGATING_TYPE: l_mitigating_dict,
            Type.SENTENCING_TYPE: cls.create_procedure_dict(),
        }

    @classmethod
    def get_label_by_name(cls, a_type, a_subtype, a_procedure, a_file_name):
        return cls.s_type_dict[a_type][a_subtype][a_procedure][a_file_name]

    @classmethod
    def add_label(cls, a_type, a_subtype, a_procedure, a_file_name, a_value, a_location, a_source):

        # TODO - Timer start
        Timers.s_add_label.start()

        assert isinstance(a_file_name, str)
        assert isinstance(a_procedure, Procedure)
        assert isinstance(a_value, str)
        assert isinstance(a_location, str)
        assert isinstance(a_source, str)

        assert isinstance(a_type, Type)

        if a_type is Type.CHARGES_TYPE:
            assert isinstance(a_subtype, Charges)

        elif a_type is Type.AGGRAVATING_TYPE:
            assert isinstance(a_subtype, Aggravating)

        elif a_type is Type.MITIGATING_TYPE:
            assert isinstance(a_subtype, Mitigating)

        elif a_type is Type.SENTENCING_TYPE:
            assert isinstance(a_subtype, Sentencing)

        else:
            raise Exception(str(a_subtype) + " is not a subtype of " + str(a_type))

        cls.s_type_dict[a_type][a_subtype][a_procedure][a_file_name] = (a_value, a_location, a_source)

        # TODO - Timer stop
        Timers.s_add_label.stop()

    #@classmethod
    #def add_charge_1(cls, a_head):


    # ----Static Methods----
    @staticmethod
    def create_procedure_dict():
        l_procedure_dict = {
            Procedure.MANUAL: dict(),
            Procedure.REGEX: dict(),
            Procedure.CLUSTERING: dict()
        }
        return l_procedure_dict


# ----Main method----
def main():
    # Label.initialise_class()
    Label.add_label(Type.MITIGATING_TYPE, Mitigating.NO_RELEVANT_PRIORS, Procedure.MANUAL,
                    "151.txt", True, "SECTION 1", "No relevant priors")
    # print(Label.get_label_by_name(Type.MITIGATING_TYPE, Mitigating.NO_RELEVANT_PRIORS, Procedure.MANUAL, "test.txt"))

    l_test = "Sentence:TES  9 years 11 months imprisonment"
    l_match = Label.SENTENCING_1.match(l_test)

    # Check for regex match
    if l_match:
        print(l_match[1])



# Define main method
if __name__ == '__main__':
    main()
    print("Done")
