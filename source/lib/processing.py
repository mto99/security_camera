import cv2 as cv
from datetime import datetime
from os import path


capture = 0
grey=0
negative=0
cam = cv.VideoCapture(0) # 0 for system cam


def frames():
    global capture,grey,negative

    while True:
        # check if cam is available
        success, frame = cam.read()
        if success:

            if (capture):
                capture=0 # reset var
                save_capture('capture', frame)

            if (grey):
                frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

            if (negative):
                frame = cv.bitwise_not(frame)


            try:
                # Encode frame into memory buffer then to array of bytes
                ret, buffer = cv.imencode('.jpg', cv.flip(frame,1))
                frame = buffer.tobytes()
                # Adjust frame to a format, needed for a http response
                yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as ex:
                print(ex)
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
    filename = "img_{}.png".format(str(timestamp).replace(":",''))
    path = ""
    if method=="capture":
        path = "/app/images/captured/"
    elif method == "detect":
        path = "/app/images/detected/"

    cv.imwrite(path.join(path, filename), frame)
