import users.models
import instruments.models

from utilities.db import db

def get_own_bands(id):
    try:
        sql = "SELECT DISTINCT band_name FROM bands, users, usersbands WHERE bands.id = usersbands.band_id AND usersbands.user_id=:id"
        result = db.session.execute(sql, {"id":id})
        bands = result.fetchall()
    except Exception as e:
        print(e)

    return bands

def get_band(band_name):
    band = None

    try:
        sql = "SELECT * FROM bands WHERE band_name = :band_name"
        result = db.session.execute(sql, {"band_name":band_name})
        band = result.fetchone()
    except Exception as e:
        print(e)

    return band

def get_band_case_insensitive(band_name):
    bands = None

    try:
        sql = "SELECT * FROM bands WHERE band_name ILIKE :band_name"
        result = db.session.execute(sql, {"band_name":band_name})
        bands = result.fetchall()
    except Exception as e:
        print(e)

    return bands

def get_bands_instruments(band_id):
    instruments = None

    try:
        sql = "SELECT instrument_name FROM instruments, bandsInstruments WHERE bandsInstruments.band_id = :band_id \
        AND instruments.id = bandsInstruments.instrument_id"
        result = db.session.execute(sql, {"band_id":band_id})
        instruments = result.fetchall()
    except Exception as e:
        print(e)

    return instruments

def create_band(band_name, band_description, instrument_roles):
    try:
        user_id = users.models.get_user(users.models.get_session()).id
        insert_band(band_name, band_description, user_id)

        band_id = int(str(get_band(band_name)).strip("(',)"))
        insert_user_band(band_id, user_id)

        instruments.models.insert_into_band_instruments(instrument_roles, band_id)
        return True
    except Exception as e:
        print(e)
        return False


def insert_band(band_name, band_description, user_id):
    try:
        sql = "INSERT INTO bands (band_name, band_description, user_id) VALUES (:band_name, :band_description, :id)"
        db.session.execute(sql, {"band_name":band_name, "band_description":band_description, "id":user_id})
        db.session.commit()
    except Exception as e:
        print(e)

def get_band(band_name):
    try:
        sql = "SELECT id FROM bands WHERE band_name = :band_name"
        result = db.session.execute(sql, {"band_name":band_name})
        band = result.fetchone()
    except Exception as e:
        print(e)
    
    return band

def insert_user_band(band_id, user_id):
    try:
        sql = "INSERT INTO usersbands (band_id, user_id) VALUES (:band_id, :user_id)"
        db.session.execute(sql, {"band_id":band_id, "user_id":user_id})
        db.session.commit()
    except Exception as e:
        print(e)

def delete_band(band_name):
    try:
        sql = "DELETE FROM bands WHERE band_name = :band_name"
        db.session.execute(sql, {"band_name":band_name})
        db.session.commit()
    except Exception as e:
        print(e)