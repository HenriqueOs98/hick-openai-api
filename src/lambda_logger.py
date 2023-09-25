import logging

class LambdaLogger:
    def __init__(self, log_level=logging.INFO):
        self.logger = logging.getLogger('lambda_logger')
        self.logger.setLevel(log_level)
        self.handler = logging.StreamHandler()
        self.handler.setLevel(log_level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.handler.setFormatter(formatter)
        self.logger.addHandler(self.handler)

    def set_log_level(self, log_level):
        self.logger.setLevel(log_level)
        self.handler.setLevel(log_level)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def exception(self, message):
        self.logger.exception(message)

    def critical(self, message):
        self.logger.critical(message)
