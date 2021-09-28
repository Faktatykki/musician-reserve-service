from flask import Flask, redirect, request, render_template, session
from app import app
import re

from utilities.db import db

import gigs.announce_gig
import gigs.own_gigs
import bands.manage_bands
import bands.create_band

session_name = None

@app.route("/front-page")
def front_page():
    #serviceen ja myös toi profile-service
    session_name = session.get("username")
    
    #if session_name is not None: eli userin ID
    sql = "SELECT id, hashed_password FROM users WHERE username=:session_name"
    result = db.session.execute(sql, {"session_name":session_name})
    user = result.fetchone()
    id = user.id
    #else:
    
    #hashmappi keikoille ja niiden soittajille
    gigs_users_dict = {}
    #hashmappi keikoille ja tarvittaville soittimille
    gigs_instruments_dict = {}

    #userserviceen/db, eli haetaan kaikki keikat PAITSI OMAT
    sql = "SELECT gigs.id, band_name, band_id, gig_date, city, venue, gig_description FROM gigs, usersgigs, \
           bands WHERE bands.id = gigs.band_id AND usersgigs.user_id != :id AND gigs.id = usersgigs.gig_id AND \
            own_gig = 'TRUE' ORDER BY gig_date"
    result = db.session.execute(sql, {"id":id})
    gigs = result.fetchall()

    #täytetään tyhjillä taulukoilla avainten arvot
    for i in range(len(gigs)):
        gigs_users_dict[gigs[i]] = []
        gigs_instruments_dict[gigs[i]] = []

    #tämäkin johonkin sovelluslogiikkaan
    for i in range(len(gigs)):
        gig_id = gigs[i].id
        band_id = gigs[i].band_id
        
        #ketkä soittaa ja mitä keikalla jo
        sql = "SELECT users.username, instruments.instrument_name FROM users \
               INNER JOIN usersGigs ON users.id = usersGigs.user_id AND usersGigs.gig_id = :gig_id \
               INNER JOIN gigsInstruments ON gigsInstruments.gig_id = :gig_id AND gigsInstruments.user_id = users.id \
               INNER JOIN instruments ON gigsInstruments.instrument_id = instruments.id" 
       
        result = db.session.execute(sql, {"gig_id":gig_id})
        players = result.fetchall()
        #instrumentit bändin/keikan
        sql = "SELECT instrument_name FROM instruments, bandsInstruments WHERE bandsInstruments.band_id = :band_id \
               AND instruments.id = bandsInstruments.instrument_id"
        result = db.session.execute(sql, {"band_id":band_id})
        instruments = result.fetchall()

        pattern_players = r"[\'()]"
        pattern_instruments = r"[\'(,)]"

        for j in range(len(players)):
            players[j] = re.sub(pattern_players, '', str(players[j]))
            
        for k in range(len(instruments)):
            instruments[k] = re.sub(pattern_instruments, '', str(instruments[k]))#tee toiseenkin oikee regex

        gigs_instruments_dict[gigs[i]] = instruments
        gigs_users_dict[gigs[i]] = players
    
    return render_template("front_page.html", gigs = gigs_users_dict, gigs_count = len(gigs), instruments = gigs_instruments_dict)

#tää omaan reitittimeen tai jotain?
@app.route("/sign-up/<int:gig_id>", methods = ["POST"])
def sign_up_for_gig(gig_id):
    instrument_name = request.form["instrument_chosen"]
    session_name = session.get("username")

    #if session_name is not None: eli userin ID
    sql = "SELECT id, hashed_password FROM users WHERE username=:session_name"
    result = db.session.execute(sql, {"session_name":session_name})
    user = result.fetchone()
    user_id = user.id

    #instrumentin id
    sql = "SELECT id FROM instruments WHERE instrument_name = :instrument_name"
    result = db.session.execute(sql, {"instrument_name":instrument_name})
    instrument_id = int(str(result.fetchone()).strip("(,')"))

    #yhdistetään keikka, käyttäjä ja instrumentti
    sql = "INSERT INTO gigsinstruments (gig_id, instrument_id, user_id) VALUES (:gig_id, :instrument_id, :user_id)"
    db.session.execute(sql, {"gig_id":gig_id, "instrument_id":instrument_id, "user_id":user_id})
    db.session.commit()

    #yhdistetään keikka ja käyttäjä
    sql = "INSERT INTO usersgigs (gig_id, user_id, own_gig) VALUES (:gig_id, :user_id, 'FALSE')"
    db.session.execute(sql, {"gig_id":gig_id, "user_id":user_id})
    db.session.commit()

    return redirect("/front-page")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")