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

    def stop_timer(self, type, triples, gen_name):
        needed_time = timer() - self.starttime
        message = gen_name + " " + type +  " time of " + str(triples) + " triples: " + str(needed_time)
        self.logger.info(message)
        return needed_time

    def message_log(self, triples, message):
        self.logger.info("Execution time of " + str(triples) + ": " + str(message))
