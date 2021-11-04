style_sheet="""

QWidget {font-size: 11pt; font-family:  ; background : #272A34; color : white;}

QTabWidget QTabBar{ min-width: 298px;}
QTabWidget QTabBar::tab{ height: 25px; color: black;background-color: #7b7b7b;}
QTabWidget QTabBar::tab:selected{background-color: #28ABCD; color: black;}

#label {font-size: 20pt; min-width: 300px; }

QTabWidget {background:  orange ; border: 2px solid orange;}

QTabWidget QTabBar::tab:hover{ background:  orange ;}

QTabWidget

QLineEdit::hover
{
    background: orange;
    color: black;
    border-radius :10px;
}

QLineEdit, .QPushButton, .QComboBox
{
    background: #28ABCD;
    color: black;
    border-radius :10px;
    border: 2px solid orange;
    padding-left : 10px;
    padding-right : 10px;



}

.QComboBox
{
    background: #28ABCD;
    color: black;
    border-radius :2px;
    border: 2px solid orange;

}




QComboBox::down-arrow
{   
    background : orange;
    border: 2px solid orange;
}


QLineEdit
{

    padding-left : 5px;


}



.QPushButton:hover:!pressed
{
  border: 2px solid white;
  background: orange;
  color: black;
  font-size: 15px;  
}




QRadioButton::indicator {
    width:                  10px;
    height:                 10px;
    border-radius:          7px;
}

QRadioButton::indicator:checked {
    background-color:       #28ABCD;
    width:                  10px;
    height:                 10px;
    border-radius:          7px;
    border:                 2px solid orange;
}


QRadioButton::indicator:unchecked {
    
    border:                 2px solid orange;
    border-radius:          7px;
}

"""



#// utilisation
#//#passphrase {color: red; }
#//self.passphrase_entry.setObjectName("passphrase")





style_sheet_v2='''



#send_button:hover:!pressed
{
  border: 2px solid orange;
  background: green;
  color: black;
  font-size: 17px;

}

#exit_button:hover:!pressed
{
	border: 2px solid orange;
	color: red;
	background: black;
	font-size: 17px;
	border-radius: 4px;
}

#body {
	background : #272A34;


}

#size_button:hover:!pressed
{

	font-size: 17px;
	border-radius: 4px;
}

#box:hover:!pressed ,  #entry:hover:!pressed 
{
	border: 2px solid white;
}

.QPushButton:hover:!pressed
{
  border: 2px solid white;
  background: orange;
  color: black;
  font-size: 17px;	
}


QListWidget::item:hover:!active, QListWidget::item:hover:active,QListWidget::item:selected
{
	background: orange;
  	color: black;
  	border-radius :10px;
}




#title 
{
	font-weight: 900;
	font-size: 15px;
	color: white;
}

#box ,  #entry , .QPushButton
{
	background : #28ABCD; 
	padding : 5 px;
	padding-left : 5 px;
	padding-right : 5 px;
	border-radius: 10px; 
	border: 2px solid orange;
	color: #272A34;
	font-weight: 500;
	font-size: 15px;

}

#box:item { padding: 3px; }


QToolTip { 
    background-color: #28ABCD; 
    color: #272A34; 
    border-width:2px;
    font-size: 15px;
    padding:2px;
    border-style: solid;
    border-radius:4px;
    border-color: orange;
}
   

#text 
{
	color : orange ;
	font-weight: 900;
	font-size: 20px;
	
}

/* HORIZZONTAL SCROLL BAR */

 QScrollBar:horizontal
 {
     height: 15px;
     margin: 3px 15px 3px 15px;
     border: 1px transparent #2A2929;
     border-radius: 4px;
     background-color: #272A34;   
 }

  QScrollBar::handle:horizontal
 {
     background-color: #28ABCD;      
     min-width: 5px;
     border-radius: 4px;
     border: 1px solid #272A34;
 }

 QScrollBar::add-line:horizontal
 {
     margin: 0px 3px 0px 3px;
     border-image: url(:/qss_icons/rc/right_arrow_disabled.png);
     width: 10px;
     height: 10px;
     subcontrol-position: right;
     subcontrol-origin: margin;
 }

  QScrollBar::sub-line:horizontal
 {
     margin: 0px 3px 0px 3px;
     border-image: url(:/qss_icons/rc/left_arrow_disabled.png);
     height: 10px;
     width: 10px;
     subcontrol-position: left;
     subcontrol-origin: margin;
 }

 QScrollBar::add-line:horizontal:hover,QScrollBar::add-line:horizontal:on
 {
     border-image: url(:/qss_icons/rc/right_arrow.png);
     height: 10px;
     width: 10px;
     subcontrol-position: right;
     subcontrol-origin: margin;
 }
 QScrollBar::sub-line:horizontal:hover, QScrollBar::sub-line:horizontal:on
 {
     border-image: url(:/qss_icons/rc/left_arrow.png);
     height: 10px;
     width: 10px;
     subcontrol-position: left;
     subcontrol-origin: margin;
 }

 QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal
 {
     background: none;
 }


 QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal
 {
     background: none;
 }


/*  VERTICAL SCROLL BAR */ 

QScrollBar:vertical
 {
     background-color: #272A34;
     width: 15px;
     margin: 15px 3px 15px 3px;
     border: 1px transparent #2A2929;
     border-radius: 4px;
 }

 QScrollBar::handle:vertical
 {
     background-color: #28ABCD ;      /* central part */
     min-height: 5px;
     border-radius: 4px;
     border: 1px solid #272A34;
 }

 QScrollBar::sub-line:vertical
 {
     margin: 3px 0px 3px 0px;
     border-image: url(:/qss_icons/rc/up_arrow_disabled.png);
     height: 10px;
     width: 10px;
     subcontrol-position: top;
     subcontrol-origin: margin;
 }

 QScrollBar::add-line:vertical
 {
     margin: 3px 0px 3px 0px;
     border-image: url(:/qss_icons/rc/down_arrow_disabled.png);
     height: 10px;
     width: 10px;
     subcontrol-position: bottom;
     subcontrol-origin: margin;
 }

 QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on
 {

     border-image: url(:/qss_icons/rc/up_arrow.png);
     height: 10px;
     width: 10px;
     subcontrol-position: top;
     subcontrol-origin: margin;
 }


 QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on
 {
     border-image: url(:/qss_icons/rc/down_arrow.png);
     height: 10px;
     width: 10px;
     subcontrol-position: bottom;
     subcontrol-origin: margin;
 }

 QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical
 {
     background: none;
 }


 QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical
 {
     background: none;
 }


'''