from os import abort
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from app import app

from utilities.db import db

import secrets

def get_session():
    session_name = session.get("username")
    return session_name

def logged_in():
    logged = False

    if get_user(get_session()) is not None:
        logged = True

    return logged

def get_user(username):
    user = None

    try:
        sql = "SELECT id, username, hashed_password FROM users WHERE username=:username"
        result = db.session.execute(sql, {"username":username})
        user = result.fetchone()
    except Exception as e:
        print(e)

    return user

def get_user_case_insensitive(username):
    users = None

    try:
        sql = "SELECT * FROM users WHERE username ILIKE :username"
        result = db.session.execute(sql, {"username":username})
        users = result.fetchall()
    except Exception as e:
        print(e)

    return users

def verify_login(user, password):
    if not user:
        return False
    else:
        hash_value = user.hashed_password
        if check_password_hash(hash_value, password):
            session["csrf_token"] = secrets.token_hex(16)
            session["username"] = user.username
            return True

    return False

def create_user(username, password):
    try:
        sql = "INSERT INTO users (username, hashed_password) VALUES (:username, :password)"
        hashed_password = generate_password_hash(password)

        db.session.execute(sql, {"username":username, "password":hashed_password})
        db.session.commit()
        
        return True
    except Exception as e:
        return False

def check_csrf_token(csrf_token):
    if session["csrf_token"] != csrf_token:
        abort(403)
        
def log_out():
    session.clear()