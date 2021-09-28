from flask import Flask, redirect, request, render_template, session
from app import app

from utilities.db import db

@app.route("/announce-gig")
def announce_gig_menu(): 
    #user-serviceen
    session_name = session.get("username")

    #id haetaan session-nimen perusteella
    sql = "SELECT id, hashed_password FROM users WHERE username=:session_name"
    result = db.session.execute(sql, {"session_name":session_name})
    user = result.fetchone()
    id = user.id

    #etitään ne omat bändit
    sql = "SELECT DISTINCT band_name FROM bands, users, usersbands WHERE bands.id = usersbands.band_id AND usersbands.user_id=:id"
    result = db.session.execute(sql, {"id":id})
    bands = result.fetchall()

    #tarvii muuallakin, voi eriyttää, eli stripataan turhat pois
    for i in range(len(bands)):
        bands[i] = str(bands[i]).strip("(,')")

    return render_template("choose_band.html", user = user, bands = bands, band_count = len(bands))

@app.route("/announce-gig/<band>")
def announce_gig(band):
    #url-forin antama parametri
    band_name = request.args.get("selected_band")#saa suoraan parametrista

    #etitään yksittäinen bändi
    sql = "SELECT * FROM bands WHERE band_name = :band_name"
    result = db.session.execute(sql, {"band_name":band_name})
    band = result.fetchone()
    band_id = band.id

    #etitään kaikki bändin instrumentit
    sql = "SELECT instrument_name FROM instruments, bandsInstruments WHERE bandsInstruments.band_id = :band_id \
               AND instruments.id = bandsInstruments.instrument_id"
    result = db.session.execute(sql, {"band_id":band_id})
    instruments = result.fetchall()

    return render_template("announce_gig.html", band = band_name, instruments = instruments)

@app.route("/announce-gig/<band>", methods = ["POST"])
def announce_gig_post(band):
    #user-service
    session_name = session.get("username")
    band_name = band

    gig_date = request.form["gig_date"]
    city = request.form["city"]
    venue = request.form["venue"]
    gig_description = request.form["description"]
    instrument_name = request.form["instrument_chosen"]

    #instrumentin id
    sql = "SELECT id FROM instruments WHERE instrument_name = :instrument_name"
    result = db.session.execute(sql, {"instrument_name":instrument_name})
    instrument = result.fetchone()
    instrument_id = instrument.id

    #id haetaan session-nimen perusteella
    sql = "SELECT id, hashed_password FROM users WHERE username=:session_name"
    result = db.session.execute(sql, {"session_name":session_name})
    user = result.fetchone()
    user_id = user.id

    #bändin id haetaan
    sql = "SELECT id FROM bands WHERE band_name=:band_name"
    result = db.session.execute(sql, {"band_name":band_name})
    band_id = int(str(result.fetchone()).strip("(',)"))

    #laitetaan keikka gigseihin
    sql = "INSERT INTO gigs (gig_date, city, venue, gig_description, band_id) VALUES (:gig_date, :city, :venue, :gig_description, (SELECT id FROM bands WHERE band_name = :band_name))"
    db.session.execute(sql, {"gig_date":gig_date, "city":city, "venue":venue, "gig_description":gig_description, "band_name":band_name})
    db.session.commit()

    #haetaan keikan id
    sql = "SELECT id FROM gigs WHERE gig_date = :gig_date AND city = :city AND venue = :venue AND gig_description = :gig_description AND band_id = :band_id"
    result = db.session.execute(sql, {"gig_date":gig_date, "city":city, "venue":venue, "gig_description":gig_description, "band_id":band_id})
    gig_id = int(str(result.fetchone()).strip("(',)"))

    #tekijälle suoraan keikka tauluun
    sql = "INSERT INTO usersgigs (gig_id, user_id, own_gig) VALUES (:gig_id, :user_id, 'TRUE')"
    db.session.execute(sql, {"gig_id":gig_id, "user_id":user_id, "band_id":band_id})
    db.session.commit()

    #keikan instrumentteihin suoraan myös
    sql = "INSERT INTO gigsInstruments (gig_id, instrument_id, user_id) \
           VALUES (:gig_id, :instrument_id, :user_id)"
    db.session.execute(sql, {"gig_id":gig_id, "instrument_id":instrument_id, "user_id":user_id})
    db.session.commit()

    return redirect("/announce-gig")