import logging


def final_logger():
    logger = logging.getLogger(__name__)
    logfile = "CoffeeForMe.log"

    formatter = logging.Formatter('%(asctime)s - %(name)s : %(levelname)s - %(message)s')

    file_handler = logging.FileHandler(logfile)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger
