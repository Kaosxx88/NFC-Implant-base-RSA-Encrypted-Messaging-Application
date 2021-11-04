#!/usr/bin/env python3
# Autor @kaosxx88
# functions to read MIFARE DESfire card with the proxmark3 easy

import re
import sys
import traceback
import subprocess
from Crypto.PublicKey import RSA


class Pmx3_read_keys_from_desfire:
    #
    # class to read the key from the MIFARE DESfire chip (card/implant)
    #

    def __init__(self, pmx3_port, passphrase, progress_callback):
        
        # linux case  for the moment
        #self.pmx3_path      =  '/usr/local/bin/proxmark3'
        self.pmx3_path      =  '/path/to/proxmark/github/pm3'
        
        
        self.pmx3_port      = pmx3_port
        self.private_key    = ""
        self.public_key     = ""    
        self.passphrase     = passphrase
        self.error          = None

        #print (self.pmx3_path)
        #print (self.pmx3_port)

        self.progress_callback = progress_callback

        self.progress_callback.emit('Check if a chip is present on the field')

        # Select the master application to check if the card is present on the proxmark field
        #response = subprocess.Popen(f" {self.pmx3_path} {self.pmx3_port} -c 'hf 14a apdu -st 5A 00 00 00'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,  text=True).communicate()[0]
        response = subprocess.Popen(f" {self.pmx3_path} -c 'hf 14a apdu -st 5A 00 00 00'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,  text=True).communicate()[0]
                
        # Split the response in line
        response = response.split('\n')
        

        #print (response)

        # Check if another process is using the proxmark
        if response[6][:3] == '[!]':
            
            self.error = response[6][11:]      
            self.progress_callback.emit('Another process is using the reader')

        else:

            self.progress_callback.emit('Proxmark available')

            try:
                # Check if the master app has been selected and the reponse is ok
                if response[10]  == '[+] <<< status: 00 00 - ':

                    self.progress_callback.emit('Defire card present on the reader')

                    # load the private key
                    self.private_key  = self.read_key(self.passphrase)

                    if self.error :
                        pass
                    else:
               
                        # load the public key
                        self.public_key = self.read_key()

                        self.progress_callback.emit(f'Process Completed!!!')

                    

            # response short no card on field
            except Exception as e:

                traceback.print_exc()
                self.error = ('\nNo valid DESFire chip on proxmark field\n')
                self.progress_callback.emit(f'No valid DESFire chip on proxmark field')



    def read_key(self, passphrase = None):

        
        error               = None
        key                 = ''
        regex               = r'[\w]{2}[\w\w\s]{43}[\w]{2}'

        if passphrase:
            key_type        = 'Private'
            memory_size     = '000CF0'
            application_id  = '999999'
            tail_to_remove  = -4


        else:
            key_type        = 'Public'
            memory_size     = '000320'
            application_id  = '888888'
            tail_to_remove  = -2

        self.progress_callback.emit(f'Trying to retrive the {key_type} key')

        #response = subprocess.Popen(f" {self.pmx3_path} {self.pmx3_port} -c 'hf mfdes readdata -n01 -t 0 -o 000000 -l {memory_size} -a {application_id}'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,  text=True).communicate()[0]
        response = subprocess.Popen(f" {self.pmx3_path} -c 'hf mfdes readdata -n01 -t 0 -o 000000 -l {memory_size} -a {application_id}'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,  text=True).communicate()[0]

        response = response.split('\n')

        self.progress_callback.emit(f'{key_type} key raw data loaded')

        # Check if there is any error
        for line in response:
            if line[:3] == '[!]':
                self.error = (f'\n{line}')
                print (self.error)
                self.progress_callback.emit(f'Error in the row key data ')
                return
                
            else:
                key += line

        self.progress_callback.emit(f'No errors in the row key data ')

        # revoving all the part that we do not need
        key = re.findall(regex, key, re.M)

        # removing all the spacing from the dump
        key = ' '.join(key).replace(" ", "")

        # Removing the last 2 hrx character that are not needed
        key = (key[:tail_to_remove])

        self.progress_callback.emit(f'{key_type} key resized')

        # format the correct spacing
        formatted_key = ''

        for i in range(len(key)):
            if i % 60 == 0:
                formatted_key += '\n'
            formatted_key += key[i]

        self.progress_callback.emit(f'{key_type} key padding')
        key = formatted_key

        # convert in byte for import the key
        print (key)
        key = bytes.fromhex(key)
        # decode the byte
        key = key.decode()

        self.progress_callback.emit(f'{key_type} key decode')

        try:
            # differentiate the keys (public and private)
            if passphrase:

                self.progress_callback.emit(f'{key_type} key validate passphrase')
                # importing the keys
                key  = RSA.import_key(key, passphrase)
            else:
                key  = RSA.import_key(key)

            self.progress_callback.emit(f'{key_type} Key Imported Correctly')

        except Exception as e:
            traceback.print_exc()
            self.error = ('\nWrong Padding, \nis the passphrase correct?')
            self.progress_callback.emit(f'Wrong padding, passphrase incorrect?')  

        return key




###################
# Testing purpuse #
###################

# if __name__ == '__main__':

#     pmx3_path           = "/home/kali/project/proxmark3/client/"
#     pmx3_port           = "/dev/ttyS0"
#     passphrase          = 'banana'

#     key = Pmx3_read_keys_from_desfire(pmx3_port, passphrase)

#     print ()
#     print (key.private_key)
#     print (key.public_key)

    


