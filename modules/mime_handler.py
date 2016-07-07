#!/usr/bin/python
# -*- coding: utf-8 -*-
###################################################################################################
# Built IN
import json, time, urllib, urllib2
import magic, mimetypes

from time import sleep, time

mimetypes.init();

###################################################################################################
#REM_URL = "http://karumba.site88.net/public/files/highlight.zip";
#LOC_URL = "Docs-Browser";

#rem_url = urllib.pathname2url( REM_URL );
#print( url );

#loc_url = urllib.pathname2url( LOC_URL );
#print( url );

# =================================================================================

# FULL-LIST OF MIME_TPES + Extentions
# http://www.freeformatter.com/mime-types-list.html

# print( mime.from_buffer( ) );
# print( mime.from_file( ) );

#mimetypes.MimeTypes().guess_type( "application/pdf" );
#mimetypes.MimeTypes().guess_all_extensions( "application/pdf" ); #>>> ['.pdf']

#req = urllib2.Request( self.DOWNLOAD_DATA_URL, headers=self.HEADERS );
#_response = urllib2.urlopen(req);


###################################################################################################
class Mime_Handler(object):

    # =======================================================================
    def __init__( self, parent ):

        # -------------------------------------------------------------------
        self.PARENT                                 = parent;
        self.DEBUG                                  = False;
        self.LOG_TAG                                = str(self.__class__.__name__).upper();

        self.MIME                                   = magic.Magic( mime=True );


        self.THROW_WARNING_ON_TYPE                  = {

            # BIN
            "application/x-msdownload",             # [.exe]        [exe]
            "application/octet-stream",             # [.bin]        [Binary]
            "application/java-vm",                  # [.class]      [Java-Byte-Code]
            "application/x-shockwave-flash",        # [.swf]        [Adobe Flash]

            # SPECIAL
            "application/pdf",                      # [.pdf]        [Pdf]
            "chemical/x-xyz",                       # [.xyz]        []
            "application/x-latex",                  # [.latex]      [LaTeX]
            "image/vnd.djvu",                       # [.djvu]       [dJvu]

            # ARCHIVES
            "application/x-7z-compressed",          # [.7z]         [7z Archive]
            "application/x-rar-compressed",         # [.rar]        [Rar Archive]
            "application/zip",                      # [.zip]        [Zip Archive]
            "application/x-tar",                    # [.tar]        [Tape Archive]
            "application/x-ustar",                  # [.ustar]      [Ustar (Uniform Standard Tape Archive)]
            "application/x-shar",                   # [.shar]       [Shell Archive]
            "application/java-archive",             # [.jar]        [Java]
            "application/epub+zip",                 # [.epub]       [Electronic Publication]
            "application/x-debian-package",         # [.deb]        [Debian package]
            "application/x-bzip",                   # [.bz]         [Bzip Archive]
            "application/x-bzip2",                  # [.bz2]        [Bzip2 Archive]
            "application/x-ace-compressed",         # [ace]         [Ace Archive]
            "application/vnd.android.package-archive", # [.apk]     [Android Package Archive]
            "application/x-bcpio",                  # [.bcpio]      [Binary CPIO Archive]
            "application/x-cpio",                   # [.cpio]       [CPIO Archive]
            "application/x-stuffit",                # [.sit]        [Stuffit Archive]
            "application/x-stuffitx",               # [.sitx]       [Stuffit Archive]

            # SEMI-READABLE
            #"application/x-bittorrent",             # [.torrent]   [Bit-Torrent file]
            #"text/x-java-source,java",              # [.java]      [Java Source File]
            #"text/csv",                             # [.csv]       [Comma-Seperated Values]
            #"application/x-csh",                    # [.csh]       [C Shell Script]
            #"text/x-c",                             # [.c]         [C Source File]
            #"text/x-asm",                           # [.s, .asm]   [Assembler Source File]
            #"text/x-python",                        # [.py]        [Python Source File]

            #"text/x-shellscript",                   # [bash]


            #"inode/x-empty",                         # [EMPTY-FILE]

        }


        # -------------------------------------------------------------------
        self.PARENT.SPLASH.STATUS( self.LOG_TAG+": [INIT]" );
        # -------------------------------------------------------------------

    # =======================================================================
    def FROM_FILE( self, _url ):

        # -------------------------------------------------------------------
        try:

            return self.MIME.from_file( _url );

        except Exception as _err:
            return "directory"
            #self.LOCAL_ERROR_LOG( "IS_NO_FILE" );

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



# =================================================================================
