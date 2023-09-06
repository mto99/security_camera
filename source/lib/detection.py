import cv2 as cv
import lib.processing as process
import lib.servo as servo


servomotor = servo.ServoCam()


class MDetection:

    def __init__(self):
        self.prev_background = None
        self.angle = servo.current_angle


    def motion_detection(self,frame, capwidth):
        """
        This function detects any motion on the camera
        and contour the area of motion
        Param:
            - cam: Capture video variable of the imports capture var
            - frame: frame of cam.read()
        """

        # Convert frame to grey scale, then to GaussianBlur
        grey = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        grey = cv.GaussianBlur(grey, (21,21), 0)

        # Assign background. The motion detection is working with the second iteration
        # after we have a previous frame to compare
        if self.prev_background is None:
            self.prev_background = grey
            

        # Compare difference between prev_background (previous frame) and current frame (grey)
        frame_diff = cv.absdiff(self.prev_background, grey)

        # Assign current frame to prev_background
        self.prev_background = grey

        frame_thresh = cv.threshold(frame_diff, 20, 255, cv.THRESH_BINARY)[1]
        frame_thresh = cv.dilate(frame_thresh, None, iterations=2)

        # Get contour of motion
        countours,_ = cv.findContours(frame_thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        for c in countours:
            if cv.contourArea(c) < 10000:
                continue

            # Contour surrounded with rectangle
            (x,y,w,h) = cv.boundingRect(c)
            cv.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), thickness=2)
            #print(f"COORDINATES - X: {x} | X2: {x+w}") # for debuging

            # get center on x-axis of countour
            contour_left = x
            contour_right = x+w

            # divide frame in 3 parts. The left, center and right part.
            # So it will be two broders: left and right
            left_border = capwidth/3
            right_border = capwidth/3*2
            
            # check where the contour is and define angle
            if contour_left < left_border and contour_right > right_border: # inleft and right
                servo.current_angle = 90
            elif contour_left < left_border and contour_right < right_border: # in left
                if servo.current_angle != 0:
                    servo.current_angle-=10
            elif contour_left > left_border and contour_right > right_border: # in right
                if servo.current_angle != 180:
                    servo.current_angle+=10
            else:
                pass

            # rotate camera
            servomotor.setAngle(servo.current_angle)
            

            process.save_capture('detect',frame)

            cv.putText(frame, '!', (20,30), cv.FONT_HERSHEY_SIMPLEX, \
                        1, (20,20,255), 2)

