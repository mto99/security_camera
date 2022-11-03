from flask import Flask, render_template, Response
import os

app = Flask(__name__)

logged_in=False


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/camera")
def camera():
    return Response()


@app.route("/login")
def login():
    # verify user
    return render_template("login.html")

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

