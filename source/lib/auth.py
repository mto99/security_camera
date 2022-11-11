from hashlib import sha256
import json

global logged_in
logged_in = False

def createHash(password:str) -> str:
    return sha256(password.encode()).hexdigest()


def authUser(username:str, password_hashed:str) -> bool:
    with open('source/authentication/auth.json') as f:
        data = json.load(f)
        if username in data:
            if data[username] == password_hashed:
                return True
        return False

