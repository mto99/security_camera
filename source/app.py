from flask import Flask, render_template, Response, request
import os
from cv2 import destroyAllWindows
import lib.processing as process


app = Flask(__name__, template_folder='./templates')

#logged_in=False


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/camera')
def camera():
    return Response(process.frames(), \
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/requests', methods=['POST','GET']) 
def button_request():

    if request.method == 'POST':
        # Button requests
        if request.form.get('capture') == 'Capture':
            process.capture = 1
        elif request.form.get('negative') == 'Negativ':
            process.negative = not process.negative

    elif request.method == 'GET':
        return render_template('index.html')
    return render_template('index.html')

@app.route('/images')
def get_images():
    return render_template('images.html')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
    #app.run()

process.cam.release()
destroyAllWindows()