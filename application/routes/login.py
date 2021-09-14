from flask import Flask, redirect, request, render_template, session
from werkzeug.security import check_password_hash, generate_password_hash

from app import app

from os import getenv
from utilities.db import db

import routes.create_user
import routes.front_page

app.secret_key = getenv("SECRET_KEY")

@app.route("/login")
def login_front():

    if session.get("username") is not None:
        return redirect("/frontpage")

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
            return redirect("/frontpage")
    
    return redirect("/login")


    
    
