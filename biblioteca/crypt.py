import random, string

from flask_bcrypt import Bcrypt
from biblioteca import app

crypto = Bcrypt(app)

def hash(pw: str):
    global crypto
    new_pw = crypto.generate_password_hash(pw).decode('utf8')
    return new_pw

def dehash(pw: str, hash:str) -> bool:
    global crypto
    return crypto.check_password_hash(hash, pw)

def new_uuid():
    values = string.ascii_uppercase + string.digits
    return ''.join(random.choice(values) for i in range(6))

