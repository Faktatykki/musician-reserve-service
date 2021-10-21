import re

import users.models

def validate_create_user(username, password, password_again):
    error_messages = []
    string_check = re.compile('[@_!#$%^&*()<>?/\|}{~:]')

    case_insensitive_user_query = users.models.get_user_case_insensitive(username)

    if len(case_insensitive_user_query) > 0:
        error_messages.append("Käyttäjänimi on jo olemassa")

    if len(username) < 3 or len(username) > 20:
        error_messages.append("Käyttäjänimen pituus pitää olla vähintään 3 merkkiä ja enintään 20")
    
    if string_check.search(username) is not None:
        error_messages.append("Käyttäjänimessä ei saa olla erikoismerkkejä kuten: @_!#$%^&*()<>?/\|}{~:")

    if len(password) < 8 or len(password) > 25:
        error_messages.append("Salasanan pituus pitää olla vähintään 8 merkkiä ja enintään 25")

    if password != password_again:
        error_messages.append("Salasanat eivät täsmää")

    return error_messages
