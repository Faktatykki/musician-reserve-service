from flask import Flask, redirect, request, render_template, session
from app import app

import re
import users.models
import bands.models
import gigs.models

from utilities.db import db

def get_instrument(instrument_name):
    try:
        sql = "SELECT * FROM instruments WHERE instrument_name = :instrument_name"
        result = db.session.execute(sql, {"instrument_name":instrument_name})
        instrument = result.fetchone()
    except Exception as e:
        print(e)

    return instrument

def get_all_instruments():
    instruments = None

    try:
        sql = "SELECT instrument_name FROM instruments"
        result = db.session.execute(sql)
        instruments = result.fetchall()
    except Exception as e:
        print(e)

    return gigs.models.trim_results(instruments)

def insert_into_band_instruments(instrument_roles, band_id):
    
    for i in range(len(instrument_roles)):
        instrument_name = instrument_roles[i]

        if instrument_name == "None":
            continue

        instrument_id = get_instrument(instrument_name).id
        insert_into_band_instrument(instrument_id, band_id)

def insert_into_band_instrument(instrument_id, band_id):
    try:
        sql = "INSERT INTO bandsinstruments (instrument_id, band_id) VALUES (:instrument_id, :band_id)"
        db.session.execute(sql, {"instrument_id":instrument_id, "band_id":band_id})
        db.session.commit()
    except Exception as e:
        print(e)

def get_instrument_by_name(instrument_name):
    instrument = None

    try:
        sql = "SELECT id FROM instruments WHERE instrument_name = :instrument_name"
        result = db.session.execute(sql, {"instrument_name":instrument_name})
        instrument = result.fetchone()
    except Exception as e:
        print(e)

    return instrument

def insert_instrument_to_gig(gig_id, instrument_id, user_id):
    try:
        sql = "INSERT INTO gigsinstruments (gig_id, instrument_id, user_id) VALUES (:gig_id, :instrument_id, :user_id)"
        db.session.execute(sql, {"gig_id":gig_id, "instrument_id":instrument_id, "user_id":user_id})
        db.session.commit()
    except Exception as e:
        print(e)



    
