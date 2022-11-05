import cv2 as cv


class MDetection:

    def __init__(self):
        self.static_background = None


    def motion_detection(self,frame):
        """
        This function detects any motion on the camera
        and contour the area of motion
        Param:
            - cam: Capture video variable of the imports capture var
            - frame: frame of cam.read()
        """
        motion = False

        # Convert frame to grey scale, then to GaussianBlur
        grey = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        grey = cv.GaussianBlur(grey, (21,21), 0)

        # Assign background. The motion detection is working with the second iteration
        # after we have a previous frame to compare
        if self.static_background is None:
            self.static_background = grey

        # Compare difference between static background and frame (grey)
        frame_diff = cv.absdiff(self.static_background, grey)

        frame_thresh = cv.threshold(frame_diff, 30, 255, cv.THRESH_BINARY)[1]
        frame_thresh = cv.dilate(frame_thresh, None, iterations=2)

        # Get contour of motion
        countours,_ = cv.findContours(frame_thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        for c in countours:
            if cv.contourArea(c) < 10000:
                continue
            motion = True

            # Contour surrounded with rectangle
            (x,y,w,h) = cv.boundingRect(c)
            cv.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), thickness=3)

            cv.putText(frame, '!', (20,30), cv.FONT_HERSHEY_SIMPLEX, \
                        1, (20,20,255), 2)
            cv.imshow('video',frame) # display text
