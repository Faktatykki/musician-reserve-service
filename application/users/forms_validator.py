from flask import Flask, redirect, request, render_template, session
from werkzeug.security import check_password_hash, generate_password_hash

from app import app

import re
from os import getenv
from utilities.db import db

import users.models

def validate_create_user(username, password, password_again):
    error_message = None
    string_check = re.compile('[@_!#$%^&*()<>?/\|}{~:]')

    case_insensitive_user_query = users.models.get_user_case_insensitive(username)

    if len(case_insensitive_user_query) > 0:
        error_message = "Käyttäjänimi on jo olemassa"
        return error_message

    if len(username) < 3 or len(username) > 20:
        error_message = "Käyttäjänimen pituus pitää olla vähintään 3 merkkiä ja enintään 20"
        return error_message
    
    if string_check.search(username) is not None:
        error_message = "Käyttäjänimessä ei saa olla erikoismerkkejä kuten: @_!#$%^&*()<>?/\|}{~:"
        return error_message

    if len(password) < 8 or len(password) > 25:
        error_message = "Salasanan pituus pitää olla vähintään 8 merkkiä ja enintään 25"
        return error_message

    if password != password_again:
        error_message = "Salasanat eivät täsmää"
        return error_message

    return error_message
