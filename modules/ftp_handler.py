#!/usr/bin/python
# -*- coding: utf-8 -*-
###################################################################################################
# Built IN
import json, time, os, math, subprocess, hashlib
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
# OyQt
from PyQt4.QtCore import Qt

from PyQt4.QtCore import QTimer, QThread, QEvent, SIGNAL, SLOT, pyqtSignal, pyqtSlot
from PyQt4.QtCore import QByteArray, QUrl, QString

from PyQt4.QtGui import QApplication, QLineEdit, QLabel, QFrame, QListWidget, QListWidgetItem
from PyQt4.QtGui import QCheckBox, QPushButton, QAction, QComboBox

# -> http://pyqt.sourceforge.net/Docs/PyQt4/qtnetwork.html
from PyQt4.QtNetwork import QNetworkRequest, QNetworkAccessManager, QNetworkReply
from PyQt4.QtNetwork import QNetworkCookie, QNetworkCookieJar, QFtp, QUrlInfo

###################################################################################################
class FTP_Handler( QFtp ):

    # =======================================================================
    def __init__( self, parent=None ):

        # -------------------------------------------------------------------
        QFtp.__init__( self, parent );
        
        # -------------------------------------------------------------------
        self.PARENT                                 = parent;
        self.DEBUG                                  = False;
        self.LOG_TAG                                = str(self.__class__.__name__).upper();

        # -------------------------------------------------------------------
        self.stateChanged.connect( self.ON_STATE_CHANGED ); 
        self.listInfo.connect( self.ON_LIST_INFO_AVAILABLE ); 
        self.commandFinished.connect( self.ON_COMMAND_FINISHED ); 
        self.commandStarted.connect( self.ON_COMMAND_STARTED ); 
        self.readyRead.connect( self.ON_READY_READ ); 
        self.done.connect( self.ON_DONE ); 
        self.dataTransferProgress.connect( self.ON_DATA_TRANSFER_PROGRESS ); 
        self.rawCommandReply.connect( self.ON_RAW_COMMAND_REPLY ); 

        # -------------------------------------------------------------------
        self.HOST                                   = "";
        self.PATH                                   = "";
        self.USER                                   = "";
        self.PWD                                    = "";
        self.PORT                                   = 21;

        # -------------------------------------------------------------------
        self.FILE_INFO_LIST                         = [];
        self.LOGIN_SUCCESS                          = False;
        self.ALLOW_TO_RUN                           = True;
        self.LAST_ERROR                             = QFtp.NoError;

        self.NEW_URL                                = "";
        self.SHOW_HIDDEN_FILES                      = False;
        self.SHOW_FILES_FIRST                       = False;

        self.PRINT_CONN_INFO                        = False;

        # -------------------------------------------------------------------
        self.REQ_UIDS                               = {

            "connect"       : 0,
            "login"         : 0,
            "cd"            : 0,
            "list"          : 0,

        } 

        # -------------------------------------------------------------------
        self.PARENT.SPLASH.STATUS( self.LOG_TAG+": [INIT]" );
        # -------------------------------------------------------------------

    # =======================================================================
    def MK_CONNECT( self, _url, _user="anonymous", _pwd="", _port=21 ):

        # -------------------------------------------------------------------
        try:

            req  = urllib2.Request( _url, headers=self.PARENT.WEB_PAGE.HEADERS );
            resp = urllib2.urlopen( req );
            t = resp.headers["content-type"];
            self.PARENT.DOWNLOAD_MANAGER.REQUEST( _url, False );

            return;

        except Exception as _err:
            pass;


        # -------------------------------------------------------------------
        try:
            
            # -----------------------------------------------------------
            # Name, isFile, date, size, owner
            for _f_info in self.FILE_INFO_LIST:
                if _url.split("/")[-1] == _f_info[0] and _f_info[1]:

                    self.PARENT.DOWNLOAD_MANAGER.REQUEST( "ftp://"+self.HOST+self.PATH+_f_info[0], False );
                    return;

            # -----------------------------------------------------------
            self.FILE_INFO_LIST                     = [];

            self.Q_URL                              = QUrl( _url ); 

            self.USER                               = str(_user);
            self.PWD                                = str(_pwd);
            self.PORT                               = int(_port);
            self.HOST                               = self.HOST if str(self.Q_URL.host()) == "" else str(self.Q_URL.host());
            self.PATH                               = "/" if str(self.Q_URL.path()) == "" else str(self.Q_URL.path());

            # -----------------------------------------------------------
            if self.PRINT_CONN_INFO:

                print(" --------------------------------------------------------- " );
                print("USER: ["+self.USER+"]" );
                print("PWD: ["+self.PWD+"]" );
                print("PORT: ["+str(self.PORT)+"]" );
                print("HOST: ["+self.HOST+"]" );
                print("PATH: ["+self.PATH+"]" );
                print(" --------------------------------------------------------- " );
            # -----------------------------------------------------------

            self.CONNECT();

        except Exception as _err:
            self.LOCAL_ERROR_LOG( "MK_CONNECT[1]: "+str(_err) );
            
        # -------------------------------------------------------------------

    # =======================================================================
    def CONNECT( self ):

        # -------------------------------------------------------------------
        try:

            self.REQ_UIDS["connect"] = self.connectToHost( self.HOST, self.PORT );
            self.REQ_UIDS["login"]   = self.login( self.USER, self.PWD );

        except Exception as _err:
            self.LOCAL_ERROR_LOG( "CONNECT: "+str(_err) );

        # -------------------------------------------------------------------

    # =======================================================================
    def ON_COMMAND_FINISHED( self, _response, _bool ):

        # -------------------------------------------------------------------
        try:

            if _response == self.REQ_UIDS["connect"]:
                print("Connected.")

            elif _response == self.REQ_UIDS["login"]:

                if self.state() == QFtp.LoggedIn:

                    print(" LoggedIn: 200");
                    self.LOGIN_SUCCESS = True;

                    print(" cd: ["+self.PATH+"]");
                    self.REQ_UIDS["cd"] = self.cd( self.PATH );


                else:
                    print(" NOT-LoggedIn: 500");

            elif _response == self.REQ_UIDS["cd"]:

                self.REQ_UIDS["list"] = self.list();                


            elif _response == self.REQ_UIDS["list"]:

                self.CREATE_TREE( self.PATH );
                self.close();

        except Exception as _err:
            self.LOCAL_ERROR_LOG( "ON_COMMAND_FINISHED: "+str(_err) );

        # -------------------------------------------------------------------

    # =======================================================================
    def CREATE_TREE( self, _ADDR ):

        # -------------------------------------------------------------------

        try:

            LEVEL_UP = "";

            if _ADDR == "/":
                LEVEL_UP = "/";

            else:
                dirs = _ADDR.split("/");
                for i in xrange(0, len(dirs)-2):

                    LEVEL_UP += dirs[i]+"/";


        except Exception as _err:
            self.LOCAL_ERROR_LOG( str(_err), "CREATE_TREE:0" );
            return False;

        # -----------------------------------------------------------------
        try:

            # GENERATE HTML-BASED-FILE-EXPLORER
            _HTML = "";
            _HR_ = '<div class="_hr_div"></div>'+"\n";


            with open( self.PARENT.DATA_DIR+"css/file_browser.css", 'r' ) as FS:
                for _l in FS:
                    _HTML += _l;

            _HTML += _HR_;
            _HTML += '&nbsp;&nbsp;&nbsp;["<a class="_nav_path" href="ftp://'+self.HOST+LEVEL_UP+'">level up</a>"] => ';

            # -----------------------------------------------------------------
            _ADDR = _ADDR.replace("//","/");

            QUICK_NAV_PATH = "";
            QUICK_NAV_NAME = '["';
            QUICK_NAV_DATA = _ADDR.split( "/" );

            for quick_nav in QUICK_NAV_DATA:
                
                QUICK_NAV_PATH += quick_nav.strip()+"/";
                QUICK_NAV_NAME += '<a class="_nav_path" href="ftp://'+self.HOST+QUICK_NAV_PATH+'">'+quick_nav.strip()+"</a>/";

            _HTML += (QUICK_NAV_NAME[ 0: len(QUICK_NAV_NAME)-1 ])+'"]';
            _HTML += _HR_;

        except Exception as _err:
            self.LOCAL_ERROR_LOG( str(_err), "CREATE_TREE:1" );
            return False;


        # -----------------------------------------------------------------
        try:

            _F = []; # files
            _D = []; # directoris
            
            host_path = 'ftp://'+self.HOST+self.PATH;

            # Name, isFile, date, size, owner
            for _f_info in self.FILE_INFO_LIST:
                
                try:
                    mod_date = "["+strftime("%d-%b-%Y %H:%M:%S", localtime( _f_info[2] ))+"]";
                except:
                    print( ":::::::::::::::: "+str(_f_info[2]) );
                    mod_date = "[out of range]";



                if _f_info[1]:

                    _sizeByte  = _f_info[3];
                    _sizeKByte = float(_sizeByte/1024);
                    _sizeMByte = float(_sizeKByte/1024);


                    if _sizeMByte > 0.99999:
                        _size = "{0:.2f} Mb".format( _sizeMByte );

                    elif _sizeKByte > 0.99999:
                        _size = "{0:.2f} KiB".format( _sizeKByte );

                    else:
                        _size = str(_sizeByte)+" Byte";

                    _f = '<div class="_line">';

                    if _f_info[0:1] == ".":
                        _f += '<div class="_long_name"><a class="_file_hidden" href="'+host_path+_f_info[0]+'"> '+_f_info[0]+'</a></div>';
                    else:
                        _f += '<div class="_long_name"><a class="_file" href="'+host_path+_f_info[0]+'"> '+_f_info[0]+'</a></div>';

                    _f += '<span class="_size">'+_size+'</span>';
                    _f += '<span class="_mod_date">'+mod_date+'</span>';
                    _f += '<span class="_descr_F">(F)</span>';
                    _f += '</div>\n';

                    _F.append( _f );

                else:

                    _d = '<div class="_line">';

                    if _f_info[0:1] == ".":
                        _d += '<div class="_long_name"><a class="_dir_hidden" href="'+host_path+_f_info[0]+'/"> '+_f_info[0]+'/</a></div>';
                    else:
                        #print(host_path, _f_info[0], [self.HOST,self.PATH])
                        _d += '<div class="_long_name"><a class="_dir" href="'+host_path+_f_info[0]+'/"> '+_f_info[0]+'/</a></div>';

                    _d += '<span class="_size">...</span>';
                    _d += '<span class="_mod_date">'+mod_date+'</span>';
                    _d += '<span class="_descr_D">(D)</span>';
                    _d += '</div>\n';

                    _D.append( _d );


        except Exception as _err:
            self.LOCAL_ERROR_LOG( str(_err), "CREATE_TREE:2" );
            return False;

        # -------------------------------------------------------------------------
        for _d in _D: _HTML += _d;
        for _f in _F: _HTML += _f;

        """
        try:

            if self.SHOW_FILES_FIRST: #if _file_first:

                for _f in _F: _HTML += _f;
                for _d in _D: _HTML += _d;

            else:

                for _d in _D: _HTML += _d;
                for _f in _F: _HTML += _f;

        except Exception as _err:
            self.LOCAL_ERROR_LOG( str(_err), "CREATE_TREE:3" );
            return False;

        """
        # -------------------------------------------------------------------------
        try:

            new_name = self.PARENT.TMP_DIR+str(int(time()))+".html";
            FS = open(new_name, "w");
            FS.write( _HTML+_HR_ );
            FS.close();
            self.NEW_URL = new_name;

        except Exception as _err:
            self.LOCAL_ERROR_LOG( str(_err), "CREATE_TREE:4" );
            return False;

        # -------------------------------------------------------------------
        try:

            self.PARENT.WEB_VIEW.load( QUrl(self.NEW_URL) );

        except Exception as _err:
            self.LOCAL_ERROR_LOG( str(_err), "CREATE_TREE:5" );
            return False;

        # -------------------------------------------------------------------
        return True;

        # -------------------------------------------------------------------

    # =======================================================================
    def ON_LIST_INFO_AVAILABLE( self, _QUrlInfo ):

        # -------------------------------------------------------------------
        try:

            _f_info = QUrlInfo( _QUrlInfo );

            self.FILE_INFO_LIST.append([

                str(_f_info.name()),
                bool( _f_info.isFile() ),
                long( _f_info.lastModified().toMSecsSinceEpoch()/1000 ),
                int(_f_info.size()),
                str(_f_info.owner())

            ]);

        except Exception as _err:
            self.LOCAL_ERROR_LOG( "LIST_INFO: "+str(_err) );

        # -------------------------------------------------------------------

    # =======================================================================
    def ON_STATE_CHANGED ( self, _state ):

        # -------------------------------------------------------------------
        try:

            if _state == QFtp.Unconnected: # 0 - There is no connection to the host.
                if self.DEBUG:
                    print("DocFTPHandler: [QFtp.Unconnected]");
                self.close();

            elif _state == QFtp.HostLookup: # 1 - A host name lookup is in progress.
                if self.DEBUG:
                    print("DocFTPHandler: [QFtp.HostLookup]");

            elif _state == QFtp.Connecting: # 2 - An attempt to connect to the host is in progress.
                if self.DEBUG:
                    print("DocFTPHandler: [QFtp.Connecting]");

            elif _state == QFtp.Connected: # 3 - Connection to the host has been achieved.
                if self.DEBUG:
                    print("DocFTPHandler: [QFtp.Connected]");

            elif _state == QFtp.LoggedIn: # 4 - Connection and user login have been achieved.
                if self.DEBUG:
                    print("DocFTPHandler: [QFtp.LoggedIn]");

            elif _state == QFtp.Closing: # 5 - The connection is closing down, but it is not yet closed. (The state will be Unconnected when the connection is closed.)
                if self.DEBUG:
                    print("DocFTPHandler: [QFtp.Closing]");
                self.close();

            else:
                print("DocFTPHandler: [QFtp.STATE: 'Unknown'");

        except Exception as _err:
            self.LOCAL_ERROR_LOG( "ON_STATE_CHANGED: "+str(_err) );

        # -------------------------------------------------------------------

    # =======================================================================
    def ON_DATA_TRANSFER_PROGRESS( self, _qint64_A, _qint64_B ):

        # -------------------------------------------------------------------
        try:

            pass;
            #print(" ON_DATA_TRANSFER_PROGRESS: ["+str(_qint64_A)+", "+str(_qint64_B)+"]" );

        except Exception as _err:
            self.LOCAL_ERROR_LOG( "ON_DATA_TRANSFER_PROGRESS: "+str(_err) );

        # -------------------------------------------------------------------

    # =======================================================================
    def ON_RAW_COMMAND_REPLY ( self, _int, _str ):

        # -------------------------------------------------------------------
        try:

            pass;
            #print(" ON_RAW_COMMAND_REPLY: ["+str(_int)+", "+str(_str)+"]" );

        except Exception as _err:
            self.LOCAL_ERROR_LOG( "ON_RAW_COMMAND_REPLY: "+str(_err) );
        # -------------------------------------------------------------------

    # =======================================================================
    def ON_DONE( self, _bool ):

        # -------------------------------------------------------------------
        try:

            pass;

        except Exception as _err:
            self.LOCAL_ERROR_LOG( "ON_DONE: "+str(_err) );

        # -------------------------------------------------------------------

    # =======================================================================
    def ON_READY_READ( self ):

        # -------------------------------------------------------------------
        try:

            pass;

        except Exception as _err:
            self.LOCAL_ERROR_LOG( "ON_READY_READ: "+str(_err) );
        # -------------------------------------------------------------------

    # =======================================================================
    def ON_COMMAND_STARTED ( self, _int ):

        # -------------------------------------------------------------------
        try:

            pass;

        except Exception as _err:
            self.LOCAL_ERROR_LOG( "ON_COMMAND_STARTED: "+str(_err) );

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
        #if self.DEBUG or self.PARENT.DEBUG_GLOBAL: self.PARENT.DEBUGGER.DEBUG();
        # -------------------------------------------------------------------
        if METHOD is None:
            self.PARENT.LOCAL_WARNING_LOG( "['"+self.LOG_TAG+"']: ["+_msg+"]" );
        else:
            self.PARENT.LOCAL_WARNING_LOG( "['"+self.LOG_TAG+"."+METHOD+"']: ["+_msg+"]" );
        # -------------------------------------------------------------------

    # =======================================================================


###################################################################################################
