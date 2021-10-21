from utilities.db import db

import re

def trim_result(s):
    pattern = r"[\'(,)A-Za-z]"
    
    s = re.sub(pattern, '', str(s))

    return s

def get_band_count():
    try:
        sql = "SELECT COUNT(*) FROM bands"
        result = db.session.execute(sql)
        band_count = result.fetchone()
    except Exception as e:
        print(e)
    
    return trim_result(band_count)

def get_gig_count():
    try:
        sql = "SELECT COUNT(*) FROM gigs"
        result = db.session.execute(sql)
        gig_count = result.fetchone()
    except Exception as e:
        print(e)

    return trim_result(gig_count)

def get_avg_count_members():
    try:
        sql = "SELECT AVG(count) FROM (SELECT COUNT(*) FROM bandsinstruments GROUP BY band_id) as count"
        result = db.session.execute(sql)
        member_avg = result.fetchone()
    except Exception as e:
        print(e)

    return '%.2f' % float(trim_result(member_avg))