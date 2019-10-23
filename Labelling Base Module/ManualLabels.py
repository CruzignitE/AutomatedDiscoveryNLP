
from Label import *
from LabelEnums import *


class ManualLabels:

    @staticmethod
    def add_manual_labels():

        """
        FILE 1016
        """

        Label.add_label(LabelType.CHARGES_TYPE, Charges.THEFT, Procedure.MANUAL,
                        "1016.txt", "True", "Body",
                        [
                            "you pleaded guilty to four charges laid on the indictment, being two charges of" +
                            " common assault, one charge of theft",

                            "75	On the charge of theft, that is Charge 1, I convict and sentence you" +
                            " to one months' imprisonment"

                        ])

        Label.add_label(LabelType.AGGRAVATING_TYPE, Aggravating.RELEVANT_PRIORS, Procedure.MANUAL,
                        "1016.txt", "True", "Body",
                        [
                            "I must impose a just and proportionate sentence in relation to your offending. " +
                            "I have spent some time dealing with your prior criminal history and I make this plain; " +
                            "you do not fall to be sentenced a second time for that past conduct. " +
                            "It does not permit me to react by imposing a disproportionate sentence, but it" +
                            "is obviously relevant to my assessment of your rehabilitative prospects, your risk" +
                            "of reoffending and the need to deter you from future offending."

                        ])

        Label.add_label(LabelType.MITIGATING_TYPE, Mitigating.PLEA_GUILTY, Procedure.MANUAL,
                        "1016.txt", "True", "Body",
                        [
                            "I turn then to consider the submissions made.  You have pleaded guilty at, what" +
                            "I will treat as, the earliest stage.  You have taken early responsibility at law for" +
                            "your offending.  I must give you credit for your decision to plead guilty and at the" +
                            "early stage which you did.  Witnesses have been spared the experience of coming to court" +
                            "to give evidence.  The community has been saved the time, the expense and the effort" +
                            "associated with the conduct of a committal hearing in the lower court or trial" +
                            "up in this court.  So you have in these ways facilitated the course of justice." +
                            "I am required to pass a lesser sentence on you than I would have imposed had you" +
                            "been found guilty by a jury. "

                        ])

        Label.add_label(LabelType.SENTENCING_TYPE, Sentencing.PRISON, Procedure.MANUAL,
                        "1016.txt", "True", "Body",
                        [
                            "This results in a total effective sentence of three years' imprisonment."

                        ])


        """
        FILE 1017
        """

        Label.add_label(LabelType.CHARGES_TYPE, Charges.THEFT, Procedure.MANUAL,
                        "1017.txt", "True", "Body",
                        [
                            "In respect to the indictment, you pleaded guilty to handling stolen goods" +
                            " (Charge 1), aggravated burglary (Charge 2), theft (Charges 3 and 6)",

                            "On Charge 3, theft, I sentence you to six months’ imprisonment.",

                            "On Charge 6, theft, I sentence you to three months’ imprisonment."

                        ])

        Label.add_label(LabelType.AGGRAVATING_TYPE, Aggravating.RELEVANT_PRIORS, Procedure.MANUAL,
                        "1017.txt", "True", "Body",
                        [
                            "Amongst your prior convictions are:",

                            "You admitted your prior convictions."


                        ])

        Label.add_label(LabelType.MITIGATING_TYPE, Mitigating.PLEA_GUILTY, Procedure.MANUAL,
                        "1017.txt", "True", "Body",
                        [

                            "you came before me on 8 February 2018 and pleaded guilty to Indictment" +
                            " No H11103284 as well as a number of related summary offences.  ",

                            "In respect to the indictment, you pleaded guilty to",

                            "In respect to the related summary offences, you pleaded guilty to two charges of",

                            "51	You entered your plea at an early stage and are entitled to the benefits that flow" +
                            " to you from that plea, being that it is some evidence of your remorse and that it" +
                            "has utilitarian value.",

                            "66	I declare, pursuant to s6AAA of the Sentencing Act 1991," +
                            " that but for your plea of guilty I would have sentenced you to seven years and" +
                            " six months’ imprisonment with a non-parole period of five years’ imprisonment."

                        ])

        Label.add_label(LabelType.SENTENCING_TYPE, Sentencing.PRISON, Procedure.MANUAL,
                        "1017.txt", "True", "Body",
                        [
                            "This results, in respect of the indictment, in a total effective" +
                            " sentence of five years and two months' imprisonment.  "
                        ])

        """
        FILE TEMPLATE
        """


        Label.add_label(LabelType.CHARGES_TYPE, Charges.THEFT, Procedure.MANUAL,
                        "TEMPLATE.txt", "BOOLEAN", "Body",
                        [


                        ])

        Label.add_label(LabelType.AGGRAVATING_TYPE, Aggravating.RELEVANT_PRIORS, Procedure.MANUAL,
                        "TEMPLATE.txt", "BOOLEAN", "Body",
                        [


                        ])

        Label.add_label(LabelType.MITIGATING_TYPE, Mitigating.PLEA_GUILTY, Procedure.MANUAL,
                        "TEMPLATE.txt", "BOOLEAN", "Body",
                        [


                        ])

        Label.add_label(LabelType.SENTENCING_TYPE, Sentencing.PRISON, Procedure.MANUAL,
                        "TEMPLATE.txt", "BOOLEAN", "Body",
                        [


                        ])