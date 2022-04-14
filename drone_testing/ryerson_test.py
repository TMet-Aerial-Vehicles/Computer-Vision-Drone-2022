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

    logging.info("Countdown 5 second")
    countdown(5)

    logging.info("Taking off")
    drone.takeoff()
    logging.info("Took off to 2m")

    logging.info("Rotating to North")
    drone.rotate(0, relative=False)

    logging.info("Rotate 1 degree")
    drone.rotate(1)
    sleep(2)

    logging.info("Rotate 5 degree")
    drone.rotate(5)
    sleep(2)

    logging.info("Rotate 15 degree")
    drone.rotate(15)
    sleep(2)

    logging.info("Rotate 30 degree")
    drone.rotate(30)
    sleep(2)

    logging.info("Rotate 45 degree")
    drone.rotate(45)
    sleep(2)

    logging.info("Rotate 45 degree")
    drone.rotate(60)
    sleep(2)

    logging.info("Rotate 90 degree")
    drone.rotate(90)
    sleep(2)

    logging.info("Rotate 359 degree")
    drone.rotate(359)
    sleep(2)

    logging.info("Moving 1m North")
    drone.move_relative(3, 0)
    sleep(2)

    logging.info("Rotate 90 degree")
    drone.rotate(90)
    sleep(2)

    logging.info("Moving 1m East")
    drone.move_relative(0, 3)
    sleep(2)

    logging.info("Rotate 90 degree")
    drone.rotate(90)
    sleep(2)

    logging.info("Moving 1m South")
    drone.move_relative(-3, 0)
    sleep(2)

    logging.info("Rotate 90 degree")
    drone.rotate(90)
    sleep(2)

    logging.info("Returning to landing")
    drone.return_home()
    sleep(5)
    countdown(5)

except Exception as e:
    logging.error(e)
finally:
    drone.close_connection() if drone is not None else logging.error("No drone")
