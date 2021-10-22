import re
import bands.models

def validate_create_band(band_name, band_description, instrument_roles):
    error_messages = []
    string_check = re.compile('[@_#$%^&*()<>?/\|}{~]')

    case_insensitive_band_query = bands.models.get_band_case_insensitive(band_name)

    if len(case_insensitive_band_query) > 0:
        error_messages.append("Yhtye on jo olemassa")
         
    if len(band_name) < 1 or len(band_name) > 80:
        error_messages.append("Yhtyeen nimi ei voi olla tyhjä tai yli 80 merkkiä pitkä")

    if string_check.search(band_name) is not None:
        error_messages.append("Yhtyeen nimessä ei saa esiintyä seuraavia erikoismerkkejä: @_#$%^&*()<>?/\|}{~")

    if len(band_description) > 2000:
        error_messages.append("Rauhoitu, yhtyeen kuvaus pitäisi olla alle 2000 merkkiä")

    only_none = True

    for i in range(len(instrument_roles)):
        if instrument_roles[i] != "None":
            only_none = False
            
    if only_none:
        error_messages.append("Yhtyeessä pitäisi olla ainakin yksi rooli valittuna")
    
    return error_messages
    