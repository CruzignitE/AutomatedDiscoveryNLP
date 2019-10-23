from typing import List

from prometheus_client.metrics import _build_full_name

import LegalDoc


class Judge:

    """"
    Judge class
    Each instance contains the judge's name and a list of cases they have presided over
    The class contains a dictionary; the key being a judge's name and the value being the associated judge instance
    """

    # ---- Static fields----
    __s_judge_dict: dict = dict()

    # ----Constructor----
    def __init__(self, a_legal_doc: LegalDoc):

        """"
        Judge constructor
        :type a_legal_doc: LegalDoc.LegalDoc
        :raises TypeError: if a_legal_doc is not a LegalDoc.LegalDoc
        """

        # Initialise
        self.__f_name = " ".join(a_legal_doc.judge_name)
        self.__f_cases = [a_legal_doc]

    # ----Method Overrides----

    def __str__(self):

        """"
        Override self.print() with formatted output
        """

        # Write name
        l_info = "Name: " + self.name

        # Write case file names (ordered numerically)
        l_file_names = [int(v.file_name.replace('.txt', '')) for v in self.__f_cases]
        l_file_names.sort(key=lambda x: x, reverse=False)
        for l_file_name in l_file_names:
            l_info += "\n\t" + str(l_file_name) + ".txt"

        return l_info

    # ----Class Methods----
    @classmethod
    def add_legal_doc(cls, a_legal_doc):

        """"
        Adds a legal doc to a judge, creating a judge in the process if necessary
        and adds them to the judge dictionary if they aren't already in the dictionary
        :type a_legal_doc: LegalDoc.LegalDoc
        :raises TypeError: if a_legal_doc is not a LegalDoc.LegalDoc
        """

        # Judge already in judge dictionary
        if " ".join(a_legal_doc.judge_name) in Judge.__s_judge_dict:
            (Judge.__s_judge_dict[" ".join(a_legal_doc.judge_name)]).__f_cases.append(a_legal_doc)

        # Judge not in judge dictionary
        else:
            Judge.__s_judge_dict[" ".join(a_legal_doc.judge_name)] = Judge(a_legal_doc)

    @classmethod
    def print_all(cls):

        """"
        Prints all judge names and the cases associated with them
        """

        # Sort the judge's by name
        l_judges = [v for v in Judge.__s_judge_dict.values()]
        l_judges.sort(key=lambda x: x.name, reverse=False)

        # Print Judges
        for l_judge in l_judges:
            print(l_judge)

    # ----Properties (Read only getters)----

    @property
    def name(self):

        """"
        :rtype: str
        :return: This judge's name
        """

        return self.__f_name

    @property
    def cases(self):

        """"
        :rtype: list
        :return: A list of this judge's cases (LegalDocs)
        """

        return self.__f_cases
