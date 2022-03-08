from cv2 import cv2
import numpy as np
import time
from pyzbar.pyzbar import decode


class QRReader:

    def __init__(self):
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
            msg = self.__qr_read(img)

            if msg is not None:
                qr_found = True
                self.message = msg
                print(msg)

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

    @staticmethod
    def __qr_read(img):
        """
        Uses pyzbar decoder to read img and display QR
        Args:
            img: img captured from video with CV2 or referenced image

        Returns:
            The QR message if found else None
        """
        embedded_data = None
        # Decode(img) is an array of QR data; iterate to find embedded data
        for qr in decode(img):
            # Converts embedded data to string format
            embedded_data = qr.data.decode('utf-8')

            # Add border detection and overlay text
            border = np.array([qr.polygon], np.int32)
            border = border.reshape((-1, 1, 2))
            border_text = qr.rect

            cv2.polylines(img, [border], True, (255, 0, 255), 8)
            cv2.putText(img, embedded_data,
                        (border_text[0], border_text[1]),
                         cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # Display QR found with overlaid border and text
        cv2.imshow('Result', img)
        cv2.waitKey(10)

        return embedded_data
