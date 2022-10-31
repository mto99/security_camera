from urllib import request
from flask import Blueprint, render_template, redirect
from flask import url_for, request, flash
from flask_login import login_user, login_required, logout_user
from . import db
from werkzeug.security import generate_password_hash, \
                            check_password_hash
from .models import User


auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template("login.html")


@auth.route('login', methods=["POST"])
def login_post():
    # verify user
    username = request.form.get("username")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False

    user = User.query.filter_by(username=username).first()

    # check if user exists
    # if wrong redirect to login
    if not user or not check_password_hash(user.password, password):
        flash("Please check your login details.")
        return redirect(url_for("auth.login"))

    # if login successful -> profile
    login_user(user, remember=remember)
    return redirect(url_for("main.profile"))


@auth.route('/signup')
def signup():
    return render_template("signup.html")


@auth.route("/signup", methods=['POST'])
def signup_post():
    # validate and ad user to db
    username = request.form.get("username")
    password = request.form.get("password")

    # check if user exists already (True if returns a user)
    user = User.query.filter_by(username=username).first()
    # redirect to userpage
    if user:
        flash("Username already exists!")
        return redirect(url_for("auth.signup"))
    
    # create a new user
    new_user = User(username=username, \
                password=generate_password_hash(password, method="sha256"))

    # add user to db
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("auth.login"))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))
