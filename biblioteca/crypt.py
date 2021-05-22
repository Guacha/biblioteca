from flask_bcrypt import Bcrypt
from biblioteca import app

crypto = Bcrypt(app)

def hash(pw: str):
    global crypto
    new_pw = crypto.generate_password_hash(str)
    return new_pw

def dehash(pw: str) -> bool:
    global crypto
    return crypto.check_password_hash(pw)
