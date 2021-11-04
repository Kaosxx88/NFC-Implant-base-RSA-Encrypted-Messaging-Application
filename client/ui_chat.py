#!/usr/bin/env python3
# Autor @kaosxx88
# GUI function for the chat window

import sys
from colors import *
from PyQt5.QtGui import QColor, QFont, QPixmap
from PyQt5.QtCore import Qt , QSize,QRect, QEvent
from PyQt5.QtWidgets import QApplication,QMessageBox,QGridLayout, QVBoxLayout, QListWidget, QLineEdit, QLabel, QPushButton, QListWidgetItem, QPlainTextEdit, QWidget


class Ui_chat(QWidget):
    def __init__(self,controller, nickname): 
        super().__init__()

        self.controller         = controller
        self.recipient          = None
        self.history            = None
        self.nickname           = nickname
        # variable to come back to original size
        self.restorePos         = ''
        self.restoreSize        = ''

        # Mouse pressing variable
        self.pressing           = False
        self.mouse_double_click = True

        # css object name
        self.setObjectName("body")

        # windows borderless (top bar removed)
        self.setWindowFlags(Qt.FramelessWindowHint)

        # The title is hided but the system will use that name anyway
        self.setWindowTitle('Nirema')


        self.logo_label = QLabel(self)
        pixmap = QPixmap('images/logo/logo3_mini_2.png')
        self.logo_label.setPixmap(pixmap)
        #self.logo_label.setScaledContents(True)
        #self.setCentralWidget(logo_label)
        #self.resize(pixmap.width(), pixmap.height())


        # title of the windows 
        self.title = QLabel('Nirema - v 1.0')
        self.title.setObjectName("title")

        # Show the windows
        self.show()

        self.load_ui_elements()

    def load_ui_elements(self):

        # Creation of the grid
        self.layout_general = QGridLayout()

        # set spacing in the grid
        self.layout_general.setSpacing(15)

        # collumn minimum width
        self.layout_general.setColumnMinimumWidth(0,10)
        self.layout_general.setColumnMinimumWidth(1,10)
        self.layout_general.setColumnMinimumWidth(2,10)
        self.layout_general.setColumnMinimumWidth(3,250)

        # Buttons column min width
        self.layout_general.setColumnMinimumWidth(7,30)
        self.layout_general.setColumnMinimumWidth(8,30)
        self.layout_general.setColumnMinimumWidth(9,30)

        #See also columnMinimumWidth(),setRowMinimumHeight(), setColumnStretch(int column, int stretch), spacing(), setVerticalSpacing(), and setHorizontalSpacing().

        # collumn expansion Stretch value
        self.layout_general.setColumnStretch(0,0)
        self.layout_general.setColumnStretch(1,5)
        self.layout_general.setColumnStretch(2,0)
        self.layout_general.setColumnStretch(3,10)

        # extension of the row
        self.layout_general.setRowStretch(0,200)
        self.layout_general.setRowStretch(2,100)
        self.layout_general.setRowStretch(3,100)
        self.layout_general.setRowStretch(6,0)

        # setting the row minimum height
        self.layout_general.setRowMinimumHeight(0,10)
        self.layout_general.setRowMinimumHeight(1,10)
        self.layout_general.setRowMinimumHeight(3,250)

        # creation of the widget
        self.left_user_list = QListWidget()
        self.left_user_list.setObjectName("box")
        self.left_user_list.itemClicked.connect(self.show_chat_after_recipient_pressed)

        # creation sample items for the list widget conversation
        # self.left_user_list.addItem("Dennis:\n   _1Conversation_1Conversation_") 
        # self.left_user_list.addItem("Matteo:\n   Conversation_2")
        # self.left_user_list.addItem("Federico:\n   Conversation_3")

        # creation main hcta list widget
        self.right_chat_list = QListWidget()
        self.right_chat_list.setObjectName("box")

        # adding sample element to the list widget main chat
        #self.right_chat_list.addItem("message_1")
        #self.right_chat_list.addItem("message_2")

        #creation of custom qlist widget 
        # item = QListWidgetItem('banana')
        # item.setTextAlignment(Qt.AlignRight)
        # item.setForeground(QColor('blue'))
        #item.setBackground(QColor('red'))
        #item.setFont(QFont('', QFont.Black    ))
        #'https://doc.qt.io/qt-5/qfont.html'

        #self.right_chat_list.addItem(item)
        #self.right_chat_list.addItem("Message_3")

        # message entry
        self.message_entry = QPlainTextEdit()
        self.message_entry.setObjectName("entry")
        #self.message_entry.returnPressed.connect(self.send_message)
        self.message_entry.setTabChangesFocus(True)
        self.message_entry.setPlaceholderText('Type a message')
        self.message_entry.installEventFilter(self)

        # search entry user
        self.search_entry_user = QLineEdit()
        self.search_entry_user.setObjectName("entry")
        self.search_entry_user.textChanged.connect(self.filter_on_text_changed_user)
        self.search_entry_user.setPlaceholderText('Search User')
        self.search_entry_user.installEventFilter(self)

        # search entry chat
        self.search_entry_chat = QLineEdit()
        self.search_entry_chat.setObjectName("entry")
        self.search_entry_chat.textChanged.connect(self.filter_on_text_changed_chat)
        self.search_entry_chat.setPlaceholderText('Search in chat')

        # search / add user transition 
        self.instruction_message_search_user = 'Press + to add a new user\n\nBe careful the user name is case sensitive'
        self.add_user_left_label_message = QLabel(self.instruction_message_search_user)
        self.add_user_left_label_message.setWordWrap(True)
        self.add_user_left_label_message.setStyleSheet( "border-radius :10px; border: 2px solid orange; padding-left : 10px; padding-right : 10px;")
        self.add_user_left_label_message.setAlignment(Qt.AlignCenter) 

        # serach in chats
        self.right_label_intro_message = QLabel()
        self.right_label_intro_message.setStyleSheet( "min-height: 400px;border-radius :10px; border: 2px solid orange; padding-left : 10px; padding-right : 10px; color:orange; font-size: 15px ")
        self.right_label_intro_message.setAlignment(Qt.AlignCenter) 
        self.right_label_intro_message.setWordWrap(True)
        self.right_label_intro_message.setText("Welcome To NIREMA,\n\n'NFC base Implant RSA Encrypted Messaging Application'\n\nSelect a recipient or add a new one to start.")


        # nicknmane of the chat referral 
        self.chat_person_nickname = QLabel(self.nickname)
        self.chat_person_nickname.setObjectName("text")

        # user nickname
        self.user_nickname = QLabel()
        self.user_nickname.setObjectName("text")

        ##################
        # Resize Buttons #
        ##################

        button_size_1 = QPushButton("-")
        button_size_1.setObjectName("size_button")
        button_size_1.clicked.connect(self.btn_min_clicked)

        self.button_size_2 = QPushButton(">")
        self.button_size_2.setObjectName("size_button")
        self.button_size_2.clicked.connect(self.btn_max_clicked)        

        self.button_size_2_2 = QPushButton("<")
        self.button_size_2_2.setObjectName("size_button")
        self.button_size_2_2.clicked.connect(self.btn_back_size_clicked)
        # hide the button (appear only in full screen mode)
        self.button_size_2_2.setVisible(False)
        
        button_size_3 = QPushButton("x")
        button_size_3.setObjectName("exit_button")
        button_size_3.clicked.connect(self.btn_close_clicked)

        #################
        # Mains Buttons #
        #################

        self.button_1 = QPushButton(" + ")
        self.button_1.setToolTip('<b>Open a new conversation </b>')   
        self.button_1.clicked.connect(self.add_new_recipient) 
 

        button_2 = QPushButton(" Hide ")
        button_2.setToolTip('<b>Hide the entire windows</b>')

        #button_3 = QPushButton(" Search ")
        #button_3.setToolTip('<b>Search in the conversation</b>')

        self.button_4 = QPushButton("Delete")
        self.button_4.setToolTip('<b>Delete the entire conversation remotly</b>')
        self.button_4.setObjectName("exit_button")
        self.button_4.clicked.connect(self.delete_conversation)

        self.button_5 = QPushButton("Send")
        self.button_5.setObjectName("send_button")
        self.button_5.clicked.connect(self.send_message)

        #button_6 = QPushButton(" Search ")
        #button_6.setToolTip('<b>Search contact conversation</b>')
        #button_6.clicked.connect(self.search_in_chat)

        self.button_7 = QPushButton("Clear")
        self.button_7.setToolTip('<b>Clear the message box</b>')
        self.button_7.setObjectName("clear_button")
        self.button_7.clicked.connect(self.clear_message)
        
        ###############################
        # Loading element to the grid #
        ###############################  

        self.layout_general.addWidget( self.logo_label                  , 0, 0 )
        self.layout_general.addWidget( self.title                       , 0, 1 ) 
        self.layout_general.addWidget( button_size_1                    , 0, 7 ) 
        self.layout_general.addWidget( self.button_size_2               , 0, 8 ) 
        self.layout_general.addWidget( self.button_size_2_2             , 0, 8 )     
        self.layout_general.addWidget( button_size_3                    , 0, 9 ) 
        self.layout_general.addWidget( self.chat_person_nickname        , 1, 0 ) 
        self.layout_general.addWidget( self.button_1                    , 2, 2, Qt.AlignRight) 
        #self.layout_general.addWidget( button_2                        , 1, 2 ) 
        self.layout_general.addWidget( self.user_nickname               , 1, 3 ) 
        self.layout_general.addWidget( self.search_entry_chat           , 1, 4, 1,4) 
        self.layout_general.addWidget( self.button_4                    , 1, 8, 1,2) 
        self.layout_general.addWidget( self.search_entry_user           , 2, 0, 1,2)         
        

        #self.layout_general.addWidget( button_6                        , 2, 2 )
        self.layout_general.addWidget( self.left_user_list              , 3, 0, 3, 3) 
        #self.layout_general.addWidget( self.right_chat_list            , 2, 3, 2,7) 
        self.layout_general.addWidget( self.right_label_intro_message   , 2, 3, 4,7)
        self.layout_general.addWidget( self.message_entry               , 4, 3, 2,5) 
        self.layout_general.addWidget( self.button_5                    , 4, 8, 1,2) 
        self.layout_general.addWidget( self.button_7                    , 5, 8, 1,2)

        # load layout in the grid
        self.setLayout(self.layout_general)

        self.inizialisation_user_list()

        # element to hide on start
        self.user_nickname.hide()
        self.button_4.hide()      
        self.button_5.hide()      
        self.button_7.hide()      
        self.search_entry_chat.hide()
        self.message_entry.hide()


    def incoming_message(self, result):
        #
        # manage incoming message (add them to the gui) 
        #
        sender = result[0]
        message = result[1]
        message_incoming = (sender, message)
        # if the message come from a new user, create a newdictionary location
        if self.recipient not in self.history:
            self.history[self.recipient] = []
        # add message to history
        (self.history[self.recipient]).append(message_incoming)
        # update the current chat
        self.add_incoming_message_to_list_view(message)



    def add_recipient_to_user_list_widget(self, list):
        #
        # serach and add new user to the recipient list menu 
        #        
        D.d('Response from the server arriver to the ui chat')

        error = list[0]     

        if error :

            error_value = list[1]
            D.d (C.red_clean('Error present'))
            D.d (error_value)
            #
            # display error to the user ->  error message on left panel
            #
            self.add_user_left_label_message.setText('<font color="orange"> User not present on the server!</font>')  
        else:
            public_key = list[1]
            recipient  = list[2]                   

            D.d(f'Adding new recipient {C.green_clean(recipient)} to the list')

            user_present = False
            # total number of user present
            recipient_number = self.left_user_list.count()
            # loop on all of them for any match
            for row in range(self.left_user_list.count()):
                # selection of each row
                available_row = self.left_user_list.item(row)
                # selecting the new insert user
                if recipient in available_row.text():

                    self.left_user_list.setCurrentRow( row )
                    #
                    # get the chat?
                    #
                    user_present = True

                    
            if user_present == False:
                # recipient name
                widget = f'{recipient}'
                # add recipient to the list of recipient
                self.left_user_list.addItem(widget)

                # select the user just added
                recipient_number = self.left_user_list.count()
                for row in range(self.left_user_list.count()):
                    available_row = self.left_user_list.item(row)
                    if recipient in available_row.text():
                        # select the added item as selected
                        self.left_user_list.setCurrentRow( row )
                        self.user_nickname.setText(recipient)
                        self.user_nickname.show()
                        #
                        # the left screen is hidden ( Maybe show it?)
                        #

            # add new recipient to the history
            self.history[recipient]= []             

            # change color of the button
            self.button_1.setStyleSheet('background: #28ABCD')  
            # change color of the recipient entry   
            self.search_entry_user.setStyleSheet('background: #28ABCD')
            # clear the search entry
            self.search_entry_user.clear()
            # show back the list recipient updated with the new one
            self.left_user_list.show()
            self.message_entry.setFocus()
            #
            # select the just added recipient
            self.show_chat_after_recipient_added(recipient)
            #
            # Show message to start to write the message with the new user
            
 
    

    def inizialisation_user_list(self):
        #
        # inizialise user list at loading time if no user show message add user
        #
        total_user_number = self.left_user_list.count()

        if total_user_number == 0:

            # change color of the button +         
            self.button_1.setStyleSheet('background: orange')     
            # change color of the entry
            self.search_entry_user.setStyleSheet('background: orange') 
            # hide the left widget list
            self.left_user_list.hide()
            # plot the net label
            self.layout_general.addWidget( self.add_user_left_label_message, 3, 0, 3,3)
            # show the new label
            self.add_user_left_label_message.show() 

    def update_recipient_in_client(self):
        #
        # update the recipient of the message in the other class (important to encrypt/ decrypt the message with the correct key)
        #
        self.controller.client.update_recipient_from_gui(self.recipient)


    def delete_conversation(self):
        #
        # function to trigger the delete conversation function (GUI)
        #
        D.d('Delete conversation triggered')

        buttonReply = QMessageBox.warning(self, 'Delete conversation', "Delete the conversation from the server?", QMessageBox.Yes | QMessageBox.No )
        
        if buttonReply == QMessageBox.Yes:

            self.controller.client.delete_conversation_ui()

        elif buttonReply == QMessageBox.No:
            pass




    def delete_conversation_ui_response(self, result):
        #
        # function to get server response for the deletion of a chat 
        #
        if result == True:
            D.d(f'Conversaton deleted = {C.green_clean("True")}')

            del self.history[self.recipient]

            # select the user just added
            recipient_number = self.left_user_list.count()
            for row in range(self.left_user_list.count()):
                available_row = self.left_user_list.item(row)
                if self.recipient == available_row.text():
                    # select the added item as selected
                    self.left_user_list.takeItem(row)
                    break

            self.user_nickname.hide()
            self.button_4.hide()      
            self.button_5.hide()      
            self.button_7.hide()      
            self.search_entry_chat.hide()
            self.message_entry.hide()
            self.right_chat_list.hide()
            self.layout_general.removeWidget(self.right_chat_list)

            self.layout_general.addWidget( self.right_label_intro_message      , 2, 3, 4,7)

            self.right_label_intro_message.show()

            # deselect the recipient
            self.recipient = None
            self.update_recipient_in_client()
            # show message label if no user present in the widget
            self.inizialisation_user_list()

        else:
            D.d(f'Conversaton deleted = {C.green_clean("False")}')


    def add_new_recipient(self):
        #
        # function that add new recipient after button has been pressed
        #
        D.d('Add new recipient button pressed')

        # load text to from entry
        recipient_to_get = self.search_entry_user.text()
        # check if the text is not empty
        if len(recipient_to_get) != 0:
            # check if there is already the recipient
            if recipient_to_get not in self.history:
                D.d(f'New Recipient added = {C.green_clean(recipient_to_get)}')
                #
                # Check if the user do not exist already
                #
                self.controller.client.add_recipient_to_client(recipient_to_get)


    def notification(self, result):
        #
        # set notification of incoming message highliting the user
        #
        sender = result[1]
        message = result[2]
        message_incoming = (sender, message)        
        # if the message sender is not in the dictionary, add it
        if sender not in self.history:
            self.history[sender] = []
        # append incoming message to dictionary
        self.history[sender].append(message_incoming)

        D.d('New conversation added to history')

        user_in_list = False

        # total number of user present
        recipient_number = self.left_user_list.count()
        # loop on all of them for any match
        for row in range(self.left_user_list.count()):
            # selection of each row
            available_row = self.left_user_list.item(row)

            if sender == available_row.text():
                # enable color for notification
                available_row.setForeground(QColor('orange'))
                #available_row.setFont(QFont('', weight=QFont.Bold))

                user_in_list = True

        if user_in_list == False:

            D.d(f'User {C.green_clean(sender)} not presend, adding it and color as notification')
            item = QListWidgetItem(sender)
            item.setForeground(QColor('orange'))
            #item.setFont(QFont('', weight=QFont.Bold))
            # add recipient to the list of recipient
            self.left_user_list.addItem(item)


    def notification_passive(self, result):
        #
        # set notification of incoming message highliting the user
        # -> different version testing

        sender = result[1]

        new_user = result[3]

        if new_user == False:  


            message = result[2]
            message_incoming = (sender, message) 

            self.history[sender].append(message_incoming)          

        user_present = False
        # total number of user present
        recipient_number = self.left_user_list.count()
        # loop on all of them for any match
        for row in range(self.left_user_list.count()):
            # selection of each row
            available_row = self.left_user_list.item(row)
            if sender in available_row.text():
                available_row.setForeground(QColor('orange'))
                user_present = True

        if user_present == False:
            item = QListWidgetItem(sender)
            item.setForeground(QColor('orange'))
            #item.setFont(QFont('', weight=QFont.Bold))
            # add recipient to the list of recipient
            self.left_user_list.addItem(item)
            self.controller.client.history_conversation()

        # refresh the list of user if a message arrive
        # change color of the butto +         
        self.button_1.setStyleSheet('background: #28ABCD')     
        # change color of the entry
        self.search_entry_user.setStyleSheet('background: #28ABCD') 
        # hide the left widget list

        # plot the net label
        self.layout_general.removeWidget(self.add_user_left_label_message)
        # show the new label
        self.add_user_left_label_message.hide() 
        self.left_user_list.show()



    def filter_on_text_changed_user(self):
        #
        # keep update the input field while the user is writing 
        # 
        # get the text in the box
        text = self.search_entry_user.text()
        # total number of user present
        recipient_number = self.left_user_list.count()
        # loop on all of them for any match
        for row in range(self.left_user_list.count()):
            # selection of each row
            available_row = self.left_user_list.item(row)

            if text in available_row.text():
                # show the row if match
                available_row.setHidden(False)
                # set color to the 
                self.button_1.setStyleSheet('background: #28ABCD')   
                # set button color  
                self.search_entry_user.setStyleSheet('background: #28ABCD') 
                # show list user
                self.left_user_list.show()
                # remove instruction list
                self.layout_general.removeWidget(self.add_user_left_label_message)
                # hide intruction label
                self.add_user_left_label_message.hide()

            else:

                available_row.setHidden(True)
                recipient_number -= 1

                if recipient_number == 0:

                    # change color of the butto +         
                    self.button_1.setStyleSheet('background: orange')     
                    # change color of the entry
                    self.search_entry_user.setStyleSheet('background: orange') 
                    # hide the left widget list
                    self.left_user_list.hide()
                    # plot the net label
                    self.layout_general.addWidget( self.add_user_left_label_message, 3, 0, 3,3)
                    # show the new label
                    self.add_user_left_label_message.show()
                    self.add_user_left_label_message.setText(self.instruction_message_search_user)  


                



    def filter_on_text_changed_chat(self):
        #
        # filter the research based on the user input fild
        #
        # get the text in the box
        text = self.search_entry_chat.text()
        recipient_number = self.right_chat_list.count()
        #https://stackoverflow.com/questions/53157962/search-filter-custom-widgets-for-qlistwidget
        
        for row in range(self.right_chat_list.count()):
            available_row = self.right_chat_list.item(row)               

            if text in available_row.text():
                available_row.setHidden(False)

                self.search_entry_chat.setStyleSheet('background: #28ABCD')                 
                self.layout_general.removeWidget(self.right_label_intro_message)
                self.right_label_intro_message.hide()
                
                self.right_chat_list.show()

            else:
                available_row.setHidden(True)
                recipient_number -=1

                if recipient_number == 0:   
                    # change color of the entry
                    self.search_entry_chat.setStyleSheet('background: orange') 
                    # hide the left widget list
                    self.right_chat_list.hide()
                    # plot the net label
                    self.layout_general.addWidget( self.right_label_intro_message      , 2, 3, 2,7)
                    # show the new label
                    # removing the minimum height ( otherwide to long)
                    self.right_label_intro_message.setStyleSheet( "border-radius :10px; border: 2px solid orange; padding-left : 10px; padding-right : 10px; color:orange; font-size: 15px ")
                    self.right_label_intro_message.show() 
                    # short the text if is to long
                    text_holder = text
                    if len(text_holder) > 30:
                        text_holder = text_holder[:30] + '...'
                    # set text
                    self.right_label_intro_message.setText(f'Sorry, No match for "{text_holder}" on the selected chat') 
                


    def send_message(self):
        #
        # get the message from the field and send it
        #

        message = self.message_entry.toPlainText()

        # check if recipient is selected
        if self.recipient == None:
            # no recipient selected
            pass
        else:

            if len(message) != 0:

                # clear the screen
                self.message_entry.clear()

                # add message to the screen
                self.add_message_to_list_view(message)
               
                # send the messge to the server
                recipient = self.recipient
                message_record = (recipient, message)
                self.controller.client.message_sign_and_send_to_request(message_record)

                # add message to the history local
                sender = self.nickname
                message_record_local = (sender, message)
                (self.history[self.recipient]).append(message_record_local)

                # when sending new message remove message stating new message.
                total_items_in_widget_chat = self.right_chat_list.count()
                # loop in the message of the chat to check if there is the separator
                for messagge_index in range(total_items_in_widget_chat -1):
                    #select the item from the list
                    item = self.right_chat_list.item(messagge_index)
                    # check if the item have roles
                    if item.data(Qt.UserRole) == 'separator':
                        # remove the items because the message had been read
                        self.right_chat_list.takeItem(messagge_index)

                        



    def add_message_to_list_view(self, message):
        #
        # show the message to the list view ( left screen)
        #
        new_item = QListWidgetItem(message)
        new_item.setTextAlignment(Qt.AlignLeft)
        self.right_chat_list.addItem(new_item)
        self.right_chat_list.scrollToBottom()

        # add to the history too()

        D.d('Message Added to widget')



    def add_incoming_message_to_list_view(self, message):
        #
        # add incoming message to the right screen
        #

        # check number of message in chat
        total_items_in_widget_chat = self.right_chat_list.count()
        # set flag 
        new_message_aller_present = False
        # loop throught the message
        for messagge_index in range(total_items_in_widget_chat):
            # load the message
            item = self.right_chat_list.item(messagge_index)
            # check if the item is a separator
            if item.data(Qt.UserRole) == 'separator':
                # set the flag separator present
                new_message_aller_present = True

        #if there is the separator for new message do not add anotheronw
        if new_message_aller_present == False:
            # create the separator
            new_message_space = QListWidgetItem('- new message -')
            # center the separator
            new_message_space.setTextAlignment(Qt.AlignCenter)
            # give a role to the separator
            new_message_space.setData(Qt.UserRole, 'separator')
            new_message_space.setForeground(QColor('orange'))
            new_message_space.setBackground(QColor('#7b7b7b'))
            # add separator
            self.right_chat_list.addItem(new_message_space)


        new_item = QListWidgetItem(message)
        #new_item.setSelected(True)
        new_item.setTextAlignment(Qt.AlignRight)
        self.right_chat_list.addItem(new_item)
        
        # get total items in the list
        total_items_in_widget_caht = self.right_chat_list.count()
        # select the last one        
        last_items_added = self.right_chat_list.item(total_items_in_widget_caht-1)
        # select the last items
        #last_items_added.setSelected(True)

        self.right_chat_list.scrollToBottom()

        D.d('Incoming message added to widget list view')
        

    def clear_message(self):
        #
        # Clear message entry
        #
        self.message_entry.clear()


    def save_history_local(self, history):
        #
        # save the actual history locally ( on memory )
        #
        self.history = history

        self.update_list_recipient(self.history)






    def update_list_recipient(self, history):
        #
        # update the list with the recipient
        #
        for user in history:
            #
            #
            # Check if there are nmot already the recipient
            #
            user_present = False

            # total number of user present
            recipient_number = self.left_user_list.count()
            # loop on all of them for any match
            for row in range(self.left_user_list.count()):
                # selection of each row
                available_row = self.left_user_list.item(row)

                if user in available_row.text():
                    user_present = True

            if user_present == False:
                widget = f'{user}'

                self.left_user_list.addItem(widget)
                # Activate left widget
                self.button_1.setStyleSheet('background: #28ABCD')     
                self.search_entry_user.setStyleSheet('background: #28ABCD') 
                self.left_user_list.show()
                self.layout_general.removeWidget(self.add_user_left_label_message)
                self.add_user_left_label_message.hide()





    def show_chat_after_recipient_pressed(self, item):#
        #
        # show the chat of the selected user
        #
        # change color (fom orange to black (notification sseen))
        item.setForeground(QColor('black'))
        #item.setFont(QFont('', weight=QFont.Normal))

        D.d(f'List widget recipient left pressed on {C.green_clean(item.text())}')

        # remove all the items from the list
        self.right_chat_list.clear()

        user_present = False

        # loop throught the history
        for user in self.history:

            if user == item.text():  

                # load the recipient from the row pressed
                self.recipient = item.text()
                # upload the recipient in the client (for activate notification)
                self.update_recipient_in_client()


                user_present = True
                # set the top label name              
                self.user_nickname.setText(user)

                for chat in self.history[user]:
                    # create a new items
                    new_item = QListWidgetItem(chat[1])

                    if chat[0] == item.text():
                        
                        new_item.setTextAlignment(Qt.AlignRight)
                        #new_item.setForeground(QColor('red'))
                        #new_item.setBackground(QColor('red'))
                    else:
                        new_item.setTextAlignment(Qt.AlignLeft)
                        #new_item.setForeground(QColor('blue'))

                    # add the item to the list
                    self.right_chat_list.addItem(new_item)
                    # show the left list widget
                    self.layout_general.addWidget( self.right_chat_list      , 2, 3, 2,7) 
                    self.right_chat_list.show()

                    self.layout_general.removeWidget(self.right_label_intro_message)
                    self.right_label_intro_message.hide()


                    # Show element hidden on start
                    self.user_nickname.show()
                    self.button_4.show()      
                    self.button_5.show()      
                    self.button_7.show()      
                    self.search_entry_chat.show()
                    self.message_entry.show()


        if user_present == False:
            self.controller.client.add_recipient_to_client(item.text())              

        # scroll dow the list after the update
        self.right_chat_list.scrollToBottom()




    def show_chat_after_recipient_added(self, recipient):
        #
        # selet the user and show the chat once the recipient have been added
        #

        # load the recipient from the row pressed
        self.recipient = recipient
        # upload the recipient in the client (for activate notification)
        self.update_recipient_in_client()

        D.d(f'Recipient {C.green_clean(recipient)} added to the list and selected\n')

        # remove all the items from the list
        self.right_chat_list.clear()
        # show the list chats
        self.layout_general.addWidget( self.right_chat_list      , 2, 3, 2,7) 
        self.right_chat_list.show()
        # remove 
        self.layout_general.removeWidget(self.right_label_intro_message)
        self.right_label_intro_message.hide()

        self.button_4.show()      
        self.button_5.show()      
        self.button_7.show()      
        self.search_entry_chat.show()
        self.message_entry.show()
                    

        # scroll dow the list after the update
        self.right_chat_list.scrollToBottom()



    def btn_close_clicked(self):
        #
        # close the application when the button x has been pressed
        #
        D.d('button close "x" clicked')
        # Closing the connnection properly
        self.controller.client.ssock.shutdown(1) 
        self.close()




    def btn_max_clicked(self):
        #
        # maximise the application chat in full screen
        #

        D.d('Maximise the screen')
        
        # hide the button and replace it
        self.button_size_2.setVisible(False)
        self.button_size_2_2.setVisible(True)
        # Change the size of the application
        self.restorePos , self.restoreSize = (self.pos(), QSize(self.width(), self.height()))

        desktopRect = QApplication.desktop().availableGeometry()
        FactRect = QRect(desktopRect.x() - 3, desktopRect.y() - 3, desktopRect.width() + 6, desktopRect.height() + 6)

        self.setGeometry(FactRect)
        self.setFixedSize(desktopRect.width() + 6, desktopRect.height() + 6)

        self.mouse_double_click = False

    def btn_back_size_clicked(self):
        #
        # restore normal application size ( after full screen )
        #
        self.button_size_2.setVisible(True)
        self.button_size_2_2.setVisible(False)

        self.setGeometry(self.restorePos.x(), self.restorePos.y(), self.restoreSize.width(), self.restoreSize.height())
        self.setFixedSize(self.restoreSize.width(), self.restoreSize.height())

        self.mouse_double_click = True

    def btn_min_clicked(self):
        #
        # control the pressing of the reduce button 
        #
        # on press minimize the app
        self.showMinimized()

    def mousePressEvent(self, event):
        #
        # manager of the mouse press event around the border
        #
        # pqt5 function to get mouse event (https://doc.qt.io/qt-5/qwidget.html)
        self.start = self.mapToGlobal(event.pos())
        self.pressing = True

        # double click full screen and back
        if (event.type() == event.MouseButtonDblClick ):
            D.d('Double click')
            if self.mouse_double_click == True:
                self.btn_max_clicked()
            elif self.mouse_double_click == False:
                self.btn_back_size_clicked()

    def mouseMoveEvent(self, event):
        #
        # magare the move mouse event once pressed the borser
        #
        # press and move app with the mouse
        if self.pressing:
            self.end = self.mapToGlobal(event.pos())
            self.movement = self.end-self.start
            self.setGeometry(self.mapToGlobal(self.movement).x(),
                                self.mapToGlobal(self.movement).y(),
                                self.width(),
                                self.height())
            self.start = self.end

    def mouse_release_event(self, QMouseEvent):
        #
        # check for the mouse release event when moving the gui
        #
        # check when the mouse release the hold
        self.pressing = False




    def eventFilter(self, obj, event): 
        #
        # fildered function for particolar task ( like if message entry is selected if enter is pressed send message)
        #
        # if enter in chat send the message
        if obj is self.message_entry and event.type() == QEvent.KeyPress:
            if event.key() in (Qt.Key_Return, Qt.Key_Enter):
                D.d('Enter pressed on chat selected  - Calling send message function')
                self.send_message()
                return True

        # enabling enter and return button for the user entry search
        elif obj is self.search_entry_user and event.type() == QEvent.KeyPress:
            if event.key() in (Qt.Key_Return, Qt.Key_Enter):
                D.d('Enter pressed on add recipient - Calling add new recipient function')
                self.add_new_recipient()
                return True

        return super().eventFilter(obj, event)

