from flask import redirect, request, render_template
from app import app

import users.models
import instruments.models
import bands.models
import bands.forms_validator

@app.route("/create-band")
def create_band():
    user = users.models.get_user(users.models.get_session())
    instruments_result = instruments.models.get_all_instruments()

    return render_template("create_band.html", message = None, user = user, id = id, instruments = instruments_result)
        
@app.route("/create-band", methods = ["POST"])
def create_band_new():
    csrf_token = request.form["csrf_token"]
    users.models.check_csrf_token(csrf_token)

    band_name = request.form["band_name"]
    band_description = request.form["description"]

    user = users.models.get_user(users.models.get_session())
    instruments_result = instruments.models.get_all_instruments()

    #roolit pois noista 1_instrument jne.
    roles = []

    for i in range(1, 9):
        roles.append(str(i) + "_instrument")

    instrument_roles = []

    for i in range(8):
        role = request.form[roles[i]]
        instrument_roles.append(role)

    messages = bands.forms_validator.validate_create_band(band_name, band_description, instrument_roles)

    if len(messages) == 0:
        if bands.models.create_band(band_name, band_description, instrument_roles):
            return render_template("error.html", message = "Yhtye luotu!", link_back = "/announce-gig", link_name = "Mene ilmoittamaan keikka")
        else:
            return render_template("create_band.html", messages = ["Jotain meni pieleen..."])
    else:
        return render_template("create_band.html", messages = messages, user = user, id = id, instruments = instruments_result)

@app.route("/delete-band/<string:band_name>", methods = ["POST"])
def delete_band(band_name):
    csrf_token = request.form["csrf_token"]
    users.models.check_csrf_token(csrf_token)
    
    bands.models.delete_band(band_name)

    return redirect("/manage-bands")

#manage-bands
@app.route("/manage-bands")
def manage_bands(): 
    user = users.models.get_user(users.models.get_session())
    user_id = user.id

    band_results = bands.models.get_own_bands(user_id)
    
    return render_template("manage_bands.html", user = user, bands = band_results, band_count = len(band_results), id = user_id)