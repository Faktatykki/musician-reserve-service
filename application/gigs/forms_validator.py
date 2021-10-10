from flask import Flask, redirect, request, render_template, session
from werkzeug.security import check_password_hash, generate_password_hash

from app import app

import datetime
import re
from os import error, getenv
from utilities.db import db

def validate_announce_gig(gig_date, city, venue, gig_description, instrument_name):
    error_message = None
    
    gig_date_parsed = datetime.datetime.strptime(gig_date, "%Y-%m-%d").date()
    current_date = datetime.datetime.today().date()
 
    if gig_date_parsed < current_date:
        error_message = "Et voi palata menneisyyteen. Tarkista keikan päivämäärä"
        return error_message
    
    if len(city) < 1 or len(city) > 100:
        error_message = "Kaupungin pitää olla vähintään yhden merkin ja enintään 100 merkin pituinen"
        return error_message

    if len(venue) < 1 or len(venue) > 100:
        error_message = "Tapahtumapaikan pitää olla vähintään yhden merkin ja enintään 100 merkin pituinen"
        return error_message

    if len(gig_description) > 5000:
        error_message = "Tapahtumakuvaus saa olla enintään 5000 merkkiä pitkä"
        return error_message
    
    return error_message