#!/usr/bin/python3 
# autor @ kaosxx88 
# This file manage the public and private keys, the sign of the messages and 

import rsa
import json
from colors import *
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
    # import a key 
    #
    with open(key_pem,'r') as f:
        key = RSA.import_key(f.read(), passphrase)
    return key

def import_pub_key(key_pem):
    #
    # import a public key
    #
    try:
        with open(key_pem,'r') as f:
            try:
                key = RSA.import_key(f.read())
                D.d("Public key Imported Right")
                return key

            except __import__('binascii').Error :
                E.e('Inporting public key : Invalid base64-encoded string: number of data characters (581) cannot be 1 more than a multiple of 4')        
                return False

            except ValueError:
                E.e('Inporting public key : RSA key format is not supported')
                return False

    except FileNotFoundError:
        E.e('Inporting public key : No such file or directory: "public_key/public_key.pem"')
        return False

def import_pub_key_digital(key):
    #
    # import publick key from digital format
    #
    D.d('Stating function import public key digital')
    try:
        key = RSA.import_key(key)
        return key
        
    except Exception as e:
        E.e(f'Importing Publick key digital -> {C.y}{e} {C.x}')
        return 1
            

def export_priv_key(pri_key, passphrase="banana" ):
    #
    # export private key
    #
    with open('private_key.pem','wb') as f_priv:
        f_priv.write(pri_key.export_key('PEM',passphrase)) 


def export_priv_key_hex(pri_key , passphrase= None) :
    #
    # export private key in hexadecimal formt
    #
    a = pri_key.export_key('PEM',passphrase, pkcs=8)
    b =  (hexlify(a))  
    with open('private_key.hex','wb') as f_priv:            
        f_priv.write(b) 

def import_Key_hex_as_virtual(file, passphrase = "banana"):   
    #
    # import key as virtual
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
    # import key from a file
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
    # export public key as pem file
    #
    with open('public_key.pem','wb') as f_pub:
        f_pub.write(pub_key.export_key('PEM'))

def export_pub_key_digital(pub_key):
    #
    # export public key as digital pem
    #
    key = pub_key.export_key('PEM')
    return key


def recreate_public_key(priv_key):
    #
    # create the public key from the private
    #
    return priv_key.publickey()

def encrypt_mex(mex, pub_key):
    #
    # encrypt give message with the given public key
    #
    D.d('Starting encrypt message')
    cipher = PKCS1_OAEP.new(pub_key)
    D.d('Message encrypted')
    return cipher.encrypt(mex)

def decrypt_mex(ciphertext, priv_key):
    #
    # decrypt given message with the give private key
    #
    D.d('Start decrypt message')
    cipher = PKCS1_OAEP.new(priv_key)
    D.d('Message decrypted')
    return cipher.decrypt(ciphertext)

def sign_mex(mex, priv_key):
    #
    # signing the given message with the given private key
    #
    D.d('Start Sign message')
    signer = PKCS1_v1_5.new(priv_key)
    digest = SHA512.new(mex)
    D.d('Message signed')
    return signer.sign(digest)

def verify(mex, signature, pub_key):
    #
    # verify the signature pf the mssage 
    #
    D.d('Start verify message')
    signer = PKCS1_v1_5.new(pub_key)
    digest = SHA512.new()
    mex = json.dumps(mex).encode('utf-8')
    digest.update(mex)
    D.d('Message verify')
    return signer.verify(digest, signature)

