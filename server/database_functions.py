#!/usr/bin/python3 
# autor @kaosxx88
# functions to manage the server database

import os
import sqlite3
from colors import *
from rsa_keys_manager import *


def check_n1ckname_into_user_db(n1ckname):
    #
    # Function to check if the user is registered into the database   
    #
    D.d('Start check_n1ckname_into_user_db function') 
    db_file_path = 'db/'
    db_name = 'user_pk.db'  

    pk = ''

    conn = sqlite3.connect(db_file_path + db_name)
    #
    # selecting user table
    #
    try:
        cursor = conn.execute("SELECT * from Users")
    except sqlite3.OperationalError as e:
        D.d(f'No table User found (probably) -> {e}')
        return False , None   

    #
    # cheking all the users
    #
    for row in cursor:
        if row[0] == n1ckname:
            pk = row[1]
            D.d(f'User {n1ckname} present in the {db_name}')
            conn.close()
            return True , pk
    
    D.d(f"User {n1ckname} not in the {db_name}")
    conn.close()
    return False , None

def db_registration(n1ckname,public_key):
    #
    # function to create a database if it is not exist , add an unique user and public key to it
    #    
    D.d('Start db_registration function')
    db_file_name = 'user_pk.db'
    db_file_location = 'db/'
    conn = sqlite3.connect(db_file_location + db_file_name)
    c = conn.cursor()
    #
    # Insert a row of data
    #
    c.execute('''CREATE TABLE IF NOT EXISTS Users (Name text PRIMARY KEY, Pk text) ''')
    c.execute("INSERT INTO Users VALUES (?,?)" , (n1ckname, public_key))
    conn.commit()
    #
    # close the connection 
    #
    # make sure any changes have been committed or they will be lost.
    #
    conn.close()
    D.d('new user and public key added')

def scan_table(db_name,x='Name , PK'):
    #
    # function to check a given table content 
    # 
    D.d('Start scan_table function')
    db_file_path = 'db/'
    conn = sqlite3.connect(db_file_path + db_name)
    #
    # select user table
    #
    cursor = conn.execute(f"SELECT {x} from Users")
    #
    # check all the user
    #
    D.d(f'Display content of the {db_name} database')
    for row in cursor:
        D.d (row)
    conn.close()

def db_pk_comparison(n1ckname,public_key):    
    #
    # function to check if the imported key match with the internal database one
    #
    D.d('Start db_pk_comparison function')
    db_file_path = 'db/'
    db_file_name = 'user_pk.db'
    conn = sqlite3.connect(db_file_path + db_file_name)
    cursor = conn.cursor()
    for row in cursor.execute('SELECT * FROM Users '):
        if row[0] == n1ckname and row[1] == public_key:
            D.d("User and Public Key match whit the internal db")
            conn.close()
            return True     
    conn.close()
    D.d('Public key do not match')
    return False


def db_pk_withdraw(receiver):  
    #
    # function to get the public key of a registered user from the database
    #      
    D.d('Start db_pk_withdraw function')
    db_file_path = 'db/'
    db_file_name = 'user_pk.db'
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

def db_load_conversations(sender, recipient):
    #
    # function to load saved conversation of an user
    #
    conversation = {}
    db_file_name = 'db_chats.db'
    db_file_location = 'db/'
    conn = sqlite3.connect(db_file_location + db_file_name)
    #
    # select user Messages table
    #
    try :
        cursor = conn.execute(f"SELECT * from Messages")

    except sqlite3.OperationalError as e:
        D.d(f'No table User Messages (probably) -> {e}')
        return False
    #
    # check the messages coming and sent from that user
    #
    for row in cursor:
        if row[1] == sender and row[2] == recipient or row[1] == recipient and row[2] == sender:
            #
            # append the matching conversation to the conversation dictionary 
            #
            conversation[row[0]] = row     
    #print(conversation) # for debug purpose
    conn.close()
    return (conversation)

def db_save_chat_locally(conversations):
    #
    # function to save the chat locally (THIS FUNCTION IN NOT IN USE)
    #
    # Create a db if not exist , add an unique user and public key'
    #
    db_file_name = 'db_chats_local.db'
    db_file_location = 'db/'

    conn = sqlite3.connect(db_file_name)
    c = conn.cursor()
    #
    # Insert a row of data
    #
    c.execute('''CREATE TABLE IF NOT EXISTS Messages (ID INTEGER PRIMARY KEY , Sender_name text, Recipient text, Message text, Downloaded INTEGER) ''')
    #
    # run all the dictionary entry and save data in the db
    #
    for i in conversations:
        Sender_name = conversations[i][1]
        Recipient   = conversations[i][2]
        Message     = conversations[i][3]
        Downloaded  = conversations[i][4]

        c.execute("INSERT INTO Messages( Sender_name, Recipient, Message, Downloaded) VALUES (?,?,?,?)", ( Sender_name, Recipient, Message, Downloaded))

    conn.commit()
    #
    # make sure any changes have been committed or they will be lost.
    #
    conn.close()    



def db_add_message_to_server_chat(sender, recipient, message):
    #
    # This function add the given message to the server database
    #
    D.d('Starting db_add_message_to_server_chat')
    db_file_name = 'db_chats.db'
    db_file_location = 'db/'

    conn = sqlite3.connect(db_file_location + db_file_name)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS Messages (ID INTEGER PRIMARY KEY , Sender_name text, Recipient text, Message text, Downloaded INTEGER) ''')

    c.execute("INSERT INTO Messages( Sender_name, Recipient, Message, Downloaded) VALUES (?,?,?,?)", ( sender, recipient, message, 0))

    conn.commit()
    conn.close()    



def read():
    #
    # function just to print and test a database structure
    #
    db_file_name = 'db_chats.db'
    db_file_location = 'db/'
    conn = sqlite3.connect(db_file_location + db_file_name )
    cursor = conn.execute(f"SELECT * from Messages")
    D.d(f'Reading {db_file_name}')
    for row in cursor:
        #print (row) # debug
        D.d(row)
    conn.close()

def read2():
    #
    # function just to print and test a database structure
    #
    db_file_name = 'user_pk.db'
    db_file_location = 'db/'
    conn = sqlite3.connect(db_file_location + db_file_name )
    # select user table
    cursor = conn.execute(f"SELECT * from Users")
    # check all the user
    D.d(f'Reading {db_file_name}')
    for row in cursor:
        #print (row)
        D.d(row)
    conn.close()


def load_public_key_from_user_db(n1ckname):
    #
    # function to check if the user is registered to the server database
    #
    D.d('Start check_n1ckname_into_user_db function') 
    db_file_path = 'db/'
    db_name = 'user_pk.db'
    conn = sqlite3.connect(db_file_path + db_name)
    try:
        cursor = conn.execute("SELECT Name from Users")
    except sqlite3.OperationalError as e:
        D.d(f'No table User found (probably) -> {e}')
        return False    

    for row in cursor:
        if row[0] == n1ckname:
            D.d(f'User {n1ckname} present in the {db_name}')
            conn.close()
            return True
    
    D.d(f"User {n1ckname} not in the {db_name}")
    conn.close()
    return False

############################################################################
################## DELETE CHAT FROM THE SERVER #############################
############################################################################

def db_erase_user_chat(user1, user2):
    #
    # function to delete the chat from the server
    #
    I.i(f'Starting db_erase_user_chat, users {user1}, {user2}')

    id_list = []
    conn = sqlite3.connect('db/db_chats_encrypted.db') 

    try:
        cursor = conn.execute(f"SELECT ID,Sender, Recipient from Messages")
        for element in cursor:
            if (element[1] == user1 and element[2] == user2):
                id_list.append(element[0])                
            if (element[2] == user1 and element[1] == user2):
                id_list.append(element[0])
        for id in id_list:
            cursor = conn.execute("DELETE FROM Messages WHERE rowid = ?;", (id,))

        conn.commit()
        conn.close()

        I.i('Conversations deleted successfully')

    except sqlite3.OperationalError as e:
        if str(e) == 'no such table: Messages':
            I.i('All the conversation are already been deleted')
        else:
            E.e (e)

############################################################################
##################### SAVE CHAT ON SERVER DB ###############################
############################################################################

def db_update_chat_on_server(sender, recipient, message_encrypted_sender, message_sign_sender, message_encrypted_recipient, message_sign_recipient):
    #
    # function to update the chat to the server database
    #
    D.d('Starting db_add_message_to_server_chat')
    db_file_name = 'db_chats_encrypted.db'
    db_file_location = 'db/'

    conn = sqlite3.connect(db_file_location + db_file_name)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS Messages (ID INTEGER PRIMARY KEY , Sender text, Recipient text, Message_encrypted_sender text, Message_sign_sender text, Message_encrypted_recipient text, Message_sign_recipient text, Downloaded INTEGER) ''')

    c.execute("INSERT INTO Messages( Sender, Recipient, Message_encrypted_sender, Message_sign_sender, Message_encrypted_recipient, Message_sign_recipient, Downloaded) VALUES (?,?,?,?,?,?,?)", ( sender, recipient, message_encrypted_sender, message_sign_sender, message_encrypted_recipient, message_sign_recipient, 0))

    conn.commit()

    conn.close()    

############################################################################
##################### READ CHAT ON SERVER DB ###############################
############################################################################


def db_load_encrypted_conversations(sender, recipient):
    #
    # function to load encrypted communication stored intop the server database from the sender and receiver
    #
    D.d('Starting db_load_encrypted_conversations')

    conversation = {}
    db_file_name = 'db_chats_encrypted.db'
    db_file_location = 'db/'
    conn = sqlite3.connect(db_file_location + db_file_name)

    # select user Messages table
    try :
        cursor = conn.execute(f"SELECT * from Messages")

    except sqlite3.OperationalError as e:
        D.d(f'No table User Messages (probably) -> {e}')
        return False

    # check the message is coming and sent from the given user
    for row in cursor:
        if row[1] == sender and row[2] == recipient :

            message = (row[1] , row[2] , row[3] , row[4] )
            conversation[row[0]] = message 

        elif row[1] == recipient and row[2] == sender:
            message = (row[1] , row[2] , row[5] , row[6] )
            conversation[row[0]] = message
     
    #print(conversation) # debug
    conn.close()
    return (conversation)

def db_load_encrypted_all_conversations(user):
    #
    # function to load encrypted message from a given user
    #
    D.d('Starting db_load_encrypted_conversations')

    conversation = {}
    users = []
    db_file_name = 'db_chats_encrypted.db'
    db_file_location = 'db/'
    conn = sqlite3.connect(db_file_location + db_file_name)

    # select user Messages table
    try :
        cursor = conn.execute(f"SELECT * from Messages")

    except sqlite3.OperationalError as e:
        D.d(f'No table User Messages (probably) -> {e}')
        return False, False

    # check the message coming and sent from the fiven user
    for row in cursor:
        if row[1] == user :            
            message = (row[1] , row[2] , row[3] , row[4] )
            conversation[row[0]] = message 
            if row[2] != user:
                if row[2] not in users:
                    users.append(row[2])

        elif row[2] == user:            
            message = (row[1] , row[2] , row[5] , row[6] )
            conversation[row[0]] = message
            if row[1] != user:
                if row[1] not in users:
                    users.append(row[1])

        if row[1] == user and  row[2] == user:
            if row[1] not in users:
                users.append(row[1])
     
    #print(conversation)
    conn.close()
    return conversation, users