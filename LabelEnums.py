from enum import Enum


class LabelType(Enum):

    """
    Types of labels
    """
    __order__ = 'CHARGES_TYPE' \
                ' MITIGATING_TYPE' \
                ' AGGRAVATING_TYPE' \
                ' SENTENCING_TYPE'

    CHARGES_TYPE = 1
    MITIGATING_TYPE = 2
    AGGRAVATING_TYPE = 3
    SENTENCING_TYPE = 4


class Charges(Enum):

    """
    Possible charges
    """
    __order__ = 'THEFT' \
                ' BURGLARY' \
                ' AGGRAVATED_BURGLARY' \
                ' ATTEMPTED_AGGRAVATED_BURGLARY' \
                ' ATTEMPTED_BURGLARY' \
                ' PROPERTY_DECEPTION' \
                ' FINANCIAL_ADVANTAGE_DECEPTION' \
                ' TRAFFICKING_DRUG_COMMERCIAL' \
                ' TRAFFICKING_DRUG_LARGE_COMMERCIAL' \
                ' TRAFFICKING_DRUG_NON_COMMERCIAL'

     # ----- Crimes Act 1958 -----

    # s 74 – theft (other than a motor vehicle)
    THEFT = 1

    # s 76(1) – burglary
    BURGLARY = 2

    # s 77(1) – aggravated burglary
    AGGRAVATED_BURGLARY = 3

    # s 321M – attempted aggravated burglary
    ATTEMPTED_AGGRAVATED_BURGLARY = 4

    # s 321M – attempted burglary
    ATTEMPTED_BURGLARY = 5

    # s 81(1) – obtaining property by deception
    PROPERTY_DECEPTION = 6

    # s 82(1) – obtaining a financial advantage by deception
    FINANCIAL_ADVANTAGE_DECEPTION = 7

    # ----- Drugs, Poisons And Controlled Substances Act 1981 (Vic) -----

    # s 71AA – trafficking in a commercial quantity of a drug of dependence
    TRAFFICKING_DRUG_COMMERCIAL = 8

    # s 71(1) – trafficking in a large commercial quantity of a drug of dependence
    TRAFFICKING_DRUG_LARGE_COMMERCIAL = 9

    # s 71AC – trafficking in a non-commercial quantity of a drug of dependence
    TRAFFICKING_DRUG_NON_COMMERCIAL = 10



class Aggravating(Enum):

    """
    Possible aggravating factors
    """
    __order__ = 'RELEVANT_PRIORS' \
                ' PLEA_NOT_GUILTY' \
                ' NO_REMORSE' \
                ' GENERAL_DETERRENCE' \
                ' SPECIFIC_DETERRENCE' \
                ' COMMUNITY_PROTECTION'

    RELEVANT_PRIORS = 1
    PLEA_NOT_GUILTY = 2
    NO_REMORSE = 3
    GENERAL_DETERRENCE = 4
    SPECIFIC_DETERRENCE = 5
    COMMUNITY_PROTECTION = 6


class Mitigating(Enum):

    """
    Possible mitigating factors
    """

    __order__ = 'NO_RELEVANT_PRIORS' \
                ' PLEA_GUILTY' \
                ' REMORSE' \
                ' GAMBLING_ADDICTION'

    NO_RELEVANT_PRIORS = 1
    PLEA_GUILTY = 2
    REMORSE = 3
    GAMBLING_ADDICTION = 4


class Sentencing(Enum):

    """
    Possible sentences
    """

    __order__ = 'PRISON' \
                ' PAROLE' \
                ' CCO'

    PRISON = 1
    PAROLE = 2
    CCO = 3


class Procedure(Enum):

    """
    Possible labelling procedures
    """

    __order__ = 'MANUAL' \
                ' REGEX' \
                ' CLUSTERING'

    MANUAL = 1
    REGEX = 2
    CLUSTERING = 3
