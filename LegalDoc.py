import regex as re


class LegalDoc:

    # ----Constant Static fields----
    __EMPTY_LINE_PATTERN = re.compile("^[\\s\t\n\r]*$")
    __SECTION_PATTERN = re.compile("(?:^[0-9]+[\\s\t]+)(.+)")
    __DOCUMENT_PATTERN = re.compile("(.+)(?:(^1[\t\\s]+(HER|HIS)[\\s]+HONOUR:.+)|(?:^(HER|HIS)[\\s]+HONOUR:[\\s\t]*$)(.+))(?:^[\\s\t-]+-[\\s\t-]+$)(.+)", re.S | re.M)
    __FILE_PATTERN = re.compile("^(.+/)*(.+\\..+)$")
    __SAVE_FILE_PATTERN = re.compile("[\\/:\"*?<>|]+'")

    __SENTENCE_PATTERN = re.compile("[\\.][\\s|\t]+")
    __CASE_NUMBER_PATTERN = re.compile("(CR[0-9\\s-]+[0-9]$)", re.S | re.M)
    __CASE_NAME_PATTERN = re.compile("CASE MAY BE CITED AS:[\n\t\\s]+(.+)[\n\t\\s]+")
    __DEFENDANT_NAME_PATTERN = re.compile("[vV][\n\\s\t]+([A-Za-z]+)[\\s]+[A-Za-z]+[\n\\s\t]+")

    # ---- Static fields----
    __fSuccessfulInitCount = 0
    __fFailedInitCount = 0
    __fExceptionData = dict()

    # ----Private fields----
    # String __fPath

    # String __fHead
    # List<List<String>> __fBody

    # String __fJudgeGender
    # String __fCaseNumber
    # String __fCaseName
    # String __fDefendantName

    # Boolean __fFailedInit

    # ----Constructor----
    def __init__(self, aPath):
        try:
            self.__fPath = aPath
            self.__fHead = "NULL"
            self.__fBody = []
            self.__fJudgeGender = "NULL"
            self.__fDefendantFirstName = "NULL"
            self.__fCaseName = "NULL"
            self.__fCaseNumber = "NULL"
            self.__fFailedInit = True

            # Read in file
            try:
                lFile = open(aPath)
                lContent = lFile.read()
                lFile.close()

            except IOError:
                LegalDoc.__noteException(aPath, "MAJOR ERROR: Unable to read file", True)
                lFile.close()
                return

            # Break up document into base components
            try:
                lDocumentGroups = re.search(LegalDoc.__DOCUMENT_PATTERN, lContent).groups()
                self.__fHead = lDocumentGroups[0]

                if lDocumentGroups[3] is None:                  # Inline "HER|HIS HONOUR:"
                    self.__fJudgeGender = lDocumentGroups[2]
                    lLines = lDocumentGroups[1].splitlines()    # Body broken down by line

                else:                                           # Separated "HER|HIS HONOUR:"
                    self.__fJudgeGender = lDocumentGroups[3]
                    lLines = lDocumentGroups[4].splitlines()    # Body broken down by line

            except (TypeError, AttributeError):                 # Very slow
                LegalDoc.__noteException(aPath, "MAJOR ERROR: Regex cannot parse document", True)
                return

            # Extract information from head
            # Extract case number
            try:
                self.__fCaseNumber = re.search(LegalDoc.__CASE_NUMBER_PATTERN, self.__fHead).group(1)

            except (TypeError, AttributeError):
                LegalDoc.__noteException(aPath, "ERROR: Unable to find case number", False)

            # Extract case name
            try:
                self.__fCaseName = re.search(LegalDoc.__CASE_NAME_PATTERN, self.__fHead).group(1)

            except (TypeError, AttributeError):
                LegalDoc.__noteException(aPath, "ERROR: Unable to find case name", False)

            # Extract defendant name
            try:
                self.__fDefendantFirstName = re.search(LegalDoc.__DEFENDANT_NAME_PATTERN, self.__fHead).group(1)

            except (TypeError, AttributeError):
                LegalDoc.__noteException(aPath, "ERROR: Unable to find defendant name", False)

            # Break up body into sections comprised of lines
            try:
                lBodyIndex = -1

                # For each line in body...
                for i in range(0, len(lLines)):
                    lLine = lLines[i]
                    lSectionMatcher = re.match(LegalDoc.__SECTION_PATTERN, lLine)

                    # Check if the line is a the start of a section
                    if lSectionMatcher:
                        lBodyIndex += 1
                        self.__fBody.append(lSectionMatcher.group(1))

                    # Check if the line is empty
                    elif re.match(LegalDoc.__EMPTY_LINE_PATTERN, lLine):
                        continue

                    # The line is part of a section
                    else:
                        self.__fBody[lBodyIndex] += lLine

                # Break up sections into sentences
                for i in range(0, len(self.__fBody)):
                    self.__fBody[i] = [x for x in LegalDoc.__SENTENCE_PATTERN.split(self.__fBody[i]) if x]

            except (TypeError, AttributeError, IndexError):
                LegalDoc.__noteException(aPath, "MAJOR ERROR: Unable to break down body", True)
                raise  # Change later

            # Document successful initialisation
            LegalDoc.__fSuccessfulInitCount += 1
            self.__fFailedInit = False

        except Exception:
            LegalDoc.__noteException(aPath, "MAJOR ERROR: Unspecified error occurred", True)
            raise

    # ----Method Overrides----
    # Override this.print() with formatted body output
    def __str__(self):
        lInfo = "CASE Name:\n\t" + self.__fCaseName + "\n"
        lInfo += "CASE NUMBER:\n\t" + self.__fCaseNumber + '\n'
        lInfo += "JUDGE GENDER:\n\t" + self.__fJudgeGender + '\n'
        lInfo += "DEFENDANT FIRST NAME:\n\t" + self.__fDefendantFirstName + '\n'
        lInfo += "SECTIONS:" + '\n'

        for i in range(0, len(self.__fBody)):
            lSection = self.__fBody[i]
            lInfo += '\t' "Section:" + str(i + 1) + '\n'

            for j in range(0, len(lSection)):
                lSentence = lSection[j]
                lInfo += "\t\t" + lSentence + '\n'

        return lInfo

    # ----Instance methods----
    # Save formatting as a txt file
    def Write(self):

        # Make sure that "CaseName" and  "CaseNumber" do not contain illegal values or are not excessively long
        lSafeCaseName = re.sub(r'[\\/:"*?<>|]+', "", self.CaseName)
        lSafeCaseName = (lSafeCaseName[:25] + '..') if len(lSafeCaseName) > 25 else lSafeCaseName
        lSafeCaseNumber = re.sub(r'[\\/:"*?<>|]+', "", self.CaseNumber)
        lSafeCaseNumber = (lSafeCaseNumber[:25] + '..') if len(lSafeCaseNumber) > 25 else lSafeCaseNumber

        # Save file
        try:
            lSaveFile = open(
                            "Resources/Output/Formatted/"
                            "(" + lSafeCaseName + ") (" + lSafeCaseNumber + ").txt",
                            "w", encoding="UTF-8")
            lSaveFile.write(self.__str__())
            lSaveFile.close()

        except IOError:
            print("ERROR: Unable to save file with path: " + self.__fPath)
            lSaveFile.close()
            return

    # ----Properties----
    # Head
    @property
    def Head(self):
        return self.__fHead

    # Body
    @property
    def Body(self):
        return self.__fBody

    # Defendant name
    @property
    def DefendantName(self):
        return self.__fDefendantName

    # Judge's gender
    @property
    def JudgeGender(self):
        return self.__fJudgeGender

    # Case name
    @property
    def CaseName(self):
        return self.__fCaseName

    # Case number
    @property
    def CaseNumber(self):
        return self.__fCaseNumber

    # Failed initialisation
    @property
    def FailedInit(self):
        return self.__fFailedInit

    # Origin path
    @property
    def Path(self):
        return self.__fPath

    # ----Class Methods----
    @classmethod
    def GetExceptionData(cls):
        lErrorData = "Successful initialisations: " + str(cls.__fSuccessfulInitCount) + '\n'
        lErrorData += "Failed initialisations: " + str(cls.__fFailedInitCount) + '\n'
        lErrorData += "Exceptions: " + '\n'

        for key, val in cls.__fExceptionData.items():

            try:
                lErrorData += "\t" + re.search(cls.__File_PATTERN, key).group(2) + '\n'

            except (TypeError, AttributeError):
                lErrorData += "\t" + key + '\n'

            for i in range(0, len(val)):
                lErrorData += "\t\t" + val[i] + '\n'

        return lErrorData

    @classmethod
    def __noteException(cls, aPath, aException, aFailedInit):

        if aPath in cls.__fExceptionData:
            cls.__fExceptionData[aPath].append(aException)

        else:
            cls.__fExceptionData[aPath] = [aException]

        if aFailedInit:
            cls.__fFailedInitCount += 1

    # ----Static Methods----
    # Static method (don't access instance or class)
    @staticmethod
    def a_static_method(a_number):
        return 2 * a_number
