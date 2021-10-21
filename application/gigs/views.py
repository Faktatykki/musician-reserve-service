from flask import redirect, request, render_template
from app import app

import users.models
import bands.models
import gigs.models

import gigs.forms_validator

@app.route("/announce-gig")
def announce_gig_menu():
    user = users.models.get_user(users.models.get_session())
    bands_result = gigs.models.trim_results(bands.models.get_own_bands(user.id))

    return render_template("choose_band.html", user = user, bands = bands_result, band_count = len(bands_result))

@app.route("/announce-gig/<band>")
def announce_gig(band):
    band_name = request.args.get("selected_band")

    band_id = bands.models.get_band(band_name).id
    instruments = bands.models.get_bands_instruments(band_id)

    return render_template("announce_gig.html", message = None, band = band_name, instruments = instruments)

@app.route("/announce-gig/<band>", methods = ["POST"])
def announce_gig_post(band):
    csrf_token = request.form["csrf_token"]
    users.models.check_csrf_token(csrf_token)

    gig_date = request.form["gig_date"]
    city = request.form["city"]
    venue = request.form["venue"]
    gig_description = request.form["description"]
    instrument_name = request.form["instrument_chosen"]
    
    band_id = bands.models.get_band(band).id

    messages = gigs.forms_validator.validate_announce_gig(gig_date, city, venue, gig_description, instrument_name)
    instruments = bands.models.get_bands_instruments(band_id)

    if len(messages) == 0:
        if gigs.models.announce_gig(gig_date, city, venue, gig_description, instrument_name, band):
            return render_template("error.html", message = "Keikka ilmoitettu!", link_back = "/own-gigs", link_name = "Omat ilmoitetut keikat")
        else:
            return render_template("announce.gig.html", messages = ["Jotain meni pieleen..."])
    else:
        return render_template("announce_gig.html", messages = messages, band = band, instruments = instruments)     

@app.route("/delete-gig/<int:id>", methods = ["POST"])
def delete_gig(id):
    csrf_token = request.form["csrf_token"]
    users.models.check_csrf_token(csrf_token)
    
    gigs.models.delete_gig(id)
    
    return redirect("/own-gigs")

@app.route("/own-gigs")
def own_gigs(): 
    gigs_dict = gigs.models.get_gigs_and_players(True)
    return render_template("own_gigs.html", gigs = gigs_dict["users"], gigs_count = len(gigs_dict["gigs"]), instruments = gigs_dict["instruments"])

@app.route("/own-gigs-to-play")
def own_gigs_to_play():
    gigs_dict = gigs.models.get_gigs_and_players(None)
    return render_template("own_gigs_to_play.html", gigs = gigs_dict["users"], gigs_count = len(gigs_dict["gigs"]), instruments = gigs_dict["instruments"])

