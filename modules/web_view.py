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
from PyQt4.QtCore import QByteArray, QUrl, Qt, QString, QPoint

from PyQt4.QtGui import QMessageBox, QTextEdit, QDialog, QAction, QLineEdit, QLabel, QIcon
from PyQt4.QtGui import QFrame, QListWidget, QListWidgetItem, QComboBox, QCheckBox, QPushButton, QProgressBar
from PyQt4.QtGui import QLCDNumber, QStyleOptionTabWidgetFrame, QFileDialog, QMenu

# -> http://pyqt.sourceforge.net/Docs/PyQt4/qtnetwork.html
from PyQt4.QtNetwork import QNetworkRequest, QNetworkAccessManager, QNetworkReply
from PyQt4.QtNetwork import QNetworkCookie, QNetworkCookieJar

#from PyQt4 import QtWebKit  
from PyQt4.QtWebKit import QWebView, QWebPage, QWebSettings, QWebHistory, QWebFrame
#from PyQt4.QtWebKit import QWebInspector


###################################################################################################
class Web_View( QWebView ):

    # =======================================================================
    def __init__(self, parent, parentMain, UID):

        # -------------------------------------------------------------------
        QWebView.__init__(self, parent);

        # -------------------------------------------------------------------
        self.PARENT                                 = parentMain;
        self.UID                                    = UID;
        self.PARENT_TAB                             = parent;
        self.DEBUG                                  = True;
        self.LOG_TAG                                = str(self.__class__.__name__).upper();

        self.ZOOM_FACTOR                            = 1.0;
        self.ZOOM_STEP                              = 0.05;
        self.CURRENT_PAGE_URL                       = "";

        # -------------------------------------------------------------------
        self.setStyleSheet( 'QWebView{ background-color: #fff;  padding: 0px; margin: 0px; }' );
        self.setGeometry( 0, 0, self.PARENT.WIDTH-4, 614-30);

        self.loadFinished.connect( self.ON_LOAD_FINISHED );
        self.urlChanged.connect( self.ON_URL_CHANGED ); 
        #self.showFullScreen();

        # -------------------------------------------------------------------
        self.URLS                                   = {
            "home"      : self.PARENT.BROWSER_DATA_PATH +"start-page.html",
            "search"    : "http://google.com/search?q=[SEARCH]&ie=utf-8&oe=utf-8&gws_rd=cr&ei=HOzOJeNIOJZOJ",
        }

        # -------------------------------------------------------------------
        # self.setContextMenuPolicy( Qt.DefaultContextMenu );
        # self.setContextMenuPolicy( Qt.CustomContextMenu );
        # self.customContextMenuRequested.connect( self.ON_CONTEXT_MENU );

        # -------------------------------------------------------------------
        self.ZOOM_IN_ACTION = QAction( self );
        self.ZOOM_IN_ACTION.setShortcut( "CTRL++" );
        self.ZOOM_IN_ACTION.triggered.connect( self.ZOOM_IN );
        self.addAction( self.ZOOM_IN_ACTION );

        self.ZOOM_OUT_ACTION = QAction( self );
        self.ZOOM_OUT_ACTION.setShortcut( "CTRL+-" );
        self.ZOOM_OUT_ACTION.triggered.connect( self.ZOOM_OUT );
        self.addAction( self.ZOOM_OUT_ACTION );

        # -------------------------------------------------------------------

    # =======================================================================
    def ZOOM_IN( self ):

        self.ZOOM_FACTOR += self.ZOOM_STEP;
        self.setZoomFactor( self.ZOOM_FACTOR );
        self.PARENT.WEB_PAGE.LOADING_BAR.setText( "ZOOM_FACTOR: ["+str(self.ZOOM_FACTOR*100)+"%]" )

    # =======================================================================
    def ZOOM_OUT( self ):

        self.ZOOM_FACTOR -= self.ZOOM_STEP;
        self.setZoomFactor( self.ZOOM_FACTOR );
        self.PARENT.WEB_PAGE.LOADING_BAR.setText( "ZOOM_FACTOR: ["+str(self.ZOOM_FACTOR*100)+"%]" )

    # =======================================================================
    def SET_RAW_CONTENT( self, _URL, _TYPE ):

        # -------------------------------------------------------------------
        print("SET_RAW_CONTENT: ['"+str(_URL)+"', '"+str(_TYPE)+"']" );
        """

        _CONTENT = QByteArray( open( _URL, "rb").read() );

        print("------------------------------------------------------------------------------------");
        print(_CONTENT)
        print("------------------------------------------------------------------------------------");


        self.setContent( _CONTENT, QString("plain/text"), QUrl(_URL) );
        #self.setHtml( _CONTENT  );
        """

        # -------------------------------------------------------------------

    # =======================================================================
    def ON_URL_CHANGED(self):

        # -------------------------------------------------------------------
        _URL = str(self.url().toString()).strip();

        if self.PARENT.CURRENT_TAB_BAR_UID == self.UID:

            if "/Doc-Browser/browser-data/start-page.html" in _URL:
                self.PARENT.URL_BAR.SET_TEXT( "__exec:home" );

            elif "file://" not in _URL:
                self.PARENT.URL_BAR.SET_TEXT( _URL );

            self.PARENT.HISTORY_HANDLER.hide();
        # -------------------------------------------------------------------

    # =======================================================================
    def RELOAD( self):

        # -------------------------------------------------------------------
        if self.PARENT.CURRENT_TAB_BAR_UID == self.UID:

            self.reload();
            self.PARENT.URL_BAR.SET_TEXT( self.PARENT.LAST_URL_ADDR );
            self.PARENT.GO_TO_URL();
            
        # -------------------------------------------------------------------

    # =======================================================================
    def LOAD( self, _url ):

        # -------------------------------------------------------------------
        try:
            self.load( _url );
            self.CURRENT_PAGE_URL = _url;

        except:
            try:
                self.load( QUrl( _url ) );
                self.CURRENT_PAGE_URL = QUrl( _url );
                
            except: 
                pass;

        # -------------------------------------------------------------------
        if self.PARENT.CURRENT_TAB_BAR_UID == self.UID:

            self.PARENT.URL_BAR.SET_TEXT( self.PARENT.LAST_URL_ADDR );

        # -------------------------------------------------------------------

    # =======================================================================
    def SET_PAGE( self, _QWebPage ):

        # -------------------------------------------------------------------
        self.setPage( _QWebPage );
        # -------------------------------------------------------------------

    # =======================================================================
    def SET_MAIN_PAGE(self):

        # -------------------------------------------------------------------
        #print("SET_MAIN_PAGE: True");
        self.LOAD(QUrl( self.URLS["home"]+"?t="+str(self.PARENT.GET_TIME()) ));
        #self.LOAD(QUrl( '/m-sys/prog-proj/ISS-Live/ISS-Live-anim.html') );
        #self.LOAD(QUrl( '/m-sys/prog/js/canvas/planets/Orbits.html') );

        #self.LOAD(QUrl( "/m-sys/prog/js/math/planetar/sin.cos.html" ) );
        #self.LOAD(QUrl( "/m-sys/prog/js/math/planetar/oscil.html" ) );
        #self.LOAD(QUrl( "/m-sys/prog/js/color-change-by-mouse-movement.html" ) );
        #self.LOAD(QUrl( "/m-sys/prog/js/slider-in-slider/slider-in-slider.html" ) );
        #self.LOAD(QUrl( "" ) );
        #self.LOAD(QUrl( "" ) );
        #self.LOAD(QUrl( "/m-sys/x/hosting/karumba.site88.net/public/js/cat/cat.html" ) );
        #self.LOAD(QUrl( "/m-sys/x/hosting/karumba.site88.net/public/js/cat/cat_2.html" ) );
        #self.LOAD(QUrl( "/m-sys/x/hosting/karumba.site88.net/public/js/cat/cat_3.html" ) );
        # -------------------------------------------------------------------

    # =======================================================================
    def ON_LOAD_FINISHED(self):

        # -------------------------------------------------------------------
        #if self.PARENT.CURRENT_TAB_BAR_UID == self.UID:
        #    pass;
        
        # -------------------------------------------------------------------
        try:

            """
            print("ON_LOAD_FINISHED: "+self.UID );
            """

            titleFULL = unicode( self.PARENT.WEB_VIEWS[ self.UID ]["WEB_PAGE"].GET_PAGE_TITLE() );
            title = titleFULL;

            if len( title ) > 10:
                title = title[0:10]+" ..";

            parentTabIndex = self.PARENT.TAB_BAR.indexOf( self.PARENT_TAB );
            self.PARENT.TAB_BAR.setTabText( parentTabIndex, title );
            self.PARENT.TAB_BAR.setTabToolTip( parentTabIndex, titleFULL );
    
        except Exception as _err:    
            self.LOCAL_ERROR_LOG( str(_err), "ON_LOAD_FINISHED" );
    
        # -------------------------------------------------------------------

    # =======================================================================
    def CMD( self, _CMD ):

        # -------------------------------------------------------------------

        # -------------------------------------------------------------------
        try:
    
            # -----------------------------------------------
            self.LOCAL_INFO_LOG( "NOT-IMPLEMENTED" );

            """
            if _CMD[0] == "exec":
                if _CMD[1] == "js":

                    self.PARENT.WEBP_AGE.EXEC_JS( _CMD[2] );
                    self.LOCAL_INFO_LOG( _CMD[2] );

            # -----------------------------------------------
            elif _CMD[0] == "cmd":
                pass;
                    
            """

            # -----------------------------------------------

        except Exception as _err:
            self.LOCAL_ERROR_LOG( str(_CMD)+": "+str(_err) );
    
        # -------------------------------------------------------------------

    # =======================================================================
    def focusInEvent (self, QFocusEvent):

        # -------------------------------------------------------------------
        #print("DocQWebView: focusInEvent: "+str(QFocusEvent.type()))

        pass;
        # -------------------------------------------------------------------

    # =======================================================================
    def focusOutEvent (self, QFocusEvent):

        # -------------------------------------------------------------------
        #print("DocQWebView: focusOutEvent: "+str(QFocusEvent.type()))

        pass;
        # -------------------------------------------------------------------

    # =======================================================================
    def resizeEvent (self, _evt ):

        # -------------------------------------------------------------------
        # *** print("resizeEvent");
        # *** print( "oldSize-H: "+str(_evt.oldSize().height()) );
        # *** print( "oldSize-W: "+str(_evt.oldSize().width()) );

        # *** print( "size-H: "+str(_evt.size().height()) );
        # *** print( "size-W: "+str(_evt.size().width()) );
        pass;
        # -------------------------------------------------------------------

    # =======================================================================
    """
    def mouseReleaseEvent ( self, _evt ):
        
        # -------------------------------------------------------------------
        self.PARENT.ESCAPE_FROM_ALL_LOCAL();
        print("mouseReleaseEvent: ")
        #return QWebView.event(self, _evt);
        # -------------------------------------------------------------------
    """

    # =======================================================================
    """
    def contextMenuEvent (self, _evt):

        # -------------------------------------------------------------------
        self.PARENT.WEB_VIEWS[ self.UID ]["WEB_PAGE"].SHOW_INSPECTOR()
        # -------------------------------------------------------------------
    
        self.popMenu = QMenu( self );
        self.popMenu.addAction( QAction('test0', self) );
        self.popMenu.addAction( QAction('test1', self) )
        self.popMenu.addSeparator()
        self.popMenu.addAction( QAction('test2', self) );
        self.popMenu.addAction( QAction('test2', self) );
        self.popMenu.addSeparator()
        self.popMenu.exec_( self.mapToGlobal( QPoint( _evt.x(), _evt.y() ) ) );


        QMenu* contextMenu = new QMenu ( this );
        contextMenu->addAction ( "New" , this , SLOT (newUnitBtnSlot()) );
        contextMenu->addAction ( "Clone" , this , SLOT (cloneUnitBtnSlot()) );
        contextMenu->popup( QCursor::pos() );
        contextMenu->exec ();



        return QWebView.contextMenuEvent( self, _evt );
        # -------------------------------------------------------------------
    """

    # =======================================================================
    def ON_CONTEXT_MENU(self, point):

        # -------------------------------------------------------------------
        self.popMenu = QMenu( self );
        self.popMenu.addAction( QAction('test0', self) );
        self.popMenu.addAction( QAction('test1', self) )
        self.popMenu.addSeparator()
        self.popMenu.addAction( QAction('test2', self) );
        self.popMenu.addAction( QAction('test2', self) );
        self.popMenu.addSeparator()

        self.popMenu.exec_( self.mapToGlobal( point ) );

        # -------------------------------------------------------------------

    # =======================================================================
    """
    def mouseDoubleClickEvent ( self, _evt ):
        print("mouseDoubleClickEvent: ")

    def mouseMoveEvent ( self, _evt ):
        print("mouseMoveEvent: ")

    def mousePressEvent ( self, _evt ):
        print("mousePressEvent: ")
    """

    """
    changeEvent (self, QEvent)
    wheelEvent (self, QWheelEvent)
    focusInEvent (self, QFocusEvent)
    focusOutEvent (self, QFocusEvent)
    """

    """
    keyPressEvent (self, QKeyEvent)
    keyReleaseEvent (self, QKeyEvent)
    """

    """
    inputMethodEvent (self, QInputMethodEvent)
    """

    """
    dragEnterEvent (self, QDragEnterEvent)
    dragLeaveEvent (self, QDragLeaveEvent)
    dragMoveEvent (self, QDragMoveEvent)
    dropEvent (self, QDropEvent)
    """
    # =======================================================================
    """
    def event(self, event):

        # -------------------------------------------------------------------
        #print("event.type(): "+str(event.type()) );
        # -------------------------------------------------------------------
        try:
            if event.type() == QEvent.KeyPress:
                if event.key() == 0x01000015:

                    self.clearFocus();
                    self.emit( self.FOCUS_ON_HISTORY_LIST, "DATA" );
                    print("Qt.Key_Down");
                    return True;

            return QWebView.event(self, event)

        except Exception as _err:
            self.LOCAL_ERROR_LOG( "0|WEB_VIEW: ['']: ['"+str(_err)+"'']" );
            return QWebView.event(self, event)

        # -------------------------------------------------------------------

    """

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
        if self.DEBUG: self.PARENT.DEBUGGER.DEBUG();
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
