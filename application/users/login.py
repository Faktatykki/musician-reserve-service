from flask import Flask, redirect, request, render_template, session
from werkzeug.security import check_password_hash, generate_password_hash

from app import app

from os import getenv
from utilities.db import db

import users.create_user
import main_page.main_page


@app.route("/login")
def login_front():
    if session.get("username") is not None:
        return redirect("/front-page")

    return render_template("login.html")

@app.route("/login", methods = ["POST"])
def login_post():
    username = request.form["username"]
    password = request.form["password"]

    #tämä serviceen
    sql = "SELECT id, hashed_password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()

    if not user:
        print("haloo")
    else:
        hash_value = user.hashed_password
        if check_password_hash(hash_value, password):
            session["username"] = username
            return redirect("/front-page")
    
    return redirect("/login")


    
    
