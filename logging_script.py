import logging
from datetime import datetime


# noinspection PyArgumentList
def start_logging(dir='logging/'):
    file = f"{dir}logging-{datetime.today().strftime('%Y-%m-%d-%H')}.log"
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(file, 'w', 'utf-8')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)
