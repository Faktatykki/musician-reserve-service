from flask import Flask
from werkzeug.utils import redirect
from os import getenv

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

import routes.login

@app.route("/")
def redirect_to_login():
    return redirect("/login")