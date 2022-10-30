from flask import Flask
from flask_login import LoginManager
from flask import render_template
import cv2 as cv
import time, datetime
import numpy as np



app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')


@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/cam")
def cam():
    raise NotImplementedError


