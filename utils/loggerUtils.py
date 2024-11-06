import logging

class Logger(object):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    def INFO(self, message):
        self.logger.info(message)
    def ERROR(self, message):
        self.logger.error(message)
    def DEBUG(self, message):
        self.logger.debug(message)
    def WARNING(self, message):
        self.logger.warning(message)
    def CRITICAL(self, message):
        self.logger.critical(message)
