import datetime
from utilities.db import db

def validate_announce_gig(gig_date, city, venue, gig_description, instrument_name):
    error_messages = []
    
    try:
        gig_date_parsed = datetime.datetime.strptime(gig_date, "%Y-%m-%d").date()
        current_date = datetime.datetime.today().date()
    
        if gig_date_parsed < current_date:
            error_messages.append("Et voi palata menneisyyteen. Tarkista keikan päivämäärä")
    except Exception as e:
        error_messages.append("Valitse päivämäärä")
        
    if len(city) < 1 or len(city) > 100:
        error_messages.append("Kaupungin pitää olla vähintään yhden merkin ja enintään 100 merkin pituinen")

    if len(venue) < 1 or len(venue) > 100:
        error_messages.append("Tapahtumapaikan pitää olla vähintään yhden merkin ja enintään 100 merkin pituinen")

    if len(gig_description) > 5000:
        error_messages.append("Tapahtumakuvaus saa olla enintään 5000 merkkiä pitkä")
    
    return error_messages