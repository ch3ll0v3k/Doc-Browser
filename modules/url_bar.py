#!/usr/bin/python
# -*- coding: utf-8 -*-
###################################################################################################
# Built IN
import json, time, os, math

#--------------------------------------------------------------------------------------------------
# -> 'ascii' codec can't encode characters in position 220-223: ordinal not in range(128)
import sys
reload(sys);
sys.setdefaultencoding('utf-8');

#--------------------------------------------------------------------------------------------------
# OyQt
from PyQt4.QtCore import QTimer, QThread, QEvent, SIGNAL, SLOT, pyqtSignal, pyqtSlot
from PyQt4.QtCore import QByteArray, QUrl, Qt, QString

from PyQt4.QtGui import QMessageBox, QTextEdit, QDialog, QAction, QLineEdit, QLabel, QIcon
from PyQt4.QtGui import QFrame, QListWidget, QListWidgetItem, QComboBox, QCheckBox, QPushButton, QProgressBar
from PyQt4.QtGui import QLCDNumber, QStyleOptionTabWidgetFrame, QFileDialog

# -> http://pyqt.sourceforge.net/Docs/PyQt4/qtnetwork.html
from PyQt4.QtNetwork import QNetworkRequest, QNetworkAccessManager, QNetworkReply
from PyQt4.QtNetwork import QNetworkCookie, QNetworkCookieJar


###################################################################################################
class Url_Bar( QLineEdit ):

    # =======================================================================
    def __init__(self, parent=None):

        # -------------------------------------------------------------------
        QLineEdit.__init__(self, parent);

        # -------------------------------------------------------------------
        self.PARENT                                 = parent;
        self.DEBUG                                  = False;
        self.LOG_TAG                                = str(self.__class__.__name__).upper();

        # -------------------------------------------------------------------
        self.setPlaceholderText ("https://www.exploit-db.com/");
        self.setGeometry(155, 0, 865, 30);
        self.setPlaceholderText("about:home");
        self.setStyleSheet("QLineEdit{ background-color: #222; color: #fff; padding-left: 10px; border-style: none; }");

        # -------------------------------------------------------------------
        self.HAS_FOCUS                              = False;
        # events
        #self.returnPressed.connect (self.GO_TO_URL );
        #self.textChanged.connect( self.SEARCH_IN_HISTIRY );

        # -------------------------------------------------------------------
        self.PARENT.SPLASH.STATUS( self.LOG_TAG+": [INIT]" );
        # -------------------------------------------------------------------

    # =======================================================================
    """
    def keyPressEvent(self, _evt):

        # -------------------------------------------------------------------
        # ALL KEYS Available @
        # http://pyqt.sourceforge.net/Docs/PyQt4/qt.html#Key-enum
        # http://pyqt.sourceforge.net/Docs/PyQt4/qevent.html#Type-enum
        # -------------------------------------------------------------------
        '''
        int count (self)
        bool isAutoRepeat (self)
        int key (self)
        bool matches (self, QKeySequence.StandardKey key)
        Qt.KeyboardModifiers modifiers (self)
        int nativeModifiers (self)
        int nativeScanCode (self)
        int nativeVirtualKey (self)
        QString text (self)
        '''

        #self.emit( self.KEY_PRESSED_SIGNAL, "["+str(_evt.key())+", "+str(_evt.isAutoRepeat())+", "+str(_evt.count())+", "+str(_evt.nativeScanCode())+", "+str(_evt.text())+", ]" );

        '''
        Qt.Key_Left 0x01000012   
        Qt.Key_Up   0x01000013   
        Qt.Key_Right    0x01000014   
        Qt.Key_Down 0x01000015   
        Qt.Key_PageUp   0x01000016   
        '''

        return QLineEdit.keyPressEvent( self, _evt );

        # -------------------------------------------------------------------
    """
    # =======================================================================
    def ON_FOCUS_ON_HISTORY_LIST(self):

        # -------------------------------------------------------------------
        if self.PARENT.HISTORY_HANDLER.FOUND_ITEMS > 0:

            self.HAS_FOCUS = False;
            self.PARENT.HISTORY_HANDLER.setFocus();

        # -------------------------------------------------------------------

    # =======================================================================
    # HOT-KEYS
    def ON_FOCUS(self):

        # -------------------------------------------------------------------
        self.PARENT.HISTORY_HANDLER.HAS_FOCUS  = False;
        self.HAS_FOCUS                      = True;

        self.PARENT.HISTORY_HANDLER.clearFocus( );

        self.clearFocus( ); # otherwise True parameter will not work
        self.setFocus( True ); # True [ select available text inside]

    # =======================================================================
    def event(self, event):

        # -------------------------------------------------------------------
        #print("event.type(): "+str(event.type()) );
        # -------------------------------------------------------------------
        if event.type() == QEvent.KeyPress:
            if event.key() == 0x01000015:

                self.clearFocus();
                self.ON_FOCUS_ON_HISTORY_LIST();
                #print("Qt.Key_Down");
                #print("FOCUS_ON_HISTORY_LIST");
                return True;

        return QLineEdit.event(self, event)
        # -------------------------------------------------------------------

    # =======================================================================
    """
    def mouseReleaseEvent(self, _evt):
        
        # -------------------------------------------------------------------
        print("mouseReleaseEvent");

        self.emit( self.FOCUS_ON_HISTORY_LIST, "DATA" );
        return True;
        # -------------------------------------------------------------------

    # =======================================================================
    def focusInEvent (self,  _evt):

        # -------------------------------------------------------------------
        print("focus_IN_Event");
        
        #return QLineEdit.event(self, _evt)
        # -------------------------------------------------------------------

    # =======================================================================
    def focusOutEvent (self, _evt):

        # -------------------------------------------------------------------
        print("focus_OUT_Event");
        #return QLineEdit.event(self, _evt)
        # -------------------------------------------------------------------
    """
    # =======================================================================
    def SET_TEXT( self, _url ):

        # -------------------------------------------------------------------
        try:
            #print("self.URL_BAR.SET_TEXT: ["+str(_url)+"]")
            self.setText( unicode(_url) );

        except Exception as _err:
            self.LOCAL_ERROR_LOG( str(_err) );

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
