import os.path
import sys
import logging.handlers
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = logging.handlers.RotatingFileHandler(os.path.abspath('./Coffee_for_me_log'))
formatter = logging.Formatter(
    "%(asctime)s : func - %(funcName)-16s - %(lineno)-3s line : %(filename)-16s : %(levelname)-6s : %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
