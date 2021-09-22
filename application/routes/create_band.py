from flask import Flask, redirect, request, render_template, session
from flask.helpers import url_for
from app import app

from utilities.db import db
import routes.manage_bands

@app.route("/create-band")
def create_band():
    #user-serviceen
    session_name = session.get("username")

    #saadaan haettua user_id session perusteella
    sql = "SELECT id, hashed_password FROM users WHERE username=:session_name"
    result = db.session.execute(sql, {"session_name":session_name})
    user = result.fetchone()
    id = user.id

    #get instruments tjsp.
    sql = "SELECT instrument_name FROM instruments"
    result = db.session.execute(sql)
    instruments = result.fetchall()
        
    #tarvii muuallakin, voi eriyttää, eli stripataan turhat pois
    for i in range(len(instruments)):
        instruments[i] = str(instruments[i]).strip("(,')")

    return render_template("create_band.html", user = user, id = id, instruments = instruments)
        
        
@app.route("/create-band", methods = ["POST"])
def create_band_new():
    #saadaan noi lomakkeesta
    username = session["username"]

    band_name = request.form["band_name"]
    band_description = request.form["description"]
    own_role = request.form["own_instrument"]

    #roolit pois noista 1_instrument jnne.
    roles = []

    for i in range(1, 9):
        roles.append(str(i) + "_instrument")

    instrument_roles = []

    instrument_roles.append(own_role)

    for i in range(8):
        role = request.form[roles[i]]
        instrument_roles.append(role)

    #db_service
    #id selville usersista
    sql = "SELECT id FROM users WHERE username = :username"
    result = db.session.execute(sql, {"username":username})
    id = int(str(result.fetchone()).strip("(,')"))

    #tungetaan bändi db:hen
    sql = "INSERT INTO bands (band_name, band_description, user_id) VALUES (:band_name, :band_description, :id)"
    db.session.execute(sql, {"band_name":band_name, "band_description":band_description, "id":id})
    db.session.commit()

    #etitään bändin id
    sql = "SELECT id FROM bands WHERE band_name = :band_name"
    result = db.session.execute(sql, {"band_name":band_name})
    band_id = int(str(result.fetchone()).strip("(,')"))

    #tungetaan liitostauluun molempien id:t
    sql = "INSERT INTO usersbands (band_id, user_id) VALUES (:band_id, :user_id)"
    db.session.execute(sql, {"band_id":band_id, "user_id":id})
    db.session.commit()

    #bandsinstrumentsiin oikeet id:t
    for i in range(len(instrument_roles)):
        instrument_name = instrument_roles[i]
        
        if instrument_name == "None":
            continue
        
        sql = "SELECT id FROM instruments WHERE instrument_name = :instrument_name"
        result = db.session.execute(sql, {"instrument_name":instrument_name})
        instrument_id = int(str(result.fetchone()).strip("(,')"))
        
        sql = "INSERT INTO bandsinstruments (instrument_id, band_id) VALUES (:instrument_id, :band_id)"
        db.session.execute(sql, {"instrument_id":instrument_id, "band_id":band_id})
        db.session.commit()

    return redirect("/manage-bands")
    