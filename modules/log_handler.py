#!/usr/bin/python
# -*- coding: utf-8 -*-
###################################################################################################
# Built IN
import os #,json, subprocess, httplib, urllib, urllib2, hashlib
from random import randint
from threading import Timer
from sys import stdout
from time import sleep, time, ctime, strftime, localtime
from datetime import datetime

#--------------------------------------------------------------------------------------------------
import magic
import mimetypes
mimetypes.init();

#--------------------------------------------------------------------------------------------------
# -> 'ascii' codec can't encode characters in position 220-223: ordinal not in range(128)
import sys
reload(sys);
sys.setdefaultencoding('utf-8');

#--------------------------------------------------------------------------------------------------
#FIXME: remove unused modules imports
# OyQt
from PyQt4.QtCore import QEvent #, QMouseEvent, QContextMenuEvent, QKeyEvent, QContextMenuEvent

from PyQt4.QtCore import QTimer, QThread, SIGNAL, SLOT, pyqtSignal, pyqtSlot
from PyQt4.QtCore import QObject, QSize, QByteArray, QUrl, Qt, QPointF, QPoint, QRectF, QRect, QString

from PyQt4.QtGui import QMessageBox, QTextEdit, QDialog, QPolygonF, QPainter, QPen, QColor, QImage
from PyQt4.QtGui import QBrush, QMainWindow, QWidget, QToolTip, QApplication, QFont, QIcon, QAction
from PyQt4.QtGui import QFrame, QListWidget,QListWidgetItem, QComboBox, QCheckBox, QPushButton, QProgressBar, QLineEdit, QLabel
from PyQt4.QtGui import QTextBrowser, QCursor, qApp, QDesktopWidget, QGraphicsView, QGraphicsScene, QPicture
from PyQt4.QtGui import QSplashScreen, QPixmap, QTabWidget, QMovie, QPaintDevice, QSizePolicy

from PyQt4.QtGui import QDoubleValidator, QRadioButton, QButtonGroup, QHBoxLayout, QVBoxLayout
from PyQt4.QtGui import QLCDNumber, QStyleOptionTabWidgetFrame, QFileDialog

#from PyQt4 import QtWebKit  
from PyQt4.QtWebKit import QWebView, QWebPage, QWebSettings, QWebHistory

# -> http://pyqt.sourceforge.net/Docs/PyQt4/qtnetwork.html
from PyQt4.QtNetwork import QNetworkRequest, QNetworkAccessManager, QNetworkReply
from PyQt4.QtNetwork import QNetworkCookie, QNetworkCookieJar


###################################################################################################
class Log_Handler_TextArea( QTextEdit ):

    # =======================================================================
    def __init__(self, parent=None):

        # -------------------------------------------------------------------
        QTextEdit.__init__(self, parent);

        # -------------------------------------------------------------------
        self.PARENT                                 = parent;
        self.DEBUG                                  = False;
        self.LOG_TAG                                = str(self.__class__.__name__).upper();
        self.HAS_FOCUS                              = False;
        self.STL                                    = {
            "default" : "QTextEdit{ font-weight: normal; font: 11px; font-family: monospace; color: #FFF; background-color: rgba(0,0,0, 160); margin: 0px; padding: 5px; border-style: none; }",
            "hovered" : "QTextEdit{ font-weight: normal; font: 11px; font-family: monospace; color: #FFF; background-color: rgba(0,0,0, 255); margin: 0px; padding: 5px; border-style: none; }",
        }

        # -------------------------------------------------------------------
        self.setText( "TEST: TEST" );
        self.setGeometry( 0, 27, 650, 110 );
        self.setStyleSheet( self.STL["default"] );

        self.setReadOnly( True );
        self.setAcceptRichText( False );
        self.setUndoRedoEnabled( True );
        self.LineWrapMode( self.WidgetWidth );

        # -------------------------------------------------------------------

    # =======================================================================
    def event( self, _evt ):

        # -------------------------------------------------------------------
        # http://pyqt.sourceforge.net/Docs/PyQt4/qevent.html#Type-enum
        #print( _evt.type() );
        # -------------------------------------------------------------------
        #if _evt.type() == QEvent.FocusOut:      # (QFocusEvent) == 9 == focus OUT BY CLICK
        #elif _evt.type() == QEvent.FocusIn:     # (QFocusEvent) == 8 == focus IN BY CLICK

        # -------------------------------------------------------------------
        #if _evt.type() == QEvent.ContextMenu:   # (QContextMenuEvent) == 82

        # -------------------------------------------------------------------
        #QEvent.MouseButtonDblClick  4   Mouse press again (QMouseEvent).
        #QEvent.MouseButtonRelease   3   Mouse release (QMouseEvent).
        #QPoint _evt.globalPos(); | int _evt.global[X|Y](); | QPoint _evt.pos(); | QPointF _evt.posF(); | int _evt.[x|y]()
        #_evt.button() == ( Qt.LeftButton | Qt.RightButton | Qt.MidButton )
        """
        if _evt.type() == QEvent.MouseButtonPress: # 2   Mouse press (QMouseEvent).

            if _evt.button() == Qt.LeftButton:
                print("Qt.LeftButton: "+str(Qt.LeftButton))

            elif _evt.button() == Qt.MidButton:
                print("Qt.MidButton: "+str(Qt.MidButton))
            
            elif _evt.button() == Qt.RightButton:
                print("Qt.RightButton: "+str(Qt.RightButton))

        """
        # -------------------------------------------------------------------
        """
        #QEvent.KeyPress 6   Key press (QKeyEvent).
        #QEvent.KeyRelease   7   Key release (QKeyEvent).
        if _evt.type() == QEvent.KeyRelease:
            print("KeyRelease: ["+str(_evt.text())+", "+str(_evt.nativeScanCode())+", "+str(_evt.key())+"]");

        int count (self)
        bool isAutoRepeat (self)
        int key (self)
        bool matches (self, QKeySequence.StandardKey key)
        Qt.KeyboardModifiers modifiers (self)
        int nativeModifiers (self)
        int nativeScanCode (self)
        int nativeVirtualKey (self)
        QString text (self)
        """

        # -------------------------------------------------------------------

        if _evt.type() == QEvent.Enter:         # 10

            self.setStyleSheet( self.STL["hovered"] );
            self.HAS_FOCUS = True;

        elif _evt.type() == QEvent.Leave:       # 11 

            self.setStyleSheet( self.STL["default"] );
            self.HAS_FOCUS = False;

        return QTextEdit.event(self, _evt);

        # -------------------------------------------------------------------

    # =======================================================================


###################################################################################################
class Log_Handler( QFrame ):

    # =======================================================================
    def __init__(self, parent=None):

        # -------------------------------------------------------------------
        QFrame.__init__(self, parent);

        # -------------------------------------------------------------------
        self.PARENT                             = parent;
        self.DEBUG                              = True;
        self.LOG_TAG                            = str(self.__class__.__name__).upper();

        self.WIDTH                              = 650;
        self.HEIGHT                             = 160;
        self.ML                                 = 10;
        self.MT                                 = 680;

        self.WIN                                = {
            "OP"    : { "W" : self.WIDTH, "H" : self.HEIGHT, "ML" : self.ML, "MT" : 480 },
            "CL"    : { "W" : 1, "H" : 1, "ML" : self.ML, "MT" : self.MT },
            "CU"    : { "W" : 1, "H" : 1, "ML" : self.ML, "MT" : self.MT } # 680 ftom TOP

        };

        self.LOG_DATA                           = {
            "error"     : [],
            "warning"   : [],
            "info"      : []
        }

        self.setGeometry( self.WIN["CL"]["ML"], self.WIN["CL"]["MT"], self.WIN["CL"]["W"], self.WIN["CL"]["H"] );

        self.setStyleSheet( """
            QFrame{ 
                font-weight: bold; font: 12px; font-family: monospace; color: #fff; background-color: rgba(0,0,0, 120); margin: 0px; padding: 0px;
            
            }""" );

        self.setMouseTracking(True);

        # -------------------------------------------------------------------

        self.IS_OPEN                            = False;
        self.KEEP_OPEN                          = False;
        self.RUNNING                            = False;

        self.STEP_DELAY_MS                      = 1;
        self.STAY_OPEN_DELAY                    = 1000;
        self.STEP_W                             = 10;
        self.STEP_H                             = 2;

        self.POP_UP_TIMER                       = QTimer();

        # -------------------------------------------------------------------
        self.LOG_HANDLER_TIMER                  = QTimer();

        self.LOG_FILE                           = self.PARENT.LOGS_DIR+"_"+strftime("%d-%b-%Y", localtime(time()))+"_.log";

        self.LOG_HEADER                          = QLabel( "Log-handler: [TIME]", self );
        self.LOG_HEADER.setGeometry( 0, 0, 650, 26 );

        self.LOG_HEADER_STYLE                    = { # 'Arial Black', 'Courier New', Courier, monospace
            "error"     : "QLabel{ font-weight: bold; font: 12px; font-family: monospace; color: #F00; background-color: rgba(0,0,0, 200); margin: 0px; padding: 20px; }",
            "warning"   : "QLabel{ font-weight: bold; font: 12px; font-family: monospace; color: #F70; background-color: rgba(0,0,0, 200); margin: 0px; padding: 20px; }",
            "info"      : "QLabel{ font-weight: bold; font: 12px; font-family: monospace; color: #0F0; background-color: rgba(0,0,0, 200); margin: 0px; padding: 20px; }",
        
        }            

        # -------------------------------------------------------------------
        self.LOG_BODY                           = Log_Handler_TextArea( self );

        # -------------------------------------------------------------------
        self.LOG_FOOTER_DEF_TEXT                = "Log-handler:";

        self.LOG_FOOTER                         = QLabel( self.LOG_FOOTER_DEF_TEXT, self );
        self.LOG_FOOTER.setGeometry( 0, 138, 650, 26 );
        self.LOG_FOOTER.setStyleSheet("QLabel{ font-style: italic; font-size: 10px; font-family: monospace; background-color: rgba(0,0,0, 160); margin: 0px; padding: 5px; }");

        # -------------------------------------------------------------------

        self.INIT();
        self.LOG_HANDLER_TIMER.singleShot( 100, self.HANDLE_ERRORS );

        # -------------------------------------------------------------------

    # =======================================================================
    def TO_LOG_FOOTER( self, _msg ):

        # -------------------------------------------------------------------
        self.LOG_FOOTER.setText( self.LOG_FOOTER_DEF_TEXT + _msg );
        # -------------------------------------------------------------------

    # =======================================================================
    def INIT( self ):

        # -------------------------------------------------------------------
        self.PARENT.SPLASH.STATUS( self.LOG_TAG+": [INIT]" );
        self.INIT_LOG_FILE();

        # -------------------------------------------------------------------

    # =======================================================================
    def HANDLE_ERRORS( self ):

        # -------------------------------------------------------------------
        try:

            # ---------------------------------------------------------------
            # print("--------------------------------------------------------");
            # print("IS_OPEN:["+str(self.IS_OPEN)+"] RUNNING:["+str(self.RUNNING)+"] HAS_FOCUS:["+str(self.LOG_BODY.HAS_FOCUS)+"]");
            # print("[I:"+str(len(self.LOG_DATA["info"]))+", W:"+str(len(self.LOG_DATA["warning"]))+", E:"+str(len(self.LOG_DATA["error"]))+"]")

            # ---------------------------------------------------------------
            if not self.IS_OPEN and not self.RUNNING:

                if len( self.LOG_DATA["info"] ) > 0:

                    _data = self.LOG_DATA["info"].pop();
                    self.SHOW( "info", _data );
                    self.WRITE_LOG( _data, " I " );

                elif len( self.LOG_DATA["warning"] ) > 0:

                    _data = self.LOG_DATA["warning"].pop();
                    self.SHOW( "warning", _data );
                    self.WRITE_LOG( _data, " W " );
            
                elif len( self.LOG_DATA["error"] ) > 0:

                    _data = self.LOG_DATA["error"].pop();
                    self.SHOW( "error", _data );
                    self.WRITE_LOG( _data, " E " );

            # ---------------------------------------------------------------
            # Allow Controll POP-Frame
            if not self.RUNNING and self.IS_OPEN and not self.LOG_BODY.HAS_FOCUS:
                self.POP_UP_TIMER.singleShot( self.STAY_OPEN_DELAY, self.HIDE );

            # ---------------------------------------------------------------

        except Exception as _err:
    
            # recursion
            #if self.DEBUG or self.PARENT.DEBUG_GLOBAL: self.PARENT.DEBUGGER.DEBUG();
            print( " LOG_HANDLER: [HANDLE_ERRORS]: ["+str(_err)+"" );

        # -------------------------------------------------------------------
        self.LOG_HANDLER_TIMER.singleShot( 2000, self.HANDLE_ERRORS );

        # -------------------------------------------------------------------

    # =======================================================================
    def SHOW( self, _type, _msg_data, setHTML=False ):

        # -------------------------------------------------------------------
        try:

            #print("SHOW: _SHOW()");
            # ---------------------------------------------------------------
            self.RUNNING = True;
            self.IS_OPEN = False;

            if "info" == _type:
                self.LOG_HEADER.setText( "Log-handler: ["+self.PARENT.GET_DATE_TIME()+"]: [info]" );
                self.LOG_HEADER.setStyleSheet( self.LOG_HEADER_STYLE["info"] );

            elif "warning" == _type:
                self.LOG_HEADER.setText( "Log-handler: ["+self.PARENT.GET_DATE_TIME()+"]: [WARNING]" );
                self.LOG_HEADER.setStyleSheet( self.LOG_HEADER_STYLE["warning"] );

            elif "error" == _type:
                self.LOG_HEADER.setText( "Log-handler: ["+self.PARENT.GET_DATE_TIME()+"]: [ERROR]" );
                self.LOG_HEADER.setStyleSheet( self.LOG_HEADER_STYLE["error"] );

            else:
                self.LOG_HEADER.setStyleSheet( self.LOG_HEADER_STYLE["info"] );

            
            # ---------------------------------------------------------------
            if setHTML:
                self.LOG_BODY.setText( _msg_data );

            else:
                self.LOG_BODY.setPlainText( _msg_data );

            self._SHOW();
            # ---------------------------------------------------------------

        except Exception as _err:
            # recursion
            #if self.DEBUG or self.PARENT.DEBUG_GLOBAL: self.PARENT.DEBUGGER.DEBUG();
            print( str(_err), "SHOW" );

        # -------------------------------------------------------------------

    # =======================================================================
    def _SHOW( self ):

        # -------------------------------------------------------------------
        AL = True;

        # -------------------------------------------------------------------
        if self.WIN["CU"]["W"] < self.WIN["OP"]["W"] :

            self.WIN["CU"]["W"] += self.STEP_W;
            AL = False;

        if self.WIN["CU"]["H"] < self.WIN["OP"]["H"]:

            self.WIN["CU"]["H"] += self.STEP_H;
            AL = False;

        if self.WIN["CU"]["MT"] > self.WIN["OP"]["MT"]:

            self.WIN["CU"]["MT"] -= self.STEP_H;
            AL = False;

        if AL:
    
            self.WIN["CU"]["W"] = self.WIN["OP"]["W"];
            self.WIN["CU"]["H"] = self.WIN["OP"]["H"];

            self.WIN["CU"]["ML"] = self.WIN["OP"]["ML"];
            self.WIN["CU"]["MT"] = self.WIN["OP"]["MT"];

            self.setGeometry( self.WIN["CU"]["ML"], self.WIN["CU"]["MT"], self.WIN["CU"]["W"], self.WIN["CU"]["H"] );

            self.IS_OPEN = True;
            self.RUNNING = False;
    
        else:

            self.setGeometry( self.WIN["CU"]["ML"], self.WIN["CU"]["MT"], self.WIN["CU"]["W"], self.WIN["CU"]["H"] );
            self.POP_UP_TIMER.singleShot( self.STEP_DELAY_MS, self._SHOW );

        # -------------------------------------------------------------------

    # =======================================================================
    def HIDE( self ):

        # -------------------------------------------------------------------
        try:

            #print("HIDE: _HIDE()");
            if not self.LOG_BODY.HAS_FOCUS:
                self.RUNNING = True;
                self._HIDE();

        except Exception as _err:
            # recursion
            #if self.DEBUG or self.PARENT.DEBUG_GLOBAL: self.PARENT.DEBUGGER.DEBUG();
            print( str(_err), "HIDE" );

        # -------------------------------------------------------------------

    # =======================================================================
    def _HIDE( self ):

        # -------------------------------------------------------------------
        AL = True;
        # -------------------------------------------------------------------
        if self.LOG_BODY.HAS_FOCUS:
            self._SHOW();
            return;


        # -------------------------------------------------------------------
        if self.WIN["CU"]["W"] > self.WIN["CL"]["W"] :

            self.WIN["CU"]["W"] -= self.STEP_W;
            AL = False;

        if self.WIN["CU"]["H"] > self.WIN["CL"]["H"]:

            self.WIN["CU"]["H"] -= self.STEP_H;
            AL = False;

        if self.WIN["CU"]["MT"] < self.WIN["CL"]["MT"]:

            self.WIN["CU"]["MT"] += self.STEP_H;
            AL = False;

        if AL:

            self.WIN["CU"]["W"] = self.WIN["CL"]["W"];
            self.WIN["CU"]["H"] = self.WIN["CL"]["H"];

            self.WIN["CU"]["ML"] = self.WIN["CL"]["ML"];
            self.WIN["CU"]["MT"] = self.WIN["CL"]["MT"];

            self.setGeometry( self.WIN["CU"]["ML"], self.WIN["CU"]["MT"], self.WIN["CU"]["W"], self.WIN["CU"]["H"] );
    
            self.IS_OPEN = False;
            self.RUNNING = False;
    
        else:

            self.setGeometry( self.WIN["CU"]["ML"], self.WIN["CU"]["MT"], self.WIN["CU"]["W"], self.WIN["CU"]["H"] );
            self.POP_UP_TIMER.singleShot( self.STEP_DELAY_MS, self._HIDE );

    # -------------------------------------------------------------------

    # =======================================================================
    def WRITE_LOG( self, _data, _TYPE=" I " ):

        # -------------------------------------------------------------------
        try:

            #log_d_time = str( strftime("%H:%M:%S", localtime( time() )) );
            log_d_time = datetime.now().strftime("%H:%M:%S.%f")

            with open( self.LOG_FILE, "a" ) as FS:
                FS.write( "[ "+log_d_time+" ] - ["+_TYPE+"] ::: "+_data+"\n" );
        
        except Exception as _err:
            # recursion
            #if self.DEBUG or self.PARENT.DEBUG_GLOBAL: self.PARENT.DEBUGGER.DEBUG();
            print( "LOG_HANDLER: [WRITE_LOG]: ["+str(_err)+"]");

        # -------------------------------------------------------------------

    # =======================================================================
    def INIT_LOG_FILE( self ):

        # -------------------------------------------------------------------
        try:

            try:
                self.PARENT.SPLASH.STATUS( self.LOG_TAG+": [LOAD]" );

                FS = open( self.LOG_FILE, "a" );

            except Exception as _err:
                FS = open( self.LOG_FILE, "w" );
                FS.write(  self.PARENT.GET_DATE_TIME()+"\n\n" );
                FS.close();
        
        except Exception as _err:
            # recursion
            #if self.DEBUG or self.PARENT.DEBUG_GLOBAL: self.PARENT.DEBUGGER.DEBUG();
            print( "LOG_HANDLER: [INIT_LOG_FILE]: ["+str(_err)+"]");

        # -------------------------------------------------------------------

###################################################################################################




