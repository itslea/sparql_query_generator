import time
import logging



class TimeTaker:
    """Mit der Initialisierung der Klasse wird der Timer gestartet. Mit Stop Timer wird der Timer beendet und die gemessene Zeit wird geloggt."""

    def __init__(self, message):
        self.logger = logging.getLogger()
        handler = logging.FileHandler('event.log')
        self.logger.addHandler(handler)
        self.logger.level = logging.INFO
        self.message = str(message)

    def starttimer(self):
        self.starttime = time.time()

    def stoptimer(self):
        needed_time = time.time() - self.starttime
        message = self.message + ": "+  str(needed_time)
        self.logger.info(message)
        return needed_time