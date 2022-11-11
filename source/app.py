from flask import Flask, render_template, Response, request
from os import environ, walk, getcwd
from cv2 import destroyAllWindows

import lib.processing as process
import lib.auth as auth


app = Flask(__name__, template_folder='./templates')


@app.route('/')
def index():
    if auth.logged_in == False:
        return render_template("login.html")
    return render_template('index.html')


@app.route("/login", methods=['POST','GET'])
def login():
    username = request.form.get('username')
    password = request.form.get('passwd')
    
    password_hashed = auth.createHash(password)
    if auth.authUser(username, password_hashed):
        auth.logged_in = True
        return render_template("index.html") # TODO RETURN RESPONSE
    return render_template("login.html")


@app.route("/logout")
def logout():
    auth.logged_in = False
    return render_template("login.html")


@app.route('/camera')
def camera():
    return Response(process.frames(), \
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/requests', methods=['POST','GET']) 
def button_request():
    if auth.logged_in == False:
        return render_template("login.html")

    if request.method == 'POST':
        # Button requests
        if request.form.get('capture') == 'Capture':
            process.capture = 1
        elif request.form.get('negative') == 'Negativ':
            process.negative = not process.negative

    elif request.method == 'GET':
        return render_template('index.html')
    return render_template('index.html')


@app.route('/captured_images')
def get_cap_images():
    if auth.logged_in == False:
        return render_template("login.html")

    return render_template('cap_images.html')


@app.route('/images')
def get_images():
    if auth.logged_in == False:
        return render_template("login.html")
    return render_template('images.html')


@app.route('/images_request')
def requ_images():
    """
    Get all filenames and return it
    """
    if auth.logged_in == False:
        return render_template("login.html")

    f =[]
    im_dir = "source/static/"
    # im_dir = "/app/images/detected/"
    for i in walk(im_dir):
        f.extend(i)
    print(getcwd())
    print(f)
    joined = ','.join(f[-1])
    lst_joined = [joined]
    return Response(lst_joined)


@app.route('/captured_images_request')
def request_captured():
    if auth.logged_in == False:
        return render_template("login.html")

    f = []
    im_dir = "source/static/captured"
    for i in walk(im_dir):
        f.extend(i)
    print(getcwd())
    print(f)
    joined = ','.join(f[-1])
    lst_joined = [joined]
    return Response(lst_joined)


if __name__ == '__main__':
    port = int(environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
    #app.run()

process.cam.release()
destroyAllWindows()