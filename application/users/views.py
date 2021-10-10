from flask import Flask, redirect, request, render_template, session
from werkzeug.security import check_password_hash, generate_password_hash

from app import app

from os import getenv
from utilities.db import db

import users.models
import users.forms_validator
import main_page.views

@app.before_request
def before_request():
    if request.path != "/login" and request.path != "/create-user" and request.path != "/logout":
        if not users.models.logged_in():
            return redirect("/login")
        
    
@app.route("/login")
def login_front():
    if users.models.logged_in():
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
    else:
        return render_template("error.html", message = "Kirjautuminen ei onnistunut, tarkista käyttäjätunnus ja salasana", link_back = "/login", link_name = "Kokeile uudelleen") 

@app.route("/create-user")
def create_user_page():
    if users.models.logged_in():
        return redirect("/main-page")

    return render_template("create_user.html")

@app.route("/create-user", methods = ["POST"])
def create_user():
    username = request.form["username"]
    password = request.form["password"]
    password_again = request.form["password_again"]

    message = users.forms_validator.validate_create_user(username, password, password_again)
    
    if message is None:
        if users.models.create_user(username, password):
            return render_template("error.html", message = "Kaikki ok! Käyttäjä luotu!", link_back = "/login", link_name = "Kirjautumiseen")
        else:
            return render_template("error.html", message = "Jotain meni pieleen..", link_back = "/create-user", link_name = "Kokeile uudelleen")
    else:
        return render_template("error.html", message = message, link_back = "/create-user", link_name = "Kokeile uudelleen")

@app.route("/logout")
def logout():
    users.models.log_out()
    return redirect("/login")