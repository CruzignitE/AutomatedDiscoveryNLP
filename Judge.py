from typing import List

import LegalDoc


class Judge:
    # ---- Static fields----
    __s_judges: dict = dict()

    # ----Private fields----
    __f_name: str
    __f_cases: List

    # ----Constructor----
    def __init__(self, a_legal_doc: LegalDoc):

        # initialise
        self.__f_name = a_legal_doc.judge_name
        self.__f_cases = []

        # Judge already in judge dictionary
        if self.__f_name in Judge.__s_judges:
            (Judge.__s_judges[self.__f_name]).__f_cases.append(a_legal_doc)
            del self

        # Judge not in judge dictionary
        else:
            self.__f_cases.append(a_legal_doc)
            Judge.__s_judges[self.__f_name] = self

    # ----Properties (Read only getters)----
    # Judge name
    @property
    def name(self):
        return self.__f_name

    # Judge cases
    @property
    def cases(self):
        return self.__f_cases

    # ----Method Overrides----
    # Override this.print() with formatted output
    def __str__(self):
        # Write name
        l_info = "Name: " + self.name

        # Write case file names
        for l_case in self.cases:
            l_info += "\n\t" + l_case.file_name + ".txt"

        return l_info

    # ----Class Methods----
    @classmethod
    def print_all(cls):
        # Sort the judge's by name
        l_judges = [v for v in Judge.__s_judges.values()]
        l_judges.sort(key=lambda x: x.name, reverse=False)

        # Print Judges
        for l_judge in l_judges:
            print(l_judge)
