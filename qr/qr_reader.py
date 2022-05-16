from cv2 import cv2
import numpy as np
import time
from pyzbar.pyzbar import decode


class QRReader:

    def __init__(self):
        self.raw_message = None
        self.message = None

    def read(self, camera, active_display=False, display_time=15, image=None):
        """
        Using input image, finds QR code within the image, and saves the
        decoded and formatted message

        Args:
            camera: OpenCV VideoCapture object
            active_display: (Boolean) Display the camera feed
            display_time: (int) How long to run the QR reader for
            image: optional (str) Path to image file

        Returns:

        """
        print(f"Starting QR Reader at {time.time()}")
        qr_found = False
        end_time = time.time() + display_time
        while not qr_found or (active_display and time.time() < end_time):
            print(f"Recapturing {time.time()}")
            if image:
                img = cv2.imread(image)
            else:
                success, img = camera.read()

            try:
                embedded_data = None
                # Decode(img) is an array of QRs; iterate to find embedded data
                for qr in decode(img):
                    # Converts embedded data to string format
                    embedded_data = qr.data.decode('utf-8')
                    print(embedded_data)

                    if active_display:
                        # Add border detection and overlay text
                        border = np.array([qr.polygon], np.int32)
                        border = border.reshape((-1, 1, 2))
                        border_text = qr.rect

                        cv2.polylines(img, [border], True, (255, 0, 255), 8)
                        cv2.putText(img, embedded_data,
                                    (border_text[0], border_text[1]),
                                    cv2.FONT_HERSHEY_PLAIN, 0.9,
                                    (255, 0, 255), 2)

                if embedded_data:
                    # Successful QR read
                    qr_found = True
                    if check_msg_format(embedded_data):
                        self.raw_message = embedded_data
                        self.message = msg_decoder(embedded_data)
                else:
                    if image:
                        # Passed in image, only attempt decoding once
                        break

                if active_display:
                    # Display QR found with overlaid border and text
                    cv2.imshow('QR Reader Image', img)
                    cv2.waitKey(1000)
            except Exception:
                # Error in Pyzbar decoding, attempt again
                continue

    def old_read(self, active_display=False, display_seconds=10, image=None):
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
            display_seconds = 0.1
            capture = cv2.VideoCapture(0)
            capture.set(3, 640)
            capture.set(4, 480)
            success, img = capture.read()

        # if active_display, continue reading QR and displaying text
        qr_found = False
        while not qr_found or active_display:
            msg = qr_read(img, active_display, display_seconds)

            if msg is not None:
                qr_found = True
                self.raw_message = msg
                self.message = msg_decoder(msg)
                print(self.message)

            # Try QR Reader on an image once
            if image:
                break

            # Retry video image if QR not found
            print("Recapturing")
            success, img = capture.read()


def qr_read(img, active_display, display_time):
    """
    Uses pyzbar decoder to read img and display QR
    Args:
        img: img captured from video with CV2 or referenced image
        active_display: Boolean whether to display and draw text on QR
        display_time: time (seconds) to display QR for

    Returns:
        The QR message if found else None
    """
    embedded_data = None
    # Decode(img) is an array of QR data; iterate to find embedded data
    for qr in decode(img):
        # Converts embedded data to string format
        embedded_data = qr.data.decode('utf-8')
        print(embedded_data)

        # Set up QR border for all QR detected
        if active_display:
            # Add border detection and overlay text
            border = np.array([qr.polygon], np.int32)
            border = border.reshape((-1, 1, 2))
            border_text = qr.rect

            cv2.polylines(img, [border], True, (255, 0, 255), 8)
            cv2.putText(img, embedded_data,
                        (border_text[0], border_text[1]),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    if active_display:
        # Display QR found with overlaid border and text
        cv2.imshow('Result', img)
        cv2.waitKey(display_time * 1000)

    return embedded_data


def check_msg_format(msg):
    """
    Check the decoded QR message format, ensure it matches competition given
    Args:
        msg: (String) of decoded message to check format

    Returns: (Boolean) of correct formatting

    """
    msg_new = msg.splitlines()
    if len(msg_new) != 3:
        return False
    if "Questions:" not in msg_new[0]:
        return False

    qr_line_3 = msg_new[2].split(';')
    if len(qr_line_3) != 5:
        return False
    try:
        # Check longitude, latitude
        float(qr_line_3[4])
        float(qr_line_3[5])
    except ValueError:
        return False

    return True


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

    response['longitude'] = float(msg_data[4].strip())
    response['latitude'] = float(msg_data[5].strip())

    return response
