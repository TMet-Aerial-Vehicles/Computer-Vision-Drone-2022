"""
Perform intruder detection using OpenCV's HOG SVM for detection
"""

import numpy as np
from cv2 import cv2
from imutils.object_detection import non_max_suppression

# Performing person detection
# Combine Histogram of Object Detection (HOG) with Canny Edge Detection

# Possible Detection Ideas:
# Edge detection
# Histogram of Object Detection
# Image Smoothing and Thresholding for Binary Image,


class Detection:

    def __init__(self):
        # Initialize the HOG descriptor/person detector
        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    def intruder_detection(self, frame, display_detection=True):
        """
        Perform intruder detection by identifying person in frame and
        creating bounding boxes around persons

        Args:
            frame: input image
            display_detection: boolean of whether to display image with boxes

        Returns: List of bounding boxes of every intruder found

        """
        # Possible image resizing needed
        # Possible Gaussian blur needed to remove noise
        # frame = cv2.GaussianBlur(frame, (3, 3), 0)

        # Perform detection
        # hog = cv2.HOGDescriptor()
        # self.hogs = hog.setSVMDetector(
        #     cv2.HOGDescriptor_getDefaultPeopleDetector())
        boxes, weights = self.hog.detectMultiScale(frame, winStride=(8, 8))
        boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])

        # Apply non-maxima suppression to reduce overlapped boxes
        final_boxes = non_max_suppression(boxes, probs=None, overlapThresh=0.65)

        # Display detection
        for (xA, yA, xB, yB) in final_boxes:
            # display the detected boxes in the colour picture
            cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)

        # Write the output video
        if display_detection:
            # out.write(frame.astype('uint8'))
            # Display the resulting frame
            cv2.imshow('frame', frame)
            cv2.waitKey(10000)
            # cv2.imshow('Contours', cnts)
            # break

        return final_boxes
