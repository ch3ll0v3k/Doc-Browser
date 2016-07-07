#!/usr/bin/python
# -*- coding: utf-8 -*-
###################################################################################################
# Built IN
import json, time, os, httplib, urllib, urllib2, hashlib
import hashlib, magic, mimetypes

from random import randint
from threading import Timer
from sys import stdout
from time import sleep, time, ctime, strftime, localtime
from datetime import datetime

#--------------------------------------------------------------------------------------------------
mimetypes.init();

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


# ######################################################################################
class Downloader( QThread ):

    # =======================================================================
    def __init__(self, parent, _url, _UID, _name, _exe, _d_dir):

        # -------------------------------------------------------------------
        QThread.__init__( self, parent );

        # -------------------------------------------------------------------
        self.PARENT                                 = parent;
        self.DEBUG                                  = False;
        self.LOG_TAG                                = "DOANLOAD_THREAD";

        # -------------------------------------------------------------------
        self.D_URL                                  = _url;
        self.D_UID                                  = _UID;
        self.D_NAME                                 = _name;
        self.D_EXE                                  = _exe;
        self.D_DIR                                  = _d_dir;
        self.D_LEN                                  = 0;
        self.D_INFO                                 = "";

        self.ABORT                                  = False; 
        self.CONTENT_LENGTH_AVAILABLE               = False;
        self.D_BUFFER                               = 1024*256;

        # -------------------------------------------------------------------
        self.URLLIB_REQ                             = None;
        self.URLLIB_RESP                            = None;

        # -------------------------------------------------------------------

    # =======================================================================
    def REQUEST(self):

        # -------------------------------------------------------------------
        self.URLLIB_REQ  = urllib2.Request( self.D_URL, headers=self.PARENT.PARENT.WEB_PAGE.HEADERS );
        self.URLLIB_RESP = urllib2.urlopen( self.URLLIB_REQ );

        # -------------------------------------------------------------------
        try:
    
            if len( self.D_EXE ) > 4 and "content-disposition" in self.URLLIB_RESP.headers:
                self.D_EXE = "."+self.URLLIB_RESP.headers["content-type"].split("/")[1];
                self.D_NAME = str( int(time()) )+self.D_EXE;

            if os.path.isfile( self.D_URL+self.D_NAME ):
                if not self.PARENT.PARENT.SHOW_QMESSAGE("info", "FILE EXISTS: \n["+self.DOWNLOAD_DIR+self.D_NAME+"] \n Overwrite ?"):
                    return False;

        except Exception as _err:
            self.PARENT.LOCAL_INFO_LOG( self.LOG_TAG+str(_err) );
            return False;

        # -------------------------------------------------------------------
        print("[0:1]")
        try:

            self.D_LEN = int(self.self.URLLIB_RESP.headers["content-length"]);
            self.D_INFO += self.self.URLLIB_RESP.headers["content-type"]+"|";

            if self.D_LEN/1024/1024 > 1:
                self.D_INFO += " "+str( self.D_LEN/1024/1024 )+"Mb";

            else:
                self.D_INFO += " "+str( self.D_LEN/1024 )+"Kb";

            self.CONTENT_LENGTH_AVAILABLE = True;
            print("[0:2]")

        except:
            pass;

        # -------------------------------------------------------------------
        return True;
        # -------------------------------------------------------------------

    # =======================================================================
    def run(self):

        # -------------------------------------------------------------------
        if not self.ABORT:
            
            print("SAVING-TO: ["+self.D_DIR+self.D_NAME+"]");


            if self.CONTENT_LENGTH_AVAILABLE:
                self.CONTENT_LENGTH_TRUE();
                return;

            self.CONTENT_LENGTH_FALSE();

            print("[0:3]")
        else:
            # FIXME
            print("[0:4]")
            self.PARENT.LOCAL_INFO_LOG( self.LOG_TAG+self.D_NAME );

        # -------------------------------------------------------------------

    # =======================================================================
    def CONTENT_LENGTH_TRUE(self):
 
        # -------------------------------------------------------------------
        try:

            self.PARENT.LOCAL_INFO_LOG( "Download started: "+self.D_NAME );

            _data_read      = 0;
            content_length  = int(self.URLLIB_RESP.headers["content-length"]);


            FS = open(self.D_DIR+self.D_NAME, "w");

            print("[0:4]")
            while _data_read < content_length:

                _data_read += self.D_BUFFER;
                FS.write( self.URLLIB_RESP.read( self.D_BUFFER ) );

                stdout.write( "DOWNLOADED: UID:["+self.D_UID+"] :[{0:10.3f}] Kib".format( float( _data_read/1024 ) )+"\r" );
                stdout.flush();

                if self.ABORT:
                    self.LOCAL_INFO_LOG( "Download aborted: "+self.file_name );
                    stdout.write( "DOWNLOADED: UID:["+self.D_UID+"] :[{0:10.3f}] Kib".format( float( _data_read/1024 ) )+"\n" );
                    FS.close();
                    
                    del self.URLLIB_RESP;
                    return;

            del self.URLLIB_RESP;
            FS.close();

            self.PARENT.LOCAL_INFO_LOG( "Download finished: "+self.D_NAME );

        except Exception as _err:
            self.PARENT.LOCAL_ERROR_LOG( str(_err), "CONTENT_LENGTH_FALSE"  );

        # -------------------------------------------------------------------

    # =======================================================================
    def CONTENT_LENGTH_FALSE(self):

        # -------------------------------------------------------------------
        try:

            # TODO:
            # FIXME: APPEND BUFFER TO open( file, mode, BUFFER ) ????????? 
            # TODO:

            self.PARENT.LOCAL_INFO_LOG( "Download started: "+self.D_NAME );

            FS = open(self.D_DIR+self.D_NAME, "w");

            _data_read = self.URLLIB_RESP.read( self.D_BUFFER );
            _bytes_read = self.D_BUFFER;

            print("[0:5]")
            while len(_data_read) > 0:

                FS.write( _data_read );
                _bytes_read += self.D_BUFFER;
                del _data_read;
                _data_read = self.URLLIB_RESP.read( self.D_BUFFER );

                stdout.write( "DOWNLOADED: UID:["+self.D_UID+"] :[{0:10.3f}] Kib".format( float( _bytes_read/1024 ) )+"\r" );
                stdout.flush();

                if self.ABORT:
                    self.PARENT.LOCAL_INFO_LOG( "Download aborted: "+self.file_name );
                    stdout.write( "DOWNLOADED: UID:["+self.D_UID+"] :[{0:10.3f}] Kib".format( float( _bytes_read/1024 ) )+"\n" );
                    FS.close();
                    
                    del self.URLLIB_RESP;
                    return;

            del self.URLLIB_RESP;
            FS.close();

            __SIZE__ = "{0:.3f} Kib".format( float( _bytes_read/1024 ) );
            self.PARENT.LOCAL_INFO_LOG( "Download finished: "+self.D_NAME );
        
        except Exception as _err:
            self.PARENT.LOCAL_ERROR_LOG( str(_err), "CONTENT_LENGTH_TRUE"  );

        # -------------------------------------------------------------------

    # =======================================================================

# ######################################################################################
class Download_Manager( QFrame ):
    
    # =======================================================================
    def __init__(self, parent=None):

        # -------------------------------------------------------------------
        QFrame.__init__( self, parent );

        # -------------------------------------------------------------------
        self.PARENT                                 = parent;
        self.DEBUG                                  = False;
        self.LOG_TAG                                = str(self.__class__.__name__).upper();

        # -------------------------------------------------------------------
        self.DOWNLOAD_DIR                           = "";
        self.DOWNLOAD_DIR_TMP                       = "";

        self.DOWNLOAD_DATA_URL                      = "";
        self.DOWNLOAD_SESSIONS                      = {};

        self.TIMER                                  = QTimer();
        self._MD5                                   = hashlib.md5;

        # FIXME: MEMORY LEAK BY HUGE FILE ZISE
        # -------------------------------------------------------------------
        self.PARENT.SPLASH.STATUS( self.LOG_TAG+": [INIT]" );
        # -------------------------------------------------------------------

    # =======================================================================
    def REQUEST( self, _request, _IS_REPLAY=True ):

        # -------------------------------------------------------------------
        try:



            # ----------------------------------------------------------
            # http://pyqt.sourceforge.net/Docs/PyQt4/qnetworkreply.html

            if _IS_REPLAY:
                _URL = _request.url().toString();

            else:
                _URL = str(_request).strip();

            print("["+_URL+"]")

            self.DOWNLOAD_DATA_URL = str(_URL).replace( "file://", "" ); # <= You never know :p
            self.DOWNLOAD_DATA_URL = str( QUrl.toPercentEncoding( self.DOWNLOAD_DATA_URL, "/:{}", " ") );

            file_name = self.DOWNLOAD_DATA_URL.split("/")[-1];
            file_name = file_name.replace(":","-");
            file_exe  = self.DOWNLOAD_DATA_URL.split(".")[-1];

            # ----------------------------------------------------------
            if os.path.isfile( self.DOWNLOAD_DATA_URL ):
                self.LOCAL_WARNING_LOG( "Make no sense:[ IS LOCAL FILE]<br>["+self.DOWNLOAD_DATA_URL+"]");
                return;

            # ----------------------------------------------------------
            self.DOWNLOAD_DIR_TMP = self.SELECT_DIR( );

            if self.DOWNLOAD_DIR_TMP == "":
                self.LOCAL_INFO_LOG( "Download: Aborted: ["+str(file_name)+"]" ); 
                return;

            elif self.DOWNLOAD_DIR_TMP == "/":
                if not self.PARENT.SHOW_QMESSAGE('info', "Save file to '/' (ROOT) ? Must be root! "):
                    self.LOCAL_INFO_LOG( "Download: Aborted!" ); 
                    return;

            else:

                self.DOWNLOAD_DIR = self.DOWNLOAD_DIR_TMP+"/";
                self.NEW_DOWNLOAD( self.DOWNLOAD_DATA_URL, file_name, file_exe, self.DOWNLOAD_DIR );

            # ----------------------------------------------------------

        except Exception as _err:
            self.LOCAL_ERROR_LOG( str(_err), "REQUEST" );

        # -------------------------------------------------------------------

    # =======================================================================
    def NEW_DOWNLOAD( self, _url, _name, _exe,  _d_dir ):

        # -------------------------------------------------------------------
        try:

            UID = self._MD5( str(int(time())) ).hexdigest()[0:6];
            self.DOWNLOAD_SESSIONS[ UID ] = Downloader( self, _url, UID, _name, _exe, _d_dir );

            if self.DOWNLOAD_SESSIONS[ UID ].REQUEST():
                self.DOWNLOAD_SESSIONS[ UID ].start();

            else:
                self.LOCAL_ERROR_LOG( "CAN'T START-UP:", "NEW_DOWNLOAD" );
                del self.DOWNLOAD_SESSIONS[ UID ];

        except Exception as _err:
            self.LOCAL_ERROR_LOG( str(_err), "NEW_DOWNLOAD" );
        # -------------------------------------------------------------------

    # =======================================================================
    def CMD( self, _CMD ):

        # -------------------------------------------------------------------
        #__exec:download_manager:wget:url
        #__exec:download_manager:abort:(UID|all)
        #__exec:download_manager:download_window:show
        #__exec:download_manager:download_window:keep_open

        # -------------------------------------------------------------------
        try:

            if _CMD[0] == "abort":
                if _CMD[1] == "all":
                    for x in xrange(0, len(self.DOWNLOAD_SESSIONS) ):
                        self.DOWNLOAD_SESSIONS[ _CMD[x] ].ABORT = True;

                elif len(_CMD) >= 3:
                    self.DOWNLOAD_SESSIONS[ _CMD[2] ].ABORT = True;

            if _CMD[0] == "wget":
                _url = "".join(_CMD[1:]).replace("http//", "http://");
                _url = _url.replace("https//", "https://");
                _url = _url.replace("ftp//", "ftp://");

                self.REQUEST( _url, False );


        except Exception as _err:
            self.LOCAL_ERROR_LOG( str(_err), "CMD" );
        # -------------------------------------------------------------------

    # =======================================================================
    def SELECT_DIR( self, _ONLY_DIRS=True ):

        # -------------------------------------------------------------------
        if _ONLY_DIRS:
            return str( QFileDialog.getExistingDirectory(
                self, "Select Directory to save:", self.DOWNLOAD_DIR, QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
            ));

        else:
            return str( QFileDialog.getExistingDirectory(
                self, "Select Directory to save:", self.DOWNLOAD_DIR, QFileDialog.DontResolveSymlinks
            ));

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

# ######################################################################################
