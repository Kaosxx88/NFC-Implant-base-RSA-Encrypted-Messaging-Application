#!/usr/bin/env python3
# Autor @kaosxx88
# this file is the login wuindows GUI

import os
import sys
import time
import traceback
import serial.tools.list_ports

# loading windows and worker
from ui_loading import Ui_loading
from ui_worker import Ui_worker

# Other files
from rsa_keys_manager import *
from pmx3_read_keys_from_desfire import Pmx3_read_keys_from_desfire

# GUI elements
from PyQt5 import QtCore 
from PyQt5.QtGui import QFont, QPalette, QColor, QMovie
from PyQt5.QtCore import Qt, QRect, pyqtSignal, QThread, QObject, pyqtSlot, QTimer, QRunnable, QThreadPool
from PyQt5.QtWidgets import (QApplication, QProgressBar, QListView, QWidget, QLabel, QMessageBox, QLineEdit, QPushButton, QCheckBox, QRadioButton, QGroupBox, QHBoxLayout, QVBoxLayout, QTabWidget, QGridLayout, QListWidget, QFileDialog, QComboBox)

# gif modding
#https://ezgif.com/effects Gif modding


class Ui_login(QWidget):
    def __init__(self, controller): # Constructor
        super().__init__()

        self.pm3_port           = ''
        self.controller         = controller
        self.path_public_key    = ''
        self.path_private_key   = ''
        
        self.loading_gui_elements()

    def loading_gui_elements(self):

        #self.setWindowFlags(Qt.FramelessWindowHint)

        # Window Title
        self.setWindowTitle('Nirema v1.0 – Login')
        # Windows size (fixed)
        self.setFixedSize(360, 425)

        # Title label
        #title_label = QLabel('N.i.r.e.m.a.', self)
        #title_label.move(115, 10)
        #title_label.setObjectName("label")

        # Username label
        name_label = QLabel("User Nickname:", self)
        name_label.move(30, 15)

        # Usarname entry
        self.name_entry = QLineEdit(self)
        self.name_entry.move(200, 12)
        self.name_entry.resize(130, 25)

        # Password label
        password_label = QLabel("Private key Passphrase:", self)
        password_label.move(30, 50)

        # password entry
        self.password_entry = QLineEdit(self)
        self.password_entry.move(200, 48)
        self.password_entry.resize(130, 25)

        # Display show password checkbox
        show_pswd_cb = QCheckBox("show", self)
        show_pswd_cb.move(200, 80)
        show_pswd_cb.stateChanged.connect(self.showPassword)
        show_pswd_cb.toggle()
        show_pswd_cb.setChecked(False)

        # Group box
        self.groupBox = QGroupBox("Select public and private key loading mode:",self)
        self.groupBox.setGeometry(20,110,320,220)

        # Tab widget
        self.tab_bar = QTabWidget(self.groupBox)

        # Tabs 
        self.nfc_tab = QWidget()
        self.file_tab = QWidget()

        # Tabs hearder
        self.tab_bar.addTab(self.nfc_tab, "NFC")
        self.tab_bar.addTab(self.file_tab, "Files")

        # Box layout
        load_box = QHBoxLayout()
        load_box.addWidget(self.tab_bar)

        # Inser layaout in the group box
        self.groupBox.setLayout(load_box)

        # load elements inside nfc tab
        self.load_nfc_tab_elements()

        # load elements inside files tab
        self.load_files_tab_elements()

        # Sign in push button
        sign_in_button = QPushButton('login', self)
        sign_in_button.move(30, 345)
        sign_in_button.resize(300, 35)
        sign_in_button.clicked.connect(self.clickLogin)


        # Display sign up label 
        not_a_member = QLabel("not a member?", self)
        not_a_member.move(70, 395)

        # Display register button
        sign_up = QPushButton(" sign up  ", self)
        sign_up.move(205, 390)
        sign_up.clicked.connect(self.controller.show_ui_registration)

        # create thread pool for the future work handling 
        self.threadpool = QThreadPool()



    def load_nfc_tab_elements(self):

        # load element for windows system
        if self.controller.system == 'Windows':
         
            nfc_win_lable = QLabel('Windows system detected', self.nfc_tab)
            nfc_win_lable.move(70, 20)


        # load element for windows
        elif self.controller.system == 'Unix':

            nfc_uni_lable = QLabel('Unix system detected', self.nfc_tab)
            nfc_uni_lable.move(74, 20)

        # Default port label
        nfc_port_lable = QLabel(f'Proxmark default port', self.nfc_tab)
        nfc_port_lable.move(72, 50)
        
        
        # combo box for the connection
        self.pm3_port_connession = QComboBox(self.nfc_tab)
        self.pm3_port_connession.setEditable(True) 
        self.pm3_port_connession.setView(QListView())
        self.pm3_port_connession.setStyleSheet("QListView::item {height:30px;}  QComboBox {min-height: 30px;}")
        self.pm3_port_connession.move(70, 90)
        self.pm3_port_connession.resize(150, 25)



        # procedure for centre the text
        line_edit = self.pm3_port_connession.lineEdit()
        line_edit.setAlignment(Qt.AlignCenter)

        line_edit.setReadOnly(True) 

        # If tehre ar connection port used
        if len(self.controller.available_port) != 0:
            for port in self.controller.available_port:
                self.pm3_port_connession.addItem(port)

            # setting the default variable
            self.pm3_port = self.controller.available_port[0]

        # if there are not connection used
        else:
            self.pm3_port_connession.addItem('0 connected devices found')
            self.pm3_port = ''



    def load_files_tab_elements(self):


        # Layout for the container
        groupBox_layout_3 = QVBoxLayout(self.file_tab)
        groupBox_layout_3.setAlignment(QtCore.Qt.AlignCenter) 

        # public key label
        public_label = QLabel('Public key path:')

        # button for select the path and display it
        self.change_public_path_button = QPushButton('Select your public key')
        self.change_public_path_button.clicked.connect(self.file_search_public) 
        self.change_public_path_button.setStyleSheet(' min-height: 30px; ')


        private_label = QLabel('Private key path:')


        self.change_private_path_button = QPushButton('Select your private key')
        self.change_private_path_button.clicked.connect(self.file_search_private)
        self.change_private_path_button.setStyleSheet(' min-height: 30px; ')

        # loading elements in the layaout
        #groupBox_layout_3.addStretch()
        groupBox_layout_3.addWidget(public_label)
        
        groupBox_layout_3.addWidget(self.change_public_path_button)
        #groupBox_layout_3.addStretch()
        groupBox_layout_3.addWidget(private_label)
        
        groupBox_layout_3.addWidget(self.change_private_path_button)
       


    def path_shortener(self, path):

        # Resize the path if is to long
        separator = [ '...\\..\\...' if self.controller.system == 'Windows' else '.../../...' ]

        if len(path) >= 30:
            return path[:+14] + (", ".join(separator)) +  path[-14:]
        else :
            return path


    def clickLogin(self):

        # Check if there is a valid nickname and passhrase 
        if len(self.name_entry.text()) == 0 or len(self.name_entry.text()) > 10 or self.name_entry.text().isalnum() == False or (len(self.password_entry.text().replace(' ','')) == 0): 

            # check if there is a passprahse
            if len(self.password_entry.text().replace(' ','')) == 0:

                QMessageBox.warning(self, "Error Message", "Please enter a passphrase", QMessageBox.Close, QMessageBox.Close)
                D.d('Nick name not valid')
            else:

                QMessageBox.warning(self, "Error Message", "The username is not valid.", QMessageBox.Close, QMessageBox.Close)
                D.d('Nick name not valid')


        ####################
        # NFC TAB SELECTED #
        ####################

        elif self.nfc_tab is self.tab_bar.currentWidget():

            # check if a port is selected
            if len(self.controller.available_port) != 0:
                self.pm3_port = str(self.pm3_port_connession.currentText())

                
                myports = [tuple(p) for p in list(serial.tools.list_ports.comports())]
                # variable proxmarck
                proxmark_available=False
                # control that the proxmark is present on the selected port
                for i in myports:
                    if self.pm3_port in i and 'proxmark3' in i:
                         proxmark_available=True
                
                if proxmark_available == True: 


                    D.d(f'selected tab NFC')

                    D.d(f'The Username is -> {self.name_entry.text()}')

                    D.d(f'The passhphrase is -> {self.password_entry.text()}')

                    D.d(f'The port selected is -> {self.pm3_port}')  

                    ########
                    # UNIX #
                    ########


                    if self.controller.system == 'Unix':

                        # load value from the GUI user input
                        pmx3_port           = self.pm3_port
                        passphrase          = self.password_entry.text()

                        #############################
                        # Desfire loading threading #
                        #############################

                        # start loading screen
                        self.start_loading_screen()

                        # Start separate worker
                        # class or function, name of it, args to be passed )
                        worker = Ui_worker(Pmx3_read_keys_from_desfire, 'Pmx3_read_keys_from_desfire',  pmx3_port, passphrase)

                        # link the signals

                        # when the process finish
                        worker.signals.finished.connect(self.thread_complete)

                        # progression of the process
                        worker.signals.progress.connect(self.progress_fn)

                        # return the value form the function or class
                        worker.signals.result.connect(self.result_from_readind_desfire)

                        # stack the process in the pool
                        self.threadpool.start(worker)

                    ###########
                    # WINDOWS #
                    ###########

                    else:
                        message =  ('Only Unix system is accepted for NFC device... working in progress for the compatibility...\nPlease select the Files tab intead of the nfc')
                        D.d(message)

                        QMessageBox.warning(None, "Error Message", message, QMessageBox.Close, QMessageBox.Close)

                else:
                    message = f'Proxmark3 NOT present on port {self.pm3_port}.\n Please check the port selected'
                    E.e(message)
                    QMessageBox.warning(None, "Error Message", message, QMessageBox.Close, QMessageBox.Close)


            #########################
            # NO USB PORT AVAILABLE #
            #########################

            else:
                QMessageBox.warning(self, "Error Message", "No port found, please select a keys file instead of the nfc", QMessageBox.Close, QMessageBox.Close)


        #####################
        # FILE TAB SELECTED #
        #####################

        elif self.file_tab is self.tab_bar.currentWidget():
            
            D.d('Files tab selected')

            D.d(f'The Username is -> {self.name_entry.text()}')

            D.d(f'The passhphrase is -> {self.password_entry.text()}')

            if self.path_private_key == '' or self.path_public_key == '':
                QMessageBox.warning(self, "Error Message", "Please make sure to select your private / public key ", QMessageBox.Close, QMessageBox.Close)

            else:
            
                # Start animation
                self.start_loading_screen()

                # Key validation
                keys_validity_check = Ui_worker(self.keys_validity_check, 'keys_validity_check')

                keys_validity_check.signals.finished.connect(self.thread_complete)

                keys_validity_check.signals.result.connect(self.return_key_validate_check)

                self.threadpool.start(keys_validity_check)



            
            
    def keys_validity_check(self, progress_callback):

        #########################
        # IMPORTING PRIVATE KEY #
        #########################

        response = import_key_custom_with_errors(self.path_private_key,self.password_entry.text())

        error = response[0]

        if error:
            return (f'{response[0]}\nis the passphrase correct?') 

        else:
            self.private_key = response[1]

            ########################
            # IMPORTING PUBLIC KEY #
            ########################

            response  = import_key_custom_with_errors(self.path_public_key)

            error = response[0]

            if error:

                return error

            else:
                self.public_key = response[1]

                D.d(f'{self.private_key} , {self.public_key}')

                return error



    def  return_key_validate_check(self, error):
        # Display error or luch chat 

        if error:
            QMessageBox.warning(self, "Error Message", error, QMessageBox.Close, QMessageBox.Close)
        else:

            #self.controller.start_client(self.private_key, self.public_key, self.name_entry.text())
            #
            #
            # CHECK THE SERVER FOR THE LOGIN
            #
            D.d(' Sending to controller')
            self.controller.start_client(self.private_key, self.public_key, self.name_entry.text())
            #self.controller.show_ui_chat()
            


    def start_loading_screen(self):
        self.loading_screen = Ui_loading(self) 
        self.loading_screen.startAnimation()
        self.loading_screen.show()

    def stop_loading_screen(self):
        self.loading_screen.stopAnimation()

    def progress_fn(self, message):
        D.d(f'Emitted message -> {message}')
        self.loading_screen.change_update_label(message)
        self.loading_screen.update_bar()

    def thread_complete(self):
        D.d("Thread completed!")
        self.loading_screen.stopAnimation()

    def result_from_readind_desfire(self, result):

        error      = result[0]
        self.private_key = result[1]
        self.public_key  = result[2]

        # check if there si some error in the process to read the keys
        if error:

            QMessageBox.warning(self, "Error Message", error, QMessageBox.Close, QMessageBox.Close)

        # card reading ok
        else: 
            D.d(f'{self.private_key} , {self.public_key}')
            # Login successfull message
            D.d('nfc tab calling controller')

            self.controller.start_client(self.private_key, self.public_key, self.name_entry.text() )
            #self.controller.show_ui_chat()

    def n1ckname_check(self, nickname):

        # Check if the username is present, if is too long and if have not allowed characters
        if len(nickname) == 0 or len(nickname) > 10 or nickname.isalnum() == False:  
            QMessageBox.warning(self, "Error Message", "The username is not valid.", QMessageBox.Close, QMessageBox.Close)
            
            return False
        else:
            return True



    def file_search_public(self, key_type ):

        # Just a debug check
        D.d(f'Before the change of the public key path -> {self.path_public_key}')

        # Current path of the program + public key folder
        path_to_open = os.path.dirname(__file__) + '/public_key'

        # File dialog to enable the reserach of the public key file in the system
        path = QFileDialog.getOpenFileName(self, 'Select file', path_to_open, '.pem(*.pem)') 

        # Change the public key file (only pem allowed) and check if is not empty (closed window)      
        if len(path[0]) != 0:
            self.path_public_key = path[0]

        # Just a debug check
        D.d(f'After the change of the public key path  -> {self.path_public_key}')

        # change the display value of the select key button with the selected key path ( short it if is to long)
        self.change_public_path_button.setText(self.path_shortener(self.path_public_key))


    def file_search_private(self, key_type ):

        # Just a debug check
        D.d(f'Before the change of the private key path -> {self.path_private_key}')

        # Current path of the program + public key folder
        path_to_open = os.path.dirname(__file__) + '/private_key'

        # File dialog to enable the reserach of the public key file in the system
        path = QFileDialog.getOpenFileName(self, 'Select file', path_to_open, '.pem(*.pem)') 

        # Change the public key file (only pem allowed) and check if is not empty (closed window)      
        if len(path[0]) != 0:
            self.path_private_key = path[0]

        # Just a debug check
        D.d(f'After the change of the private key path  -> {self.path_private_key}')

        # change the display value of the select key button with the selected key path ( short it if is to long)
        self.change_private_path_button.setText(self.path_shortener(self.path_private_key))

    def showPassword(self, state):

        if state == Qt.Checked:
            self.password_entry.setEchoMode(QLineEdit.Normal)
        else:
            self.password_entry.setEchoMode(QLineEdit.Password)
           

    def import_user_public_key(self):
        ''' importing user public key'''
        key_name = f'public_key/public_key.pem'                                                         
        self.user_public_key = import_pub_key(key_name)  


    def load_private_key(self, passphrase):                                                                                                 # loading the private key
        D.d('Starting load_private_key function ')
        ''' Load private key from username_private_key.pem'''


        try:
            private_key = import_key(f'private_key/private_key.pem', passphrase)
            D.d('Private key loaded')
            return private_key

        except Exception as e:
            D.d(f'Private key not loaded correctly (it is a valid key? it is a correct passphrase?)') 
            D.d ('...client Shutting down...')


    #########################################
    # pressing enter login button triggered #
    #########################################
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.clickLogin()





