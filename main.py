import time
import sys
from qr_reader import QRReader
from detection import Detection
# from serial_communication import SerialCommunication
from calculations import intruder_centre_offset, bounding_box_centroid, \
    calculate_intruder_position
from cv2 import cv2
from datetime import datetime
# Main Python script


def detection(image_path=None, detect_once=False):
    """
    Perform intruder detection
    Using input feed, find the intruder on the screen

    Args:
        image_path:
        detect_once:

    Returns:

    """
    # Initialize Detection class
    d = Detection()

    exit_call = False
    while not exit_call:
        # Create image frames or read from source
        # success, frame = capture.read()
        frame = cv2.imread(
            '/Users/craig/Projects/JTC_ComputerVision/images/multi2.png')

        # Perform intruder detection on frame
        bounding_boxes = d.intruder_detection(frame, display_detection=True)

        # Return offsets
        if len(bounding_boxes) == 0:
            # Not intruder detected
            # Spin
            # Check history
            pass
        elif len(bounding_boxes) > 1:
            # Multiple intruders detected
            pass
        else:
            # Determine centroid of bounding box
            x_centre, y_centre = bounding_box_centroid(bounding_boxes[0])
            print(f"Image Size: {frame.shape}")
            x_offset, y_offset = intruder_centre_offset(frame.shape[1],
                                                        frame.shape[0],
                                                        x_centre, y_centre)
            print(f"{datetime.now()}: Offset ({x_offset}, {y_offset})")

            # Save offset to file?
            pass

        # Calculate intruder position (long, lat)
        # long, lat = calculate_intruder_position(cam_height, cam_angle)

        # Check stdin for exit call
        # if detect_once or sys.stdin:
        if detect_once:
            exit_call = True


if __name__ == "__main__":
    # START PROGRAM

    # Boot camera
    camera = cv2.VideoCapture(0)

    try:
        # Sleep to load camera
        time.sleep(5)
        # Test that camera is ready
        if camera.isOpened():
            time.sleep(1)
        else:
            raise Exception
            # raise ConnectionError
    except:
        print("Unable to open camera capture")
        sys.exit(1)

    # Boot ports
    # Set up connection with Arduino
    # ser = SerialCommunication()

    # Detect QR from image feeds and Decode/Format Message
    qrr = QRReader()

    # Live Feed
    qrr.read(camera=camera, active_display=True, display_time=20)
    # From Image
    # img_path = "/Users/craig/Projects/JTC_ComputerVision/sampleQR2.png"
    # qrr.read(active_display=display_qr, image=img_path)

    # Read QR and coordinates
    if qrr.message:
        print(qrr.message)
        longitude = qrr.message.longitude
        latitude = qrr.message.latitude
    else:
        print("Unable to detect QR")
        sys.exit()

    # Send Coordinates to PixHawk loaded with ArduPilot
    # Figure out connection to send data

    # 20 sec countdown,
    time.sleep(20)

    # Fly to position

    # Figure out how to know when Drone reaches coordinates

    # Get image picture

    # Find intruder
    # detection(detect_once=True)

    # Rotate Camera to centre

    # Calculate drone position
    # Calculate intruder position

    # Save position data

    # Repeat get image picture and finding intruder

    #

    # END PROGRAM

    # SAFETY FEATURES
    # 1) Check drone coordinates. Ensure its within the given position
            # If flying outside, return back to starting position

    # 2) Anything goes wrong, send data to return to home, Dont land
