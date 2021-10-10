from flask import Flask, redirect, request, render_template, session
from werkzeug.security import check_password_hash, generate_password_hash

from app import app

import re
import bands.models
from utilities.db import db

def validate_create_band(band_name, band_description, instrument_roles):
    error_message = None
    string_check = re.compile('[%?]')

    case_insensitive_band_query = bands.models.get_band_case_insensitive(band_name)

    if len(case_insensitive_band_query) > 0:
         error_message = "Yhtye on jo olemassa"
         return error_message
         
    if len(band_name) < 1 or len(band_name) > 80:
        error_message = "Yhtyeen nimi ei voi olla tyhjä tai yli 80 merkkiä pitkä"
        return error_message

    if string_check.search(band_name) is not None:
        error_message = "Yhtyeen nimessä ei saa esiintyä seuraavia erikoismerkkejä: %?"
        return error_message

    if len(band_description) > 2000:
        error_message = "Rauhoitu, yhtyeen kuvaus pitäisi olla alle 2000 merkkiä"
        return error_message

    only_none = True

    for i in range(len(instrument_roles)):
        print(instrument_roles[i])
        if instrument_roles[i] != "None":
            only_none = False
            
    if only_none:
        error_message = "Yhtyeessä pitäisi olla ainakin yksi rooli valittuna"
    
    return error_message
    

    
