from flask import Flask, redirect, request, render_template, session
from werkzeug.security import check_password_hash, generate_password_hash

from app import app

from os import getenv
from utilities.db import db

import main_page.views
import users.models

@app.route("/login")
def login_front():
    if session.get("username") is not None:
        return redirect("/main-page")

    return render_template("login.html")

@app.route("/login", methods = ["POST"])
def login_post():
    username = request.form["username"]
    password = request.form["password"]

    user = users.models.get_user(username)
    verify_login = users.models.verify_login(user, password)

    if verify_login:
        return redirect("/main-page") 
    
    return redirect("/login")

#create_user
@app.route("/create-user")
def create_user_page():
    return render_template("create_user.html")

@app.route("/create-user", methods = ["POST"])
def create_user():
    username = request.form["username"]
    password = request.form["password"]
    password_again = request.form["password_again"]

    users.models.create_user(username, password, password_again)

    return redirect("/login")

@app.route("/logout")
def logout():
    users.models.log_out()
    return redirect("/login")