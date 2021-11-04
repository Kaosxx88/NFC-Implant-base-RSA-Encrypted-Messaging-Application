#!/usr/bin/env python3
# Autor @kaosxx88
# registration functions
# [FILE NOT IN USE ATM] -> needed for command line user interface


import os
import ssl
import json
import time
import socket
import struct 
import os.path
import argparse
import threading
from colors import *
from random import randint 
from getpass import getpass
from Crypto.Cipher import AES
from rsa_keys_manager import *
from database_functions import *






######################################################################
######################## CLIENT ######################################
######################################################################



class Client:    

    def __init__(self,   private , public , nickname , progress_callback): 

        # emit signal to gui
        self.progress_callback = progress_callback
        self.progress_callback.emit('Building client')  

        self.host                       = "127.0.0.1"
        self.port                       = "4444"  
        self.n1ckname                   = nickname
        self.response                   = ''
        self.private_key                = private
        self.user_public_key            = public
        self.server_public_key          = ''

        self.recipient_n1ckname         = ''
        self.responde_is_arrived        = False       
        self.user_check_server_response = ()
       
        self.start()
       

    def start(self):

        self.progress_callback.emit('Start') 
        # estabilish the connection with the server
        if self.connection_to_the_server() == True:
            # start the receiver thread                                         
            self.receive = Receive(self.ssock, self.recipient_n1ckname, self.n1ckname, self)                            
            self.receive.start() 

            self.req_server_public_key()

            self.registration()   

        else:
            D.d ('No connection to the server')
            pass 

######################################################################
#################### CLIENT FUNCTIONS ################################
######################################################################

    def n1ckname_input(self, type_of_validation):
        #
        # function to get the username from the user ( sendr or recipient )
        # 

        if type_of_validation == 'sender':
            message = (f'{ C.info }Please insert your nickname ("exit" to quit): ')

        elif type_of_validation == 'recipient':
            message = (f'{C.info}please write the n1ckname of the person to link with: ("exit" to quit): ')

        print (message, end='')
        user_input = input()  
        # validation input
        # > 0 | <= 10 | only alphanumeric
        while len(user_input) == 0 or len(user_input) > 10 or user_input.isalnum() == False:                           
            E.e('Minimum n1ckname length 1 , Max user length 10, only alphanumeric value allowed')
            print (message, end='')
            user_input = input()

        if user_input == 'exit' :                                                                                      
            I.i('Thanks for using the application')
            I.i('...Closing the connection...')
            # close the connection
            os._exit(0)
        else:
            return user_input


    def req_server_public_key(self):        
        #
        # request publick key to the server with the token for encryption
        #

        request                          = {}
        request['request']               = 'server_public_key'
        request['client_public_key']     = export_pub_key_digital(self.user_public_key).decode('utf-8') 

        self.send_splitted_message(request)
        
        if self.wait_for_server_response() == True:

            response = self.response['response']                                                             

            if response == 'server_public_key' :

                self.server_public_key  = self.response['server_public_key']
                self.server_public_key  = import_pub_key_digital(self.server_public_key)
                self.token              = self.response['encrypted_token']                                                   
                self.token              = bytes.fromhex(self.token)                                                           
                self.token              = decrypt_mex(self.token, self.private_key)                           


    def aes_encrypt(self,data):
        #
        # encrypt with AES ( token size)
        #
        D.d('Starting aes_encrypt')
        secret  = self.token

        data    = json.dumps(data)                                                              # string
        data    = data.encode()                                                                 # binary

        cipher  = AES.new(secret, AES.MODE_EAX)                                                 # bin
        nonce   = cipher.nonce                                                                  #bin
        ciphertext, tag = cipher.encrypt_and_digest(data)                                       # bin

        output  = {'ciphertext' : ciphertext.hex() , 'tag': tag.hex() , 'nonce':nonce.hex()}    # hexa

        return output

    def aes_decrypt(self, data):   
        #
        # decrypt the AES encryption
        #
        D.d('Starting aes_decrypt')

        ciphertext  = bytes.fromhex(data['ciphertext'])
        tag         = bytes.fromhex(data['tag'])
        nonce       = bytes.fromhex(data['nonce'])
        key         = self.token
        cipher      = AES.new(key, AES.MODE_EAX, nonce=nonce)
        plaintext   = cipher.decrypt(ciphertext)
        plaintext   = json.loads(plaintext)

        try:
            cipher.verify(tag)
            D.d("The message is verified")
            return True, plaintext

        except ValueError:
            D.d("Key incorrect or message corrupted")
            return False, None


    def registration(self):
        #
        # function to register the new user
        #
        self.progress_callback.emit('Registration start') 

        I.i('Registration process starting...\n') 


        request                 = {}                                                                                    
        request['request']      = 'registration'
        request['n1ckname']     = self.n1ckname
        request['public_key']   = export_pub_key_digital(self.user_public_key).decode('utf-8')

        request = self.aes_encrypt(request)

        self.progress_callback.emit('Sending request to the server')  

        self.send_splitted_message(request)


        self.progress_callback.emit('Waiting server response')  

        if self.wait_for_server_response() == True:
            response_name   = self.response['response']
            response_value  = self.response['response_value']    
            if response_name == 'registration' and response_value == True:
                D.d('User registered')
                # send to login

                self.user_check_server_response = (True, 'Registered')
                self.ssock.shutdown(1)
                #self.ssock.close()
                #os._exit(0)                  

            elif response_name == 'registration' and response_value == False:
                E.e('User already exist on the server database, try another Nickname')
                # start loop again
                user_selction = ''      

                self.user_check_server_response = (False, 'Nickname already taken')

                self.ssock.shutdown(1)
                #self.ssock.close()
                #os._exit(0)  

    def return_value(self):
        #
        # function to get the check from another class
        #
        return self.user_check_server_response

        
    def update_server_response(self, response):
        #
        # function to update the response from the server (the receive section trigger it)
        #
        D.d(f'New response')
        # print the incoming response
        for element in response: D.d(f'{element} = {response[element]}')   
        # allocate the response to the self.response                                                     
        self.response = response                       
        # print the response type                                                                         
        D.d(f'Response type  -> {C.yellow_clean(self.response["response"])}')                                                   
        response_value = self.response["response_value"]                                                                        
        # check if the response value is True
        # print in red if false and green if true
        D.d(f'Response value -> {C.green_clean(response_value) if response_value == True else C.red_clean(response_value)}')    
        # flag that the response is arrived
        self.responde_is_arrived = True                                                                                         
                                        
    def wait_for_server_response(self):                                     
        #
        # loop to wait for a server response
        #
        #    
        # 30 seconds (300 * 0.1)                                    
        second_to_wait = 300     
        # wait for server response                                                                                                 
        while second_to_wait != 0 and self.responde_is_arrived == False:                                        
            D.d(f'Response is arrived? -> {self.responde_is_arrived}')                                                  
            D.d(f'...Waiting for server response... ')     
            # Sleep 0.1 seconds                                                                                
            time.sleep(0.1)       
            # decrease the variable for each iteration                                                                                                                 
            second_to_wait -= 1       
        # reset the notification variable                                                                                          
        self.responde_is_arrived = False                                                                                        
        # if time ended (no response arrived)                          
        if second_to_wait == 0: 
            # close the connection if server do not response after 30 second                                                                                                
            D.d(f'No server response after 30 seconds, operation aborted')                                      
            E.e('No response from the server, Closing application...')                                      
            self.ssock.shutdown(1)                                                                                                  
            os._exit(0) 
        # if time not ended (response arrived)                                        
        else:                                                                                                                   
            D.d(f'Response arrived from the server')                                        
            return True                                     
                                        
    def load_private_key(self):    
        #
        # load private key from location [NOT IN USER] just for testing 
        #                                                                                             
        D.d('Starting load_private_key function ')
        ''' Load private key from username_private_key.pem'''
        message = (f'{C.info}Please enter the phassprhrase for the private_key.pem file: ' )
        print(message)
        passphrase = getpass('\r')

        try:
            private_key = import_key(f'private_key/private_key.pem', passphrase)
            I.i ('Private key loaded')
            return private_key

        except Exception as e:
            E.e (f'Private key not loaded correctly (it is a valid key? it is a correct passphrase?)') 
            I.i ('...client Shutting down...')
            os._exit(0)




    def send_splitted_message(self, dictionary):
        #
        # send message that are bigger of the normal buffer side (1024) '''
        #
        D.d('Starting send_splitted_message function ')        
        dictionary = json.dumps(dictionary)                                                                         
        msg = struct.pack('>I', len(dictionary)) + dictionary.encode()                                              
        self.ssock.sendall(msg)         
            
 

    def import_user_public_key(self):
        #
        # [NOT IN USE] just for testing
        # 
        key_name = f'public_key/public_key.pem'                                                         
        self.user_public_key = import_pub_key(key_name)                                                                 
                                


    def connection_to_the_server(self):                     
        #
        #   handle server connection
        #    
        try:                        
            D.d(f'Trying to connect to {self.host}:{self.port}...')    
            # ssl setting                                                             
            context     = ssl.SSLContext(ssl.PROTOCOL_TLS)  
            # create the connection Thread                                 
            self.sock   = socket.create_connection((self.host, self.port))    
            # wrap the connection                                                      
            self.ssock  = context.wrap_socket(self.sock, server_hostname=self.host)    
            # check ssocket version                                              
            I.i(f'Connection secured by {self.ssock.version()}')      
            # I.i connection establisih                                                               
            D.d(f'Successfully connected to {self.host}:{self.port}')                                                       
            
            return (True)    
        # error in case of connection refuse (client offline, server not up)
        except ConnectionRefusedError:                                  
            E.e('Server unreachable')  
            self.user_check_server_response = (False, 'Server unreachable')                                                                                            
            #os._exit(0) 

            return (False)                                                                                                
                        




######################################################################
######################## RECEIVE THREAD ##############################
######################################################################       

class Receive(threading.Thread):    

    def __init__(self, ssock, recipient_n1ckname, n1ckname, client_thread):
        super().__init__()
        self.ssock              = ssock  
        self.recipient_n1ckname = recipient_n1ckname
        self.n1ckname           = n1ckname
        self.client_thread      = client_thread


    def run(self): 

        registration_process_complete = False
        
        while registration_process_complete != True:                                                                         
            dictionary = self.receiver_splitted_message()                                 

            if dictionary: 
                D.d(dictionary) 

                dictionary = json.loads(dictionary) 

                if 'response' in dictionary and dictionary['response'] == 'server_public_key': 

                    Client.update_server_response(self.client_thread, dictionary)

                else:

                    verification , dictionary =  Client.aes_decrypt(self.client_thread, dictionary)

                    if verification == True:


                        Client.update_server_response(self.client_thread, dictionary)             

                    else:
                        E.e('Incorrect verification, closing the application of the response')

            else:                
                
                I.i('Connection with the server closed, (registration.py')                        
                #self.ssock.shutdown(1)                                                        
                registration_process_complete = True             
                #os._exit(0)                                                                 



######################################################################
#################### INCOMING MESSAGE HANDLER ########################
######################################################################


    def receiver_splitted_message(self):
        #
        # function to read custom data lenth in data receiving
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


if __name__ == '__main__':
    parser  = argparse.ArgumentParser(description='chat')
    parser.add_argument('-host', default='127.0.0.1' , help='Interface the server listens at')
    parser.add_argument('-p', metavar='PORT', type=int, default=4444, help='TCP port (default 4444)')
    args    = parser.parse_args()
    client  = Client(args.host, args.p)
    client.start()