# ui_registration.py

import os
import sys
import serial.tools.list_ports

from PyQt5 import QtWidgets
from PyQt5 import QtCore , QtGui
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt, QThreadPool
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QMessageBox, QLineEdit, QPushButton, QCheckBox, QRadioButton, QGroupBox, QHBoxLayout, QVBoxLayout, QTabWidget, QGridLayout, QListWidget, QFileDialog, QProgressBar, QComboBox)


# importing ui elements 
from ui_loading import Ui_loading
from ui_worker import Ui_worker

from rsa_keys_manager import *
from pmx3_read_keys_from_desfire import Pmx3_read_keys_from_desfire
from registration import Client as Client_registration 

class Ui_registration(QWidget):
    def __init__(self, controller):
        super().__init__()

        self.pm3_port                       = ''
        self.controller                     = controller
        self.path_public_key                = os.path.dirname(__file__) + '/public_key/public_key.pem'
        self.path_private_key               = os.path.dirname(__file__) + '/private_key/private_key.pem'
        self.path_public_key_folder         = os.path.dirname(__file__) + '/public_key'
        self.path_private_key_folder        = os.path.dirname(__file__) + '/private_key'

        # loading general ui setting
        self.ui_setting()

        # loading ui screens
        self.registration_main_screen()
        self.registration_create_screen()  
        self.registration_load_screen()
        self.registration_desfire()
        self.registration_nickname()

    def ui_setting(self):

        ###############
        # UI SETTINGS #
        ################

        # Window Title
        self.setWindowTitle('Nirema v1.0 - Registration') 
        # Windows size (fixed)
        self.setFixedSize(360, 425)  
        # create thread pool for the future work handling 
        self.threadpool = QThreadPool()

    def registration_main_screen(self):

        ############################
        # REGISTRATION MAIN SCREEN #
        ############################

        message = """To register, you need to have an RSA key pair of 4096 bit and the private key must be passphrase protected.\n\n( The format of the keys must be .pem )"""

        # intro label
        self.main_screen_label = QLabel(message, self)
        self.main_screen_label.move(20, 20)
        self.main_screen_label.resize(300, 100)
        self.main_screen_label.setWordWrap(True)
        
        # Box for the elements
        self.main_screen_box = QGroupBox('Select one of the following options:', self)
        self.main_screen_box.setGeometry(20,140,320,260)

        # Layout for the box
        main_screen_box_layout = QVBoxLayout()
        main_screen_box_layout.setAlignment(QtCore.Qt.AlignCenter) 

        # button for the menu selection
        self.main_screen_button_1 = QPushButton("Create a new key pair")
        self.main_screen_button_1.clicked.connect(self.show_create_menu)
        self.main_screen_button_1.setStyleSheet('min-width: 270px ; min-height: 60px; font-size: 13pt;') 

        self.main_screen_button_2 = QPushButton("Load key pair from files")
        self.main_screen_button_2.clicked.connect(self.show_load_menu)
        self.main_screen_button_2.setStyleSheet('min-width: 270px ; min-height: 60px; font-size: 13pt;')

        self.main_screen_button_3 = QPushButton("Load key pair from DESFire")
        self.main_screen_button_3.clicked.connect(self.show_desfire_menu)
        self.main_screen_button_3.setStyleSheet('min-width: 270px ; min-height: 60px; font-size: 13pt;')

        # adding element to the box
        main_screen_box_layout.addWidget(self.main_screen_button_1)
        main_screen_box_layout.addStretch()
        main_screen_box_layout.addWidget(self.main_screen_button_2)
        main_screen_box_layout.addStretch()
        main_screen_box_layout.addWidget(self.main_screen_button_3)

        # set the layout in the box
        self.main_screen_box.setLayout(main_screen_box_layout)

    def registration_create_screen(self):

        ############################
        # CREATE A NEW PAIR SCREEN #
        ############################

        # create screen box 
        self.create_screen_box = QGroupBox('Choose where to save the keys:', self)
        self.create_screen_box.setGeometry(20,30,320,320)
        self.create_screen_box.setHidden(True)

        # create screen layout
        create_screen_box_layout = QVBoxLayout()
        create_screen_box_layout.setAlignment(QtCore.Qt.AlignCenter) 

        create_screen_public_key_label = QLabel('Public key folder path:')

        # button for select the path and display it
        self.create_screen_change_public_key_folder_path_button = QPushButton(self.path_shortener(self.path_public_key_folder))
        self.create_screen_change_public_key_folder_path_button.clicked.connect(self.search_public_key_folder)
        self.create_screen_change_public_key_folder_path_button.setStyleSheet(' min-height: 30px')

        create_screen_private_key_label = QLabel('Private key folder path:')

        self.change_private_folder_path_button = QPushButton(self.path_shortener(self.path_private_key_folder))
        self.change_private_folder_path_button.setStyleSheet(' min-height: 30px')
        self.change_private_folder_path_button.clicked.connect(self.folder_search_private)

        # Password label
        create_screen_passphrase_label = QLabel("Please provide a private key Passphrase:")

        # password entry
        self.create_screen_passphrase_entry = QLineEdit()
        self.create_screen_passphrase_entry.setStyleSheet('min-height: 30px')
        self.create_screen_passphrase_entry.setPlaceholderText('Passphrase')
        self.create_screen_passphrase_entry.setAlignment(QtCore.Qt.AlignCenter) 

        self.back_button = QPushButton('Back', self)
        self.back_button.move(30, 370)
        self.back_button.resize(145, 35)
        self.back_button.clicked.connect(self.back_button_pressed)
        self.back_button.setHidden(True)

        self.next_button = QPushButton('Next', self)
        self.next_button.move(185, 370)
        self.next_button.resize(145, 35)
        self.next_button.clicked.connect(self.next_button_pressed)
        self.next_button.setHidden(True)

        # Display show password checkbox
        create_screen_show_pswd_check_box = QCheckBox("show passphrase")
        create_screen_show_pswd_check_box.stateChanged.connect(self.create_screen_show_password)
        create_screen_show_pswd_check_box.toggle()
        create_screen_show_pswd_check_box.setChecked(False)

        # add element to the layout
        create_screen_box_layout.addStretch()
        create_screen_box_layout.addWidget(create_screen_public_key_label)
        create_screen_box_layout.addWidget(self.create_screen_change_public_key_folder_path_button)
        create_screen_box_layout.addStretch()
        create_screen_box_layout.addWidget(create_screen_private_key_label)
        create_screen_box_layout.addWidget(self.change_private_folder_path_button)
        create_screen_box_layout.addStretch()
        create_screen_box_layout.addWidget(create_screen_passphrase_label)
        create_screen_box_layout.addWidget(self.create_screen_passphrase_entry)
        create_screen_box_layout.addWidget(create_screen_show_pswd_check_box)

        # set the layout of create screen box
        self.create_screen_box.setLayout(create_screen_box_layout)



    def registration_load_screen(self):

        ##################################
        # LOAD KEY PAIR FROM FILE SCREEN #
        ##################################

        # build box containe
        self.load_screen_box = QGroupBox('Please select your keys path:', self)
        self.load_screen_box.setGeometry(20,30,320,320)#(40,70,280,275)(20,30,320,320)
        self.load_screen_box.setHidden(True)

        # Layout for the container
        load_screen_box_layout = QVBoxLayout()
        load_screen_box_layout.setAlignment(QtCore.Qt.AlignCenter) 

        # public key label
        load_screen_public_key_label = QLabel('Public key path:')

        # button change public key path
        self.load_screen_change_public_key_path_button = QPushButton(self.path_shortener(self.path_public_key))
        self.load_screen_change_public_key_path_button.clicked.connect(self.file_search_public)
        self.load_screen_change_public_key_path_button.setStyleSheet('min-height: 30px')

        # private key label
        load_screen_private_label = QLabel('Private key path:')

        # button change private key path
        self.load_screen_change_private_key_path_button = QPushButton(self.path_shortener(self.path_private_key))
        self.load_screen_change_private_key_path_button.setStyleSheet('min-height: 30px')
        self.load_screen_change_private_key_path_button.clicked.connect(self.file_search_private)

        # Password label
        load_screen_password_label = QLabel("Please provide a private key Passphrase:")

        # password entry
        self.load_screen_passphrase_entry = QLineEdit()
        self.load_screen_passphrase_entry.setPlaceholderText('Passphrase')
        self.load_screen_passphrase_entry.setAlignment(QtCore.Qt.AlignCenter)
        self.load_screen_passphrase_entry.setStyleSheet('min-height: 30px') 

        # Display show password checkbox
        load_screeen_show_pswd_check_box = QCheckBox("show passphrase")
        load_screeen_show_pswd_check_box.stateChanged.connect(self.load_screen_show_password)
        load_screeen_show_pswd_check_box.toggle()
        load_screeen_show_pswd_check_box.setChecked(False)

        # loading elements in the layout
        load_screen_box_layout.addStretch()
        load_screen_box_layout.addWidget(load_screen_public_key_label)        
        load_screen_box_layout.addWidget(self.load_screen_change_public_key_path_button)
        load_screen_box_layout.addStretch()
        load_screen_box_layout.addWidget(load_screen_private_label)        
        load_screen_box_layout.addWidget(self.load_screen_change_private_key_path_button)
        load_screen_box_layout.addStretch()
        load_screen_box_layout.addWidget(load_screen_password_label)
        load_screen_box_layout.addWidget(self.load_screen_passphrase_entry)
        load_screen_box_layout.addWidget(load_screeen_show_pswd_check_box)

        # load the layout in the box
        self.load_screen_box.setLayout(load_screen_box_layout)



    def registration_desfire(self):

        ##########################
        # LOAD KEYS FROM DESFIRE #
        ##########################

        # build box containe
        self.desfire_screen_box = QGroupBox('Please select the correct port:', self)
        self.desfire_screen_box.setGeometry(20,30,320,320)

        # Layout for the container
        desfire_screen_box_layout = QVBoxLayout()
        

        # load element for windows system
        if self.controller.system == 'Windows':

            ##################
            # WINDOWS SYSTEM #
            ##################

            desfire_screen_system_detection_label = QLabel('Windows system detected')
            desfire_screen_system_detection_label.move(70, 20)
            desfire_screen_system_detection_label.setAlignment(Qt.AlignCenter) 


        # load element for Unix
        elif self.controller.system == 'Unix':

            ###############
            # UNIX SYSTEM #
            ###############

            desfire_screen_system_detection_label = QLabel('Unix system detected')
            desfire_screen_system_detection_label.move(85, 20)
            desfire_screen_system_detection_label.setAlignment(Qt.AlignCenter)

        # Default port label
        desfire_screen_nfc_port_lable = QLabel(f'Proxmark default port:')
        desfire_screen_nfc_port_lable.move(80, 50)        
        #desfire_screen_nfc_port_lable.setAlignment(Qt.AlignCenter)
        
        # combo box for the connection
        self.desfire_screen_pm3_port_combo_box = QComboBox()
        self.desfire_screen_pm3_port_combo_box.setEditable(True) 
        self.desfire_screen_pm3_port_combo_box.move(70, 80)
        self.desfire_screen_pm3_port_combo_box.resize(150, 90)
        self.desfire_screen_pm3_port_combo_box.setView(QtWidgets.QListView())
        self.desfire_screen_pm3_port_combo_box.setStyleSheet("QListView::item {height:30px;}  QComboBox {min-height: 30px;}")

        # procedure for centre the text
        desfire_screen_combo_box_entry = self.desfire_screen_pm3_port_combo_box.lineEdit()
        desfire_screen_combo_box_entry.setAlignment(Qt.AlignCenter)
        desfire_screen_combo_box_entry.setReadOnly(True) 

        # Check if there is a connection available
        if len(self.controller.available_port) != 0:
            for port in self.controller.available_port:
                self.desfire_screen_pm3_port_combo_box.addItem(port)

            # setting the default port variable
            self.pm3_port = self.controller.available_port[0]

        # in case there are not connection
        else:
            self.desfire_screen_pm3_port_combo_box.addItem('0 connected devices found')
            self.pm3_port = ''

        # Password label
        password_label_section_4 = QLabel("Please provide a private key Passphrase:")

        # passphrase entry
        self.desfire_screen_passphrase_entry = QLineEdit()
        self.desfire_screen_passphrase_entry.setPlaceholderText('Passphrase')
        self.desfire_screen_passphrase_entry.setAlignment(QtCore.Qt.AlignCenter) 
        self.desfire_screen_passphrase_entry.setStyleSheet('min-height: 30px') 

        # passphrase check box checkbox
        desfire_screen_show_pswd_check_box = QCheckBox("show passphrase")
        desfire_screen_show_pswd_check_box.stateChanged.connect(self.desfire_screen_show_password)
        desfire_screen_show_pswd_check_box.toggle()
        desfire_screen_show_pswd_check_box.setChecked(False)

        # add witdget to layout
        desfire_screen_box_layout.addWidget(desfire_screen_system_detection_label)
        desfire_screen_box_layout.addStretch()
        desfire_screen_box_layout.addWidget(desfire_screen_nfc_port_lable)
        desfire_screen_box_layout.addWidget(self.desfire_screen_pm3_port_combo_box)
        desfire_screen_box_layout.addStretch()       
        desfire_screen_box_layout.addStretch()
        desfire_screen_box_layout.addWidget(password_label_section_4)
        desfire_screen_box_layout.addWidget(self.desfire_screen_passphrase_entry)
        desfire_screen_box_layout.addWidget(desfire_screen_show_pswd_check_box)
        desfire_screen_box_layout.addStretch()

        # set the layout of the box
        self.desfire_screen_box.setLayout(desfire_screen_box_layout)

        # hide the box
        self.desfire_screen_box.setHidden(True)

    def registration_nickname(self):

        ###################
        # CHOOSE NICKNAME #
        ###################

        # build box containe
        self.nickname_screen_box = QGroupBox('Please choose a nickname:', self)
        self.nickname_screen_box.setGeometry(20,30,320,380)#(40,70,280,275)(20,30,320,320)

        # Layout for the container
        nickname_screen_box_layout = QVBoxLayout()
        nickname_screen_box_layout.setAlignment(QtCore.Qt.AlignCenter) 

        # options label
        self.nickname_screen_intruction_label_1 = QLabel('- Only letters and numbers allowed')
        self.choose_nickname_intruction_label_2 = QLabel('- Max length 10')

        # nickname label
        nickname_screen_nickname_label = QLabel('Nickname:')

        # nickname entry
        self.nickname_screen_nickname_entry = QLineEdit()
        self.nickname_screen_nickname_entry.setPlaceholderText('Nickname')
        self.nickname_screen_nickname_entry.setAlignment(QtCore.Qt.AlignCenter)
        self.nickname_screen_nickname_entry.setStyleSheet('min-height: 30px') 

        # register button       
        self.nickname_screen_register_button = QPushButton('Register')
        self.nickname_screen_register_button.clicked.connect(self.nickname_screen_request_server)
        self.nickname_screen_register_button.setStyleSheet('min-height: 30px')

        # Back to login page button
        self.nickname_screen_show_login_screen_button = QPushButton('Back to login page')
        self.nickname_screen_show_login_screen_button.clicked.connect(self.show_login_screen)
        self.nickname_screen_show_login_screen_button.setStyleSheet('min-height: 30px')

        # set button hidden
        self.nickname_screen_show_login_screen_button.setHidden(True)

        # Response status
        self.nickname_screen_response_status_label = QLabel('.........')
        self.nickname_screen_response_status_label.setStyleSheet('font-size: 14pt;') 
        self.nickname_screen_response_status_label.setAlignment(QtCore.Qt.AlignCenter) 

        # loading elements in the layout
        nickname_screen_box_layout.addStretch()
        nickname_screen_box_layout.addWidget(self.nickname_screen_intruction_label_1)
        nickname_screen_box_layout.addWidget(self.choose_nickname_intruction_label_2)
        nickname_screen_box_layout.addStretch()
        nickname_screen_box_layout.addWidget(nickname_screen_nickname_label)
        nickname_screen_box_layout.addWidget(self.nickname_screen_nickname_entry)
        nickname_screen_box_layout.addStretch()
        nickname_screen_box_layout.addWidget(self.nickname_screen_response_status_label)
        nickname_screen_box_layout.addStretch()
        nickname_screen_box_layout.addWidget(self.nickname_screen_register_button)
        nickname_screen_box_layout.addWidget(self.nickname_screen_show_login_screen_button)

        # lset the layout in the box
        self.nickname_screen_box.setLayout(nickname_screen_box_layout)

        # set the box hidden
        self.nickname_screen_box.setHidden(True)


    def show_create_menu(self):

        D.d("Menu create a new key pair selected")

        self.main_screen_box.setHidden(True)
        self.create_screen_box.setHidden(False)
        self.back_button.setHidden(False)
        self.next_button.setHidden(False)
        self.main_screen_label.setHidden(True)

    def show_load_menu(self):

        D.d("Menu load key from files selected")

        self.main_screen_box.setHidden(True)
        self.create_screen_box.setHidden(True)
        self.load_screen_box.setHidden(False)
        self.back_button.setHidden(False)
        self.next_button.setHidden(False)
        self.main_screen_label.setHidden(True)

    def show_desfire_menu(self):

        D.d("Menu load from DESFIRE selected\n")

        self.main_screen_box.setHidden(True)
        self.create_screen_box.setHidden(True)
        self.load_screen_box.setHidden(True)
        self.desfire_screen_box.setHidden(False)
        self.back_button.setHidden(False)
        self.next_button.setHidden(False)
        self.main_screen_label.setHidden(True)
              

    def nickname_screen_request_server(self):

        D.d('Verifying nickname on the server')

        if len(self.nickname_screen_nickname_entry.text()) == 0 or len(self.nickname_screen_nickname_entry.text()) > 10 or self.nickname_screen_nickname_entry.text().isalnum() == False :

            QMessageBox.warning(None, "Error Message", 'Please Insert a valid Nickname', QMessageBox.Close, QMessageBox.Close)

        else:

            self.start_loading_screen()
            # Start separate worker
            # class or function, name of it, args to be passed )
            registration = Ui_worker(Client_registration, 'Client_registration', self.private_key, self.public_key, self.nickname_screen_nickname_entry.text() )
            # when the process finish
            registration.signals.finished.connect(self.thread_complete)
            # progression of the process
            registration.signals.progress.connect(self.progress_fn)
            # return the value form the function or class
            registration.signals.result.connect(self.result_from_registration)
            # stack the process in the pool
            self.threadpool.start(registration)                  
   

    def result_from_registration(self, result):

        D.d('Result from registration')

        registered  = result[0]
        status      = result[1]

        D.d(status)

        if registered == False  :
            D.d('Error in the registration process')
            D.d(status)

            self.nickname_screen_response_status_label.setStyleSheet('font-size: 16pt ; color: red')

            self.nickname_screen_response_status_label.setText(status)

            QMessageBox.warning(None, "Error Message", status, QMessageBox.Close, QMessageBox.Close)

        elif registered == True:

            D.d('New User created')

            self.nickname_screen_intruction_label_1.setText('Congratulations')
            self.nickname_screen_intruction_label_1.setStyleSheet('font-size: 25pt ; color: orange')            
            self.nickname_screen_intruction_label_1.setAlignment(QtCore.Qt.AlignCenter)

            self.nickname_screen_show_login_screen_button.setHidden(False)
            self.nickname_screen_response_status_label.setStyleSheet('font-size: 16pt ; color: orange')
            self.nickname_screen_response_status_label.setText('Nickname registered Correctly')
            self.nickname_screen_show_login_screen_button.setHidden(False)
            self.nickname_screen_register_button.setHidden(True)

            #
            #
            self.nickname_screen_nickname_entry.setStyleSheet('min-height: 30px; background : 272A34; color: ') 
            #
            #


            self.choose_nickname_intruction_label_2.setHidden(True)

        self.loading_screen.stopAnimation()

    def show_login_screen(self):
        self.close()
        self.controller.show_ui_login()

    def show_screen_user_choose(self):

        self.desfire_screen_box.setHidden(True)
        self.nickname_screen_box.setHidden(False)
        self.back_button.setHidden(True)
        self.next_button.setHidden(True)



    ###############
    # NEXT BUTTON #
    ###############

    def next_button_pressed(self):

        D.d('Next button pressed')

        if self.create_screen_box.isHidden() == False :

            ###########################
            # SAVE KEY LOCALLY STEP 2 #
            ###########################

            if self.create_screen_passphrase_entry.text().replace(' ','') != '':

                ###########################
                # IF PASSPHRASE NOT EMPTY #
                ###########################

                D.d('Option save key locally selected')

                D.d(f'passphrase --> {self.create_screen_passphrase_entry.text()}')

                D.d('Calling the loading screeen and the creation of the keys')

                # Start animation
                self.start_loading_screen()

                key_creator = Ui_worker(key_creator_and_export, 'key_creator_and_export', self.create_screen_passphrase_entry.text(), self.path_private_key_folder , self.path_public_key_folder )
                key_creator.signals.finished.connect(self.thread_complete)
                key_creator.signals.result.connect(self.result_key_creator)
                key_creator.signals.progress.connect(self.progress_fn)
                self.threadpool.start(key_creator)
              
            else:

                ####################
                # EMPTY PASSPHRASE #
                ####################

                QMessageBox.information(self, "Allert", "Please enter a valid passphrase", QMessageBox.Close, QMessageBox.Close)


        elif self.load_screen_box.isHidden() == False :

            ##################################
            # LOAD KEY PAIR FROM FILE STEP 2 #
            ##################################

            if self.load_screen_passphrase_entry.text().replace(' ','') != '':

                ####################
                # PASSPHRASE VALID #
                ####################

                # Start loading screen
                self.start_loading_screen()

                # start key validation thread
                worker_keys_validity_check = Ui_worker(self.keys_validity_check, 'keys_validity_check', self.load_screen_passphrase_entry.text())
                # link the thread completo to the function
                worker_keys_validity_check.signals.finished.connect(self.thread_complete)
                # link the return function
                worker_keys_validity_check.signals.result.connect(self.result_key_validate_check)
                # add thread to the pool thread
                self.threadpool.start(worker_keys_validity_check)

            else:

                ####################
                # PASSPHRASE EMPTY #
                ####################

                QMessageBox.information(self, "Allert", "Please enter a valid passphrase", QMessageBox.Close, QMessageBox.Close)


        elif self.desfire_screen_box.isHidden() == False:

            #########################
            # LOAD KEY FROM DESFIRE #
            #########################

            if self.desfire_screen_passphrase_entry.text().replace(' ','') != '':

                ####################
                # PASSPHRASE VALID #
                ####################

                D.d(f'Passphrase -> {self.desfire_screen_passphrase_entry.text()}')
                D.d(f'Pmx3 port  -> {self.pm3_port}')

                if self.controller.system == 'Unix':


                    ########
                    # UNIX #
                    ########

                    # load value from the GUI user input
                    pmx3_port           = self.desfire_screen_pm3_port_combo_box.currentText()
                    print (pmx3_port)
                    passphrase          = self.desfire_screen_passphrase_entry.text()

                    # checking the available port connected in the system
                    myports = [tuple(p) for p in list(serial.tools.list_ports.comports())]

                    # variable proxmarck
                    proxmark_available=False
                    # control that the proxmark is present on the selected port
                    for i in myports:
                        if pmx3_port in i and 'proxmark3' in i:
                            proxmark_available=True

                    # if the proxmark is plugged
                    if proxmark_available == True:        
                        
                        D.d(f'Proxmark3 present on port {pmx3_port}')
                        #############################
                        # Desfire loading threading #
                        #############################
                        # start loading screen
                        self.start_loading_screen()
                        # Start separate worker
                        # class or function, name of it, args to be passed )
                        worker = Ui_worker(Pmx3_read_keys_from_desfire, 'Pmx3_read_keys_from_desfire',  pmx3_port, passphrase)
                        # when the process finish
                        worker.signals.finished.connect(self.thread_complete)
                        # progression of the process
                        worker.signals.progress.connect(self.progress_fn)
                        # return the value form the function or class
                        worker.signals.result.connect(self.result_from_reading_desfire)
                        # stack the process in the pool
                        self.threadpool.start(worker)

                    else:

                        message = f'Proxmark3 NOT present on port {pmx3_port}.\n Please check the port selected'
                        E.e(message)
                        QMessageBox.warning(None, "Error Message", message, QMessageBox.Close, QMessageBox.Close)



                else:

                    ###########
                    # WINDOWS #
                    ###########

                    message =  ('Only Unix system is accepted for NFC device... working in progress for the compatibility...')
                    D.d(message)

                    QMessageBox.warning(None, "Error Message", message, QMessageBox.Close, QMessageBox.Close)



            else:

                ####################
                # PASSPHRASE EMPTY #
                ####################

                QMessageBox.information(self, "Allert", "Please enter a valid passphrase", QMessageBox.Close, QMessageBox.Close)





    ###############
    # BACK BUTTON #
    ###############

    def back_button_pressed(self):
        D.d('back button pressed')

        # back from page 1
        if self.main_screen_box.isHidden() == False:
            # return to the login screen
            self.show_login_screen()

        # back from page 2
        elif self.create_screen_box.isHidden() == False:
          
            self.create_screen_box.setHidden(True)
            self.main_screen_box.setHidden(False)
            self.back_button.setHidden(True)
            self.next_button.setHidden(True)
            self.main_screen_label.setHidden(False)

        # back from page 3
        elif self.load_screen_box.isHidden() == False:

            self.load_screen_box.setHidden(True)
            self.main_screen_box.setHidden(False)
            self.back_button.setHidden(True)
            self.next_button.setHidden(True)
            self.main_screen_label.setHidden(False)

        # back from page 4
        elif self.desfire_screen_box.isHidden() == False:

            self.desfire_screen_box.setHidden(True)
            self.main_screen_box.setHidden(False)
            self.back_button.setHidden(True)
            self.next_button.setHidden(True)
            self.main_screen_label.setHidden(False)

    def result_from_reading_desfire(self, result):

        error      = result[0]
        self.private_key = result[1]
        self.public_key  = result[2]

        # check if there si some error in the process to read the keys
        if error:

            QMessageBox.warning(self, "Error Message", error, QMessageBox.Close, QMessageBox.Close)


        else: 

            self.show_screen_user_choose()

        self.loading_screen.stopAnimation()


    def keys_validity_check(self, passphrase,  progress_callback):

        #########################
        # IMPORTING PRIVATE KEY #
        #########################

        response = import_key_custom_with_errors(self.path_private_key, passphrase)

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

                D.d(f'{self.private_key}, {self.public_key}')

                return error


    def  result_key_validate_check(self, error):
        # Display error or luch chat 

        if error:
            QMessageBox.warning(self, "Error Message", error, QMessageBox.Close, QMessageBox.Close)
        else:
            self.show_screen_user_choose()

        self.loading_screen.stopAnimation()


    def result_key_creator(self, result):
        # return function from the thread

        # path to the keys
        self.path_private_key = result[0]
        self.path_public_key  = result[1] 

        # load the keys in the system after the creation

        # Start loading screen

        #self.start_loading_screen()

        # start key validation thread
        worker_keys_validity_check = Ui_worker(self.keys_validity_check, 'keys_validity_check', self.create_screen_passphrase_entry.text())
        # link the thread completo to the function
        worker_keys_validity_check.signals.finished.connect(self.thread_complete)
        # link the return function
        worker_keys_validity_check.signals.result.connect(self.result_key_validate_check)
        # add thread to the pool thread
        self.threadpool.start(worker_keys_validity_check)


    def path_shortener(self, path):

        # Resize the path if is to long to display
        separator = [ '...\\..\\...' if self.controller.system == 'Windows' else '.../../...' ]

        if len(path) >= 30:
            return path[:+15] + (", ".join(separator)) +  path[-15:]
        else :
            return path

    def check_proxmark3_port_selection(self):

        # Custom port used (remove empty character from port imput)
        if self.pm3_port_entry.text().replace(' ', '') != '':
            self.pm3_port = self.pm3_port_entry.text()
            D.d(f'pm3 -> Custom port used ({self.pm3_port})')

        # Default port used
        else:
            D.d(f'pm3 -> Default port used ({self.pm3_port})')

    def n1ckname_check(self, nickname):
        
        # Check if the username is present, if is too long and if have not allowed characters
        if len(nickname) == 0 or len(nickname) > 10 or nickname.isalnum() == False:  
            QMessageBox.warning(self, "Error Message", "The username is not valid.", QMessageBox.Close, QMessageBox.Close)
        
        else:
            QMessageBox.information(self, "Login Successful!", "Login Successful!", QMessageBox.Ok, QMessageBox.Ok)


    def file_search_public(self ):

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


        self.load_screen_change_public_key_path_button.setText(self.path_shortener(self.path_public_key))

    def search_public_key_folder(self ):

        # Just a debug check
        D.d(f'Before the change of the public key path -> {self.path_public_key_folder}')

        # Current path of the program + public key folder
        path_to_open = os.path.dirname(__file__) 

        # File dialog to enable the reserach of the public key file in the system
        path = QFileDialog.getExistingDirectory(self, 'Select folder', path_to_open) 

        # Change the public key file (only pem allowed) and check if is not empty (closed window)      
        if len(path) != 0:
            self.path_public_key_folder = path

        # Just a debug check
        D.d(f'After the change of the public key path  -> {self.path_public_key_folder}')


        self.create_screen_change_public_key_folder_path_button.setText(self.path_shortener(self.path_public_key_folder))



    def file_search_private(self ):

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

        self.load_screen_change_private_key_path_button.setText(self.path_shortener(self.path_private_key))

    def folder_search_private(self ):

        # Just a debug check
        D.d(f'Before the change of the private key path -> {self.path_private_key_folder}')

        # Current path of the program + public key folder
        path_to_open = os.path.dirname(__file__) 

        # File dialog to enable the reserach of the public key file in the system
        path = QFileDialog.getExistingDirectory(self, 'Select folder', path_to_open) 


        # Change the public key file (only pem allowed) and check if is not empty (closed window)      
        if len(path) != 0:
            self.path_private_key_folder = path

        # Just a debug check
        D.d(f'After the change of the private key path  -> {self.path_private_key_folder}')

        self.change_private_folder_path_button.setText(self.path_shortener(self.path_private_key_folder))



    def create_screen_show_password(self, state):

        if state == Qt.Checked:
            self.create_screen_passphrase_entry.setEchoMode(QLineEdit.Normal)
        else:
            self.create_screen_passphrase_entry.setEchoMode(QLineEdit.Password)

    def load_screen_show_password(self, state):

        if state == Qt.Checked:
            self.load_screen_passphrase_entry.setEchoMode(QLineEdit.Normal)
        else:
            self.load_screen_passphrase_entry.setEchoMode(QLineEdit.Password)

    def desfire_screen_show_password(self, state):

        if state == Qt.Checked:
            self.desfire_screen_passphrase_entry.setEchoMode(QLineEdit.Normal)
        else:
            self.desfire_screen_passphrase_entry.setEchoMode(QLineEdit.Password)


    def closeEvent(self, event):
        D.d('User pressed the x to close the screen')
        self.show_login_screen()        

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
        
