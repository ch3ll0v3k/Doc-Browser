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

#from PyQt4 import QtWebKit  
#from PyQt4.QtWebKit import QWebView, QWebPage, QWebSettings, QWebHistory

# -> http://pyqt.sourceforge.net/Docs/PyQt4/qtnetwork.html
from PyQt4 import Qt
from PyQt4.QtNetwork import QNetworkReply, QNetworkRequest
#from PyQt4.QtNetwork import QNetworkRequest, QNetworkAccessManager, QNetworkCookie, QNetworkCookieJar

from PyQt4.QtGui import QFrame, QListWidget,QListWidgetItem, QComboBox, QCheckBox, QPushButton
from PyQt4.QtGui import QProgressBar, QLineEdit, QLabel, QTextEdit

###################################################################################################
"""
class DocRequestHandler( QNetworkRequest ):

QNetworkRequest request = new QNetworkRequest();
request->setRawHeader(
    QString("User-Agent").toAscii(),
    QString("Your User Agent").toAscii()
    );
// ... set the URL, etc.
yourWebView->load(request);


"""


class Request_Handler( QNetworkReply ):

    # =======================================================================
    def __init__(self, parent=None):

        # -------------------------------------------------------------------
        # http://pyqt.sourceforge.net/Docs/PyQt4/qnetworkreply.html
        QNetworkReply.__init__( self, parent );
        # -------------------------------------------------------------------
        self.PARENT                                 = parent;
        self.DEBUG                                  = False;
        self.LOG_TAG                                = str(self.__class__.__name__).upper();
        
        # -------------------------------------------------------------------
        self.HEADERS_FRAME                          = QFrame( self.PARENT );
        self.HEADERS_FRAME.setGeometry( 10, 50, 980, 520 );
        self.HEADERS_FRAME.setStyleSheet( "QFrame{ font: 12px 'monospace'; color: #000; background-color: rbga(0,0,0, 170); border-style: solid; border-width: 5px; border-color: #FFF; }" );
        self.HEADERS_FRAME.hide();

        # -------------------------------------------------------------------
        self.HEADERS_RAW                            = QTextEdit("TEST: TEST", self.HEADERS_FRAME);
        self.HEADERS_RAW.setGeometry(5, 5, 970, 510);
        self.HEADERS_RAW.setStyleSheet("QTextEdit{  color: #fff; margin: 5px; padding: 5px; border-style: dashed; border-width: 1px; border-color: #FFF; }")
        self.HEADERS_RAW.setReadOnly(True);
        #self.HEADERS_RAW.setOpenExternalLinks(True);
        #self.HEADERS_RAW.show();

        # -------------------------------------------------------------------
        self.downloadProgress.connect( self._DOWN );
        self.uploadProgress.connect( self._UP );

        self.error.connect( self._ERROR);
        self.finished.connect( self._FINISH );
        self.metaDataChanged.connect( self._META_DATA_CHANGED );
        self.sslErrors.connect( self._SSL_ERROR );

        # -------------------------------------------------------------------
        self.SHOW_NOT_REQUESTED_HEADERS             = False; 
        self.LAST_PAGE_REQUEST_HEADERS              = {};
        self.LAST_PAGE_REQUEST_FILES                = [];


        # -------------------------------------------------------------------
        self.IS_OPEN                                = False;
        self.KEEP_OPEN                              = False;

        # -------------------------------------------------------------------
        self.PARENT.SPLASH.STATUS( self.LOG_TAG+": [INIT]" );

        # -------------------------------------------------------------------

    # =======================================================================
    def CMD( self, _CMD ):

        # -------------------------------------------------------------------
        #__exec:request_handler:headers:show
        #__exec:request_handler:headers:hide
        #__exec:request_handler:headers:keep_open:(0|1)
        # -------------------------------------------------------------------
        if self.DEBUG:
            print( )
        # -------------------------------------------------------------------
        try:
    
            # -----------------------------------------------
            if _CMD[0] == "headers":

                if _CMD[1] == "show":
                    self.SHOW_HEADERS( );

                elif _CMD[1] == "hide":
                    self.HIDE_HEADERS( );

                elif _CMD[1] == "keep_open":
                    self.KEEP_OPEN = True if _CMD[2] == "1" else False;
                    self.LOCAL_INFO_LOG( "request_handler:headers:keep_open:"+_CMD[2] );

                return;
            # -----------------------------------------------
            if _CMD[0] == "cmd":
                pass;
                    
            # -----------------------------------------------

        except Exception as _err:
            self.LOCAL_ERROR_LOG( str(_CMD)+" | "+str(_err) );
    
        # -------------------------------------------------------------------

    # =======================================================================
    def SHOW_HEADERS( self ):

        # -------------------------------------------------------------------
        try:

            out = '["'+self.PARENT.LAST_URL_ADDR+']"\n';

            for _key in self.LAST_PAGE_REQUEST_HEADERS:
                _l = "-----------------------------------------------------------------------\n"
                _l += '["'+_key+'"] => \n["'+self.LAST_PAGE_REQUEST_HEADERS[ _key ]+'"]'+"\n"
                #print( "L: "+_l );
                out += _l;

            self.HEADERS_RAW.setText( out );
            self.HEADERS_FRAME.show();

            self.IS_OPEN = True;


        except Exception as _err:
            self.LOCAL_ERROR_LOG( "'Can't show header: "+str(_err) );

        # -------------------------------------------------------------------

    # =======================================================================
    def HIDE_HEADERS( self ):

        # -------------------------------------------------------------------
        self.HEADERS_FRAME.hide();
        self.IS_OPEN = False;

        # -------------------------------------------------------------------

    # =======================================================================
    def REQUEST_FINISHED( self, _netReplay ):

        # -------------------------------------------------------------------
        # _raw_header_list.size();    # -> size in bytes && array.data()[ size() ]; // returns '\0'
        # _raw_header_list.length();  # -> same as size()
        # _raw_header_list.count();   # -> Returns the number of (potentially overlapping) occurrences of string str in the byte array.
        # _raw_header_list.mid(5, 20);# -> get mid piece
        # _raw_header_list.data()[0]; # -> char At 0
        # _raw_header_list.data();    # -> string
        """
        QByteArray x("Five pineapples");
        QByteArray y = x.mid(5, 4);     // y == "pine"
        QByteArray z = x.mid(5);        // z == "pineapples"
        """
        # -------------------------------------------------------------------
        #del self.LAST_PAGE_REQUEST_HEADERS;
        #self.LAST_PAGE_REQUEST_HEADERS = {};

        #del self.LAST_PAGE_REQUEST_FILES;
        #self.LAST_PAGE_REQUEST_FILES = [];

        # -------------------------------------------------------------------
        _req_url = str( _netReplay.url().toString() );
        #print('["'+_req_url+'"]')

        # -------------------------------------------------------------------
        try:
            
            # ---------------------------------------------------------------
            if not self.SHOW_NOT_REQUESTED_HEADERS:

                if _req_url == self.PARENT.LAST_URL_ADDR:

                    if self.IS_OPEN:

                        _raw_header_list = _netReplay.rawHeaderList();

                        del self.LAST_PAGE_REQUEST_HEADERS;
                        self.LAST_PAGE_REQUEST_HEADERS = {};
                        
                        for _header in _raw_header_list:
                            self.LAST_PAGE_REQUEST_HEADERS[ str(_header) ] = str(_netReplay.rawHeader( _header ) );
                            #print( 'HEAD: ["'+_header+'"] : ["'+_netReplay.rawHeader( _header ) +'"]' );

                        self.SHOW_HEADERS();


            # ---------------------------------------------------------------
            else:

                print("-----------------------------------------------------------");
                print('REQ_URL: ["'+_req_url+'"] : [FETCHING]');
                _raw_header_list = _netReplay.rawHeaderList();

                del self.LAST_PAGE_REQUEST_HEADERS;
                self.LAST_PAGE_REQUEST_HEADERS = {};

                for _header in _raw_header_list:
                    print( 'HEAD: ["'+_header+'"] : ["'+_netReplay.rawHeader( _header ) +'"]' );
                    self.LAST_PAGE_REQUEST_HEADERS[ str(_header) ] = str(_netReplay.rawHeader( _header ) );

            # ---------------------------------------------------------------

        except Exception as _err:
            self.LOCAL_ERROR_LOG( str(_err) );


        # -------------------------------------------------------------------
        if int(_netReplay.error()) == 1:
            _msg = "ERR_NUM: ["+str(_netReplay.error())+", "+str( _netReplay.errorString() )+"]";
            print( "["+self.PARENT.GET_DATE_TIME()+"]:["+_msg+"]" );

        elif int(_netReplay.error()) == 3:
            self.LOCAL_WARNING_LOG( str(_netReplay.errorString()) );

        return;

        # -------------------------------------------------------------------
        if _netReplay.error() == QNetworkReply.NoError: # .error() == 0
            # Note: When the HTTP protocol returns a redirect no error will be reported. You can check if there is a redirect with the QNetworkRequest.RedirectionTargetAttribute attribute.
            #print("NoError: # .error() == 0");
            pass;

        elif _netReplay.error() == QNetworkReply.ConnectionRefusedError: # .error() == 1
            #the remote server refused the connection (the server is not accepting requests)
            print("ConnectionRefusedError: # .error() == 1");

        elif _netReplay.error() == QNetworkReply.ConnectionRefusedError: # .error() == 2
            # the remote server closed the connection prematurely, before the entire reply was received and processed
            print("ConnectionRefusedError: # .error() == 2");

        elif _netReplay.error() == QNetworkReply.ConnectionRefusedError: # .error() ==  3
            # the remote host name was not found (invalid hostname)
            print("ConnectionRefusedError: # .error() ==  3");

        elif _netReplay.error() == QNetworkReply.ConnectionRefusedError: # .error() == 4
            # the connection to the remote server timed out
            print("ConnectionRefusedError: # .error() == 4");

        elif _netReplay.error() == QNetworkReply.ConnectionRefusedError: # .error() == 5
            # the operation was canceled via calls to abort() or close() before it was finished.
            print("ConnectionRefusedError: # .error() == 5");

        elif _netReplay.error() == QNetworkReply.ConnectionRefusedError: # .error() == 6
            # the SSL/TLS handshake failed and the encrypted channel could not be established. The sslErrors() signal should have been emitted.
            print("ConnectionRefusedError: # .error() == 6");

        elif _netReplay.error() == QNetworkReply.ConnectionRefusedError: # .error() == 7
            # the connection was broken due to disconnection from the network, however the system has initiated roaming to another access point. The request should be resubmitted and will be processed as soon as the connection is re-established.
            print("ConnectionRefusedError: # .error() == 7");

        elif _netReplay.error() == QNetworkReply.ConnectionRefusedError: # .error() == 101
            # the connection to the proxy server was refused (the proxy server is not accepting requests)
            print("ConnectionRefusedError: # .error() == 101");

        elif _netReplay.error() == QNetworkReply.ConnectionRefusedError: # .error() == 102
            # the proxy server closed the connection prematurely, before the entire reply was received and processed
            print("ConnectionRefusedError: # .error() == 102");

        elif _netReplay.error() == QNetworkReply.ConnectionRefusedError: # .error() == 103
            # the proxy host name was not found (invalid proxy hostname)
            print("ConnectionRefusedError: # .error() == 103");

        elif _netReplay.error() == QNetworkReply.ConnectionRefusedError: # .error() == 104
            # connection to the proxy timed out or the proxy did not reply in time to the request sent
            print("ConnectionRefusedError: # .error() == 104");

        elif _netReplay.error() == QNetworkReply.ConnectionRefusedError: # .error() == 105
            # the proxy requires authentication in order to honour the request but did not accept any credentials offered (if any)
            print("ConnectionRefusedError: # .error() == 105");

        elif _netReplay.error() == QNetworkReply.ConnectionRefusedError: # .error() == 201
            # the access to the remote content was denied (similar to HTTP error 401)
            print("ConnectionRefusedError: # .error() == 201");

        elif _netReplay.error() == QNetworkReply.ConnectionRefusedError: # .error() == 202
            # the operation requested on the remote content is not permitted
            print("ConnectionRefusedError: # .error() == 202");

        elif _netReplay.error() == QNetworkReply.ConnectionRefusedError: # .error() == 203
            # the remote content was not found at the server (similar to HTTP error 404)
            print("ConnectionRefusedError: # .error() == 203");

        elif _netReplay.error() == QNetworkReply.ConnectionRefusedError: # .error() == 204
            # the remote server requires authentication to serve the content but the credentials provided were not accepted (if any)
            print("ConnectionRefusedError: # .error() == 204");

        elif _netReplay.error() == QNetworkReply.ConnectionRefusedError: # .error() == 205
            # the request needed to be sent again, but this failed for example because the upload data could not be read a second time.
            print("ConnectionRefusedError: # .error() == 205");

        elif _netReplay.error() == QNetworkReply.ConnectionRefusedError: # .error() == 301
            # the Network Access API cannot honor the request because the protocol is not known
            print("ConnectionRefusedError: # .error() == 301");

        elif _netReplay.error() == QNetworkReply.ConnectionRefusedError: # .error() == 302
            # the requested operation is invalid for this protocol
            print("ConnectionRefusedError: # .error() == 302");

        elif _netReplay.error() == QNetworkReply.ConnectionRefusedError: # .error() == 99
            # an unknown network-related error was detected
            print("ConnectionRefusedError: # .error() == 99");

        elif _netReplay.error() == QNetworkReply.ConnectionRefusedError: # .error() == 199
            # an unknown proxy-related error was detected
            print("ConnectionRefusedError: # .error() == 199");

        elif _netReplay.error() == QNetworkReply.ConnectionRefusedError: # .error() == 299
            # an unknown error related to the remote content was detected
            print("ConnectionRefusedError: # .error() == 299");

        elif _netReplay.error() == QNetworkReply.ConnectionRefusedError: # .error() == 399
            # 399 a breakdown in protocol was detected (parsing error, invalid or unexpected responses, etc.)
            print("ConnectionRefusedError: # .error() == 399");

        # -------------------------------------------------------------------
        _msg = None;

        if _netReplay.error() == 0:
            #print("ERR_NUM: ["+str(_netReplay.error())+", "+str( _netReplay.errorString() )+"]");
            pass;

        elif _netReplay.error() == 1:
            _msg = "ERR_NUM: ["+str(_netReplay.error())+", "+str( _netReplay.errorString() )+"]";

        elif _netReplay.error() == 2:
            _msg = "ERR_NUM: ["+str(_netReplay.error())+", "+str( _netReplay.errorString() )+"]";

        elif _netReplay.error() == 3: # Host [host-name] not found
            _msg = "ERR_NUM: ["+str(_netReplay.error())+"]";
            _msg += str(_netReplay.errorString()).replace("Host ","Host ['").replace(" not found","'] not found!");

        elif _netReplay.error() == 5: # [5, Operation canceled]
            #print("ERR_NUM: ["+str(_netReplay.error())+", "+str( _netReplay.errorString() )+"]");
            pass;

        elif _netReplay.error() == 6: # [6, SSL handshake failed]
            _msg = "ERR_NUM: ["+str(_netReplay.error())+", "+str( _netReplay.errorString() )+"]";

        elif _netReplay.error() == 202: # Error downloading 
            _msg = "ERR_NUM: ["+str(_netReplay.error())+", "+str( _netReplay.errorString() )+"]";

        else:
            _msg = str(_netReplay.error())+", "+str( _netReplay.errorString() )+"]";


        # -------------------------------------------------------------------
        if _msg is not None:
            self.LOCAL_ERROR_LOG( str(_netReplay.error())+", "+_msg+", "+str(_netReplay.readAll().data()) );

        # -------------------------------------------------------------------

        """
        data = json.loads(str(_QNetworkReply.readAll().data())) # get data
        str( _QNetworkReply.readAll().data() );
        """
        # -------------------------------------------------------------------

    # =======================================================================
    def _DOWN(self, _a, _b):

        self.LOCAL_ERROR_LOG( "DOWN]: "+str(_a)+", "+str(_b));

    def _UP(self, _a, _b):
        self.LOCAL_ERROR_LOG( "UP]: "+str(_a)+", "+str(_b));

    def _ERROR(self, _error):
        self.LOCAL_ERROR_LOG( "_ERROR]: "+str(_error));

    def _FINISH(self):
        self.LOCAL_ERROR_LOG( "_FINISH]: NO-ARGS");

    def _META_DATA_CHANGED(self):
        self.LOCAL_ERROR_LOG( "_META_DATA_CHANGED]: NO-ARGS");

    def _SSL_ERROR(self, _ssl_error_list):
        self.LOCAL_ERROR_LOG( "_SSL_ERROR]: "+str(_ssl_error_list));

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
        #if self.DEBUG or self.PARENT.DEBUG_GLOBAL: self.PARENT.DEBUGGER.DEBUG();
        # -------------------------------------------------------------------
        if METHOD is None:
            self.PARENT.LOCAL_WARNING_LOG( "['"+self.LOG_TAG+"']: ["+_msg+"]" );
        else:
            self.PARENT.LOCAL_WARNING_LOG( "['"+self.LOG_TAG+"."+METHOD+"']: ["+_msg+"]" );
        # -------------------------------------------------------------------

    # =======================================================================

###################################################################################################
