from flask import redirect, request, render_template
from app import app

import bands.views
import gigs.views

import main_page.models
import gigs.models
import users.models

@app.route("/main-page")
def front_page():
    gigs_dict = gigs.models.get_gigs_and_players(False)
    
    band_count = main_page.models.get_band_count()
    gig_count = main_page.models.get_gig_count()
    avg_members = main_page.models.get_avg_count_members()

    return render_template("front_page.html", gigs = gigs_dict["users"], gigs_count = len(gigs_dict["gigs"]), instruments = gigs_dict["instruments"],
                            band_count = band_count, gig_count = gig_count, avg_members = avg_members)

#tää omaan reitittimeen tai jotain?
@app.route("/sign-up/<int:gig_id>", methods = ["POST"])
def sign_up_for_gig(gig_id):
    csrf_token = request.form["csrf_token"]
    users.models.check_csrf_token(csrf_token)
    
    instrument_name = request.form["instrument_chosen"]

    gigs.models.sign_up_for_gig(instrument_name, gig_id)

    return redirect("/main-page")

@app.route("/delete-sign-up/<int:gig_id>/<string:username>", methods = ["POST"])
def delete_sign_up(gig_id, username):
    csrf_token = request.form["csrf_token"]
    users.models.check_csrf_token(csrf_token)

    gigs.models.delete_sign_up(gig_id, username)

    return redirect(request.referrer)

