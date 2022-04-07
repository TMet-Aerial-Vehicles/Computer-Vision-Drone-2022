import logging
from datetime import datetime


# noinspection PyArgumentList
def start_logging():
    file = f"logging/logging-{datetime.today().strftime('%Y-%m-%d-%H')}.log"
    logging.basicConfig(encoding='utf-8', filename=file, level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')
