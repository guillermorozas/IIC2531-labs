from zoodb import *
from debug import *

import hashlib
import random
import pbkdf2
import os

def newtoken(db, cred):
    hashinput = "%s%.10f" % (cred.password, random.random())
    cred.token = hashlib.md5(hashinput.encode('utf-8')).hexdigest()
    db.commit()
    return cred.token

def login(username, password):
    db = cred_setup()
    cred = db.query(Cred).get(username)
    if not cred:
        return None
    if cred.password == pbkdf2.PBKDF2(password, cred.salt).hexread(32):
        return newtoken(db, cred)
    else:
        return None

def register(username, password):
    db = person_setup()
    creddb = cred_setup()
    person = db.query(Person).get(username)
    cred = creddb.query(Cred).get(username)
    if person or cred:
        return None
    newperson = Person()
    newcred = Cred()

    salt = os.urandom(8)
    hash_password = pbkdf2.PBKDF2(password, salt).hexread(32)
    newperson.username = username
    newcred.username = username
    newcred.password = hash_password
    newcred.salt = salt
    
    db.add(newperson)
    creddb.add(newcred)
    db.commit()
    creddb.commit()
    return newtoken(creddb, newcred)

def check_token(username, token):
    db = cred_setup()
    cred = db.query(Cred).get(username)
    if cred and cred.token == token:
        return True
    else:
        return False

