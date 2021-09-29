from flask import Flask, redirect, request, render_template, session
from app import app
import re

from utilities.db import db

import bands.views
import gigs.views
import gigs.models
import users.models

session_name = None

@app.route("/main-page")
def front_page():
    gigs_dict = gigs.models.get_gigs_and_players(False)
    return render_template("front_page.html", gigs = gigs_dict["users"], gigs_count = len(gigs_dict), instruments = gigs_dict["instruments"])

#tää omaan reitittimeen tai jotain?
@app.route("/sign-up/<int:gig_id>", methods = ["POST"])
def sign_up_for_gig(gig_id):
    instrument_name = request.form["instrument_chosen"]

    gigs.models.sign_up_for_gig(instrument_name, gig_id)

    return redirect("/main-page")
