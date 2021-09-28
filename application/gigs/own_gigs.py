from flask import Flask, redirect, request, render_template, session
from app import app
import re

from utilities.db import db


@app.route("/own-gigs")
def own_gigs(): 
    #user-serviceen
    session_name = session.get("username")

    #db-serviceen
    sql = "SELECT id, hashed_password FROM users WHERE username=:session_name"
    result = db.session.execute(sql, {"session_name":session_name})
    user = result.fetchone()
    id = user.id

    #user-service/db
    sql = "SELECT gigs.id, band_name, band_id, gig_date, city, venue, gig_description FROM gigs, usersgigs, \
           bands WHERE bands.id = gigs.band_id AND usersgigs.user_id = :id AND gigs.id = usersgigs.gig_id AND \
            own_gig = 'TRUE' ORDER BY gig_date"
    result = db.session.execute(sql, {"id":id})
    gigs = result.fetchall()

    for i in range(len(gigs)):
        print(gigs[i])
    
    #TÄSTÄ ETEENPÄIN SAMA KUIN FRONT_PAGESSA
    #hashmappi keikoille ja niiden soittajille
    gigs_users_dict = {}
    #hashmappi keikoille ja tarvittaville soittimille
    gigs_instruments_dict = {}

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

        pattern = r"[\'()]"

        for j in range(len(players)):
            players[j] = re.sub(pattern, '', str(players[j]))
            
        for k in range(len(instruments)):
            instruments[k] = re.sub(pattern, '', str(instruments[k]))#tee toiseenkin oikee regex

        gigs_instruments_dict[gigs[i]] = instruments
        gigs_users_dict[gigs[i]] = players
    #TÄNNEs

    #JATKA TÄSTÄ TAUON JÄLKEEN, tsiigasit noita keikkoja vaan silleen, että tulee omat keikat oikeassa muodossa


    return render_template("own_gigs.html", gigs = gigs_users_dict, gigs_count = len(gigs), instruments = gigs_instruments_dict)