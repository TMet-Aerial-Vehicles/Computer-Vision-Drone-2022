import cv2
import numpy as np
from pyzbar.pyzbar import decode


# img = cv2.imread("qr_1.png")
capture = cv2.VideoCapture(0)
capture.set(3, 640)
capture.set(4, 480)

# Keep running camera until SIGINT
while True:
    # Engage camera
    success, img = capture.read()

    # Decode(img) is an array of data; cycle through to find embedded data
    for qr in decode(img):

        # Converts embedded data to string format
        embedded_data = qr.data.decode('utf-8')
        print(embedded_data)

        # Add border detection and overlay text
        border = np.array([qr.polygon], np.int32)
        border = border.reshape((-1, 1, 2))
        border_text = qr.rect

        cv2.polylines(img, [border], True, (255, 0, 255), 8)
        cv2.putText(img, embedded_data,
                    (border_text[0], border_text[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    # code = decode(img)
    # print(code)
    # print(code[0][0].decode('utf-8'))

    cv2.imshow('Result', img)
    cv2.waitKey(1)
