import re
import users.models
import bands.models
import instruments.models

from utilities.db import db

def get_gigs_and_players(own_gigs):
    user_id = users.models.get_user(users.models.get_session()).id

    gigs_users_dict = {}
    gigs_instruments_dict = {}

    print(own_gigs)

    if own_gigs:
        gigs = get_own_gigs(user_id)
    elif own_gigs == None:
        gigs = get_signed_up_gigs(user_id)
    elif not own_gigs:
        gigs = get_not_own_gigs(user_id)
    
    for i in range(len(gigs)):
        gigs_users_dict[gigs[i]] = []
        gigs_instruments_dict[gigs[i]] = []

    for i in range(len(gigs)):
        gig_id = gigs[i].id
        band_id = gigs[i].band_id
        
        players = get_gigs_players(gig_id)
        instruments = get_bands_instruments(band_id)

        gigs_users_dict[gigs[i]] = players
        gigs_instruments_dict[gigs[i]] = trim_results(instruments)

    return {"gigs": gigs, "users": gigs_users_dict, "instruments": gigs_instruments_dict}

def sign_up_for_gig(instrument_name, gig_id):
    user_id = users.models.get_user(users.models.get_session()).id
    instrument = instruments.models.get_instrument_by_name(instrument_name)
    instrument_id = int(str(instrument).strip("(,')"))

    instruments.models.insert_instrument_to_gig(gig_id, instrument_id, user_id)
    insert_user_to_gig(gig_id, user_id)

def delete_sign_up(gig_id, username):
    user_id = users.models.get_user(username).id

    try:
        sql = "DELETE FROM usersgigs WHERE gig_id = :gig_id AND user_id = :user_id"
        db.session.execute(sql, {"gig_id":gig_id, "user_id":user_id})
        
        sql = "DELETE FROM gigsinstruments WHERE gig_id = :gig_id AND user_id = :user_id"
        db.session.execute(sql, {"gig_id":gig_id, "user_id":user_id})

        db.session.commit()
    except Exception as e:
        print(e)

    return

def announce_gig(gig_date, city, venue, gig_description, instrument_name, band_name):
    try:
        user_id = users.models.get_user(users.models.get_session()).id
        instrument_id = instruments.models.get_instrument(instrument_name).id
        band_id = bands.models.get_band(band_name).id

        insert_into_gigs(gig_date, city, venue, gig_description, band_name)

        gig_id = get_gig(gig_date, city, venue, gig_description, band_id).id

        insert_user_to_own_gig(gig_id, user_id)
        instruments.models.insert_instrument_to_gig(gig_id, instrument_id, user_id)
        return True
    except Exception as e:
        return False

def insert_into_gigs(gig_date, city, venue, gig_description, band_name):
    try:
        sql = "INSERT INTO gigs (gig_date, city, venue, gig_description, band_id) VALUES (:gig_date, :city, :venue, :gig_description, (SELECT id FROM bands WHERE band_name = :band_name))"
        db.session.execute(sql, {"gig_date":gig_date, "city":city, "venue":venue, "gig_description":gig_description, "band_name":band_name})
        db.session.commit()
    except Exception as e:
        print(e)

def get_gig(gig_date, city, venue, gig_description, band_id):
    gig = None
    
    try:
        sql = "SELECT * FROM gigs WHERE gig_date = :gig_date AND city = :city AND venue = :venue AND gig_description = :gig_description AND band_id = :band_id"
        result = db.session.execute(sql, {"gig_date":gig_date, "city":city, "venue":venue, "gig_description":gig_description, "band_id":band_id})
        gig = result.fetchone()
    except Exception as e:
        print(e)

    return gig


def get_not_own_gigs(user_id):
    gigs = None

    try:
        sql = "SELECT gigs.id, band_name, band_id, gig_date, city, venue, gig_description FROM gigs, usersgigs, \
            bands WHERE bands.id = gigs.band_id AND usersgigs.user_id != :id AND gigs.id = usersgigs.gig_id AND \
            own_gig = 'TRUE' ORDER BY gig_date"
        result = db.session.execute(sql, {"id":user_id})
        gigs = result.fetchall()
    except Exception as e:
        print(e)
        
    return gigs

def get_own_gigs(user_id):

    gigs = None
    
    try:
        sql = "SELECT gigs.id, band_name, band_id, gig_date, city, venue, gig_description FROM gigs, usersgigs, \
        bands WHERE bands.id = gigs.band_id AND usersgigs.user_id = :id AND gigs.id = usersgigs.gig_id AND \
        own_gig = 'TRUE' ORDER BY gig_date"
        result = db.session.execute(sql, {"id":user_id})
        gigs = result.fetchall()
    except Exception as e:
        print(e)

    return gigs

def get_signed_up_gigs(user_id):
    gigs = None

    try:
        sql = "SELECT gigs.id, band_name, band_id, gig_date, city, venue, gig_description FROM gigs, usersgigs, \
            bands WHERE bands.id = gigs.band_id AND usersgigs.user_id = :id AND gigs.id = usersgigs.gig_id AND \
            own_gig = 'FALSE' ORDER BY gig_date"
        result = db.session.execute(sql, {"id":user_id})
        gigs = result.fetchall()
    except Exception as e:
        print(e)

    return gigs

def get_gigs_players(gig_id):
    players = None

    try:
        sql = "SELECT users.username, instruments.instrument_name FROM users \
                INNER JOIN usersGigs ON users.id = usersGigs.user_id AND usersGigs.gig_id = :gig_id \
                INNER JOIN gigsInstruments ON gigsInstruments.gig_id = :gig_id AND gigsInstruments.user_id = users.id \
                INNER JOIN instruments ON gigsInstruments.instrument_id = instruments.id ORDER BY gigsInstruments.instrument_id" 
        result = db.session.execute(sql, {"gig_id":gig_id})
        players = result.fetchall()
    except Exception as e:
        print(e)

    return players

def get_bands_instruments(band_id):
    instruments = None
 
    try:
        sql = "SELECT DISTINCT instrument_name FROM instruments, bandsInstruments WHERE bandsInstruments.band_id = :band_id \
                AND instruments.id = bandsInstruments.instrument_id"
        result = db.session.execute(sql, {"band_id":band_id})
        instruments = result.fetchall()
    except Exception as e:
        print(e)

    return instruments

#tää johonkin utilities
def trim_results(array):
    pattern = r"[\'(,)]"

    for i in range(len(array)):
        array[i] = re.sub(pattern, '', str(array[i]))

    return array

def insert_user_to_own_gig(gig_id, user_id):
    try:
        sql = "INSERT INTO usersgigs (gig_id, user_id, own_gig) VALUES (:gig_id, :user_id, 'TRUE')"
        db.session.execute(sql, {"gig_id":gig_id, "user_id":user_id})
        db.session.commit()
    except Exception as e:
        print(e)

def insert_user_to_gig(gig_id, user_id):
    try:
        sql = "INSERT INTO usersgigs (gig_id, user_id, own_gig) VALUES (:gig_id, :user_id, 'FALSE')"
        db.session.execute(sql, {"gig_id":gig_id, "user_id":user_id})
        db.session.commit()
    except Exception as e:
        print(e)

def delete_gig(gig_id):
    try:
        sql = "DELETE FROM gigs WHERE id = :gig_id"
        db.session.execute(sql, {"gig_id":gig_id})
        db.session.commit()
    except Exception as e:
        print(e)

