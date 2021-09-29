from flask import Flask, redirect, request, render_template, session
from app import app

import re
import users.models
import bands.models
import instruments.models
import gigs.models

from utilities.db import db

@app.route("/announce-gig")
def announce_gig_menu(): 
    user = users.models.get_user(users.models.get_session())
    bands_result = bands.models.get_own_bands(user.id)

    return render_template("choose_band.html", user = user, bands = bands_result, band_count = len(bands_result))

@app.route("/announce-gig/<band>")
def announce_gig(band):
    #url-forin antama parametri
    band_name = request.args.get("selected_band")

    band_id = bands.models.get_band(band_name).id
    instruments = bands.models.get_bands_instruments(band_id)

    return render_template("announce_gig.html", band = band_name, instruments = instruments)

@app.route("/announce-gig/<band>", methods = ["POST"])
def announce_gig_post(band):
    gig_date = request.form["gig_date"]
    city = request.form["city"]
    venue = request.form["venue"]
    gig_description = request.form["description"]
    instrument_name = request.form["instrument_chosen"]
    
    gigs.models.announce_gig(gig_date, city, venue, gig_description, instrument_name, band)

    return redirect("/announce-gig")

@app.route("/own-gigs")
def own_gigs(): 
    gigs_dict = gigs.models.get_gigs_and_players(True)
    return render_template("own_gigs.html", gigs = gigs_dict["users"], gigs_count = len(gigs_dict), instruments = gigs_dict["instruments"])