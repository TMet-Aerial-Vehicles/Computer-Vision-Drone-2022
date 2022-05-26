import time
import sys
from qr.qr_reader import QRReader
from sound import countdown, play_quick_sound
from pixhawk import PixHawk
from cv2 import cv2
from datetime import datetime

import logging
from logging_script import start_logging
start_logging()


# Overview
# Reads QR
# Drone connect and takeoff to destination
# Record visuals from QR to flying


if __name__ == "__main__":
    # START PROGRAM

    # Boot camera
    camera = cv2.VideoCapture(0)

    # Get camera params
    frame_width = int(camera.get(3))
    frame_height = int(camera.get(4))
    cam_size = (frame_width, frame_height)

    # Create video save location
    loc = f"../videos/video-test-{datetime.today().strftime('%d-%H-%M-%S')}.avi"
    vid_writer = cv2.VideoWriter(loc, cv2.VideoWriter_fourcc(*'MJPG'), 10,
                                 cam_size)

    try:
        # Sleep to load camera
        time.sleep(5)
        # Test that camera is ready
        if camera.isOpened():
            time.sleep(1)
        else:
            raise IOError("Unable to open webcam")
    except:
        logging.info("Unable to open camera capture")
        sys.exit(1)

    # Play sound to signify qr reading started
    play_quick_sound(5)

    # Detect QR from image feeds and Decode/Format Message
    qrr = QRReader()

    # Live Feed
    qrr.read(camera=camera, active_display=True, display_time=20)
    # From Image
    # img_path = "/Users/craig/Projects/JTC_ComputerVision/sampleQR2.png"
    # qrr.read(active_display=display_qr, image=img_path)

    # Play sound to signify qr reading started
    play_quick_sound(5)

    # Read QR and coordinates
    if qrr.message:
        logging.info(qrr.message)
        longitude = qrr.message.longitude
        latitude = qrr.message.latitude
    else:
        logging.info("Unable to detect QR")
        sys.exit()

    # 20 sec countdown,
    countdown(20)
    play_quick_sound(5)

    # Instantiate drone
    logging.info("Connect to drone")
    drone = PixHawk(min_altitude=30, max_altitude=50,
                    boundary_circle=True, boundary_radius=3000)

    play_quick_sound(3)
    logging.info("Taking off")
    drone.takeoff()

    # Fly to position
    logging.info("Going to target")
    drone.move(latitude, longitude)

    # Start capturing video feed
    while True:

        ret, frame = camera.read()
        if ret is True:
            # Save to video feed
            vid_writer.write(frame)

            # Save image
            cv2.imwrite(f"../images/video-test-{datetime.today().strftime('%Y-%m-%d-%H-%M-%S')}.jpg", frame)

        # When drone reaches location, break

        break

    camera.release()
    vid_writer.release()

    # Close all the frames
    cv2.destroyAllWindows()
