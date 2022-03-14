from qr_reader import QRReader
from detection import Detection
from serial_communication import SerialCommunication
from calculations import intruder_centre_offset, bounding_box_centroid, \
    calculate_intruder_position
from cv2 import cv2
from datetime import datetime
import sys
# Main Python script


def read_qr():
    """
    Using input image, finds QR code within the image, and outputs its data

    Returns: qr text data message from qr code read
    """
    qrr = QRReader()
    display_qr = False   # Whether to continuously display QR captured

    # Saved Image
    img_path = "/Users/craig/Projects/JTC_ComputerVision/sampleQR1.png"
    qrr.read(active_display=display_qr, image=img_path)

    # Live Input
    # qrr.read(active_display=display_qr)

    # May require double pass, ensure QR message is consistent across reads
    # Read QR twice, and return if same data

    print(qrr.message)
    return qrr.message


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
        bounding_boxes = d.intruder_detection(frame, display_detection=False)

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
    # read_qr()

    # Set up connection with Arduino
    ser = SerialCommunication()

    detection()

    # Possible commands:
    # init - initialize the Detection class
    # qr - init and read qr codes
    # end - end script
    # detect single/continuously
    # stop, pause and continue detection
    #
