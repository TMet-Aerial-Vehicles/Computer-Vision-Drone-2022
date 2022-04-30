import sys
sys.path.append("..")
from pixhawk import PixHawk
from sound import countdown
from time import sleep
import logging
from logging_script import start_logging
start_logging()

logging.info("Starting 20 second countdown")
countdown(20)
drone = None
try:
    logging.info("Connecting to drone")
    drone = PixHawk(min_altitude=3, max_altitude=10,
                    boundary_circle=True, boundary_radius=10)

    drone.print_drone_stats()

    logging.info("Countdown 5 second")
    countdown(5)

    drone.print_drone_stats()

    logging.info("Setting stabilize mode")
    drone.set_stabilize_mode()
    sleep(5)

    drone.print_drone_stats()

except Exception as e:
    logging.error(e)
finally:
    drone.close_connection() if drone is not None else logging.error("No drone")
