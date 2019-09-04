import datetime
import logging

from src.constants import CONVERSATION_LOG, INFORMATION_EXTRACTION_LOG, DIALOGUE_MODEL_LOG
class Logger:

    def __init__(self):
        pass

    @staticmethod
    def setup_loggers():
        date = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        Logger.setup_logger(CONVERSATION_LOG, '../logs/conversation/' + date)
        Logger.setup_logger(INFORMATION_EXTRACTION_LOG, '../logs/information extraction/' + date)
        Logger.setup_logger(DIALOGUE_MODEL_LOG, '../logs/dialogue model/' + date)

    @staticmethod
    def setup_logger(name, log_file, level=logging.INFO):
        """Function setup as many loggers as you want"""
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', "%Y-%m-%d %H:%M:%S")

        handler = logging.FileHandler(log_file)
        handler.setFormatter(formatter)

        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.addHandler(handler)

        return logger

    @staticmethod
    def log_conversation(content):
        logger = logging.getLogger(CONVERSATION_LOG)
        logger.info(content)

    @staticmethod
    def log_information_extraction(content):
        logger = logging.getLogger(INFORMATION_EXTRACTION_LOG)
        logger.info(content)

    @staticmethod
    def log_dialogue_model(content):
        logger = logging.getLogger(DIALOGUE_MODEL_LOG)
        logger.info(content)

    # logging.basicConfig(filename='../logs/conversation/' + date + '.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
    # logging.warning('This will get logged to a file')