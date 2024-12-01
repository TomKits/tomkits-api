import re #Regex

# Fungsi validasi password
def validate_password(password):
    errors = []
    if not password:
        errors.append("Password cannot be empty ")
    elif len(password) < 8:
        errors.append("Password must 8 character or longer")
    return errors

# Fungsi validasi email
def validate_email(email):
    errors = []
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]{2,}$'
    if not email:
        errors.append("Email tidak boleh kosong")
    elif not re.match(email_regex, email):
        errors.append("Email invalid")
    return errors