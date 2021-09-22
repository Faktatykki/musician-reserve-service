from flask import Flask, redirect, request, render_template, session
from app import app

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
    sql = "SELECT band_name, gig_date, city, venue, gig_description FROM gigs, usersgigs, \
           bands WHERE bands.id = gigs.band_id AND usersgigs.user_id = :id AND gigs.id = usersgigs.gig_id AND \
            own_gig = 'TRUE' ORDER BY gig_date"
    result = db.session.execute(sql, {"id":id})
    gigs = result.fetchall()

    for i in range(len(gigs)):
        print(gigs[i])

    #JATKA TÄSTÄ TAUON JÄLKEEN, tsiigasit noita keikkoja vaan silleen, että tulee omat keikat oikeassa muodossa


    return render_template("own_gigs.html", gigs = gigs, gigs_count = len(gigs))