import logging
from datetime import datetime

raspberry_pi = False        # True if running on raspberry pi


# noinspection PyArgumentList
def start_logging():
    if raspberry_pi:
        directory = '/home/pi/Desktop/JTC_ComputerVision/'
    else:
        directory = ''
    file = f"{directory}logging-{datetime.today().strftime('%Y-%m-%d-%H')}.log"
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(file, 'a', 'utf-8')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)
