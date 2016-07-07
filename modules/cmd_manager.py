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
class CMD_Manager( object ):

    # =======================================================================
    def __init__(self, parent=None):

        # -------------------------------------------------------------------
        self.PARENT                                 = parent;
        self.DEBUG                                  = False;
        self.LOG_TAG                                = str(self.__class__.__name__).upper();

        # -------------------------------------------------------------------
        self.PARENT.SPLASH.STATUS( self.LOG_TAG+": [INIT]" );
        # -------------------------------------------------------------------

    # =======================================================================
    def PROCCESS( self, _CMD ):

        # -------------------------------------------------------------------
        try:
            
            # :::::::::::::::::::::::::::::::::::::::::::::::::::::::
            #print( self.LOG_TAG+": [PROCCESS]: [INTERNAL-CMD]: [True]");
            # :::::::::::::::::::::::::::::::::::::::::::::::::::::::
            if _CMD == "__exec:home":
                self.PARENT.LAST_URL_ADDR = _CMD;
                self.PARENT.WEB_VIEW.SET_MAIN_PAGE();
                return;

            # :::::::::::::::::::::::::::::::::::::::::::::::::::::::
            _CMD = _CMD.split(":");

            if len(_CMD) < 3:
                self.LOCAL_ERROR_LOG( "CMD_MANAGER: [PROCCESS]: [unknown cmd | wrong format]" );
                return;

            # :::::::::::::::::::::::::::::::::::::::::::::::::::::::
            if _CMD[1] == "download_manager": # wget:(url)/abort:(all|index)
                
                #__exec:download_manager:wget:url
                #__exec:download_manager:abort:(UID|all)
                #__exec:download_manager:download_window:show
                #__exec:download_manager:download_window:keep_open
                self.PARENT.DOWNLOAD_MANAGER.CMD( _CMD[2:] );

            # ----------------------------------------
            elif _CMD[1] == "request_handler": # OK

                self.PARENT.REQUEST_HANDLER.CMD( _CMD[2:] );

                #__exec:request_handler:headers:show
                #__exec:request_handler:headers:hide
                #__exec:request_handler:headers:keep_open:(0|1)

            # ----------------------------------------
            elif _CMD[1] == "settings": # OK

                self.PARENT.SETTINGS.CMD( _CMD[2:] );
                #__exec:settings:window:show"
                #__exec:settings:window:hide"
                #__exec:settings:window:keep_open:(0|1)

            # ----------------------------------------
            elif _CMD[1] == "notebook": # OK

                self.PARENT.NOTEBOOK.CMD( _CMD[2:] );
                #__exec:notebook:notes:show"
                #__exec:notebook:notes:hide"
                #__exec:notebook:notes:keep_open:(0|1)

            # ----------------------------------------
            elif _CMD[1] == "file_manager": # OK

                self.PARENT.FILE_MANAGER.CMD( _CMD[2:] );
                #__exec:file_manager:show_hidden_files:(0|1)"
                #__exec:file_manager:show_files_first:(0|1)"

                #print("_CMD:[2:]: "+str(_CMD[2:]))

            # ----------------------------------------
            elif _CMD[1] == "home_page": # wget:(url)/abort:(all|index)

                #__exec:home_page:favorites:add
                self.LOCAL_INFO_LOG( _CMD[1]+":* [not-implemented]" );

            # ----------------------------------------
            elif _CMD[1] == "page": #:js:function_name":

                #__exec:page:js:function_name
                self.PARENT.WEB_PAGE.CMD( _CMD[2:] );
                
            # ----------------------------------------
            else:
                self.LOCAL_ERROR_LOG( "PROCCESS: UNKNOWN CMD: \n"+str(_CMD) );

            # :::::::::::::::::::::::::::::::::::::::::::::::::::::::

        except Exception as _err:
            self.LOCAL_ERROR_LOG( str(_err), "PROCCESS" );

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
