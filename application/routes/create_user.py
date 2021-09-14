from flask import Flask, redirect, request, render_template
from werkzeug.security import check_password_hash, generate_password_hash
from app import app

from utilities.db import db

@app.route("/create_user")
def create_user_page():
    return render_template("create_user.html")

@app.route("/create_user", methods = ["POST"])
def create_user():
    username = request.form["username"]
    password = request.form["password"]
    password_again = request.form["password_again"]

    #serviceen
    sql = "INSERT INTO users (username, hashed_password) VALUES (:username, :password)"
    hashed_password = generate_password_hash(password)

    if password != password_again:
        print("VÄÄRÄT")
    else:
        db.session.execute(sql, {"username":username, "password":hashed_password})
        db.session.commit()
    #jonnekin tänne asti

    return redirect("/login")