import logging
import os

LOGGER = logging.getLogger('fetch_deezer_data')
formatter = logging.Formatter("[%(asctime)s] [%(process)s] [%(levelname)s]: %(message)s")

level = "DEBUG"
LOGGER.setLevel(level)
ch = logging.StreamHandler()
ch.setFormatter(formatter)
LOGGER.addHandler(ch)

