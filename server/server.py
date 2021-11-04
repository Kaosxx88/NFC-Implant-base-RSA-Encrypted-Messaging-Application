#!/usr/bin/python3 
# server.py v2.0 KaOs

import os
import ssl
import time
import json
import struct 
import socket
import secrets
import argparse
import threading
import traceback
from colors import *
from binascii import hexlify 
from Crypto.Cipher import AES
from rsa_keys_manager import *
from secrets import token_bytes
from database_functions import *


######################################################################
########################## SERVER ####################################
######################################################################

class Server(threading.Thread):
    ''' Class to setup the server connection'''

    def __init__(self, host, port):
        super().__init__()
        #
        # Loading variables 
        #
        self.connections            = []               
        self.host                   = host
        self.port                   = port
        self.connections_authorised = []
    
    def run(self):
        ''' Auto run function for the Server Class'''        
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER) 
        #  
        # load server certificate and key        
        #                                         
        context.load_cert_chain('certificate/server/server.cer', 'certificate/server/server.key')  
        #
        # socket creation and options             
        #
        sock    =  socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)                                    
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        sock.bind((self.host, self.port))
        sock.listen(5)
        #
        # SSL wrap
        #
        ssock   = context.wrap_socket(sock, server_side=True)  
        #   
        # Screen output
        #
        I.i(f'Nirema server started ( {C.cyan_clean("digit .quit to close it")} ) ')                                        
        I.i(f'Listening at {C.cyan_clean(ssock.getsockname()[0])} port {C.cyan_clean(ssock.getsockname()[1])}')
        

        while True:
            #
            # Try (in case a client crush in the connection, the server stay alive) 
            #
            try:
                # accepting multi connections                                                                                        
                sc, sockname = ssock.accept() 
                # 
                # print a line to separate messages and print name and sockname
                #                                                                  
                I.i(C.cyan_clean("-"* 75))                                                              
                I.i(f'Accepted a new connection from {sc.getpeername()} to {sc.getsockname()}') 
                #
                # initialise new thread server socket
                #
                server_socket = ServerSocket(sc, sockname, self)                                        
                server_socket.start() 
                #
                # append the new connection to the list of connections  
                #                 
                self.connections.append(server_socket) 
                #
                # print connections active      
                #                                         
                D.d(self.connections)
                I.i(f'Ready to receive messages from {sc.getpeername()}')

            except Exception as e:
                E.e('(1) Error in Server.Run ( Wrong client feed )')



                
    def redirect_message_to_reveiver(self, message, recipient, sockname , n1ckname):
        ''' Check if the recipient is on-line and send the message to him '''   
        #
        # for the connections in the list of connections        
        #
        for connection in self.connections:                                                             
            
            if connection.n1ckname == recipient:  
                # encrypt the message with the token of the receiver
                message_enc_1 = connection.aes_encrypt(message, connection.token)  
                # send the message                                                                              
                connection.send_splitted_message(message_enc_1)  

            if connection.n1ckname == n1ckname and connection.sockname != sockname:
                # send the message to the other session of the sender (multi application open)                     
                message_enc_2 = connection.aes_encrypt(message, connection.token)
                connection.send_splitted_message(message_enc_2)


######################################################################
####################### SERVER SOCKET ################################
######################################################################

class ServerSocket(threading.Thread):

    def __init__(self, sc, sockname, server):
        super().__init__()
        self.sc                     = sc
        self.sockname               = sockname
        self.server                 = server
        self.n1ckname               = ''
        self.client_public_key      = ''
        self.secret_key             = ''
        self.server_private_key     = import_key('keys/server_private_key.pem', 'banana' )
        self.server_public_key      = import_pub_key('keys/server_public_key.pem')
        self.token_given            = False
        self.provvisory_n1ckname    = ''

    def run(self):
        '''self run from the socket class '''

        # stop signal
        stop_run = False
        #
        # Check if the connection have the token
        #
        while self.token_given == False and stop_run == False:
            #
            # check if there is an incoming request
            #
            dictionary = self.receiver_splitted_message()
            #
            # If there is the request
            #
            if dictionary : 
                D.d('Incoming request')
                #
                # check if the request is named 'server_public_key' to accept it
                #
                if dictionary['request'] == 'server_public_key':
                    #
                    # If there is error in the request report the error
                    #
                    error = self.rsp_server_public_key(dictionary)
                    #
                    # In case of error close everithing
                    #
                    if error: 
                        E.e(f'{error["type"]}')                                                    
                        I.i('closing connection')

                        self.sc.close()
                        server.connections.remove(self)
                        break  
                #
                # Request not supported
                #  
                else:                                                               
                    E.e('Wrong request, closing connection...') 

                    self.sc.close()                    
                    server.connections.remove(self) 
                    break
            #
            # Closing the connection from the client
            #
            else:               
                I.i(f'{self.sockname} has closed the connection')    

                self.sc.close()                    
                server.connections.remove(self)                                                     
                return

        D.d('------------------------------- Token Given ------------------- Accepting only AES communications ')
        #
        # Only AES encrypted communication accept
        #
        try:                                                                                                                                                                                
            while self.token_given == True and stop_run == False:  
                #
                # receiving the request
                #
                dictionary = self.receiver_splitted_message()     

                if dictionary :
                    #
                    # Decrypting the incoming request
                    #   
                    verification , dictionary = self.aes_decrypt(dictionary)
                    #
                    # check if the verification is correct
                    #
                    if verification == True:

                        I.i('Incoming request')
                        #
                        # check if the request is a login request
                        #
                        if dictionary['request']    == 'login':
                            error = self.login(dictionary)  
                            #
                            # In case of error in the login procedure
                            #
                            if error:                                                      
                                E.e(f'{error["type"]}') 

                                self.sc.close()
                                server.connections.remove(self)
                                break   

                        elif    'registration'              == dictionary['request'] :  self.registration(dictionary)

                        ##################################################
                        ############# Signature Required #################
                        ##################################################


                        elif self.request_signature_verification(dictionary) == True:

                            if   'link_to_other_user'       == dictionary['request'] : self.link_to_other_user(dictionary)                                                              

                            elif 'add_recipient_to_client'  == dictionary['request'] : self.add_recipient_to_client(dictionary)                                      
                               
                            elif 'user_swap'                == dictionary['request'] : self.user_swap(dictionary)                                                  
                                          
                            elif 'delete_chats'             == dictionary['request'] : self.delete_chats(dictionary)                                  

                            elif 'message'                  == dictionary['request'] : self.incoming_message_handler(dictionary)

                            elif 'history'                  == dictionary['request'] : self.history_conversation(dictionary)
                                
                            else:                                                               
                                E.e('Signature fericated but invalid request , closing the connection...')        

                                self.sc.close()                    
                                server.connections.remove(self) 
                                break

                        else:                                                               
                            E.e('Invalid request or signature , closing the connection...')        

                            self.sc.close()                    
                            server.connections.remove(self) 
                            break
                    else:                                                               
                        E.e('Verification encryption not valid, closing the connection...') 

                        self.sc.close()                    
                        server.connections.remove(self) 
                        break
                else:               
                    I.i(f'{self.sockname} has closed the connection')  

                    self.sc.close()                    
                    server.connections.remove(self)                                                     
                    return                
                
        except ConnectionResetError:
            E.e('(01) Connection reset by the peer!!')

            self.sc.close()                    
            server.connections.remove(self) 
            stop_run == True

        except Exception as e:
            E.e(f'(1) EXCEPTION HANDLING -> {C.r}{e} {C.x}')
            traceback.print_exc()

            self.sc.close()
            server.connections.remove(self)
            stop_run == True
            return

#################################################################
####################### REQUESTS HANDLER ########################
#################################################################

    def add_recipient_to_client(self, dictionary):
        D.d('Add user to client -> function started')

        # load recipient n1ckname
        recipient = dictionary['recipient_n1ckname']   
        #                                       
        # loading recipient public from the server database
        #
        recipient_public_key = db_pk_withdraw(recipient)                                      

        # if the user is present, load the possible conversations
        if recipient_public_key != False:                                                                                                       

            # load the conversation
            conversations                       = db_load_encrypted_conversations(self.provvisory_n1ckname, recipient) 

            response                            = {}                                                                     
            response['response']                = 'add_recipient_to_client'
            response['response_value']          = True
            response['recipient_n1ckname']      = recipient
            response['recipient_public_key']    = recipient_public_key.decode()
            response['conversations']           = conversations
            # Encripting the response
            response                            = self.aes_encrypt(response)  
            # Sending the encrypted response                         
            self.send_splitted_message(response)  
                                

        else:
            # creating the response
            response                    = {}
            response['response']        = 'add_recipient_to_client'
            response['response_value']  = False
            # encrypting the response
            response                    = self.aes_encrypt(response)
            # send the encrypted response
            self.send_splitted_message(response)
            

    def history_conversation(self, dictionary):
        D.d('History_conversations -> function started')

        result = db_load_encrypted_all_conversations(self.provvisory_n1ckname)
        #
        # Check if the database is empty ( false / false respose )
        #
        if result[0] == False and result[1] == False:
            #
            # If is empty create new history variable and user_list array
            #
        	history = ''
        	users_list = []

        #
        # if the database is not empty
        #
        else:
	        # loading the stored conversations 
	        history        = result[0]
	        # loading the stored users
	        users_list     = result[1]
        #
        # creating an empty disctionary
        #
        users_public_key_pairs = {}
        #
        # retrieving the public key of the users and adding them to the dictionary
        #
        for user in users_list:
            user_public_key = db_pk_withdraw(user)
            users_public_key_pairs[user] = user_public_key.decode()
        #
        # debuggin print
        #
        X.x('Users plublic key pair')
        X.x(users_public_key_pairs)
        #
        # creating the response
        #
        response                            = {}                                                                     
        response['response']                = 'history'
        response['response_value']          = True
        response['history']                 = history
        response['users_public_key_pairs']  = users_public_key_pairs
        #
        # encrypting the request
        #
        response                            = self.aes_encrypt(response) 
        #
        # sending the request        
        #                  
        self.send_splitted_message(response)  

    def aes_decrypt(self, data):   
        D.d('Starting aes_decrypt')

        ciphertext  = bytes.fromhex(data['ciphertext'])
        tag         = bytes.fromhex(data['tag'])
        nonce       = bytes.fromhex(data['nonce'])
        key         = self.token
        cipher      = AES.new(key, AES.MODE_EAX, nonce=nonce)
        plaintext   = cipher.decrypt(ciphertext)
        plaintext   = json.loads(plaintext)
        #
        # Verify the key
        #
        try:
            cipher.verify(tag)
            D.d("The message is verified")
            return True, plaintext

        except ValueError:
            D.d("Key incorrect or message corrupted")
            return False, None

    def aes_encrypt(self,data, token = None):
        D.d('Starting aes_encrypt')
        #
        # Check if there is the token
        if token:
            secret      = token
        else:
            secret      = self.token
        # converting format of the data
        data            = json.dumps(data)  
        # encode the data (binary)           
        data            = data.encode()        
        # loading secret 
        cipher          = AES.new(secret, AES.MODE_EAX)  
        nonce           = cipher.nonce    
        # encryption
        ciphertext, tag = cipher.encrypt_and_digest(data)
        # conversion output in hexadecimal
        output          = {'ciphertext' : ciphertext.hex() , 'tag': tag.hex() , 'nonce':nonce.hex()} 
        # return the output
        return output


    def rsp_server_public_key(self, dictionary):
        D.d('Starting req_server_key function')
        #
        # loading public key of the client from the request
        #
        self.client_public_key          = dictionary['client_public_key'] 
        #
        # importing the public key from the client request
        #
        self.client_public_key          = import_pub_key_digital(self.client_public_key)
        #
        # export the server public key
        #
        server_public_key               = export_pub_key_digital(self.server_public_key)
        #
        # change format of the key
        #
        server_public_key               = server_public_key.decode()
        #
        # check that the file tipe is correct
        #
        current_type_client_pk          = str(type(self.client_public_key))
        aspected_type_client_pk         = "<class 'Crypto.PublicKey.RSA.RsaKey'>"

        if current_type_client_pk   != aspected_type_client_pk:
            #
            # in case the key is not working ( return error )
            #
            return {'error': True, 'type': 'Invalid client public key, closing the connection'}

        # creating the token
        self.token                      = token_bytes(32)
        # Encrypting the token with the server private key
        encrypted_token                 = encrypt_mex(self.token, self.client_public_key)
        # converting token in hexadecimal
        encrypted_token                 = encrypted_token.hex()
        # creating the response
        response                        = {}
        response['response']            = 'server_public_key'
        response['response_value']      = True
        response['server_public_key']   = server_public_key
        response['encrypted_token']     = encrypted_token#
        #
        # set the token as given to confirm the encrypted communication 
        #
        self.token_given = True
        # send the response
        self.send_splitted_message(response)

    def login(self,dictionary):
        D.d('Login request incoming')

        self.provvisory_n1ckname        = dictionary['user_name']    
        self.n1ckname                   = dictionary['user_name']      
        #
        # 
        # MAKE A CHECK FOR THE APPLICATION TO SAVE THE NAME [TO IMPLEMENT]
        # 
        #                                                           
        max_lenght_allowed              = 10
        n1ckname_leght                  = len(self.provvisory_n1ckname)

        if n1ckname_leght > max_lenght_allowed: return {'error' : True, 'type': 'Nickname to long, closing the connection...'}                                                                                           
            
        else:   
                                          
            user_present_response, public_key   = check_n1ckname_into_user_db(self.provvisory_n1ckname)                           # search in the database if the user exist or not
            
            if public_key == None:     
                E.e('Nickname not in the server database, sending response to client ')

                response = {}
                response['response']            = 'login'
                response['response_value']      = False
                response['response_message']    = 'User do not exist on the server database'

                response = self.aes_encrypt(response)
                self.send_splitted_message(response)
                pass
                                                           
            else:
                public_key = import_pub_key_digital(public_key)   
                key_comparison =  True if self.client_public_key == public_key else False                                # compare the keys from the user and the server database
                if user_present_response == True and key_comparison == True:                                             # if user in database and public key match
                    D.d('N1ckname on the server database and public key comparison completed successful')          
                    
                    response                        = {}
                    response['response']            = 'login'
                    response['response_value']      = True
                    response = self.aes_encrypt(response)
                    self.send_splitted_message(response)

                elif key_comparison == False:                                                                              # if the user exist but the public is different
                    E.e('public key comparison failed')
                    I.i('The public key saved in the server is different from the one that the client provide') 

                    response                        = {}
                    response['response']            = 'login'
                    response['response_value']      = False
                    response['response_message']    = 'User exist but the public key provided do not match'
                    response = self.aes_encrypt(response)
                    self.send_splitted_message(response)
                    pass

    def request_signature_verification(self, dictionary):

        D.d('Start request_signature_verification')                                     # check the signature
        signature = dictionary['request_sign']                                          # save the signature
        signature = bytes.fromhex(signature)                                            # convert the signature
        dictionary.pop('request_sign', None)                                            # remove the signature to the request to compare it
        veryfy_signature = verify(dictionary, signature, self.client_public_key)        # verify the signature
        if veryfy_signature == True:                                                    # if signature confirmed, return true else, close connections
            D.d('Signature confirmed')
            return True
        else:
            E.e('Signature Do not match')                                              # Client has closed the socket, exit the thread                    
            I.i(f'{self.sockname} has closed the connection')
            self.sc.close()
            return False                    


######################################################################
####################### MESSAGE HANDLER ##############################
######################################################################


    def incoming_message_handler(self, dictionary):
    	#
    	# Implement confirmation on message sent? [TO IMPLEMENT]
    	#
        I.i(f'New Message')

        recipient = dictionary["recipient"]                                                             # check the recipient of the message
        message = f'-Encrypted-'

        I.i( '-' * 60 )
        I.i( f'Socket-name = {C.magenta_clean(self.sockname)} ')                                        # print in to the server
        I.i( f'Sender      = {C.green_clean(self.n1ckname)} ')                                           # detail about the incoming message
        I.i( f'Recipient   = {C.cyan_clean(recipient)}')
        I.i( f'Message     = {C.yellow_clean(message)}')
        I.i( '-' * 60)         

        # add the sender from the sender so the client cannot change it
        dictionary['sender']            = self.n1ckname 

        del dictionary['request']

        dictionary['response']          = 'message'

        message_encrypted_sender        = dictionary['message_encrypted_sender']
        message_sign_sender             = dictionary['message_sign_sender']  
        message_encrypted_recipient     = dictionary['message_encrypted_recipient']
        message_sign_recipient          = dictionary['message_sign_recipient']        

        db_update_chat_on_server(self.n1ckname, recipient, message_encrypted_sender, message_sign_sender, message_encrypted_recipient, message_sign_recipient )
      
        self.server.redirect_message_to_reveiver(dictionary, recipient, self.sockname, self.n1ckname)   # send the message to the redirector


######################################################################
####################### GENERAL FUNCTIONS ############################
######################################################################


    def registration(self, dictionary):
        #
        # register the new user in the server user_db
        #
        D.d('Starting registration function')

        self.provvisory_n1ckname            = dictionary['n1ckname']
        self.client_public_key              = dictionary['public_key'] 
        self.client_public_key              = import_pub_key_digital(self.client_public_key)

        #
        # CHECK VALIDITY OF THE PROVVISORY NICKNAME BEFORE TO CHECK ON THE SERVER (max 10 char and no specila) [TO IMPLEMENT]
        #

        D.d(f'Public key = {self.client_public_key}')
 
        user_present_check , public_key =  check_n1ckname_into_user_db(self.provvisory_n1ckname)

        if user_present_check == False:

            db_registration(self.provvisory_n1ckname,export_pub_key_digital(self.client_public_key))

            scan_table('user_pk.db','Name')

            I.i(f'User {self.provvisory_n1ckname} registered')
            #
            # creation of the response
            #
            response                    = {}
            response['response']        = 'registration'
            response['response_value']  = True
            response = self.aes_encrypt(response)
            self.send_splitted_message(response)

        else:
            # 
            # user already exist
            #
            D.d('User already exist on the server database')                                
            #
            # Creation of the response
            #
            response                    = {}                                                                   
            response['response']        = 'registration'
            response['response_value']  = False
            response = self.aes_encrypt(response)
            self.send_splitted_message(response)


    def user_swap(self, dictionary):
        #
        # function not in use ATM from the client. destinated for the command line interface [TO IMPLEMENT]
        #
        # check if the user exist in the server database and response the public key 
        #

        D.d('Start for use swap function')

        user_to_swap = dictionary['recipient']                                                              # user to swap with

        user_present_response , user_to_swap_public_key = check_n1ckname_into_user_db(user_to_swap)         # check if user in server db and save the public key
        
        if user_present_response == True:                                                                   # if the user is present

            conversations = db_load_encrypted_conversations(self.n1ckname, user_to_swap)

            response = {}                                                                                   # create teh response
            response['response'] = 'user_swap'
            response['response_value'] = True
            response['user_to_swap_public_key'] = user_to_swap_public_key.decode()
            response['conversations'] = conversations 
            response = self.aes_encrypt(response)
            self.send_splitted_message(response)                                                            # send the response

        else:                                                                                               # if the user is not present

            response = {}                                                                                   # create the response
            response['response'] = 'user_swap'
            response['response_value'] = False
            response = self.aes_encrypt(response)
            self.send_splitted_message(response)                                                            # send the message

    def link_to_other_user(self, dictionary):
        #
        # change the chat for the client command line interface
        #
        D.d('Link to other user function started')

        recipient = dictionary['recipient_n1ckname']                                          # load recipient n1ckname
        D.d(f'Recipient to swap whit n1ckname -> {recipient}')      
        
        recipient_public_key = db_pk_withdraw(recipient)                                      # loading recipient public from the server db

        if recipient_public_key != False:                                                     # if there is the public key of the recipient                                                  

            conversations = db_load_encrypted_conversations(self.provvisory_n1ckname, recipient) 

            response = {}                                                                     # create the request
            response['response'] = 'link_to_other_user'
            response['response_value'] = True
            response['recipient_n1ckname'] = recipient
            response['recipient_public_key'] = recipient_public_key.decode()
            response['conversations'] = conversations
            response = self.aes_encrypt(response)                           
            self.send_splitted_message(response)  

            self.n1ckname = self.provvisory_n1ckname                                    

        else:

            response = {}
            response['response'] = 'link_to_other_user'
            response['response_value'] = False
            response = self.aes_encrypt(response)
            self.send_splitted_message(response)


    def delete_chats(self, dictionary):
        #
        # Delete the chats from the server database
        #
        I.i('Start delete chat function')
        # recipient of the chat coming from the client
        recipient_n1ckname = dictionary['recipient_n1ckname']                       
        # colling the database function to delete the chat
        db_erase_user_chat(self.n1ckname, recipient_n1ckname)                      
        # creation of the response for the client
        response= {}                                                        
        response['response'] = 'delete_chats'
        response['response_value'] = True
        response = self.aes_encrypt(response)
        self.send_splitted_message(response)

######################################################################
#################### SEND RECEIVE FUNCTIONS ##########################
######################################################################

    def send_splitted_message(self, message):
        #
        # reorganize the message size to be sended correctly (send message that are bigger of the normal buffer side (1024))
        #
        message = json.dumps(message)
        msg = struct.pack('>I', len(message)) + message.encode()
        self.sc.sendall(msg)

        D.d('Message splitted sent')

    def receiver_splitted_message(self):
        #
        # rebuild of the message that has been sended splitted to stay in the allowed size 
        #
        ''' read the head of the incoming packet '''
        raw_msglen = self.recvall(4)
        if not raw_msglen:
            return None
        msglen = struct.unpack('>I', raw_msglen)[0]
        # Read the message data
        dictionary = self.recvall(msglen)
        dictionary = json.loads(dictionary)
        return  dictionary

    def recvall(self,n):
        #
        # reorder the incoming bite (Helper function to recv n bytes or return None if EOF is hit)
        #
        data = bytearray()
        while len(data) < n:
            packet = self.sc.recv(n - len(data))
            if not packet:
                return None
            data.extend(packet)
        return data


######################################################################
#################### EXIT THREAD #####################################
######################################################################

def exit(server):
    #
    # shout down the server and all the server connection (.quit)
    #
    while True:
        ipt = input('')
        if ipt == '.quit':
            I.i('Closing all connections...')
            for connection in server.connections:
                connection.sc.close()
            I.i('Shutting down the server...')
            os._exit(0)

######################################################################
########################### MAIN #####################################
######################################################################

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Chat Server')

    parser.add_argument('-p', metavar='PORT', type=int, default=4444, help='TCP port (default 4444)')
    args = parser.parse_args()    

    ###########################################################
    # This is the server ip , change it in the real schenario #
    ###########################################################
    server_ip = '127.0.0.1' 

    server = Server(server_ip, args.p)
    server.start()    
    exit = threading.Thread(target = exit, args = (server,))
    exit.start()