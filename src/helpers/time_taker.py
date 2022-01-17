from timeit import default_timer as timer
import logging

class TimeTaker:
    """Calculates execution time of a function and writes the calculated time in a log file"""

    def __init__(self):
        self.logger = logging.getLogger()
        handler = logging.FileHandler('event.log')
        self.logger.addHandler(handler)
        self.logger.level = logging.INFO
        self.starttime = 0

    def start_timer(self):
        self.starttime = timer()

    def stop_timer(self):
        needed_time = timer() - self.starttime
        # message = gen_name + " " + type +  " time of " + str(triples) + " triples: " + str(needed_time)
        # self.logger.info(message)
        return needed_time

    def message_log(self, gen_type, triples, gen_time, ev_time, answers):
        self.logger.info(gen_type + ", " + str(triples) + " triples --> Gen: " + str(gen_time) + ", Ev: " + str(ev_time) + ", Answers: " + str(answers))

    def add_log(self, message):
        self.logger.info(message)
