from cv2 import cv2
import numpy as np
import time
from pyzbar.pyzbar import decode


class QRReader:

    def __init__(self):
        self.raw_message = None
        self.message = None

    def read(self, active_display=False, display_seconds=30, image=None):
        """
        Reads a QR code from an image or using camera
        Args:
            active_display: boolean on actively displaying QR image with text
            display_seconds: number of seconds to display QR when active_display
            image: path to qr image file

        Returns:
            The QR message if found else None
        """
        if image:
            capture = None
            img = cv2.imread(image)
        else:
            capture = cv2.VideoCapture(0)
            capture.set(3, 640)
            capture.set(4, 480)
            success, img = capture.read()

        qr_found = False
        end_time = time.time() + display_seconds
        # if active_display, continue reading QR and displaying text
        while not qr_found or active_display:
            msg = qr_read(img, display=active_display)

            if msg is not None:
                qr_found = True
                self.raw_message = msg
                self.message = msg_decoder(msg)
                print(self.message)

            # Try QR Reader on an image once
            if image:
                # Display QR for input seconds if active_display True
                if active_display:
                    time.sleep(display_seconds)
                break

            # Show QR code reader image for up to display_seconds
            if time.time() > end_time:
                break

            # Retry video image if QR not found
            print("Recapturing")
            success, img = capture.read()


def qr_read(img, display=False):
    """
    Uses pyzbar decoder to read img and display QR
    Args:
        img: img captured from video with CV2 or referenced image
        display: Boolean whether to display and draw text on QR

    Returns:
        The QR message if found else None
    """
    embedded_data = None
    # Decode(img) is an array of QR data; iterate to find embedded data
    for qr in decode(img):
        # Converts embedded data to string format
        embedded_data = qr.data.decode('utf-8')

        if display:
            # Add border detection and overlay text
            border = np.array([qr.polygon], np.int32)
            border = border.reshape((-1, 1, 2))
            border_text = qr.rect

            cv2.polylines(img, [border], True, (255, 0, 255), 8)
            cv2.putText(img, embedded_data,
                        (border_text[0], border_text[1]),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    if display:
        # Display QR found with overlaid border and text
        cv2.imshow('Result', img)
        cv2.waitKey(10)

    return embedded_data


def msg_decoder(msg):
    """Formulate the QR code into a digestible dictionary

    Format:
    Questions:\n
    Word word? Word word? Word word?\n
    Date; Time; device_id; sensor_id; longitude; latitude

    Example Format
    Questions:
    Tshirt colour? Hair colour? Item carried?
    2021-08-18; 16:37; S_Comm1; S02; 49.90440649280493; -98.27393447717382

    """
    msg_new = msg.splitlines()
    response = {
        'questions': msg_new[1].split('?')
    }

    msg_data = msg_new[2].split(';')
    response['date'] = msg_data[0].strip()
    response['time'] = msg_data[1].strip()
    response['device_id'] = msg_data[2].strip()
    response['sensor_id'] = msg_data[3].strip()

    # response['longitude'] = int(msg_data[4].strip())
    # response['latitude'] = int(msg_data[5].strip())

    # Temp Fix, CONOPS uses ',' between long and lat,
    response['longitude'] = float(msg_data[4].split(',')[0].strip())
    response['latitude'] = float(msg_data[4].split(',')[1].strip())

    return response
