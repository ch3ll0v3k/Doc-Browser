#!/usr/bin/python
# -*- coding: utf-8 -*-
###################################################################################################
# Built IN
import json, time, os, math, subprocess
import httplib, urllib, urllib2, hashlib, hmac
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
class NoteBook( QFrame ):

    # =======================================================================
    def __init__(self, parent=None):

        # -------------------------------------------------------------------
        QFrame.__init__(self, parent);

        # -------------------------------------------------------------------
        self.PARENT                                 = parent;
        self.DEBUG                                  = False;
        self.LOG_TAG                                = str(self.__class__.__name__).upper();

        self.setGeometry( 4, 34, 1012, 606 );
        self.setStyleSheet( "QFrame{ font: 12px 'monospace'; color: #fff; background-color: rbga(0,0,0, 190); border-style: solid; border-width: 5px; border-color: #FFF; }" );

        # -------------------------------------------------------------------
        self.NOTEBOOK_FILE                          = self.PARENT.STORAGE_ROOT+"notebook.file";
        # -------------------------------------------------------------------
        self.TEXT                                   = QTextEdit( "TEST: TEST", self );
        self.TEXT.setGeometry(5, 35, 980, 560);
        self.TEXT.setStyleSheet("QTextEdit{ font: 12px 'monospace'; color: #fff; margin: 5px; padding: 5px; border-style: solid; border-width: 1px; border-color: #FFF; }")
        self.TEXT.setReadOnly( False );
        self.TEXT.setAcceptRichText( False );
        self.TEXT.setUndoRedoEnabled( True );
        self.TEXT.LineWrapMode( self.TEXT.WidgetWidth );

        self.TEXT.textChanged.connect( self.TEXT_CHANGED );


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
    def TEXT_CHANGED( self ):

        # -------------------------------------------------------------------
        pass;
        #self.TEXT.setText( str(self.TEXT.toPlainText() );
        #self.TEXT.setText( str(self.TEXT.text() ) );
        # -------------------------------------------------------------------

    # =======================================================================
    def CMD( self, _CMD ):

        # -------------------------------------------------------------------
        #__exec:notebook:notes:show"
        #__exec:notebook:notes:hide"
        #__exec:notebook:notes:keep_open:(0|1)

        # -------------------------------------------------------------------
        try:
    
            # -----------------------------------------------
            if _CMD[0] == "notes":

                if _CMD[1] == "show":
                    self.SHOW_NOTES( );

                elif _CMD[1] == "hide":
                    self.HIDE_NOTES( );

                elif _CMD[1] == "keep_open":

                    self.KEEP_OPEN = True if _CMD[2] == "1" else False;
                    self.LOCAL_INFO_LOG( "notebook:notes:keep_open:"+_CMD[2] );


                return;
            # -----------------------------------------------
            if _CMD[0] == "cmd":
                pass;
                    
            # -----------------------------------------------

        except Exception as _err:
            self.LOCAL_ERROR_LOG( str(_CMD)+" | "+str(_err) );
    
        # -------------------------------------------------------------------


    # =======================================================================
    def SHOW_NOTES( self ):

        # -------------------------------------------------------------------
        try:
            """
            out = "";
            for _key in self.LAST_PAGE_REQUEST_HEADERS:
                _l = "-----------------------------------------------------------------------\n";
                _l += '["'+_key+'"] => \n["'+self.LAST_PAGE_REQUEST_HEADERS[ _key ]+'"]'+"\n";
                print( "L: "+_l );
                out += _l;

            self.TEXT.setText( out );
            """
            self.show();
            self.IS_OPEN = True;
            self.TEXT.setFocus( True );

        except Exception as _err:
            self.LOCAL_ERROR_LOG( "'Can't show notes: "+str(_err) );


        # -------------------------------------------------------------------

    # =======================================================================
    def HIDE_NOTES( self ):

        # -------------------------------------------------------------------
        self.hide();

        self.IS_OPEN = False;
        self.TEXT.clearFocus();
        # -------------------------------------------------------------------

    # =======================================================================
    def UPDATE_FRAME(self):

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

            # ---------------------------------------------------
            self.PARENT.SPLASH.STATUS( self.LOG_TAG+": [LOAD]" );
            self.PARENT.LOG_HANDLER.WRITE_LOG( "Doc-Browser: NOTEBOOK: LODE: ");

            self.TEXT.clear();

            with open( self.NOTEBOOK_FILE, "r") as FS:

                for line in FS:
                    self.TEXT.append(line.strip());
                    #self.TEXT.insertPlainText(line);
                    #self.TEXT.insertHtml(line);

            self.PARENT.LOG_HANDLER.WRITE_LOG( "Doc-Browser: NOTEBOOK: LODE: Done");
            # ---------------------------------------------------

        except Exception as _err:
            self.LOCAL_ERROR_LOG( "Can't load notes: "+str(_err) );
        # -------------------------------------------------------------------

    # =======================================================================
    def SAVE(self):

        # -------------------------------------------------------------------
        if self.DEBUG:
            pass;

        # -------------------------------------------------------------------
        try:

            # ---------------------------------------------------
            self.PARENT.LOG_HANDLER.WRITE_LOG( "Doc-Browser: NOTEBOOK: SAVE: ");

            DATA = str(self.TEXT.toPlainText()).split("\n");

            with open( self.NOTEBOOK_FILE, "w") as FS:

                for line in DATA:
                    FS.write( line+"\n" );

            self.PARENT.LOG_HANDLER.WRITE_LOG( "Doc-Browser: NOTEBOOK: SAVE: Done");
            # ---------------------------------------------------

        except Exception as _err:
            self.LOCAL_ERROR_LOG( "Can't save notes: "+str(_err) );

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

