from enum import Enum


class Type(Enum):
    CHARGES_TYPE = 1
    MITIGATING_TYPE = 2
    AGGRAVATING_TYPE = 3
    SENTENCING_TYPE = 4


class Charges(Enum):
    """
    Possible charges
    """

    '''
    "Theft, 
    Theft of electricity, 
    Theft of firearm"
    '''

    THEFT = 1

    '''
    trafficking in a drug of dependence, 
    Trafficking and possession of methylamphetamine,
    trafficking in a drug of dependence large commercial quantity
    '''
    TRAFFICKING_DRUG = 2

    '''
    burglary
    aggravated burglary
    '''
    BURGLARY = 3

    '''
    Assault,
    Indecent assault
    common assault
    Assault with a weapon

    '''
    ASSAULT = 4

    '''
    Sexual assault of a child under 16		
    Sexual penetration of a child under 16
    committing an indecent act on a child under 16
    Indecent act with child under 16
    Sexual penetration with a child between 10 and 16
    '''
    SEXUAL_ASSAULT_OF_MINOR = 5

    '''
    intentionally causing injury
    causing injury intentionally
    causing serious injury recklessly
    Causing injury recklessly
    causing serious injury intentionally  
    Recklessly causing injury
    recklessly cause injury
    '''
    CAUSING_INJURY = 6

    '''
    Armed Robbery
    Robbery
    '''
    ROBBERY = 7

    '''
    a prohibited person in possession of a firearm
    possession of a firearm whilst being a prohibited person
    prohibited person possess a firearm
    Prohibited person using firearm
    prohibited person possess imitation firearm
    '''
    PROHIBITED_FIREARM = 8

    '''
    dishonestly obtain financial advantage by deception
    obtain financial advantage by deception
    obtaining property by deception
    attempting to obtain property by deception
    obtaining a financial advantage by deception
    '''
    OBTAIN_BY_DECEPTION = 9


class Aggravating(Enum):
    """
    Possible Aggravating factors
    """

    '''
    relevant prior criminal offending
    relevant prior convictions
    Some relevant prior criminal history
    Relevant criminal record
    relevant prior convictions
    '''
    RELEVANT_PRIORS = 1

    '''
    Plea of not Guilty
    Not guilty plea
    Pleas of not Guilty
    '''
    PLEA_NOT_GUILTY = 2

    '''
    no remorse
    '''
    NO_REMORSE = 3

    '''
    general deterrence
    '''
    GENERAL_DETERRENCE = 4

    '''
    specific deterrence
    '''

    SPECIFIC_DETERRENCE = 5

    '''
    community protection
    '''
    COMMUNITY_PROTECTION = 6


class Mitigating(Enum):
    """
    Possible Mitigating factors
    """

    '''
    No relevant priors
    no prior offending
    no prior convictions
    no relevant prior offences
    '''

    NO_RELEVANT_PRIORS = 1

    '''
    Plea of guilty
    Pleas of guilty
    early guilty plea
    early plea and admissions
    Guilty plea
    '''

    PLEA_GUILTY = 2

    '''
    remorse
    genuine remorse
    '''

    REMORSE = 3

    '''
    gambling addiction
    gambling
    '''
    GAMBLING_ADDICTION = 4


class Sentencing(Enum):

    '''
    sentence of 3 years imprisonment
    sentence of two years and eleven months imprisonment
    Sentence (State) is 2 year/s 6 month/s imprisonment
    6AAA declaration: 6 years imprisonment
    '''
    PRISON = 1

    PAROLE = 2

    CCO = 3


class Procedure(Enum):

    MANUAL = 1
    REGEX = 2
    CLUSTERING = 3
