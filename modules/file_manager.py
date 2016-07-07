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

###################################################################################################
class File_Manager( object ):

    # =======================================================================
    def __init__(self, parent=None):

        # -------------------------------------------------------------------
        self.PARENT                                 = parent;
        self.DEBUG                                  = False;
        self.LOG_TAG                                = str(self.__class__.__name__).upper();

        # -------------------------------------------------------------------
        self.SHOW_HIDDEN_FILES                      = False;
        self.SHOW_FILES_FIRST                       = False;
        self.NEW_URL                                = "";

        # -------------------------------------------------------------------
        self.THEMAs                                 = [
            "monokai-sublime.css",
            "brown-paper.css",
            "dark.css",
            "default.css",
            "qtcreator_dark.css",
        ];

        self.THEMA                                  = self.THEMAs[ 0 ];

        # -------------------------------------------------------------------
        self.PARENT.SPLASH.STATUS( self.LOG_TAG+": [INIT]" );
        # -------------------------------------------------------------------

    # =======================================================================
    def CMD( self, _CMD ):

       # -------------------------------------------------------------------
        #__exec:file_manager:show_hidden_files:(0|1)"
        #__exec:file_manager:show_files_first:(0|1)"

       # -------------------------------------------------------------------
        try:
    
            # -----------------------------------------------
            if _CMD[0] == "show_hidden_files":

                self.SHOW_HIDDEN_FILES = True if _CMD[1] == "1" else False;
                self.PARENT.PAGE_RELOAD();
                self.LOCAL_INFO_LOG( "file_manager:show_hidden_files:"+_CMD[1] );
                    
                return;

            # -----------------------------------------------
            if _CMD[0] == "show_files_first":

                self.SHOW_FILES_FIRST = True if _CMD[1] == "1" else False;
                self.PARENT.PAGE_RELOAD();
                self.LOCAL_INFO_LOG( "file_manager:show_files_first:"+_CMD[1] );

                return;
            

            # -----------------------------------------------
            self.LOCAL_INFO_LOG( "Unknown: CMD: "+str(_CMD[0:]) );

            # -----------------------------------------------

        except Exception as _err:
            self.LOCAL_ERROR_LOG( str(_err), "CMD" );
    
        # -------------------------------------------------------------------

    # =======================================================================
    def SORT_BY( self, _this ):

        # -------------------------------------------------------------------
        pass;
        # -------------------------------------------------------------------

    # =======================================================================
    def HIDDEN_FILES_CTRL( self, _action ):

        # -------------------------------------------------------------------
        self.SHOW_HIDDEN_FILE = True if _action == "1" else False;
        # -------------------------------------------------------------------

    # =======================================================================
    def SHOW_SOURCE( self, _ADDR, _MIME, REMOTE_FILE, HIGH_LIGHT ):

        # -------------------------------------------------------------------
        #html = self.WEB_PAGE.GET_PAGE_HTML();
        
        # -------------------------------------------------------------------
        old_name = str( _ADDR.split("/")[-1] );
        new_name = self.PARENT.TMP_DIR+old_name+".html";

        # -------------------------------------------------------------------
        print("-1")
        try:

            if REMOTE_FILE:

                _req = urllib2.Request( _ADDR, headers=self.PARENT.WEB_PAGE.HEADERS );
                #DATA = (urllib2.urlopen( _req ).read()).split("\n");
                DATA = urllib2.urlopen( _req ).read();


            else:
                
                FS = open(_ADDR, "r");
                DATA = FS.readlines();
                FS.close();


        except Exception as _err:
            self.LOCAL_ERROR_LOG( str(_err), "SHOW_SOURCE[0]" );
            return False;
        # -------------------------------------------------------------------

        try:
            

            FS_OUT = open( new_name, "w" );

            if HIGH_LIGHT:

                FS_OUT.write( """
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <title>src:h:["""+old_name+"""]</title>

                        <link rel="stylesheet" href="../browser-data/css/styles/"""+self.THEMA+"""">
                        <script src="../browser-data/js/highlight.pack.js"></script>
                        <script>
                            hljs.initHighlightingOnLoad();
                        </script>

                    </head>
                    <body>\n<pre><code class=\"\">""");
                
                for data in DATA:
                    FS_OUT.write( data.replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>") );

                FS_OUT.write( "</code></pre>\n</body></html>" );                            

            else:

                FS_OUT.write( "<title>src:["+old_name+"]</title>" );
                FS_OUT.write( "<pre>" );
                for data in DATA:
                    FS_OUT.write( data.replace("<", "&lt;").replace(">", "&gt;") ); #.replace("\n", "<br>") );

                FS_OUT.write( "</pre>" );


            FS_OUT.close();

            self.NEW_URL = new_name;
            return True;

        except Exception as _err:
            self.LOCAL_ERROR_LOG( str(_err), "SHOW_SOURCE[1]" );
            return False;

        # -------------------------------------------------------------------

    # =======================================================================
    def PROCCESS_FILE( self, _ADDR, RENDER_SOURCE=False, REMOTE_FILE=False, HIGH_LIGHT=False ):

        # -------------------------------------------------------------------
        mime_type     = self.PARENT.MIME_HANDLER.FROM_FILE( _ADDR );
        mime_type_arr = mime_type.split("/");
        old_name      = str( _ADDR.split("/")[-1] );

        # -------------------------------------------------------------------
        try:

            if not REMOTE_FILE:
                _sizeByte  = os.stat( _ADDR ).st_size;
                _sizeKByte = float(_sizeByte/1024);
                _sizeMByte = float(_sizeKByte/1024);

                if _sizeMByte > 0.99999:
                    _size = "{0:.2f} Mb".format( _sizeMByte );

                elif _sizeKByte > 0.99999:
                    _size = "{0:.2f} KiB".format( _sizeKByte );

                else:
                    _size = str(_sizeByte)+" Byte";

        except Exception as _err:
            self.LOCAL_ERROR_LOG( str(_err), "PROCCESS_FILE[0]" );
            return False;

        # -------------------------------------------------------------------
        try:

            if not REMOTE_FILE:
                # WARNING BY FILE TYPE:
                for w_type in self.PARENT.MIME_HANDLER.THROW_WARNING_ON_TYPE:

                    if mime_type == w_type:
                        if not self.PARENT.SHOW_QMESSAGE("warning", "File["+_ADDR+"]<br> Size: ["+_size+"]<br> Is["+w_type+"] <br> Open it ?" ):
                            return;
                        break;

                # -------------------------------------------------------------------
                if mime_type_arr == "audio" or mime_type_arr == "video":
                    if not self.PARENT.SHOW_QMESSAGE("warning", "File["+_ADDR+"]<br> Size: ["+_size+"]<br> Is["+mime_type+"] <br> Open it ?" ):
                        return;


                # -------------------------------------------------------------------
                if _sizeMByte > 0.99999:
                    if not self.PARENT.SHOW_QMESSAGE("warning", "File["+_ADDR+"]<br> Size: ["+_size+"] Open it ?" ):
                        return;

        except Exception as _err:
            self.LOCAL_ERROR_LOG( str(_err), "PROCCESS_FILE[1]" );
            return False;

        # -------------------------------------------------------------------
        try:

            if RENDER_SOURCE:

                if self.SHOW_SOURCE( _ADDR, mime_type_arr, REMOTE_FILE, HIGH_LIGHT ):
                    return True;
                return False;

            else:

                # -------------------------------------------------------------------------
                print( old_name, mime_type_arr );
                # -------------------------------------------------------------------------
                if mime_type_arr[1] == "html":

                    self.NEW_URL = _ADDR;
                    return True;

                # -------------------------------------------------------------------------
                if mime_type_arr[0] == "image":

                    new_name = self.PARENT.TMP_DIR+old_name+".html";
                    FS_OUT = open( new_name, "w" );                            
                    FS_OUT.write( '<title>src:['+old_name+']</title>' );
                    FS_OUT.write( '<img src="'+_ADDR+'"/>' );
                    FS_OUT.close();
                    self.NEW_URL = new_name;
                    
                    return True;

                # -------------------------------------------------------------------------
                if mime_type_arr[0] == "inode" or mime_type_arr[1] == "x-empty":

                    self.LOCAL_INFO_LOG(" File: ['"+old_name+"'] is empty!");
                    return False;


                # -------------------------------------------------------------------------
                # IF WE NEED SOURCE

                FS = open(_ADDR, "r");
                DATA = FS.readlines();
                FS.close();

                # -------------------------------------------------------------------------
                if mime_type_arr[0] == "text":

                    new_name = self.PARENT.TMP_DIR+str(self.PARENT.GET_TIME())+".html";
                    FS_OUT = open( new_name, "w" );                            
                    FS_OUT.write( '<title>src:['+old_name+']</title>' );

                    for _data in DATA:
                        FS_OUT.write( _data.replace("\n")+"<br/>\n" );

                    FS_OUT.close();
                    self.NEW_URL = new_name;
                    
                    return True;

                # -------------------------------------------------------------------------

        except Exception as _err:
            self.LOCAL_ERROR_LOG( str(_err), "PROCCESS_FILE[2]" );
            return False;

        # -------------------------------------------------------------------

    # =======================================================================
    def CREATE_TREE( self, _ADDR ):

        # -------------------------------------------------------------------
        try:

            LEVEL_UP = "";
            _FILES   = [];

            while _ADDR != _ADDR.replace("//","/"):
                _ADDR = _ADDR.replace("//","/");

            if _ADDR[-1:] != "/":
                _ADDR += "/";



            if _ADDR == "/":
                LEVEL_UP = "/";

            else:
                dirs = _ADDR.split("/");
                for i in xrange(0, len(dirs)-2):

                    LEVEL_UP += dirs[i]+"/";


            _FILES = os.listdir( _ADDR );
            _FILES.sort();

        except Exception as _err:
            self.LOCAL_ERROR_LOG( str(_err), "CREATE_TREE:0" );
            return False;

        # -----------------------------------------------------------------
        try:

            # GENERATE HTML-BASED-FILE-EXPLORER
            _HTML = '<title>src:[TITLE]</title>';


            _HTML += '<div class="_local_time">'+self.PARENT.GET_DATE_TIME()+'</div>';
            _HR_ = '<div class="_hr_div"></div>'+"\n";


            with open( self.PARENT.DATA_DIR+"css/file_browser.css", 'r' ) as FS:
                for _l in FS:
                    _HTML += _l;

            _HTML += _HR_;
            _HTML += '<a class="_nav_level_up" href="'+LEVEL_UP+'">level up</a> => ';

            # -----------------------------------------------------------------
            _ADDR = _ADDR.replace("//","/");

            QUICK_NAV_PATH = "";
            QUICK_NAV_NAME = "['";
            QUICK_NAV_DATA = _ADDR.split( "/" );

            for quick_nav in QUICK_NAV_DATA:
                
                QUICK_NAV_PATH += quick_nav.strip()+"/";
                QUICK_NAV_NAME += '<a class="_nav_path" href="'+QUICK_NAV_PATH+'">'+quick_nav.strip()+"</a>/";

            _HTML = _HTML.replace( "[TITLE]", QUICK_NAV_DATA[-1]+"/" )


            _HTML += (QUICK_NAV_NAME[ 0: len(QUICK_NAV_NAME)-1 ])+"']";
            _HTML += _HR_;

        except Exception as _err:
            self.LOCAL_ERROR_LOG( str(_err), "CREATE_TREE:1" );
            return False;
                                
        # -----------------------------------------------------------------
        try:

            # TODO: Add Sort by and show|hide hidden files/dirs

            _F = []; # files
            _D = []; # directoris

            for _file in _FILES:

                if _file[0:1] == ".":
                    if not self.SHOW_HIDDEN_FILES:
                        continue;
                
                stat     = os.stat(_ADDR+_file);
                mod_date = strftime("%d-%b-%Y %H:%M:%S", localtime( stat.st_mtime ));

                # ** st_mode   - protection bits,
                # ** st_ino    - inode number,
                # ** st_dev    - device,
                # ** st_nlink  - number of hard links,
                # ** st_uid    - user id of owner,
                # ** st_gid    - group id of owner,
                # ** st_size   - size of file, in bytes,
                # ** st_atime  - time of most recent access,
                # ** st_mtime  - time of most recent content modification,
                # ** st_ctime  - platform dependent; time of most recent metadata change on Unix, or the time of creation on Windows)


                if os.path.isfile(_ADDR+_file):

                    _sizeByte  = stat.st_size; # /1024/1024 == Mb
                    _sizeKByte = float(_sizeByte/1024);
                    _sizeMByte = float(_sizeKByte/1024);


                    if _sizeMByte > 0.99999:
                        _size = "{0:.2f} Mb".format( _sizeMByte );

                    elif _sizeKByte > 0.99999:
                        _size = "{0:.2f} KiB".format( _sizeKByte );

                    else:
                        _size = str(_sizeByte)+" Byte";

                    _f = '<div class="_line">';

                    if _file[0:1] == ".":
                        _f += '<div class="_long_name"><a class="_file_hidden" href="'+_ADDR+_file+'"> '+_file+'</a></div>';
                    else:
                        _f += '<div class="_long_name"><a class="_file" href="'+_ADDR+_file+'"> '+_file+'</a></div>';

                    _f += '<span class="_size">'+_size+'</span>';
                    _f += '<span class="_mod_date">'+mod_date+'</span>';
                    _f += '<span class="_descr_F">(F)</span>';
                    _f += '</div>\n';

                    _F.append( _f );

                else:

                    _d = '<div class="_line">';

                    if _file[0:1] == ".":
                        _d += '<div class="_long_name"><a class="_dir_hidden" href="'+_ADDR+_file+'/"> '+_file+'/</a></div>';
                    else:
                        _d += '<div class="_long_name"><a class="_dir" href="'+_ADDR+_file+'/"> '+_file+'/</a></div>';

                    _d += '<span class="_size">...</span>';
                    _d += '<span class="_mod_date">'+mod_date+'</span>';
                    _d += '<span class="_descr_D">(D)</span>';
                    _d += '</div>\n';

                    _D.append( _d );


        except Exception as _err:
            self.LOCAL_ERROR_LOG( str(_err), "CREATE_TREE:2" );
            return False;

        # -------------------------------------------------------------------------
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
        return True;

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

