#!/usr/bin/env python3
# Autor @kaosxx88

# client.py
# This is the client heart 

import os
import ssl
import sys 
import json
import time
import struct 
import socket
import os.path
import argparse
import traceback
import threading
from random import randint 
from getpass import getpass
from Crypto.Cipher import AES


# importing color and debug
from colors import *
# importing needed functions
from rsa_keys_manager import *
from database_functions import *

from PyQt5.QtCore import pyqtSignal, QRunnable, QObject, pyqtSlot

######################################################################
######################## CLIENT ######################################
######################################################################


class WorkerSignals(QObject):
    #
    # This class set the signal to interact with the function of the gui (pyqt5)
    #

    notification            = pyqtSignal(tuple)
    chat_history            = pyqtSignal(object)
    login_validation        = pyqtSignal(tuple)
    incoming_message        = pyqtSignal(tuple)
    add_new_recipient       = pyqtSignal(tuple)
    delete_conversation     = pyqtSignal(bool)
    notification_passive    = pyqtSignal(tuple)
    lost_connection         = pyqtSignal(tuple)


class Client(QRunnable):          

    def __init__(self,  private , public , nickname , controller):
        super(Client, self).__init__()

        # gui signals
        self.signals = WorkerSignals()

        # host and port of the server
        self.host                   = "127.0.0.1"
        self.port                   = "4444"  
        self.n1ckname               = nickname
        self.response               = ''
        self.controller             = controller
        self.private_key            = private
        self.user_public_key        = public
        self.server_public_key      = ''
        self.recipient_n1ckname     = ''
        self.responde_is_arrived    = False 
        self.recipient_public_key   = None


    @pyqtSlot()
    def run(self):
        #
        # estabilish the connection with the server
        #
        if self.connection_to_the_server() :
            # create new receiver thread   
            self.receive = Receive(self.ssock, self.recipient_n1ckname, self.n1ckname, self)        
            # start new receiver thread                      
            self.receive.start() 
            # request key to the server
            self.req_server_public_key()
            # try to login
            login_confirmation = self.login()   
            # if login ok
            if login_confirmation:
                # download history
                self.history_conversation()                                                                                            
                                                                                     


    def req_server_public_key(self):   
        #
        # request the public key to the server 
        #
        request                          = {}
        request['request']               = 'server_public_key'
        request['client_public_key']     = export_pub_key_digital(self.user_public_key).decode('utf-8') 

        self.send_request(request)
        
        if self.wait_for_server_response() == True:

            response = self.response['response']                                                             

            if response == 'server_public_key' :

                self.server_public_key  = self.response['server_public_key']
                self.server_public_key  = import_pub_key_digital(self.server_public_key) #[TO IMPLEMENT] encrypt the token with the server public
                self.token              = self.response['encrypted_token']                                                   
                self.token              = bytes.fromhex(self.token)                                                           
                self.token              = decrypt_mex(self.token, self.private_key)                           


    def encrypt_request_aes(self, data):
        #
        # Encrypt the request with AES
        #

        D.d('Starting encrypt_request_aes')
        # load the token
        secret  = self.token
        # dump the data to encrypt
        data    = json.dumps(data)        
        # encode the data                                                      
        data    = data.encode()  
        # select cypher  
        cipher  = AES.new(secret, AES.MODE_EAX)  
        # load nonce                                               
        nonce   = cipher.nonce                                                                 
        ciphertext, tag = cipher.encrypt_and_digest(data)
        output  = {'ciphertext' : ciphertext.hex() , 'tag': tag.hex() , 'nonce':nonce.hex()}    

        return output

    def decrypt_request_aes(self, data):   
        #
        # Decrypt the request AES
        #
        D.d('Starting decrypt_request_aes')
        # load ciphertext
        ciphertext  = bytes.fromhex(data['ciphertext'])
        # load tag
        tag         = bytes.fromhex(data['tag'])
        # load noce
        nonce       = bytes.fromhex(data['nonce'])
        # load key
        key         = self.token
        cipher      = AES.new(key, AES.MODE_EAX, nonce=nonce)
        plaintext   = cipher.decrypt(ciphertext)
        plaintext   = json.loads(plaintext)
        #
        # try to decrypt the request
        #
        try:
            cipher.verify(tag)

            D.d(f'(AES) Message Decrypted = {C.green_clean("True")}')
            return True, plaintext

        except ValueError:
            D.d(C.red_clean("(AES) Key incorrect or message corrupted"))
            return False, None


    def login(self):
        #
        # login function
        #
        D.d('starting login function')
        # create the request
        request                 = {}                                                                                                    
        request['request']      = 'login'                                                                              
        request['user_name']    = self.n1ckname                                                                       
        # encrypt the request
        request = self.encrypt_request_aes(request)
        # send the request
        self.send_request(request)                                                                             
        # wait for response
        if self.wait_for_server_response() == True:                                                                     #
            # load response data
            response_name   = self.response['response']
            response_value  = self.response['response_value']
            # if validation response True
            if response_name == 'login' and response_value == True:                       
    
                D.d('user present on the server db, saving secret and server pk') 
                # send seignal to the gui
                self.signals.login_validation.emit((True, ''))
                return True    


            # if the validation response is False
            elif response_name == 'login' and response_value == False:                     

                response_message = self.response['response_message'] 

                if response_message == 'User exist but the public key provided do not match':
                    D.d('The provided public key do not match with the provided user')
                    # close the connection with the server
                    self.ssock.shutdown(1)                   

                    # tell the receiver class to do not reload the login because we are alreadi there
                    self.receive.invalid_login_change(True)

                    # Display message to the user
                    self.signals.login_validation.emit((False, 'The provided public key do not match with the provided user'))

                    return False
                    

                elif response_message == 'User do not exist on the server database':

                    # tell the receiver class to do not reload the login because we are alreadi there
                    self.receive.invalid_login_change(True)

                    I.i('Account not present on the server db')

                    # Display message to the user
                    self.signals.login_validation.emit((False, 'Account not present on the server db'))
                    self.ssock.shutdown(1)

                    return False

    def update_server_response(self, response):
        #
        #  function to update the response from the server (the receive section trigger it)
        #
        D.d(f'New response ')

        for element in response: D.d(f'{element} = {response[element]}')     

        self.response = response 
        # print the response  type                                                                                                                   
        D.d(f'Response type  = {C.yellow_clean(self.response["response"])}')                                                  
        # allocate the response to the self.response
        response_value = self.response["response_value"]                                                                        
        # check if the response value is True
        D.d(f'Response value = {C.green_clean(response_value) if response_value == True else C.red_clean(response_value)}')    
        # flag that the response is arrived
        self.responde_is_arrived = True                                                                                         
                                        
    def wait_for_server_response(self):   
        #
        # loop to wait for a server response                                   
        #
        # 20 seconds (300 * 0.1)
        second_to_wait = 300 
        # wait for server response                                                                                                   
        while second_to_wait != 0 and self.responde_is_arrived == False:                                        
            D.d(f'Response is arrived? -> { C.red_clean(self.responde_is_arrived)}')                                                  
            D.d(f'...Waiting for server response... ')     
            # Sleep 0.1 seconds                                                                                 
            time.sleep(0.1)  
            # decrease the variable for each iteration                                                                                                              
            second_to_wait -= 1    
        # reset the notification variable                                                                                                   
        self.responde_is_arrived = False                                                                                        
        
        # if time ended (no response arrived)    
        # close the connection if server do not response after 30 second              
        if second_to_wait == 0:                                                                                                 
            D.d(f'No server response after 20 seconds, operation aborted')                                      
            E.e('No response from the server, Closing application...')                                      
            self.ssock.shutdown(1)                                                                                                  
            os._exit(0) 
            #
            #
            # If response not arrived do something do not shut the applicaiton [TO IMPLEMENT]
            #
            #
            #

        else:                                                                                                                   
            # if time not ended (response arrived)
            D.d (f'Response arrived from the server = { C.red_clean(self.response["response"])}')                                      
            return True                                     
                                        

              
    def history_conversation(self):
        #
        # function to request the conversation of the user on the server database
        #

        D.d('Starting Downlod conversation')

        request                         = {}                                                                                                
        request['request']              = 'history'

        # sign and send the request
        self.request_sign_and_send(request)                                                                       

        # if the server send the respose to re quest
        if self.wait_for_server_response() == True:     

            response        = self.response['response']
            response_value  = self.response['response_value']


            if response == 'history' and response_value == True: 

                D.d('Response Download Conversation is arrive....') 

                history = self.response['history']
                self.users_public_key_pairs = self.response['users_public_key_pairs']

                D.d(history)
                D.d(self.users_public_key_pairs)

                # load the history conversation on the gui
                self.load_incoming_history_in_the_gui(history, self.n1ckname )



    def add_recipient_to_client(self, new_recipient):
        #
        # add a new recipient to the client ( download the public key of the new client from the server)
        #
        # [TO IMPLEMENT] -> double check the public key into another server if match
        #

        D.d('Start adding a new recipient ')
 
        request                         = {}                                                                                               
        request['request']              = 'add_recipient_to_client'
        request['recipient_n1ckname']   = new_recipient

        self.request_sign_and_send(request)                                                                         

        if self.wait_for_server_response() == True:  

            response        = self.response['response']
            response_value  = self.response['response_value']

            if response == 'add_recipient_to_client' and response_value == True:  

                D.d('Recipient present on the server')  

                recipient_public_key   = self.response['recipient_public_key']                                  
                recipient_n1ckname     = self.response['recipient_n1ckname']                                     

                # add the publicc key to the local list of public key under the correct user
                self.users_public_key_pairs[recipient_n1ckname] =  recipient_public_key

                list = (None,recipient_public_key, recipient_n1ckname )
                
                self.signals.add_new_recipient.emit(list)

            elif response == 'add_recipient_to_client' and response_value == False:                
                
                error = 'User not present on the server database'
                D.d(error)

                list = (True,error, None )
                self.signals.add_new_recipient.emit(list)
                         

    def send_request(self, dictionary):
        #
        # function to send the request to the server  (send message that are bigger of the normal buffer side (1024) )
        #

        D.d('Starting send_request function ')   
        # convert dictionary into string      
        dictionary = json.dumps(dictionary)     
        # Prefix each message with a 4-byte length (network byte order)                                                                           
        msg = struct.pack('>I', len(dictionary)) + dictionary.encode()                                              
        self.ssock.sendall(msg)         
            


    def load_incoming_history_in_the_gui(self, history, n1ckname):   
        #
        # load the incoming conversation (history) and print them in the GUI
        #                                                
        local_message_history = {} 

        # create dictionary entry for each user
        for user in self.users_public_key_pairs:
                local_message_history[user] = []

        # check if there is not a history
        if len(history) == 0:         
            D.d ("The history is empty")     
            self.signals.chat_history.emit(local_message_history)                      
        # in case there is an history 
        else:           
            
            for chat in history:                                                                                            
                message = bytes.fromhex(history[chat][2])                                                     
                message_sing = bytes.fromhex(history[chat][3])    
                
                # check the sender of the message (if is the user use his key to decrypt)
                if history[chat][0] == n1ckname :
                    # decrypt the message and check the signature
                    message = self.decrypt_and_sign_check_history(message, message_sing, self.user_public_key)                          
                    # add the decrypted message to the history
                    sender_and_message = (history[chat][0], message)
                    local_message_history[history[chat][1]].append(sender_and_message)
                # if the user is the recipient , decrypt the message with the sender
                elif history[chat][1] == n1ckname: 
                    # load recipient public key
                    recipient_key = self.users_public_key_pairs[history[chat][0]]
                    # import the key
                    public_key = import_pub_key_digital(recipient_key) 
                    # decrypt message
                    message = self.decrypt_and_sign_check_history(message, message_sing, public_key)    
                    # load message in to the history
                    sender_and_message = (history[chat][0], message)
                    local_message_history[history[chat][0]].append(sender_and_message)

            # emit signal to gui
            self.signals.chat_history.emit(local_message_history)
    


    def delete_conversation_ui(self):
        #
        # delete the conversation from the server
        #
        D.d('Starting delete_conversations function ui')           
        # create the request
        request = {}                                                                                             
        request['request'] = 'delete_chats'
        request['recipient_n1ckname'] = self.recipient_n1ckname
        # sign and send the request
        self.request_sign_and_send(request)  
        # wait for the server response                          
        if self.wait_for_server_response() == True:  
                                                                        #
            if self.response['response'] == 'delete_chats' and self.response['response_value'] == True:

                D.d('Conversations Deleted')
                # emit signal to the ui

                del self.users_public_key_pairs[self.recipient_n1ckname]
                
                # emit seignal to the gui
                self.signals.delete_conversation.emit(True)
            else:
                D.d('Conversations Not Deleted')
                self.signals.delete_conversation.emit(False)


     
    def connection_to_the_server(self):                     
        #
        # connection with the server
        #   

        try:                        
            D.d(f'Trying to connect to {self.host}:{self.port}...')     
            # ssl setting (For the testing use of self signed certificate this option is like that) [to improve security once in possession of real CA certificate have a look at (https://docs.python.org/3/library/ssl.html)]                                                     
            context     = ssl.SSLContext(ssl.PROTOCOL_TLS) 
            # create the connection Thread                                
            self.sock   = socket.create_connection((self.host, self.port))    
            # wrap the connection                                                      
            self.ssock  = context.wrap_socket(self.sock, server_hostname=self.host)  
            # check ssocket version                                               
            I.i(f'Connection secured by {self.ssock.version()}')                                                                    
            D.d(f'Successfully connected to {self.host}:{self.port}')  
            # I.i connection establisih                                           
            return True    
                        
        except ConnectionRefusedError:                                  
            E.e('Server unreachable') 
            #
            # Do not block the app but send a message to the user
            #                                                                                  
            # os._exit(0) 
            # implement a visual solution

            self.signals.login_validation.emit((False, 'No connection with the server'))
            return False                     


    def request_sign_and_send(self, request):   
        #
        # function to sign the request
        #                    
        D.d('Start request_sign_and_send')  
        # dump the request
        request_converted = json.dumps(request).encode('utf-8')
        # sign the request
        request_sign = sign_mex(request_converted, self.private_key) 
        # verify the signature                                                   
        D.d(f'Verify my sign     = {C.green_clean(verify(request_converted, request_sign, self.user_public_key))}')      
        # add the signature to the request                  
        request['request_sign'] = request_sign.hex()                                                                    
        # encrypt the request
        request = self.encrypt_request_aes(request)
        # send the request
        self.send_request(request)                                                                              


    def message_sign_and_send_to_request(self, list): 
        #
        # function to sign the message
        #
        recipient               = list[0]
        message                 = list[1]

        # update the local recipient
        self.recipient_n1ckname = recipient
        # update the recipient the in send and receive thread
        self.receive.change_recipient(recipient)                                     
        # encode the message to be encrypted
        message = message.encode()                                                                                       
        # load recipient public key                      
        recipient_public_key        = import_pub_key_digital(self.recipient_public_key)  
        # encrypt the message for the recipient                                
        message_encrypted_recipient = encrypt_mex(message, recipient_public_key)     
         # encrypt the message for the sender (needed to read back the chat)                                    
        message_encrypted_sender    = encrypt_mex(message, self.user_public_key)                                        
        # if the message is not to big                    
        if message_encrypted_recipient != False and message_encrypted_sender != False:                                   
            D.d('Messages recipient / sender encrypted')                           
            # sign the messag for the recipient                
            message_sign_recipient = sign_mex(message_encrypted_recipient, self.private_key)   
            # sign the message for the sender                          
            message_sign_sender    = sign_mex(message_encrypted_sender, self.private_key)                                
            # create the request                
            request                                 = {}                                                                 
            request['request']                      = 'message'                         
            request['recipient']                    = self.recipient_n1ckname                               
            request['message_encrypted_sender']     = message_encrypted_sender.hex()                            
            request['message_sign_sender']          = message_sign_sender.hex()                         
            request['message_encrypted_recipient']  = message_encrypted_recipient.hex()                             
            request['message_sign_recipient']       = message_sign_recipient.hex()                          
             # sign and send the request                
            self.request_sign_and_send(request)     
        # message to big for the encryption                                                                     
        else:
            D.d('...Message to big...')                                                         
            #
            # LET the user know that the message is to big to be public key encrypted
            #
            # [TO IMPLEMENT] split the message and send it anyway


    def decrypt_and_sign_check(self,encrypted_message, encrypred_message_sign, sender_receiver):   
        #
        # function to decrypt and check the signature of the message
        #
        # check if the message os from the sender or the receiver
        if sender_receiver      == 'receiver':        
            # load the public key                                                                          
            public_key = import_pub_key_digital(self.recipient_public_key)                                                 
            # load the public key
        elif sender_receiver    == 'sender':
            public_key = self.user_public_key
        # veridy the sign  
        check_the_sign = verify(encrypted_message, encrypred_message_sign, public_key )                                       

        D.d(f'Incoming message signed = {C.green_clean(check_the_sign)}')
        # if signed
        if check_the_sign == True:  
            # decrypt message                                                                                        
            decrypted_message = decrypt_mex(encrypted_message, self.private_key)   
            # decode the message                                         
            decrypted_message = (decrypted_message).decode('ascii')                                                         
            return decrypted_message
        # if the signature is not valid 
        else:
            D.d('Signature Not valid')                                                                                      
            message = 'Signature not valid'
            return message

    

    def decrypt_and_sign_check_new_user(self,encrypted_message, encrypred_message_sign, nickname_sender):   
        #
        # check the sign of the message and decrypt it
        # 
        # load public key in case the sender of the message is the actual user
        if nickname_sender    == self.n1ckname:
            public_key = self.user_public_key

        else:   
            for user in self.users_public_key_pairs:

                # if the user is know and present on the list of keys(load the key)
                if nickname_sender == user:
                    public_key = import_pub_key_digital(self.users_public_key_pairs[user])      
        # veridy the sign   
        check_the_sign = verify(encrypted_message, encrypred_message_sign, public_key )                                      

        # if signed  
        if check_the_sign == True:       
            # decrypt message                                                                                 
            decrypted_message = decrypt_mex(encrypted_message, self.private_key)   
            # decode the message                                         
            decrypted_message = (decrypted_message).decode('ascii')                                                         
            return decrypted_message
        # if not signed
        else:
            message = 'Signature not valid'
            return message



    def decrypt_and_sign_check_history(self, encrypted_message, encrypred_message_sign, public_key):  
        #
        # function to decrypt and check the sign of the history
        #
        # verify the sign
        check_the_sign = verify(encrypted_message, encrypred_message_sign, public_key )                                        

        D.d(f'Message signed    = {C.green_clean(check_the_sign)}')
        # if signed
        if check_the_sign == True:  
            # decrypt message                                                                                        
            decrypted_message = decrypt_mex(encrypted_message, self.private_key)    
            # decode the message                                        
            decrypted_message = (decrypted_message).decode('ascii')                                                         
            return decrypted_message
        # if the signature is not valid 
        else:
            D.d('Signature Not valid')                                                                                      
            message = 'Signature not valid'
            return message

    def update_recipient_from_gui(self, recipient):
        #
        # update the recipiend of the message (need to change the encryption key)
        #

        self.recipient_n1ckname = recipient        
        # update the recipient in the receive thread and local
        self.receive.change_recipient(recipient)                                    

        for user in self.users_public_key_pairs:
            
            if user == recipient:
                D.d(f'New recipient = {C.green_clean(recipient)}' )
                D.d(f'Public Key =\n{self.users_public_key_pairs[user]}')
                self.recipient_public_key = self.users_public_key_pairs[user]
                


######################################################################
######################## RECEIVE THREAD ##############################
######################################################################       

class Receive(threading.Thread):    
    #
    # Class listening for new incoming message/response
    #

    def __init__(self, ssock, recipient_n1ckname, n1ckname, client):
        super().__init__()

        self.ssock              = ssock  
        self.n1ckname           = n1ckname
        self.client             = client
        self.recipient_n1ckname = recipient_n1ckname
        self.invalid_login      = False

    def run(self): 
        # wait to receive message

        connection_open = True

        while connection_open == True:     
            
            # incoming message variable                                                                  
            dictionary = self.receiver_splitted_message()                                   
            # if there is a message
            if dictionary: 
                D.d(C.green_clean("-- Receiving Data --"))
                # reload trhe message in json
                dictionary = json.loads(dictionary) 
                # check if it is a response 
                if 'response' in dictionary and dictionary['response'] == 'server_public_key': 
                    # upldate the client with the response
                    self.client.update_server_response(dictionary)

                else:
                    # verify the validity of the message encryption
                    verification , dictionary =  self.client.decrypt_request_aes(dictionary)
                    # if the validation is true
                    if verification == True:
                        # check if is a message
                        if dictionary['response'] == 'message':
                            # if is a message send to the message handler
                            self.incoming_message_handler(dictionary)
                        else:
                            # if is a response update the client response section
                            self.client.update_server_response(dictionary)            
                    else:

                        #connection_open = False

                        D.d('Incorrect verification, closing the application of the response')


            else: 

                # if the login credential are not valid do not shut the connection

                if self.invalid_login == True:

                    self.invalid_login = False

                    connection_open = False
                    

                else:               
                    print (f'\n')
                    D.d('Connection to the server closed!, closing down the application (client.py)...')                 

                    connection_open = False


                    self.client.signals.lost_connection.emit(('True','The application lost the connection with the server, For security reason please login again'))

                    # close local socket 
                    #self.ssock.shutdown(1)                                                                         
                    #os._exit(0)
                    #
                    #
                    # Let the user know, do not shut the chat
                    #
                    # [TO IMPLEMENT]



    def invalid_login_change(self, value):
        #
        # function to change the value of invalid login from outside the class itself
        #
        self.invalid_login = value


######################################################################
#################### INCOMING MESSAGE HANDLER ########################
######################################################################

    def incoming_message_handler(self, dictionary):
        #
        # function that handle the incoming message
        #

        # actual user of nirema application
        application_user                = self.n1ckname
        # recipient selected in the application ( on screen)
        application_selected_recipient  = self.recipient_n1ckname
        # sender of the incoming message
        incoming_message_sender         = dictionary['sender']
        # recipient of the incoming message
        incoming_message_recipient      = dictionary['recipient']
        # message encrypted for the sender
        message_encrypted_sender        = bytes.fromhex(dictionary['message_encrypted_sender'])                 
        # message encrypted for the recipient
        message_encrypted_recipient     = bytes.fromhex(dictionary['message_encrypted_recipient'])
        # signature of the sender
        message_sign_sender             = bytes.fromhex(dictionary['message_sign_sender'])                                  
        # signature for the recipient
        message_sign_recipient          = bytes.fromhex(dictionary['message_sign_recipient']) 
       
        D.d(f'Message sender    = {C.green_clean(incoming_message_sender)}') 
        D.d(f'Message recipient = {C.green_clean(incoming_message_recipient)}')

        # message to yourself, two chat open, in the second one you are selecting another user screen
        if application_user != application_selected_recipient and incoming_message_sender == incoming_message_recipient:

            D.d(C.cyan_clean(f'\r (Notification) New message from = {incoming_message_sender}'))
            incoming_message_to_recipient = self.client.decrypt_and_sign_check_new_user(message_encrypted_recipient, message_sign_recipient, incoming_message_sender)
            list = ('Notification to myself from ->',incoming_message_sender,incoming_message_to_recipient)
            # send notification to the guy
            self.client.signals.notification.emit(list)


        # Notification if the selected chat  tab is different from the message sender
        elif application_selected_recipient != incoming_message_sender and application_user != incoming_message_sender:
            D.d(C.cyan_clean(f'\r (Notification) New message from = {incoming_message_sender}')) 

            # check if the user exist in the list of public keys saved
            if incoming_message_sender in self.client.users_public_key_pairs:
                D.d ('Incoming message sender public key present locally')
                # if is present decrypt the message
                incoming_message_to_recipient = self.client.decrypt_and_sign_check_new_user(message_encrypted_recipient, message_sign_recipient, incoming_message_sender)
                new_user = False
            # if the user is not in the list
            else:
                D.d ('Incoming message sender public key not present locally (no possible to decrypt the message)')
                # do not decrypt the message
                incoming_message_to_recipient = None
                new_user = True

            list = ('(Notification) ',incoming_message_sender, incoming_message_to_recipient, new_user)
            # send the notification to the gui
            self.client.signals.notification_passive.emit(list)

        #if the selected recipient is the sender of the incoming message
        elif application_selected_recipient == incoming_message_sender:

            incoming_message_to_recipient = Client.decrypt_and_sign_check(self.client, message_encrypted_recipient, message_sign_recipient, 'receiver')

            list = (incoming_message_sender,incoming_message_to_recipient,'Section 1 ')
            self.client.signals.incoming_message.emit(list)


        if application_user == application_selected_recipient:
            pass


    def change_recipient(self, recipient_n1ckname): 
        #
        # change the recepient of the chat, update the recipient from outside the object
        #
        self.recipient_n1ckname = recipient_n1ckname
        D.d(f'(Receiver thread) New recipient selected = {C.green_clean(self.recipient_n1ckname)}')


    def receiver_splitted_message(self):
        #
        # function to read custom data lennth in data receiving
        #
        raw_msglen = self.recvall(4)
        if not raw_msglen:
            return None
        msglen = struct.unpack('>I', raw_msglen)[0]
        return self.recvall(msglen)


    def recvall(self,n):
        #
        # function to read the number of byte of the file incoming
        #
        data = bytearray()
        while len(data) < n:
            packet = self.ssock.recv(n - len(data))
            if not packet:
                return None
            data.extend(packet)
        return data

