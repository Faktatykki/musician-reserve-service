from flask import Flask, redirect, request, render_template, session
from app import app

from utilities.db import db

@app.route("/manage-bands")
def manage_bands(): 
    #user-serviceen
    session_name = session.get("username")

    #id sessionin perusteella
    sql = "SELECT id, hashed_password FROM users WHERE username=:session_name"
    result = db.session.execute(sql, {"session_name":session_name})
    user = result.fetchone()
    id = user.id
    
    #db-service (eti kaikki userin bändit)
    sql = "SELECT DISTINCT band_name FROM bands, users, usersbands WHERE bands.id = usersbands.band_id AND usersbands.user_id=:id"
    result = db.session.execute(sql, {"id":id})
    bands = result.fetchall()
    
    return render_template("manage_bands.html", user = user, bands = bands, band_count = len(bands), id = id)