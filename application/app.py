from os import getenv
from flask import Flask
from werkzeug.utils import redirect

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

import users.views

@app.route("/")
def redirect_to_login():
    return redirect("/login")
