import logging

logger = logging.getLogger(__name__)
logfile = "Coffee_for_me.log"

formatter = logging.Formatter('%(asctime)s - %(name)s:  %(levelname)s - %(message)s')

file_handler = logging.FileHandler(logfile)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)
