#!/usr/bin/python
# -*- coding: utf-8 -*-
###################################################################################################
# Built IN
import json, time, os, math, subprocess
import httplib, urllib, urllib2, hashlib, hmac
from random import randint
from threading import Timer
from sys import stdout
from time import sleep, time
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
from PyQt4.QtCore import QTimer, QThread, QEvent, SIGNAL, SLOT, pyqtSignal, pyqtSlot
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
class Settings(QFrame):

    # =======================================================================
    def __init__(self, parent=None):

        # -------------------------------------------------------------------
        QFrame.__init__(self, parent);

        # -------------------------------------------------------------------
        self.PARENT                                 = parent;
        self.DEBUG                                  = False;
        self.LOG_TAG                                = str(self.__class__.__name__).upper();

        self.setGeometry( 4, 34, 1012, 606 );
        self.setStyleSheet( "QFrame{ font: 12px 'monospace'; color: #fff; background-color: rbga(0,0,0, 220); border-style: solid; border-width: 5px; border-color: #FFF; }" );

        # -------------------------------------------------------------------
        self.WIDGET_NAME_LABEL                      = QLabel( "Settings: ", self );
        self.WIDGET_NAME_LABEL.setStyleSheet( "QLabel{ background-color: none; border-style: none; width: 96px; padding: 10px; } " );

        # -------------------------------------------------------------------
        self.hide();

        self.IS_OPEN                                = False;
        self.KEEP_OPEN                              = False;

        # -------------------------------------------------------------------
        self.UPDATE_TIMER                           = QTimer();
        self.UPDATE_TIMER.singleShot( 1000, self.UPDATE_FRAME );

        # -------------------------------------------------------------------

        self.PARENT.SPLASH.STATUS( self.LOG_TAG+": [INIT]" );
        # -------------------------------------------------------------------

    # =======================================================================
    def CMD( self, _CMD ):

        # -------------------------------------------------------------------
        #__exec:settings:window:show"
        #__exec:settings:window:hide"
        #__exec:settings:window:keep_open:(0|1)
        # -------------------------------------------------------------------
        if self.DEBUG:
            print(self.LOG_TAG+": CMD: "+_CMD);

        # -------------------------------------------------------------------
        try:
    
            # -----------------------------------------------
            if _CMD[0] == "window":

                if _CMD[1] == "show":
                    self.SHOW_WINDOW( );

                elif _CMD[1] == "hide":
                    self.HIDE_WINDOW( );

                elif _CMD[1] == "keep_open":

                    self.KEEP_OPEN = True if _CMD[2] == "1" else False;
                    self.LOCAL_INFO_LOG( "settings:window:keep_open:"+_CMD[2] );

                return;
            # -----------------------------------------------
            if _CMD[0] == "cmd":
                pass;
                    
            # -----------------------------------------------

        except Exception as _err:
            self.LOCAL_ERROR_LOG( str(_err), "CMD");
    
        # -------------------------------------------------------------------

    # =======================================================================
    def SHOW_WINDOW( self ):

        # -------------------------------------------------------------------
        if self.DEBUG:
            print(self.LOG_TAG+": SHOW_WINDOW");

        # -------------------------------------------------------------------
        try:

            """
            out = "";
            for _key in self.LAST_PAGE_REQUEST_HEADERS:
                _l = "-----------------------------------------------------------------------\n"
                _l += '["'+_key+'"] => \n["'+self.LAST_PAGE_REQUEST_HEADERS[ _key ]+'"]'+"\n"
                print( "L: "+_l );
                out += _l;

            self.HEADERS_RAW.setText( out );
            """
            self.show();
            self.IS_OPEN = True;

        except Exception as _err:
            self.LOCAL_ERROR_LOG( "Can't show settings: "+str(_err) );
        # -------------------------------------------------------------------

    # =======================================================================
    def HIDE_WINDOW( self ):

        # -------------------------------------------------------------------
        if self.DEBUG:
            print("HIDE_WINDOW");

        # -------------------------------------------------------------------
        self.hide();

        self.IS_OPEN = False;
        # -------------------------------------------------------------------

    # =======================================================================
    def UPDATE_FRAME(self):

        # -------------------------------------------------------------------
        if self.DEBUG:
            print("UPDATE_FRAME");

        # -------------------------------------------------------------------

        return;
        # -------------------------------------------------------------------
        """
        try:
            _style = "";
            _conf  = [];

            with open( "./ALPHA_FRAME.conf" ) as FS:
                _conf = FS.readline();
                print(_conf );
                _conf = _conf.split("|");

                self.setGeometry( 
                    int(_conf[0]), 
                    int(_conf[1]), 
                    int(_conf[2]), 
                    int(_conf[3])
                );


                for _line in FS:
                    _style += _line;

            self.setStyleSheet( _style );

        except Exception as _err:
            print("ERROR: "+str(_err));
            
        self.UPDATE_TIMER.singleShot( 1000, self.UPDATE_FRAME );
        """
        # -------------------------------------------------------------------

    # =======================================================================
    def LOAD(self):

        # -------------------------------------------------------------------
        if self.DEBUG:
            pass;
        # -------------------------------------------------------------------
        try:

            self.PARENT.SPLASH.STATUS( self.LOG_TAG+": [LOAD]" );
            self.PARENT.LOG_HANDLER.WRITE_LOG( "Doc-Browser: SETTINGS: LOAD: ");

            self.PARENT.LOG_HANDLER.WRITE_LOG( "Doc-Browser: SETTINGS: LOAD: Done");

        except Exception as _err:
            self.LOCAL_ERROR_LOG( "Can't load settings: "+str(_err) );

        # -------------------------------------------------------------------

    # =======================================================================
    def SAVE(self):

        # -------------------------------------------------------------------
        if self.DEBUG:
            pass;

        # -------------------------------------------------------------------
        try:

            self.PARENT.LOG_HANDLER.WRITE_LOG( "Doc-Browser: SETTINGS: SAVE: ");

            self.PARENT.LOG_HANDLER.WRITE_LOG( "Doc-Browser: SETTINGS: SAVE: Done");

        except Exception as _err:
            self.LOCAL_ERROR_LOG( "Can't save settings: "+str(_err) );

        # -------------------------------------------------------------------

    # =======================================================================
    def LOCAL_INFO_LOG( self, _msg, METHOD=None ):

        # -------------------------------------------------------------------
        if METHOD is None:
            self.PARENT.LOCAL_INFO_LOG( "['"+self.LOG_TAG+"']: ["+_msg+"]" );
        else:
            self.PARENT.LOCAL_INFO_LOG( "['"+self.LOG_TAG+"."+METHOD+"']: ["+_msg+"]" );
        # -------------------------------------------------------------------

    # =======================================================================
    def LOCAL_ERROR_LOG( self, _msg, METHOD=None ):

        # -------------------------------------------------------------------
        if self.DEBUG or self.PARENT.DEBUG_GLOBAL: self.PARENT.DEBUGGER.DEBUG();
        # -------------------------------------------------------------------
        if METHOD is None:
            self.PARENT.LOCAL_ERROR_LOG( "['"+self.LOG_TAG+"']: ["+_msg+"]" );
        else:
            self.PARENT.LOCAL_ERROR_LOG( "['"+self.LOG_TAG+"."+METHOD+"']: ["+_msg+"]" );
        # -------------------------------------------------------------------

    # =======================================================================
    def LOCAL_WARNING_LOG( self, _msg, METHOD=None ):

        # -------------------------------------------------------------------
        if METHOD is None:
            self.PARENT.LOCAL_WARNING_LOG( "['"+self.LOG_TAG+"']: ["+_msg+"]" );
        else:
            self.PARENT.LOCAL_WARNING_LOG( "['"+self.LOG_TAG+"."+METHOD+"']: ["+_msg+"]" );
        # -------------------------------------------------------------------

    # =======================================================================


###################################################################################################

