from enum import Enum


class LabelType(Enum):

    """
    Types of labels
    """

    CHARGES_TYPE = 1
    MITIGATING_TYPE = 2
    AGGRAVATING_TYPE = 3
    SENTENCING_TYPE = 4


class Charges(Enum):

    """
    Possible charges
    """

    THEFT = 1
    TRAFFICKING_DRUG = 2
    BURGLARY = 3
    ASSAULT = 4
    SEXUAL_ASSAULT_OF_MINOR = 5
    CAUSING_INJURY = 6
    ROBBERY = 7
    PROHIBITED_FIREARM = 8
    OBTAIN_BY_DECEPTION = 9


class Aggravating(Enum):

    """
    Possible aggravating factors
    """

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

    NO_RELEVANT_PRIORS = 1
    PLEA_GUILTY = 2
    REMORSE = 3
    GAMBLING_ADDICTION = 4


class Sentencing(Enum):

    """
    Possible sentences
    """

    PRISON = 1
    PAROLE = 2
    CCO = 3


class Procedure(Enum):

    """
    Possible labelling procedures
    """

    MANUAL = 1
    REGEX = 2
    CLUSTERING = 3
