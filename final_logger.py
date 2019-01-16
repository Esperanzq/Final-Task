import os.path
import sys
import logging.handlers
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
path = os.path.abspath('./log')
try:
    os.mkdir(path)
except OSError:
    pass

file_handler = logging.handlers.RotatingFileHandler(os.path.abspath('./log/Coffee_for_me_log'), maxBytes=1048576, backupCount=2)
formatter = logging.Formatter(
    "%(asctime)s : func - %(funcName)-16s - %(lineno)-3s line : %(filename)-16s : %(levelname)-6s : %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
