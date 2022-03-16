"""
Performs any calculations needs to determine intruder location and offsets
"""
from typing import List


def intruder_centre_offset(img_width: int, img_height: int, intruder_x: int,
                           intruder_y: int):
    """
    Calculates the pixel offset from the image centre, needed to centre
    the intruder on the image
    Note:
        (0, 0) is top left corner of image
        intruder coordinates uses centre of bounded box

    Args:
        img_width: number of pixels in image width
        img_height: number of pixels in image height
        intruder_x: x position of intruder on image
        intruder_y: y position of intruder on image

    Returns: The (x, y) offset needed to centre the intruder on the image

    """
    change_x = intruder_x - (img_width // 2)
    change_y = intruder_y - (img_height // 2)
    return change_x, change_y


def bounding_box_centroid(bounding_box: List):
    """
    Calculate the centre of the given bounding box
    (x1, y1)-------------|
    |                    |
    |                    |
    |_____________(x2, y2)

    Args:
        bounding_box: List of coordinates containing 4 values,
                        top left x,y and bottom right x,y
                        format: [x1, y1, x2, y2]

    Returns: (x, y) coordinate
    """
    x1, y1, x2, y2 = bounding_box
    x_centre = (x2 - x1) // 2 + x1
    y_centre = (y2 - y1) // 2 + y1
    return x_centre, y_centre


def calculate_intruder_position():
    pass
