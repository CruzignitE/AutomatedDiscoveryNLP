import time


class Timer:

    # ---- Static fields----
    __s_timer_list: list = []

    # ----Constructor----
    def __init__(self, a_name, a_parent_timer=None):
        self.__f_name = a_name
        self.__f_parent_timer = a_parent_timer
        self.__f_start = 0
        self.__f_elapsed = 0
        self.__f_run_count = 0
        self.__f_average_elapsed = 0
        self.__f_percent_of_total = 0
        self.__f_percent_of_parent = 0
        self.__stopped = True

        Timer.__s_timer_list.append(self)

    # ----Instance Methods----
    def start(self):
        if self.__stopped:
            self.__f_start = time.time()
            self.__stopped = False
        else:
            raise Exception(self.__f_name + " was started before it was stopped")

    def stop(self):
        if not self.__stopped:
            self.__f_elapsed += time.time() - self.__f_start
            self.__f_start = 0
            self.__f_run_count += 1
            self.__stopped = True
        else:
            raise Exception(self.__f_name + " was stopped before it was started")

    def calculate_average(self):
        if self.__f_run_count is not 0:
            return str(round(self.__f_elapsed / self.__f_run_count, 3)) + "s"
        else:
            return 0

    def calculate_percent_of_total(self):
        return str(round((self.__f_elapsed / Timers.s_main_timer.__f_elapsed) * 100, 3)) + "%"

    def calculate_percent_of_parent(self):
        if self.__f_parent_timer is None:
            return "N/A"
        else:
            if self.__f_parent_timer.__f_elapsed is not 0:
                return str(round((self.__f_elapsed / self.__f_parent_timer.__f_elapsed) * 100, 3)) + "%"
            else:
                return "N/A"

    # ----Method Overrides----
    def __str__(self):
        return \
            '{: <32}'.format(self.__f_name) + '{: <3}'.format("|") + \
            '{: <14}'.format(str(round(self.__f_elapsed, 3)) + 's') + '{: <3}'.format("|") + \
            '{: <14}'.format(str(self.__f_run_count)) + '{: <3}'.format("|") + \
            '{: <16}'.format(str(self.calculate_average())) + '{: <3}'.format("|") + \
            '{: <20}'.format(str(self.calculate_percent_of_total())) + '{: <3}'.format("|") + \
            '{: <21}'.format(str(self.calculate_percent_of_parent()))

    @classmethod
    def headings(cls):
        return \
            '{:-<129}'.format("") + "\n" + \
            '{: <32}'.format("Method Name:") + '{: <3}'.format("|") + \
            '{: <14}'.format("Total Time:") + '{: <3}'.format("|") + \
            '{: <14}'.format("Total Runs:") + '{: <3}'.format("|") + \
            '{: <16}'.format("Average Time:") + '{: <3}'.format("|") + \
            '{: <20}'.format("Percent of Total:") + '{: <3}'.format("|") + \
            '{: <21}'.format("Percent of Parent:") + \
            "\n" + '{:-<129}'.format("")


    @classmethod
    def print_all(cls):

        """"
        Prints all timers
        """
        Timers.s_main_timer.stop()

        # Print timers
        print(Timer.headings())
        for l_timer in sorted(Timer.__s_timer_list, key=lambda x: x.__f_elapsed, reverse=True):
            if l_timer.__stopped:
                if l_timer.__f_elapsed is not 0:
                    print(l_timer)
            else:
                raise Exception(l_timer.__f_name + " was not stopped before the end of the program")
        print('{:-<129}'.format(""))

class Timers:

    # ---- Static fields----
    s_main_timer = Timer("Main")
    s_main_timer.start()

    # Location: Main.load_formatted_files
    # Location: Main.load_unformatted_files
    s_init_timer = Timer("Initialise")

    # Location: LegalDoc.__initialise
    s_init_load_state_timer = Timer("Initialise Load State", s_init_timer)

    # Location: LegalDoc.__initialise
    s_init_gen_state_timer = Timer("Initialise Generate State", s_init_timer)

    # Location: LegalDoc.generate_corpus_from_sections
    s_gen_corpus_from_secs_timer = Timer("Generate Corpus from Sections", s_init_gen_state_timer)

    # Location: LegalDoc.__clean_sections
    s_clean_sections_timer = Timer("Clean Sections", s_init_gen_state_timer)

    # Location: LegalDoc.__anonymize_names
    s_anonymize_names_timer = Timer("Anonymize Names", s_init_gen_state_timer)

    # Location: LegalDoc.LegalDoc.__anonymize_names
    s_anonymization_timer = Timer("*Anonymization*", s_anonymize_names_timer)

    # Location: LegalDoc.generate_sections_from_corpus
    s_gen_secs_from_corpus_timer = Timer("Generate Sections from Corpus", s_anonymize_names_timer)

    # Location: LegalDoc.__write
    s_write_timer = Timer("Write")

    # Location: Label.add_label
    s_add_label = Timer("Add Label")

