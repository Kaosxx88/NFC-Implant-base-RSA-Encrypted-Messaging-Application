#!/usr/bin/env python3
# Autor @kaosxx88
# keys and encryption functions

import rsa
import time
import json
import os.path
from colors import *
#from os import path
from Crypto import Random
from binascii import hexlify 
from Crypto.Hash import SHA512
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_v1_5


def new_keys():
    #
    # create new key pair
    #
    random_gen = Random.new().read
    key = RSA.generate(4096, random_gen)
    private, public = key, key.publickey()
    return public, private

def import_key(key_pem, passphrase = None):
    #
    # import key
    #
    with open(key_pem,'r') as f:
        key = RSA.import_key(f.read(), passphrase)
    return key

def import_pub_key(key_pem):
    #
    # import public key from file
    #
    try:
        with open(key_pem,'r') as f:
            try:
                key = RSA.import_key(f.read())
                D.d("Public key Imported Right")
                return key

            except __import__('binascii').Error :
                E.e('Inporting public key : Invalid base64-encoded string: number of data characters (581) cannot be 1 more than a multiple of 4')  
                exit(0)      


            except ValueError:
                E.e('Inporting public key : RSA key format is not supported')
                exit(0) 


    except FileNotFoundError:
        E.e('Inporting public key : No such file or directory: "public_key/public_key.pem"')
        exit(0) 


def import_pub_key_digital(key):
    #
    # import public key digitally
    #
    try:
        key = RSA.import_key(key)
        return key
        
    except Exception as e:
        print (f'{C.error}Importing Publicc key digital {C.y}{e} {C.x}')
        pass

           
    
    

def export_priv_key(pri_key, passphrase="banana" ):
    #
    # export private key
    #
    with open('private_key.pem','wb') as f_priv:
        f_priv.write(pri_key.export_key('PEM',passphrase)) 

def export_priv_key_hex(pri_key , passphrase= None) :
    #
    # export private key in hex format
    #
    a = pri_key.export_key('PEM',passphrase, pkcs=8)
    b =  (hexlify(a))  
    with open('private_key.hex','wb') as f_priv:            
        f_priv.write(b) 

def import_Key_hex_as_virtual(file, passphrase = "banana"):   
    #
    # import key from hex format in to virtual
    #
    contents = file.getvalue()
    file.close()     
    bytes_object = bytes.fromhex(contents)
    ascii_string = bytes_object.decode("ASCII")
    key =RSA.import_key(ascii_string, passphrase)
    print(key)
    return key

def import_Key_hex_as_file(key_pem, passphrase = "banana"):
    #
    # import key in hex format from a file
    #
    with open(key_pem,'r') as f:
        hex_string = f.read()
        bytes_object = bytes.fromhex(hex_string)
        ascii_string = bytes_object.decode("ASCII")
        key = RSA.import_key(ascii_string, passphrase)
    print(key)
    return key

def export_pub_key(pub_key):
    #
    # export public key
    #
    with open('public_key.pem','wb') as f_pub:
        f_pub.write(pub_key.export_key('PEM'))

def export_pub_key_digital(pub_key):
    #
    # export public key digitally
    #
    key = pub_key.export_key('PEM')
    return key


def recreate_public_key(priv_key):
    #
    # create publick key from private
    #
    return priv_key.publickey()

def encrypt_mex(mex, pub_key):
    #
    # enxrypt message with public key
    #
    try:
        cipher = PKCS1_OAEP.new(pub_key)
        D.d(f'Message encrypted = {C.green_clean("Message encrypted")}')

        return cipher.encrypt(mex)

    except ValueError:
        D.d(C.red_clean("Message to big"))
        return False



def decrypt_mex(ciphertext, priv_key):
    #
    # decrypt message with private key
    #
    cipher = PKCS1_OAEP.new(priv_key)

    D.d(f'Message Decrypted = {C.green_clean("True")}')
    try:
        return cipher.decrypt(ciphertext)
    except ValueError:
        return b'Impossible decode the message, wrong private key'

        E.e('Impossible decode the message, wrong private key')


def sign_mex(mex, priv_key):
    #
    # sign message with private key
    #
    #mex = json.dumps(mex).encode('utf-8')
    signer = PKCS1_v1_5.new(priv_key)
    digest = SHA512.new(mex)
    D.d(f'Message now signed = {C.green_clean("True")}')
    return signer.sign(digest)

def verify(mex, signature, pub_key):
    #
    # verify signature
    #
    signer = PKCS1_v1_5.new(pub_key)
    digest = SHA512.new()
    #mex = json.dumps(mex).encode('utf-8')
    digest.update(mex)

    D.d(f'Message verify     = {C.green_clean("True")}')
    return signer.verify(digest, signature)

def sign_mex2(mex, priv_key):
    #
    # sign message version 2
    #
    D.d('Start Sign message')
    signer = PKCS1_v1_5.new(priv_key)
    digest = SHA512.new(mex)
    D.d(f'Message now signed = {C.green_clean("True")}')

    return signer.sign(digest)






def import_key_custom_with_errors(key_pem, passphrase = None):

    ##############################
    # IMPORT KEYS ERROR HANDLING #
    ##############################

    error = None
    key = ''

    if passphrase:
        key_type = 'Private'
    else:
        key_type = 'Public'

    try:
        with open(key_pem,'r') as f:
            try:
                if passphrase:
                    key = RSA.import_key(f.read(), passphrase)
                    D.d(f"{key_type} key Imported Correctly")
                else:
                    key = RSA.import_key(f.read())
                    D.d (f"{key_type}  key Imported Correctly") 

                return (error , key )

            except __import__('binascii').Error :
                error =  (f'Inporting {key_type} key : Invalid base64-encoded string: number of data characters (581) cannot be 1 more than a multiple of 4')  
                E.e (error)
                return (error , key )    


            except ValueError:
                error =  (f'Inporting {key_type} key : RSA key format is not supported')
                E.e (error)
                return (error , key ) 

    except FileNotFoundError:
        error = (f'Inporting {key_type} key : No such file or directory: "public_key/public_key.pem"')
        E.e (error)
        return (error , key ) 





def key_creator_and_export( passphrase , private_key_folder_path, public_key_folder_path, progress_callback, export_type='file' ):

    ################
    # KEY CREATION #
    ################
    
    progress_callback.emit('Starting the creation of the keys')

    random_gen = Random.new().read
    key = RSA.generate(4096, random_gen)

    progress_callback.emit('Keys Generated')

    private, public = key, key.publickey()

    progress_callback.emit('Public key extraction')    

    ####################
    # SAVE KEY LOCALLY #
    ####################    

    if export_type == 'file':


        # Custom name for the keys (day + time + name)
        private_key_file_name = f'{private_key_folder_path}/{time.strftime("%Y%m%d-%H%M%S")}_private_key.pem'

        public_key_file_name = f'{public_key_folder_path}/{time.strftime("%Y%m%d-%H%M%S")}_public_key.pem'

        with open(private_key_file_name,'wb') as f_priv:
            f_priv.write(private.export_key('PEM',passphrase)) 


        with open(public_key_file_name,'wb') as f_pub:
            f_pub.write(public.export_key('PEM'))

        progress_callback.emit('Keys saved locally')


        return private_key_file_name , public_key_file_name

    ######################
    # RETURN KEY DIGITAL #
    ######################

    elif export_type == 'digital':

        return public.export_key('PEM'), private.export_key('PEM', passphrase)

