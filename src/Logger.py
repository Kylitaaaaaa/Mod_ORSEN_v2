import datetime
import logging
import os

from src.constants import CONVERSATION_LOG, INFORMATION_EXTRACTION_LOG, DIALOGUE_MODEL_LOG, EVENT_CHAIN_LOG, EMOTION_CLASSIFICATION, DUMP_LOG
class Logger:

    def __init__(self):
        pass

    @staticmethod
    def setup_loggers():
        date = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        # Logger.__setup_logger__(CONVERSATION_LOG, '../logs/conversation/' + date + '.txt')
        # Logger.__setup_logger_basic__(INFORMATION_EXTRACTION_LOG, '../logs/information extraction/' + date + '.txt')
        # Logger.__setup_logger_basic__(DIALOGUE_MODEL_LOG, '../logs/dialogue model/' + date + '.txt')
        # Logger.__setup_logger_basic__(EVENT_CHAIN_LOG, '../logs/event chain/' + date + '.txt')
        #
        # Logger.__setup_logger_basic__(EMOTION_CLASSIFICATION, '../logs/emotion classification/' + date + '.txt')

        Logger.__setup_logger__(CONVERSATION_LOG, '../Mod_ORSEN_v2/logs/conversation/' + date + '.txt')
        Logger.__setup_logger_basic__(INFORMATION_EXTRACTION_LOG,
                                      '../Mod_ORSEN_v2/logs/information extraction/' + date + '.txt')
        Logger.__setup_logger_basic__(DIALOGUE_MODEL_LOG, '../Mod_ORSEN_v2/logs/dialogue model/' + date + '.txt')
        Logger.__setup_logger_basic__(EVENT_CHAIN_LOG, '../Mod_ORSEN_v2/logs/event chain/' + date + '.txt')
        Logger.__setup_logger_basic__(EMOTION_CLASSIFICATION, '../Mod_ORSEN_v2/logs/emotion classification/' + date + '.txt')

    @staticmethod
    def __setup_logger__(name, log_file, level=logging.INFO):
        """Function setup as many loggers as you want"""
        formatter = logging.Formatter('%(asctime)s - %(message)s', "%m-%d-%y %H:%M:%S")

        handler = logging.FileHandler(log_file)
        handler.setFormatter(formatter)

        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.addHandler(handler)

        return logger

    @staticmethod
    def __setup_logger_basic__(name, log_file, level=logging.INFO):
        """Function setup as many loggers as you want"""
        formatter = logging.Formatter('%(message)s')

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
    def log_dialogue_model(content):
        logger = logging.getLogger(DIALOGUE_MODEL_LOG)
        logger.info(content)

    @staticmethod
    def log_dialogue_model_basic(content):
        logger = logging.getLogger(DIALOGUE_MODEL_LOG)
        logger.info("  >> " + str(content))

    @staticmethod
    def log_dialogue_model_basic_example(content):
        logger = logging.getLogger(DIALOGUE_MODEL_LOG)
        logger.info("        " + str(content))


    @staticmethod
    def log_information_extraction(content):
        logger = logging.getLogger(INFORMATION_EXTRACTION_LOG)
        logger.info(content)

    @staticmethod
    def log_information_extraction_basic(content):
        logger = logging.getLogger(INFORMATION_EXTRACTION_LOG)
        logger.info("  >> " + str(content))

    @staticmethod
    def log_information_extraction_basic_example(content):
        logger = logging.getLogger(INFORMATION_EXTRACTION_LOG)
        logger.info("        " + str(content))


    @staticmethod
    def log_event(event_type, content):
        logger = logging.getLogger(EVENT_CHAIN_LOG)
        logger.info(event_type[0] + ": " + content)
    # logging.basicConfig(filename='../logs/conversation/' + date + '.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
    # logging.warning('This will get logged to a file')

    @staticmethod
    def log_event_response_eval(content):
        logger = logging.getLogger(EVENT_CHAIN_LOG)
        logger.info("  >> EVALUATING: "+ content)

    @staticmethod
    def log_occ_values(content):
        logger = logging.getLogger(EMOTION_CLASSIFICATION)
        logger.info(content)

    @staticmethod
    def log_occ_values_basic(content):
        logger = logging.getLogger(EMOTION_CLASSIFICATION)
        logger.info("  >> " + str(content))

    @staticmethod
    def dump_log(content):
        logger = logging.getLogger(EMOTION_CLASSIFICATION)
        logger.info(content)

        logger = logging.getLogger(EVENT_CHAIN_LOG)
        logger.info(content)

        logger = logging.getLogger(INFORMATION_EXTRACTION_LOG)
        logger.info(content)




