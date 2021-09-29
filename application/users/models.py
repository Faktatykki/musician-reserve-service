from flask import Flask, redirect, request, render_template, session
from werkzeug.security import check_password_hash, generate_password_hash
from app import app

from utilities.db import db

def get_session():
    session_name = session.get("username")
    return session_name

def get_user(username):
    user = None

    try:
        sql = "SELECT id, username, hashed_password FROM users WHERE username=:username"
        result = db.session.execute(sql, {"username":username})
        user = result.fetchone()
    except Exception as e:
        print(e)

    return user

def verify_login(user, password):
    if not user:
        return False
    else:
        hash_value = user.hashed_password
        if check_password_hash(hash_value, password):
            session["username"] = user.username
            return True

    return False

def create_user(username, password, password_again):
    sql = "INSERT INTO users (username, hashed_password) VALUES (:username, :password)"
    hashed_password = generate_password_hash(password)

    if password != password_again:
        #ilmoita väärä logini
        print("VÄÄRÄT")
    else:
        db.session.execute(sql, {"username":username, "password":hashed_password})
        db.session.commit()

def log_out():
    session.clear()