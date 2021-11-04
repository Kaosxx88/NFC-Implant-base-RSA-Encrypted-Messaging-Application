#!/usr/bin/env python3
# Autor @kaosxx88
# this file display the loading animation


from PyQt5.QtWidgets import ( QProgressBar, QWidget, QLabel)
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt


class Ui_loading(QWidget):
    def __init__(self,  parent=None):
        super().__init__(parent)

        self.progess_value = 0
        #self.setAlignment(QtCore.Qt.AlignCenter)
        self.setFixedSize(360, 425) 

        #self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint)

        self.label_animation = QLabel(self)

        #self.label_animation.move(-120, 0)
        self.movie = QMovie('gif/loading_8.gif')
        self.label_animation.setMovie(self.movie)

        self.update_label = QLabel( self)

        self.update_label.move(0, 330)
        self.update_label.setObjectName("update_label")
        self.update_label.setStyleSheet('color: white ; font-size: 12pt')
        self.update_label.setAlignment(Qt.AlignCenter)
        self.update_label.resize(360,40)

        self.progress_bar_loading = QProgressBar(self)
        self.progress_bar_loading.resize(300, 20)
        self.progress_bar_loading.move(30,390)
        self.progress_bar_loading.setAlignment(Qt.AlignCenter) 
        self.progress_bar_loading.setValue(0)
        self.progress_bar_loading.setStyleSheet('border: 2px solid ; border-radius: 5px; background-color: #272A34; font-size: 12pt; border-color : linear-gradient(to right, red,orange,yellow,green,blue,indigo,violet)' )
        self.progress_bar_loading.setTextVisible(False)

    def update_bar(self):
        self.progess_value += 7
        self.progress_bar_loading.setValue(self.progess_value)


    def startAnimation(self): 
        self.movie.start() 
  
    # Stop Animation(According to need) 
    def stopAnimation(self): 
        self.movie.stop() 
        self.close()

    def change_update_label(self, text):
        self.update_label.setText(text)
