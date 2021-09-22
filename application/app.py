from flask import Flask
from werkzeug.utils import redirect

app = Flask(__name__)

import routes.login

@app.route("/")
def redirect_to_login():
    return redirect("/login")