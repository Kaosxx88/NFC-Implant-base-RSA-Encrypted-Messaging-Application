

<img align="left" width="200" src="https://github.com/Kaosxx88/NFC-Implant-base-RSA-Encrypted-Messaging-Application/blob/main/client/images/logo/logo1.png?raw=true">
<br>

# &nbsp;&nbsp; N.I.R.E.M.A.
### NFC Implant-base RSA Encrypted Messagging application
<br clear="left"/>
<br>
This project aims to develop an NFC implant-based RSA encrypted messaging application that ensures secure  communication  between  the  users  and  lets  the  user  be  the  only  one  who  can  decrypt  the exchanged messages. Besides secure transmission, this application focuses on saving the user private key on an external underskin implant. Thanks to the Mifare DESFire chip’s security, the user can keep out-system the private key used to sign and encrypt the communications.  Therefore, the only way to access the messages will be with the possession of the unique implant.


# Installation steps on Linux Debian base
- [ Setup proxmark3 client and firmware ](#proxmark3-client-version)
- [ Installation Server Side ](#installation-server-side-linux-debian-base)
- [ Installation Client Side ](#installation-client-side-linux-debian-base)
- [ Start the server](#start-the-server-application)
- [ Start the client](#start-the-client-application)

# Hardware required
- [ Proxmark3](#proxmark3)
- [ACR](#acr)
- [ MIFARE DESfire ](#mifare-desfire)

# Documentations
- [ N.I.R.E.M.A. file structure ](#nirema-file-structure)
- [ Registration ](#registration)
- [ Login ](#login)
- [ Chat GUI ](#chat-gui)
- [ MIFARE DESfire structure](#mifare-desfire-structure)
- [ Request schema](#requests-schema)
- [ Application flow](#application-flow)
- [ Database structure](#database-structure)
- [ Creation of a DESFIRE MIFARE app](#creation-of-a-desfire-mifare-apps)
- [ Credit](#credit)





# Proxmark3 client version 
ATM this application is not working with the last version of the [Iceman proxmark firmware](https://github.com/RfidResearchGroup/proxmark3). (There are problems related to the dinanic memory).
[HERE]((https://github.com/RfidResearchGroup/proxmark3/tree/ea80ea21ad5bfba83a8c63d30b1bbfc4d8adde2b)) there is the last tested working version, released 20,2021 (ea80ea2).

The proxmark firmware and client should be matching every time. But as I have tested the firmware of the 4-11-2021 with the client of the 20-5-2021, I can confirm that it is working for this occasion. ( I am explain that so if you have a proxmark3 with the last firmware you do not need to reflash it with an old one.)



# Installation Server Side (Linux Debian base)
- cloning the repo

```git clone https://github.com/Kaosxx88/NFC-Implant-base-RSA-Encrypted-Messaging-Application.git```
- cd in the folder

```cd NFC-Implant-base-RSA-Encrypted-Messaging-Application.git```
- python 3.7+ 

```sudo apt-get install python3```
- pip3

```sudo apt-get install python3-pip```
- Requirements Installation

```python3 -m pip install -r requirements.txt```



# Installation Client Side (Linux Debian base)
- cloning the repo

```git clone https://github.com/Kaosxx88/NFC-Implant-base-RSA-Encrypted-Messaging-Application.git```
- cd in the folder

```cd NFC-Implant-base-RSA-Encrypted-Messaging-Application.git```
- python 3.7+ 

```sudo apt-get install python3```
- pyqt5

```sudo apt-get install python3-pyqt5```
- install python3 pip

```sudo apt-get install python3-pip```
-  Requirements Installation

```python3 -m pip install -r requirements.txt```

### IMPORTANT

The file 'pmx3_read_keys_from_desfire.py' in the client folder of the repo, need to be modified accordly. 
In line 22 the variable self.pm3_path must be change to the user path where the proxmark client have been dowloaded. 

<br>
###  Kali linux ONLY
<br>
(Setting up a virtual environment top avoid conflict with the python3 modules  "serial" / "pyserial" )

- installation of virtual environment

```sudo apt-get install python3-venv```
- creation virtual environment

```python3 -m venv path/to/the/folder```
- activation of the virtual environment

```source /path/to/the/environment/bin/activate```
<br>

# Start the server application
- change directory into the repo

```cd /path/to/the/repo```
- change directory into the server folder

```cd server```
- run the file server.py

```python3 server.py```
<br>
# Start the client application
- change directory into the repo

```cd /path/to/the/repo```
- change directory into the server folder

```cd client```
- run the file ui.controller.py

```python3 ui_controller.py```
<br>


# proxmark3

<p align="center">
  <img width="400" height="280" src="https://github.com/Kaosxx88/NFC-Implant-base-RSA-Encrypted-Messaging-Application/blob/main/screenshots/proxmark3easy.png?raw=true">
</p>
The Proxmark is one of the most must-have of a hacker inventory. It is a cards reader that can read, write, force, and simulate many different types of chips on the market.  In this project, the proxmark3 easy have been used to read and write the keys on the MIFARE DESFire chip.

# ACR

<p align="center">
  <img width="400" height="280" src="https://github.com/Kaosxx88/NFC-Implant-base-RSA-Encrypted-Messaging-Application/blob/main/screenshots/ACR.png?raw=true">
</p>
The ACR122U is a card reader able to communicate with the MIFARE DESFire chip using the Application Protocol Data Unit called ADPU. This device has been used to change the standard key of the chip MIFARE DESFire. The sample DESFire cards have been bought directly from an abroad supplier, and they come with a standard key formed of all 0 digits.

# MIFARE DESfire

<p align="center">
  <img width="400" height="280" src="https://github.com/Kaosxx88/NFC-Implant-base-RSA-Encrypted-Messaging-Application/blob/main/screenshots/MIFAREDESfire.png?raw=true">
</p>
The Mifare Desfire chip is one of the most secure chips in the market right now (the same chip that is present on the card of the London Underground, known as Oyster Card ). It offers an Advanced Encryption Standard of 128 bit and has enough storage capacity to store a public key pair of 4096 bit. The same chip has been embedded in an implant from a company called [Dangerous things](https://dangerousthings.com/) .


 # N.I.R.E.M.A. file structure
 <br>
 <p align="center">
  <img  src="https://github.com/Kaosxx88/NFC-Implant-base-RSA-Encrypted-Messaging-Application/blob/main/screenshots/server_structure.jpg?raw=true">
</p>
 <br>
 <p align="center">
  <img src="https://github.com/Kaosxx88/NFC-Implant-base-RSA-Encrypted-Messaging-Application/blob/main/screenshots/client_structure.jpg?raw=true">
</p>

# Registration

<p align="center">
  <img width="250" height="300" src="https://github.com/Kaosxx88/NFC-Implant-base-RSA-Encrypted-Messaging-Application/blob/main/screenshots/registration_1.png?raw=true">
</p>
The Nirema registration screen has three main buttons that can be pressed. The
first one, called “Create a new key pair,” helps the user create new keys if he does not own them already. The second button, called “ Load key pair from files”, allows the user to select the key from a user-chosen folder. The last button, called “ Load key from DESFire”, allows the user to load the keys directly from the MIFARE DESFire chip 
<br clear="left"/>
<br>
<p align="center">
  <img width="500" height="300" src="https://github.com/Kaosxx88/NFC-Implant-base-RSA-Encrypted-Messaging-Application/blob/main/screenshots/registration_2.png?raw=true">
</p>

The first and the second button are bringing the user to two different pages, but they are almost the same in graphical. In the following picture, there is a comparison of them. On the left one, the user has to choose the path to save the keys, and on the right one, the user has to select the path from where to load the keys.

<p align="center">
  <img width="250" height="300" src="https://github.com/Kaosxx88/NFC-Implant-base-RSA-Encrypted-Messaging-Application/blob/main/screenshots/registration_3.png?raw=true">
</p>
Both of the above screenshots show the need for the passphrase location to encrypt
or decrypt the private key. The back and next buttons are helping the user to move in between the registration process. If the user selects the load key from the DESFire button, the screen on the left picture will appear. As in the login screen, the COM port will be automatically detected, and the first one available will be set as the default one. The user will be able to change the default port with another one by clicking on it and selecting another port to use. Elements 2 is the passphrase entry for the private key. Without it, the application will not be able to load the key in the system.
<br>
<br>
<p align="center">
  <img width="500" height="300" src="https://github.com/Kaosxx88/NFC-Implant-base-RSA-Encrypted-Messaging-Application/blob/main/screenshots/registration_4.png?raw=true">
</p>
The three previously explained application screens are bringing the user to the final part of the registration. In this section, point 1 shows the rules to follow in the nickname selection. Point 2 is where the user has to input the nickname that he wants to use. The registration button on the left side of the image, once pressed, will send the registration request to the server, and if the chosen name is available, the registration process will be authorised and completed. At this point, the left screen will appear. The top label will show a congratulations message to the user, and the bottom label will confirm the correct registration of the user. After the registration process is concluded, the user will be redirected to the login screen, and he can finally log in to the Nirema application.
The following image shows the pseudocode of the registration process. The pseudocode is an informal language that helps the programmer to develop the algorithm. It is giving a better understanding of the registration code behind the user interface. It is crucial to keep in mind the final code is much more complex.
<br>

# Login


<p align="center">
  <img width="250" height="300" src="https://github.com/Kaosxx88/NFC-Implant-base-RSA-Encrypted-Messaging-Application/blob/main/screenshots/login_1.png?raw=true">
<p>
The first screen of the Nirema application is the log in one. There are many elements; let’s take a look at all of them one by one. Points 1 and 2 are the user nickname and the private key passphrase input; the 3 and 4 are the tabs selection for the upload
method of the keys. The NFC tab allows the user to load the keys by scanning the MIFARE DESFire chip. On the other side, the File tab, let the user search for the keys in the system directory (There will be another screenshot explaining this part). Point 5 show the available COM port connected to the system. This is the port where the Proxmark or any other card reader will be connected. Point 6 is the login button, and point 7 redirect the user to the registration screen.
<br>

<p align="center">
  <img src="https://github.com/Kaosxx88/NFC-Implant-base-RSA-Encrypted-Messaging-Application/blob/main/screenshots/login_2.png?raw=true">
</p>
The Files tab allow the user to select the key set from the system. Once button one or button two are pressed from the uses, a window with a file selection will appear. It is essential to state that only key file with the extension (.pem) are allowed to be imported. The button’s label shows the actual path selected. As a standard path, the application will look up the presence of the keys inside a dedicated folder called keys inside the Nirema main installation folder.

# Chat GUI

<p align="center">
  <img width="450" height="300" src="https://github.com/Kaosxx88/NFC-Implant-base-RSA-Encrypted-Messaging-Application/blob/main/screenshots/chat_1.png?raw=true">
</p>

1) Application logo
2) Name and version of the application.
3) Logged user nickname.
4) Entry to search for new users
5) Button to send the request to the server to search the new user.
6) Label that shows an intro message to the user with instruction
7) Instruction label
<p align="center">
  <img width="450" height="300" src="https://github.com/Kaosxx88/NFC-Implant-base-RSA-Encrypted-Messaging-Application/blob/main/screenshots/chat_2.png?raw=true">
</p>

1) The top chat label will show the selected chat user destination.
2) The delete button, delete all the conversation with the user from the server.
3) The search button, search in the chat any corresponding text.
4) The message entry allows the user to write the message.
5) The left user list shows all the linked user and conversation in the account
6) The send button sends the message and clears the message entry.
7) The Chatbox will display the conversation.
8) The clear button will clear the message entry box.

<p align="center">
  <img width="450" height="300" src="https://github.com/Kaosxx88/NFC-Implant-base-RSA-Encrypted-Messaging-Application/blob/main/screenshots/chat_3.png?raw=true">
</p>

1) New message notification
2) New user on the user list  

<br>

# MIFARE DESfire structure
<p align="center">
  <img src="https://github.com/Kaosxx88/NFC-Implant-base-RSA-Encrypted-Messaging-Application/blob/main/screenshots/DESFIRE_enumeration.png?raw=true">
</p>

The MIFARE DESFire chip can store up to 28 different applications; each application can have up to 32 files between standards, backup, value file, record file and cycling recording file. Each Desfire chip has a card master key, and each application on it have a maximum of 14 different keys that can be assigned to write, read and delete data in the chip (NXP, 2015). 
For the realisation of this project, two applications have been written to the DESFire cards. The first one with the  Application ID number 0x888888 has been assigned to the public key, and the second application with the AID 0x999999 has been allocated to the encrypted private key.
The picture on the left side shows the enumeration of the Desfire chip using the proxmark3 easy. It is possible to notice the two applications written on the chip  ( Green arrow). Each of them has one file with the keys inside ( Blue arrow). The files have free read permission but need a predefined key to be written on the card to avoid any unauthorised alteration (Orange arrow). All the keys and the linked authorisation are customisable on the application and file creation. 
When read from the smart card reader, the internal structure of the MIFARE DESFire chip will be displayed as in the following picture. Please keep in mind that the next image only shows part of the saved private key. 

<p align="center">
  <img width="500" height="300" src="https://github.com/Kaosxx88/NFC-Implant-base-RSA-Encrypted-Messaging-Application/blob/main/screenshots/data_in_card.png?raw=true">
</p>
As is possible to notice from the picture above, the displayed memory is around 240 bit ( left bottom corner). To give an idea of the private keys’ real size, the number of 240 bit has to reach 3296 bit. Therefore the saved key will be more or less 14 times longer than the sowed picture. The same idea must be applied to the public key representation, but it will reach only 784 bit of size.  The two keys added together will form a public key pair 4096 bit. Therefore it is simple to understand that a lot of data have been written to the card. 
<br>

# Requests schema

The server side of the Nirema application is in charge of handling the requests and the connections coming from the clients. The servers configuration allows it to accept only specific requests and reject the not recognised or unauthorised ones. The following schema shows the requests of the server. 

<p align="center">
  <img   src="https://github.com/Kaosxx88/NFC-Implant-base-RSA-Encrypted-Messaging-Application/blob/main/screenshots/request_connections.png?raw=true">
</p>

As is possible to notice in the above picture, all the requests and responses are encrypted apart for the public key request. It is essential to keep in mind that the server uses SSL/TLS certificates. Therefore even if the public key request is not encrypted directly, it is encrypted at the socket level.  The symbol   (PK) on the above schema’s encryption section means that the communication is encrypted using the counterpart public key and signed using the sender’s private key. Using this encryption method, the recipient of the request/response is sure of the authenticity and the confidentiality of the content. The symbol (RSA) means that the communication is encrypted using RSA at a 256-bit algorithm based on a shared secret key. 

<p align="center">
  <img src="https://github.com/Kaosxx88/NFC-Implant-base-RSA-Encrypted-Messaging-Application/blob/main/screenshots/request_incapsulation.png?raw=true">

Analysing the above request, the utmost level is the SSL/TLS certificate, which protects its content. At the current moment, the server uses a self-signed certificate, but on the day of the Nirema lunch, it will be necessary to buy a certificate for the domain. The second level is the RSA 256 bit encryption. This encryption is based on a secret exchanged between the server and the client on the public key request. Inside the kernel of the request, there are five elements. The first one is the nickname of the recipient of the message. It is needed for the server to redirect the message to the correct user. Therefore the server needs to be able to read this information. The other four elements are not being decrypted from the server because the server does not have the private key to do it.  The only way to decrypt the encrypted messages is to be in possession of the sender or recipient private key. Talking about the last four elements looks like they are present twice on the request. It is accurate, but for a reason. For the sender of a message to be able to download the conversation from the server in the future and do not keep the conversation decrypted locally, it is needed to keep on the server a copy of the message that he can read and decrypted. In the case that only the version of the message that is destinated to a recipient is kept on the server, the sender will not be able to decrypt it anymore because only the recipient’s private keys can do it. 

# Application flow
<p align="center">
  <img width="800" height="900" src="https://github.com/Kaosxx88/NFC-Implant-base-RSA-Encrypted-Messaging-Application/blob/main/screenshots/structure.png?raw=true">

The above picture shows the concept flow of the N.I.R.E.M.A. application. The utilisation of the local public key database and the (public) public key database NEED TO BE IMPLEMENTED as 2FA and 3FA.  
<br>

# Database structure

<p align="center">
  <img  src="https://github.com/Kaosxx88/NFC-Implant-base-RSA-Encrypted-Messaging-Application/blob/main/screenshots/database_chat_history.png?raw=true">

The above image show the structure of the server database in which the message are stored. The structure is former of:
1) Message number
2) Sender Nickname
3) Recipient Nickname
4) Message encrypted with the sender public key
5) Message sign
6) Message encrypted with the recipient publick key 
7) Message sign

<br>

# Creation of a DESFIRE MIFARE apps

(WORK IN PROGRESS) 

# Colors and logos

<p align="center">
  <img src="https://github.com/Kaosxx88/NFC-Implant-base-RSA-Encrypted-Messaging-Application/blob/main/screenshots/colors_palette.JPG?raw=true">

The color palette has been inspirated from Kali Linux theme design ( 2020.1). The following N.I.R.E.M.A. logos are available on the client side folder. 

<p align="center">
  <img src="https://github.com/Kaosxx88/NFC-Implant-base-RSA-Encrypted-Messaging-Application/blob/main/screenshots/logos.png?raw=true">

# Credits

<br> A big thanks go to [Fausto Fasan](https://www.linkedin.com/in/fausto-fasan-4587a71a9/) for the N.I.R.E.M.A. application logos 
