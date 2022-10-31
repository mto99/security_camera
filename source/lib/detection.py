from copyreg import constructor
from datetime import datetime
import cv2 as cv
import os


global neg,capture,motion


camera = cv.VideoCapture(0)


def negative(frame):
    """
    This function applies a negative filter on the frame
    """
    return cv.bitwise_not(frame)


def capture(frame):
    """
    This function creates a capture of the current stream
    """
    capture=0
    timestamp = datetime.now()
    file_name = os.path.sep.join(['captures', "capture_{}.png".format(str(timestamp).replace(":",''))])
    cv.imwrite(file_name, frame)


def detect_motion():
    """
    This function detects motion on the frame.
    The detected areas will be contoured by a rectangle
    """
    while True:
        check, frame = camera.read()

        static_background = None
        motion = 0

        # convert to gray scale
        gray_camera = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        # Convert grayed image to GaussianBlur
        gray_camera = cv.GaussianBlur(gray_camera, (21,21), 0)

        if static_background is None:
            static_background = gray_camera
            
        # Get difference between background and current frame (GaussianBlur)
        diff_frame = cv.absdiff(static_background, gray_camera)
        
        # If change is greater than 30 (between static background and current frame)
        # it will show white
        thresh_frame = (diff_frame, 30, 255, cv.THRESH_BINARY)[1]
        thresh_frame = cv.dilate(thresh_frame, None, iterations=2)

        # find contours of motion
        contours,_ = cv.findContours(thresh_frame.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        for c in contours:
            if cv.contourArea(c) < 10000:
                continue
            motion = 1

            # making rectangle on frame
            (x,y,w,h) = cv.boundingRect(c)
            cv.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 3)

detect_motion()

camera.release()