import logging
from datetime import datetime


# noinspection PyArgumentList
def start_logging():
    file = f"logging/logging-{datetime.today().strftime('%Y-%m-%d-%H')}.log"
    # logging.basicConfig(encoding='utf-8', filename=file, level=logging.DEBUG,
    #                     format='%(asctime)s - %(levelname)s - %(message)s',
    #                     datefmt='%m/%d/%Y %I:%M:%S %p')

    root_logger= logging.getLogger()
    root_logger.setLevel(logging.DEBUG) # or whatever
    handler = logging.FileHandler(file, 'w', 'utf-8') # or whatever
    handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    root_logger.addHandler(handler)
