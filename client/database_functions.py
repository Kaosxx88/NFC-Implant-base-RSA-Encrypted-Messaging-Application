#!/usr/bin/python
# autor @Kaosxx88
# function to interact with locals databases

import os
import sqlite3
from colors import *
from rsa_keys_manager import *

def db_save_recipient_locally(n1ckname,public_key):
    #
    # [function not in use]
    #
    # Save recipient locally (function not in use)
    #
    # Create a db if not exist , add an unique user and public key
    D.d('Start db_registration_local function')
    db_file_name = 'recipient.db'
    db_file_location = 'db/'
    conn = sqlite3.connect(db_file_location + db_file_name)
    c = conn.cursor()
    # Insert a row of data
    c.execute('''CREATE TABLE IF NOT EXISTS Users (Name text PRIMARY KEY, Pk text) ''')
    # if the user already exist , compare the key
    try:
        c.execute("INSERT INTO Users VALUES (?,?)" , (n1ckname, public_key))
    except sqlite3.IntegrityError:
        D.d('User already exist')
        conn.commit()
        conn.close()
        return False

    conn.commit()
    conn.close()
    D.d('new user and public key added')
    return True


def db_pk_withdraw(receiver):    
    #
    # [function not in use]
    #
    # retieve the public key from a given user
    #
    D.d('Start db_pk_withdraw function')
    db_file_path = 'db/'
    db_file_name = 'recipient.db'
    conn = sqlite3.connect(db_file_path + db_file_name)
    cursor = conn.cursor()
    for row in cursor.execute('SELECT * FROM Users '):
        if row[0] == receiver :
            receiver_public_key = row[1]
            D.d(f"{receiver} found on the server db")
            conn.close()
            return receiver_public_key

    conn.close()
    D.d('User not found')
    return False