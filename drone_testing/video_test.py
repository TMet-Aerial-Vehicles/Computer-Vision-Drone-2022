from cv2 import cv2
from datetime import datetime

video = cv2.VideoCapture(0)


# We need to check if camera
# is opened previously or not

if video.isOpened() is False:
    print("Error reading video file")


# We need to set resolutions.
# so, convert them from float to integer.

frame_width = int(video.get(3))

frame_height = int(video.get(4))



size = (frame_width, frame_height)


# Below VideoWriter object will create
# a frame of above defined The output
# is stored in 'filename.avi' file.

result = cv2.VideoWriter(f"../videos/video-test-{datetime.today().strftime('%Y-%m-%d-%H-%M-%S')}.avi",
                         cv2.VideoWriter_fourcc(*'MJPG'), 10, size)



while(True):

    ret, frame = video.read()

    if ret is True:

        # Write the frame into the
        # file 'filename.avi'
        result.write(frame)

        # Save image
        cv2.imwrite(f"../images/video-test-{datetime.today().strftime('%Y-%m-%d-%H-%M-%S')}.jpg", frame)

        # Display the frame
        # saved in the file
        cv2.imshow('Frame', frame)

        # Press S on keyboard
        # to stop the process
        if cv2.waitKey(1) & 0xFF == ord('s'):
            break

    # Break the loop
    else:
        break


# When everything done, release
# the video capture and video
# write objects
video.release()
result.release()


# Closes all the frames
cv2.destroyAllWindows()

