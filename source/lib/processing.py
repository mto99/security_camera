import cv2 as cv
from datetime import datetime
from os import path
import lib.detection as detection


global capture, negative
capture = 0
negative = 0
cam = cv.VideoCapture(0) # 0 for system cam

# get videocapture width
capwidth = cam.get(cv.CAP_PROP_FRAME_WIDTH) # float

# init object of detection
md = detection.MDetection()

def frames():
    global capture

    while True:
        # check if cam is available
        success, frame = cam.read()
        print(f"FRAME: {frame}")
        if success:

            if (negative):
                frame = cv.bitwise_not(frame)
                cv.putText(frame,"N",(50,50),cv.FONT_HERSHEY_SIMPLEX, 1, (20,20,255), 2)

            if (capture):
                capture=0 # reset var
                save_capture('capture', frame)

            # Motion detection. Happens always
            md.motion_detection(frame)

            try:
                # Encode frame into memory buffer then to array of bytes
                _, buffer = cv.imencode('.jpg', cv.flip(frame,1))
                frame = buffer.tobytes()
                # Adjust frame to a format, needed for a http response
                yield(b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception:
                pass

        else:
            pass


def save_capture(method:str, frame):
    """
    This function saves the captured images
    Param:
        - method: 'capture' or 'detect'
    The target directories of the capture are independent of the param
    For capture: '/app/images/captured'
    For detect: '/app/images/detected'
    """
    timestamp = datetime.now()
    filename = "img_{}".format(str(timestamp).replace(":",'')
                                            .replace(" ",'_')
                                            .replace(".","_"))
    filename = filename+".png"
    filepath = ""
    if method=="capture":
        filepath = "source/static/captured/"
    elif method == "detect":
        filepath = "source/static/detected/"
    filepath = filepath+filename
    cv.imwrite(filepath, frame)
