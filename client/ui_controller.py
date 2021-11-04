#!/usr/bin/env python3
# Autor @kaosxx88
# This file is in charge of controll all the other interfaces (chat registration login ...)

from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtWidgets
from PyQt5.QtCore import QThreadPool

# import pyserial (to check the usable connection port)
import serial.tools.list_ports 

# import the ui and stylesheet
from ui_style_sheet import style_sheet, style_sheet_v2
from ui_registration import Ui_registration
from ui_login import Ui_login
from ui_chat import Ui_chat

# import the client
from client import *
# import colors functions and debug
from colors import *


class Controller:
    #
    # The controller chose which windows display and which window to hide
    #
    def __init__(self):

        # check os details
        self.system = ['Windows' if os.name == 'nt' else 'Unix'][0]       
        # Check port used on the os
        self.available_port = [p.device for p in serial.tools.list_ports.comports()]
        # create thread pool for the future work handling
        self.threadpool = QThreadPool()

        I.i (f'System in use   -> {self.system}')
        I.i (f'Available ports -> {self.available_port}')

    def show_ui_login(self):
        '''Loading the login interface'''
        self.ui_login = Ui_login(self)
        self.ui_login.show()

    def show_ui_registration(self):
        '''Loading the registration interface'''
        self.ui_registration = Ui_registration(self)
        self.ui_login.close()
        self.ui_registration.show()

    def show_ui_chat(self):
        '''Loading chat interface'''
        self.ui_chat = Ui_chat(self, self.nickname)
        self.ui_chat.setStyleSheet(style_sheet_v2)
        # close the login screen before the chat open
        self.ui_login.close()
        self.ui_chat.show()

    def start_client(self, private , public , nickname ):

        self.nickname = nickname

        D.d('Client Started')
        I.i (f'Private Key : {private}')
        I.i (f'Public Key  : {public}')
        I.i (f'Nickname    : {nickname}')

        #Load the client
        self.client = Client(private , public , nickname , self)
        # login validation signal
        self.client.signals.login_validation.connect(self.login_validation_response)
        # connection closed from the server
        self.client.signals.lost_connection.connect(self.client_lost_connection)
        # add process to the pool
        self.threadpool.start(self.client)

    def client_lost_connection(self,result):

        message = result[1]

        # if the chat is open 
        if self.ui_chat.isHidden() == False:
            self.ui_chat.close()

        QMessageBox.warning(None, 'Error Message',  message, QMessageBox.Close, QMessageBox.Close)
        self.show_ui_login()


    def client_signals(self):
        '''Setting all the signal link'''

        # get the notification
        self.client.signals.notification.connect(self.ui_chat.notification)
        # update chat history function
        self.client.signals.chat_history.connect(self.ui_chat.save_history_local)
        # incoming message signals
        self.client.signals.incoming_message.connect(self.ui_chat.incoming_message)
        # notification passsive
        self.client.signals.notification_passive.connect(self.ui_chat.notification_passive)
        # add new recipient
        self.client.signals.add_new_recipient.connect(self.ui_chat.add_recipient_to_user_list_widget)
        # delete conversation
        self.client.signals.delete_conversation.connect(self.ui_chat.delete_conversation_ui_response)
              

    def login_validation_response(self, result):
        D.d (f'Controller login validation response = {result}')

        response = result[0]
        message  = result[1]

        if response == True:
            # Lunch the chat gui
            self.show_ui_chat()
            # activate all the signals
            self.client_signals()

        elif response == False:
            # meesage to the user
            QMessageBox.warning(None, 'Error Message',  message, QMessageBox.Close, QMessageBox.Close)

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)  
    app.setStyleSheet(style_sheet)    
    controller = Controller()
    controller.show_ui_login()
    sys.exit(app.exec_())
