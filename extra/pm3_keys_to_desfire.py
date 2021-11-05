#!/usr/bin/python
# author @Kaosxx88
# script to write private/ public key data into the MIFARE DESfire

import rsa
import binascii
import subprocess, re
from io import StringIO 
from Crypto.PublicKey import RSA

# MIFARE DESfire Card Master Key
mfdes_CMK = '9999999999999999'  
# MIFARE DESfire Application Master Key
mfdes_AMK = '0000000000000000'  


##################################
# This is to be changed accordly #
#########################################################
                                                        #
# system proxmark3 repo path                            #
pmx3_path = "/home/kali/project/proxmark3/client/"      #
                                                        #
#########################################################

#easy sample 
#hf mfdes auth -m 1 -t 1 -a 000000 -n 0
#hf mfdes createaid -a 888888 -k 0E -l 2E --name Public_key -f 8888
#hf mfdes createfile -a 888888 -f 8888 -n 01 -c 0 -r EEEE -s 000320

#################################################################
############# SET THE SPACE (60) ON THE KEY FILE ################
#################################################################

def format_key(x):
    #
    # format the imported PRIVATE/PUBLIC key in line of 60 characters
    #
    count = 0
    key = ""
    for i in x:
        if count == 60:
            key +="\n"
            count = 0
        count +=1
        key += i
    print (key)
    return key

#################################################################
############# LOAD THE KEY FROM THE PROXMARK  ###################
#################################################################

def Load_private_key_from_pmx3(pmx3_path):
    #
    # function to load the private key from the proxmark
    #
    private_key = ""    
    
    p = subprocess.Popen(f" {pmx3_path}proxmark3 /dev/ttyS0 -c 'hf mfdes readdata -n01 -t 0 -o 000000 -l 000CF0 -a 999999'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
    #
    # check if there is some error in the reading
    #
    if "[!]".encode() in p : 
        print ("\n\nError\n\nPlease Try Again")
        print (p)
    #
    # if there is not error in the reading
    #
    else:
        for i in p.split("\n".encode()):

            print (i.decode())

            private_key += i.decode()
        
        print ("Private key founded\n")

        # regex to filter the downloaded data
        regex           = r'[\w]{2}[\w\w\s]{43}[\w]{2}'
        # revoving all the part that we do not need
        private_key     = re.findall(regex,private_key,re.M)
        # removing all the spacing from the dump
        private_key     = ' '.join(private_key).replace(" ", "")
        # Removing the last 2 hrx character that are not needed
        private_key     = (private_key[:-4])
        # format the correct spacing
        private_key     = format_key(private_key)       
        # convert in byte for import the key
        private_key     = bytes.fromhex(private_key)
        # decode the byte
        private_key     = private_key.decode()
        #
        # display the loaded key
        #
        print (private_key)
        #   
        # import the key 
        # 
        private_key     = RSA.import_key(private_key, 'banana')
        #
        # check the key time
        #
        print(type(private_key))
        return private_key

#################################################################
############# PROCESS TO LOAD THE KEY IN TO THE PM3 #############
#################################################################


#################################################################
###### IMPORT PRIVATE (PEM) AND TRANFORM IN TO HEX ##############
#################################################################

def import_Key(key_pem):
    with open(key_pem,'r') as f:
        private_key = f.read()

        print(private_key)
        a = RSA.import_key(private_key, 'banana')
        print (type(private_key))
        private_key = bytearray(private_key, "utf8")        # converted in binary
        private_key = binascii.hexlify(private_key)         # converted in hex
        private_key = private_key.decode()                  # decode in str
        print (private_key)

    return (private_key)


def create_arrey_key():
    #
    # creating a turple with the hex key splitted by line,
    # so later I can sent line by line in the proxmark and then load it to the card
    #
    # Splitting the hex to group of 94 elements
    #
    print ("create_arrey_key")
    priv_key_hex = import_Key("private/private_key.pem")    
    letter_count = 1
    line_count = 1
    hex_value_line = ""
    hex_map= []
    for i in priv_key_hex:
        letter_count += 1
        hex_value_line += i
        #
        # 95 is the number of letters that the  proxmark3 easy can write in one round (in one command alone) 
        #
        if letter_count == 95 : 
            letter_count =1         
            hex_map.append(hex_value_line)
            line_count += 1
            hex_value_line = ""
    hex_map.append(hex_value_line)
    print ("\n\n\n\nHex Mamps\n\n\n\n")
    print (hex_map)

    return hex_map


def create_file_with_private_key_for_the_proxmark():
    #
    # This function create a file with the list of commands to be sent to the proxmark
    # 
    # format and create the file to input in the proxmax command
    #
    pmx3_commands = ""
    # autheticate with the CMK
    pmx3_commands +=  f"hf mfdes auth -m 1 -t 1 -a 000000 -n 0 -k {mfdes_CMK}\n"
    # erase the cards
    pmx3_commands +=  f"hf mfdes formatpicc\n"
    # authenticate again with the CMK
    pmx3_commands +=  f"hf mfdes auth -m 1 -t 1 -a 000000 -n 0 -k {mfdes_CMK}\n"
    # crete the private key application
    pmx3_commands +=  f"hf mfdes createaid -a 999999 -k 0E -l 2E --name Private_key -f 9999\n"
    # crete the file for the private key
    pmx3_commands +=  f"hf mfdes createfile -a 999999 -f 9999 -n 01 -c 0 -r EEEE -s 000CF0\n"
    # autheticate with the CMK
    pmx3_commands +=  f"hf mfdes auth -m 1 -t 1 -a 999999 -n 0 -k {mfdes_AMK}\n"
    # load the private key splitted 
    hex_map = create_arrey_key()
    line = 0
    #
    # different line that we need to load the key in the memory with offset
    #
    for i in range(0,3295,47): 
        x = str(hex(i))[2:]
        pmx3_commands +=  f"hf mfdes writedata -a 999999 -n 01 -t 0 -o {x.zfill(6)} -d {hex_map[line]}\n" 
        line +=1
    #
    # write the set of commands created into a file (pmx3.cmd) 
    # 
    with open('pmx3.cmd','w') as f:
        f.write(pmx3_commands)




def Load_priv_key_to_pmx3(pmx3_path):
    #
    # this function load the file pmx3.cmd, and send all the commands inside to the proxmark, then all the data will be written to the DESfire card
    #
    # load the key into the proxmark
    #
    print ("Load_priv_key_to_pmx3")
    output = ""
    exit = False

    p = subprocess.Popen(f" {pmx3_path}proxmark3 /dev/ttyS0 -s pmx3.cmd", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]

    if "!".encode() in p : 
        print ("\n\nError\n\n")
        for i in p.split("\n".encode()):
            check = i.decode()
            if "!" in check:
                print (i.decode())
    else:
        for i in p.split("\n".encode()):
            print (i.decode())      
        print ("Private key Loaded in proxmark3 without errors\n")


# test half script

#Load_private_key_from_pmx3()
#create_file_with_private_key_for_the_proxmark()
#Load_priv_key_to_pmx3()




#################################################################
###### IMPORT PUBLIC (PEM) AND TRANFORM IN TO HEX ##############
#################################################################

def import_Key2(key_pem):
    #
    # function to import the key
    #
    print (' Start import key 2')
    with open(key_pem,'r') as f:
        key = f.read()
        key = bytearray(key, "utf8")        # converted in binary
        key = binascii.hexlify(key)         # converted in hex
        key = key.decode()                  # decode in str

    return (key)


def create_arrey_key2():
    #
    # This function create a file with the list of commands to be sent to the proxmark
    # 
    # format and create the file to input in the proxmax command
    #
    print ("create_arrey_key")
    priv_key_hex = import_Key2("public/public_key.pem")     
    letter_count = 1
    line_count = 1
    hex_value_line = ""
    hex_map= []
    for i in priv_key_hex:
        letter_count += 1
        hex_value_line += i
        #
        # 95 is the number of letters that the  proxmark3 easy can write in one round (in one command alone) 
        #
        if letter_count == 95 :  
            letter_count =1         
            hex_map.append(hex_value_line)
            line_count += 1
            hex_value_line = ""
    hex_map.append(hex_value_line)
    print ("\n\n\n\nHex Mamps\n\n\n\n")
    print (hex_map)

    return hex_map


def create_file_with_public_key_for_the_proxmark():
    #
    # format and create the file to input in the proxmax command
    # 
    pmx3_commands = ""

    hex_map = create_arrey_key2()
    line = 0
    #
    # different line that we need to load the key in the memory with offset
    #
    for i in range(0,799,47): 
        x = str(hex(i))[2:]
        pmx3_commands +=  f"hf mfdes writedata -a 888888 -n 01 -t 0 -o {x.zfill(6)} -d {hex_map[line]}\n" 
        line +=1
    #
    # write all the commands in a file (pmx3.cmd)
    #
    with open('pmx3.cmd','w') as f:
        f.write(pmx3_commands)


def Load_private_key_to_the_proxmark(pmx3_path):
    #
    # load private key to the proxmark
    #
    print ("Load_priv_key_to_pmx3")
    output = ""
    exit = False

    p = subprocess.Popen(f" {pmx3_path}proxmark3 /dev/ttyS0 -s pmx3.cmd", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]

    if "!".encode() in p : 
        print ("\n\nError\n\n")
        for i in p.split("\n".encode()):
            check = i.decode()
            if "!" in check:
                print (i.decode())
    else:
        for i in p.split("\n".encode()):
            print (i.decode())      
        print ("Private key Loaded in proxmark3 without errors\n")


def Load_private_key_from_pmx32(pmx3_path):
    #
    # Loading the public key from the proxmark
    #


    private_key = ""    
    
    p = subprocess.Popen(f" {pmx3_path}proxmark3 /dev/ttyS0 -c 'hf mfdes readdata -n01 -t 0 -o 000000 -l 000320 -a 888888'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]

    if "[!]".encode() in p : 
        print ("\n\nError\n\nPlease Try Again")
        print (p)
    else:
        for i in p.split("\n".encode()):

            print (i.decode())

            private_key += i.decode()
        
        print ("Private key founded\n")

        # regex to filter the downloaded data
        regex           = r'[\w]{2}[\w\w\s]{43}[\w]{2}'
        # revoving all the part that we do not need
        private_key     = re.findall(regex,private_key,re.M)
        # removing all the spacing from the dump
        private_key     = ' '.join(private_key).replace(" ", "")
        # Removing the last 2 hrx character that are not needed
        private_key     = (private_key[:-2])
        # format the correct spacing
        private_key     = format_key(private_key)       
        # convert in byte for import the key
        private_key     = bytes.fromhex(private_key)
        # decode the byte
        private_key     = private_key.decode()

        print (private_key)
        

        # import the key
        private_key     = RSA.import_key(private_key)

        print(type(private_key))
        return private_key




########################################################
# WRITING OF THE PUBLIC AND PRIVATE KEY ON THE DESFIRE #
########################################################


if __main__ == "__name__":

    # Create a file with the private key
    create_file_with_private_key_for_the_proxmark()
    # load the private key to the desfire chip
    Load_priv_key_to_pmx3(pmx3_path)
    # create a file with the public key
    create_file_with_public_key_for_the_proxmark()
    # load the private key to the proxmark
    Load_private_key_to_the_proxmark(pmx3_path)


