from supplychain.settings import BASE_DIR
import os
import logging.config
# def get_logger():
#     logging.basicConfig(filename=BASE_DIR + "/log_file.log",format="%(asctime)s:%(message)s", level=logging.DEBUG)
#     logger = logging.getLogger()
#     return logger


def get_logger():
    logging.config.fileConfig(os.path.join(BASE_DIR, 'logger_config.ini'))
    logger = logging.getLogger()
    return logger
