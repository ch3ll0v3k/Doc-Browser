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
from PyQt4.QtCore import QByteArray, QUrl, Qt, QString, QRect, QSize

from PyQt4.QtGui import QTextEdit, QDialog, QAction, QLineEdit, QLabel, QIcon
from PyQt4.QtGui import QComboBox, QCheckBox, QPushButton, QProgressBar, QFileDialog

from PyQt4.QtGui import QPrinter, QFrame, QKeySequence

# -> http://pyqt.sourceforge.net/Docs/PyQt4/qtnetwork.html
from PyQt4.QtNetwork import QNetworkRequest, QNetworkAccessManager, QNetworkReply
from PyQt4.QtNetwork import QNetworkCookie, QNetworkCookieJar

#from PyQt4 import QtWebKit  
from PyQt4.QtWebKit import QWebView, QWebPage, QWebSettings, QWebHistory, QWebFrame
from PyQt4.QtWebKit import QWebInspector;



###################################################################################################
class Web_Page( QWebPage ):

    # =======================================================================
    def __init__(self, parent, parentMain, UID):

        # -------------------------------------------------------------------
        QWebPage.__init__(self, parent);

        # -------------------------------------------------------------------
        self.PARENT                                 = parentMain;
        self.UID                                    = UID;
        self.PARENT_TAB                             = parent;
        self.DEBUG                                  = False;
        self.LOG_TAG                                = str(self.__class__.__name__).upper();

        # -------------------------------------------------------------------
        self.L_BTN_CLICK                            = False;
        self.M_BTN_CLICK                            = False;
        self.R_BTN_CLICK                            = False;

        # -------------------------------------------------------------------
        self.PROGRESS_BAR                           = None;

        self.PROGRESS_BAR_PR                        = float( self.PARENT.WIDTH / 100);
        self.PROGRESS_BAR_W                         = 0;

        # -------------------------------------------------------------------

        # SEARCH_INPUT
        self.SEARCH_INPUT                           =  QLineEdit("", self.PARENT);
        self.SEARCH_INPUT.setGeometry(0, 615, 400, 30);
        self.SEARCH_INPUT.setStyleSheet("QLineEdit{ background-color: rgba(0,0,0, 180); font-size: 12px; font-family: monospace; color: #fff; padding-left: 10px; border-style: none;}");
        self.connect( self.SEARCH_INPUT, SIGNAL('textChanged(const QString)') , self.FIND_ON_PAGE );
        self.connect( self.SEARCH_INPUT, SIGNAL('returnPressed()') , self.FIND_ON_PAGE );
        #self.SEARCH_INPUT.setReadOnly( True );
        self.SEARCH_INPUT_IS_OPEN                   = False;
        self.SEARCH_INPUT.hide();

        # -------------------------------------------------------------------
        self.AGENTS                                 = [

            # Chrome 41.0.2228.0
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
            # Chrome 41.0.2227.1
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
            # Chrome 41.0.2227.0
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
            # Chrome 41.0.2226.0
            "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36",
            # Chrome 41.0.2225.0
            "Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
            # Chrome 41.0.2224.3
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36",
            # Chrome 40.0.2214.93
            "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36",
            # Chrome 37.0.2062.124
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36",
            # Chrome 37.0.2049.0
            "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
            # Chrome 36.0.1985.67
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
            # Chrome 36.0.1985.125
            "Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36",
            # Chrome 36.0.1944.0
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36",
            # Chrome 35.0.3319.102
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36",
            # Chrome 35.0.2309.372
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2309.372 Safari/537.36",
            # Chrome 35.0.2117.157
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36",
            # Chrome 35.0.1916.47
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36",
            # Chrome 34.0.1866.237
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1866.237 Safari/537.36",
            # Chrome 34.0.1847.137
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/4E423F",
            # Chrome 34.0.1847.116
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36",
            "Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10",
            

        ];


        # -------------------------------------------------------------------
        self.USER_AGENT                             = self.AGENTS[0];

        self.HEADERS                                = {
            "User-Agent"        : "[USER-AGENT]",
            "Accept"            : "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",

            #"Accept-Language"   : "en-US,en;q=0.5",
            #"Referer"           : "https://btc-e.com/",
            #"Connection"        : "keep-alive",
            #"Cache-Control"     : "max-age=0",
            #"Cookie"            : ""

        }

        # -------------------------------------------------------------------
        #self.setContentEditable( True );
        self.setLinkDelegationPolicy( QWebPage.DelegateAllLinks );
        self.setForwardUnsupportedContent( True );
        self.setNetworkAccessManager( self.PARENT.NET_MANAGER );

        self.linkClicked.connect( self.ON_LINK_CLICKED );
        self.linkHovered.connect( self.ON_LINK_HOVERED );
        self.loadProgress.connect( self.ON_PAGE_LOAD_PROGRESS );

        self.downloadRequested.connect( self.PARENT.DOWNLOAD_MANAGER.REQUEST );
        self.unsupportedContent.connect( self.PARENT.DOWNLOAD_MANAGER.REQUEST );

        # -------------------------------------------------------------------
        self.PRINT_ACTION = QAction( self );
        self.PRINT_ACTION.setShortcuts( QKeySequence.Print );
        self.PRINT_ACTION.triggered.connect( self.PRINT );
        self.PARENT.addAction( self.PRINT_ACTION );

        # -------------------------------------------------------------------
        # SETTINGS
       
        self.SETTINGS                               = self.settings();
        self.SETTINGS.setDefaultTextEncoding("utf-8"); # <= [TO-CONFIG.FILE] + ALL FROM BELOW

        #self.SETTINGS.clearIconDatabase();
        #self.SETTINGS.clearMemoryCaches();

        self.SETTINGS.setAttribute( QWebSettings.AutoLoadImages, True );
        self.SETTINGS.setAttribute( QWebSettings.DnsPrefetchEnabled, True );
        self.SETTINGS.setAttribute( QWebSettings.JavascriptEnabled, True );
        self.SETTINGS.setAttribute( QWebSettings.JavaEnabled, False );
        self.SETTINGS.setAttribute( QWebSettings.PluginsEnabled, True );
        self.SETTINGS.setAttribute( QWebSettings.PrivateBrowsingEnabled, False );
        self.SETTINGS.setAttribute( QWebSettings.JavascriptCanOpenWindows, True ); #
        self.SETTINGS.setAttribute( QWebSettings.JavascriptCanCloseWindows, False ); #
        self.SETTINGS.setAttribute( QWebSettings.JavascriptCanAccessClipboard, True ); #
        self.SETTINGS.setAttribute( QWebSettings.DeveloperExtrasEnabled, True ); #
        self.SETTINGS.setAttribute( QWebSettings.SpatialNavigationEnabled, False );
        self.SETTINGS.setAttribute( QWebSettings.LinksIncludedInFocusChain, True );
        self.SETTINGS.setAttribute( QWebSettings.ZoomTextOnly, False );
        self.SETTINGS.setAttribute( QWebSettings.PrintElementBackgrounds, False );
        self.SETTINGS.setAttribute( QWebSettings.OfflineStorageDatabaseEnabled, True );
        self.SETTINGS.setAttribute( QWebSettings.OfflineWebApplicationCacheEnabled, True );
        self.SETTINGS.setAttribute( QWebSettings.LocalStorageEnabled, True );
        self.SETTINGS.setAttribute( QWebSettings.LocalStorageDatabaseEnabled, True );
        self.SETTINGS.setAttribute( QWebSettings.LocalContentCanAccessRemoteUrls, True );
        self.SETTINGS.setAttribute( QWebSettings.LocalContentCanAccessFileUrls, True );
        self.SETTINGS.setAttribute( QWebSettings.XSSAuditingEnabled, True );
        self.SETTINGS.setAttribute( QWebSettings.AcceleratedCompositingEnabled, True );
        self.SETTINGS.setAttribute( QWebSettings.TiledBackingStoreEnabled, False );
        self.SETTINGS.setAttribute( QWebSettings.FrameFlatteningEnabled, False );
        self.SETTINGS.setAttribute( QWebSettings.SiteSpecificQuirksEnabled, True );

        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

        self.SETTINGS.enablePersistentStorage( self.PARENT.STORAGE_ROOT );
        self.SETTINGS.setLocalStoragePath( self.PARENT.STORAGE_ROOT+"local_storage/" );
        self.SETTINGS.setIconDatabasePath ( self.PARENT.STORAGE_ROOT+"icons_path/" )
        self.SETTINGS.setMaximumPagesInCache ( 10 );

        # FIXME: Create settings config file [TO-CONFIG.FILE]

        self.SETTINGS.setOfflineWebApplicationCachePath( self.PARENT.STORAGE_ROOT+"/cache/" );
        self.SETTINGS.setOfflineWebApplicationCacheQuota ( 25 * 1024 *1024 );

        self.SETTINGS.setOfflineStoragePath( self.PARENT.STORAGE_ROOT );
        self.SETTINGS.setOfflineStorageDefaultQuota ( 25 * 1024 *1024 );
        #self.SETTINGS.setObjectCacheCapacities (int cacheMinDeadCapacity, int cacheMaxDead, int totalCapacity)

        # -------------------------------------------------------------------
        self.INSPECTOR    = QWebInspector( None );

        """
        __init__ (self, QWidget parent = None)
        closeEvent (self, QCloseEvent event)
        bool event (self, QEvent)
        hideEvent (self, QHideEvent event)
        QWebPage page (self)
        resizeEvent (self, QResizeEvent event)
        setPage (self, QWebPage page)
        showEvent (self, QShowEvent event)
        QSize sizeHint (self)
        """

        # -------------------------------------------------------------------
        self.INIT();
        # -------------------------------------------------------------------

    # =======================================================================
    def INIT( self ):

        # -------------------------------------------------------------------
        self.HEADERS["User-Agent"] = self.USER_AGENT;

        # -------------------------------------------------------------------

    # =======================================================================
    def POST_INIT( self ):

        # -------------------------------------------------------------------
        self.PROGRESS_BAR = QFrame( self.PARENT.WEB_VIEWS[ self.UID ]["WEB_VIEW"] );
        self.PROGRESS_BAR.setStyleSheet( "QFrame{ background-color: #F00; }" );
        self.PROGRESS_BAR.setGeometry( 0, 0, 0, 5 );
        # -------------------------------------------------------------------

    # =======================================================================
    def EXEC_JS( self, _JS ):

        # -------------------------------------------------------------------
        #frame = self.PARENT.WEB_VIEW.page().mainFrame();
        #frame = self.mainFrame();
        #frame.evaluateJavaScript( _JS );
        
        self.mainFrame().evaluateJavaScript( _JS.encode("utf-8") );
        
        # -------------------------------------------------------------------

    # =======================================================================
    def GET_EXTENTIONS( self ):

        # -------------------------------------------------------------------
        #supportsExtension();
        pass;
        # -------------------------------------------------------------------

    # =======================================================================
    def GET_META_DATA( self ):

        # -------------------------------------------------------------------
        print( "GET_META_DATA:" );

        frame = self.mainFrame();

        meta_data =frame.metaData(); #dict-of-QString-list-of-QString metaData

        for meta in meta_data:
            print(meta);

        # -------------------------------------------------------------------

    # =======================================================================
    def GET_PAGE_HTML( self ):

        # -------------------------------------------------------------------
        frame = self.mainFrame();
        return unicode(frame.toHtml()).encode('utf-8');

        # -------------------------------------------------------------------

    # =======================================================================
    def GET_PAGE_TITLE( self ):

        # -------------------------------------------------------------------
        return str(self.mainFrame().title());

        # -------------------------------------------------------------------

    # =======================================================================
    def CMD( self, _CMD ):

        # -------------------------------------------------------------------
        #__exec:page:exec:js:function_name

        # -------------------------------------------------------------------
        try:
    
            # -----------------------------------------------
            if _CMD[0] == "exec":
                if _CMD[1] == "js":

                    self.EXEC_JS( "".join(_CMD[2:]) );
                    self.LOCAL_INFO_LOG( str(_CMD) );
                    return True;

            # -----------------------------------------------
            elif _CMD[0] == "set":
                if _CMD[1] == "user-agent":

                    self.USER_AGENT = "".join(_CMD[2:]).replace('\"', '\\"').replace("\'", "\\'");
                    self.EXEC_JS( "alert('set:user-agent:"+self.USER_AGENT+"');" );
                    self.LOCAL_INFO_LOG( str(_CMD) );
                    return True;

            # -----------------------------------------------
            elif _CMD[0] == "get":
                if _CMD[1] == "user-agent":

                    self.EXEC_JS( "alert('get:user-agent:"+self.USER_AGENT+"');" );
                    self.LOCAL_INFO_LOG( str(_CMD) );
                    return True;

            # -----------------------------------------------

            self.LOCAL_ERROR_LOG( "UNKNOWN: "+str(_CMD)+" CMD" );                    
            return False;

            # -----------------------------------------------

        except Exception as _err:
            self.LOCAL_ERROR_LOG( str(_CMD)+": "+str(_err) );
            return False;
    
        # -------------------------------------------------------------------

    # =======================================================================
    def AAA_user_BBB_AgentForUrl( self, _url ):

        # -------------------------------------------------------------------
        # Chrome Win/NT 32 Doc-Browser');

        #print("-------------------------------------------------------------")
        #_ByteArray = QUrl.toPercentEncoding( _url.toString(), "{}", " ");
       
        #encoded_url = str( _url.encodedQuery() )
        #print( encoded_url );


        """
        print( "authority(): "+str( _url.authority() ) );
        print( "encodedHost(): "+str( _url.encodedHost() ) );
        print( "encodedPath(): "+str( _url.encodedPath() ) );
        print( "encodedQuery(): "+str( _url.encodedQuery() ) );
        
        print( "encodedUserName(): "+str( _url.encodedUserName() ) );
        print( "host(): "+str( _url.host() ) );
        print( "isLocalFile(): "+str( _url.isLocalFile() ) );
        print( "path(): "+str( _url.path() ) );
        print( "port(): "+str( _url.port() ) );
        print( "userInfo(): "+str( _url.userInfo() ) );
        print( "userName(): "+str( _url.userName() ) );
        print( "topLevelDomain(): "+str( _url.topLevelDomain() ) );
        print( "toString(): "+str( _url.toString() ) );
        """


        #print("-------------------------------------------------------------")
        return self.USER_AGENT;
        # -------------------------------------------------------------------

    # =======================================================================
    def REPAINT_REQUESTED ( self, _QRect ): #repaintRequested (const QRect&)

        # -------------------------------------------------------------------
        print("NOT-IMPLEMENTED: repaintRequested (const QRect&):");
        # -------------------------------------------------------------------
    
    # =======================================================================
    def SHOW_INSPECTOR( self ):

        # -------------------------------------------------------------------
        self.INSPECTOR.setPage( self );


        self.INSPECTOR.setGeometry( 0,0, 800, 450 );
        self.INSPECTOR.show( );
        #self.INSPECTOR.showMaximized( );

        toolbar_items = [
            ".elements", ".resources", ".network", ".scripts", 
            ".timeline", ".profiles", ".audits", ".console"
        ];

        self.mainFrame().evaluateJavaScript("""
            document.addEventListener('DOMContentLoaded',function(){
                setTimeout(function(){
                    document.querySelector('.toolbar-item.network').click()
                }, 2000);
            });
        """);

        # -------------------------------------------------------------------

    # =======================================================================
    def ON_LINK_HOVERED(self, _url_A, _url_B, _url_C ): # (const QString&,const QString&,const QString&)

        # -------------------------------------------------------------------
        #print( "ON_LINK_HOVERED: "+self.UID+": ["+str(_url_A)+"]" );
        
        self.PARENT.STATUS_BAR.setText( unicode(str(_url_A)) );
        # -------------------------------------------------------------------

    # =======================================================================
    def ON_LINK_CLICKED(self, _url):

        # -------------------------------------------------------------------
        _url = unicode( str(_url.toString()).replace("file://", "") );

        # -------------------------------------------------------------------
        #print("ON_LINK_CLICKED: "+self.UID );

        if self.M_BTN_CLICK:
            self.PARENT.CREATE_TAB( _url );
            self.PARENT.URL_BAR.SET_TEXT( _url );

        else:
            self.PARENT.URL_BAR.SET_TEXT( _url );
            self.PARENT.GO_TO_URL();


        self.PARENT.HISTORY_HANDLER.hide();
        # -------------------------------------------------------------------
        #toAscii();
        #toUtf8();
        #toLatin1();
        #toLocal8Bit();
        self.L_BTN_CLICK = False;
        self.M_BTN_CLICK = False;
        self.R_BTN_CLICK = False;
        # -------------------------------------------------------------------

    # =======================================================================
    def ON_PAGE_LOAD_PROGRESS(self, _int_pr):

        # -------------------------------------------------------------------
        if _int_pr >= 100:

            if self.PARENT.CURRENT_TAB_BAR_UID == self.UID:
                self.PARENT.LOADING_BAR.setText( "Loading: Done." );
            self.PROGRESS_BAR_W = 0;


        else:

            if self.PARENT.CURRENT_TAB_BAR_UID == self.UID:
                self.PARENT.LOADING_BAR.setText( "Loading: ["+str(_int_pr)+"]" );

            self.PROGRESS_BAR_W = self.PROGRESS_BAR_PR * _int_pr;

        self.PROGRESS_BAR.setGeometry( 0, 0, self.PROGRESS_BAR_W, 5 );
        # -------------------------------------------------------------------

    # =======================================================================
    def SEARCH_INPUT_CTRL( self, _action ):

        # -------------------------------------------------------------------
        if _action == "show":
            self.SEARCH_INPUT_IS_OPEN = True;
            self.SEARCH_INPUT.setFocus();
            self.SEARCH_INPUT.show();

        else:
            self.SEARCH_INPUT_IS_OPEN = False;
            self.SEARCH_INPUT.clearFocus();
            self.SEARCH_INPUT.hide();
        # -------------------------------------------------------------------

    # =======================================================================
    def FIND_ON_PAGE(self):

        # -------------------------------------------------------------------
        #print("FIND_ON_PAGE: "+self.UID );

        try:

            self.SEARCH_INPUT.setFocus();
            self.SEARCH_INPUT_CTRL("show");

            _value = unicode( str(self.SEARCH_INPUT.text()).strip() );

            #findText (self, QString subString, FindFlags options = 0)
            self.findText (_value, QWebPage.FindWrapsAroundDocument);

            # QWebPage.HighlightAllOccurrences

        except Exception as _err:
            self.LOCAL_ERROR_LOG( str(_err) );

        # -------------------------------------------------------------------

    # =======================================================================
    def PRINT( self ):

        # -------------------------------------------------------------------
        try: 

            pdf_name = self.GET_PAGE_TITLE()+"_"+str(self.PARENT.GET_TIME(True))+"_";
            pdf_name = pdf_name.replace( " ", "-" ).replace( ":", "-" )+".pdf";

            self.PRINTER = QPrinter( QPrinter.ScreenResolution );
            self.PRINTER.setFontEmbeddingEnabled( False );
            self.PRINTER.setFullPage( True );
            #self.PRINTER.setPrinterName ("name of printer");
            #self.PRINTER.setPrintProgram ( "print program");

            self.PRINTER.setOutputFileName ( self.PARENT.DOWNLOAD_DIR+pdf_name );

            # ------ >
            #self.PRINTER.setOutputFormat( QPrinter.NativeFormat ); # <= IMAGE
            self.PRINTER.setOutputFormat( QPrinter.PdfFormat ); # <= TEXT
            #self.PRINTER.setOutputFormat( QPrinter.PostScriptFormat ); # ???

            #QPrinter will print output using a method defined by the platform it is running on. 
            # This mode is the default when printing directly to a printer.
            #QPrinter.NativeFormat [0]   
            
            #QPrinter will generate its output as a searchable PDF file. This mode is the default when printing to a file.
            #QPrinter.PdfFormat [1]   

            #QPrinter will generate its output as in the PostScript format. (This feature was introduced in Qt 4.2.)
            #QPrinter.PostScriptFormat [2]

            self.mainFrame().print_( self.PRINTER );

            self.LOCAL_INFO_LOG( "PDF: Saved ["+str(self.PARENT.DOWNLOAD_DIR+pdf_name)+"]" );


        except Exception as _err:
            self.LOCAL_ERROR_LOG( str(_err) );

        # -------------------------------------------------------------------

    # =======================================================================
    def SEND_ESC( self ):

        # -------------------------------------------------------------------
        #print("SEND_ESC: START");
        js = '''
                
            try{

                var e = document.createEvent('KeyboardEvent');
                e.initKeyboardEvent("keyup", true, true, window, 0,0,0,0,0, 27,0 );
                document.dispatchEvent(e);

                var e = document.createEvent('KeyboardEvent');
                e.initKeyboardEvent("keydown", true, true, window, 0,0,0,0,0, 27,0 );
                document.dispatchEvent(e);

                var e = document.createEvent('KeyboardEvent');
                e.initKeyboardEvent("keypress", true, true, window, 0,0,0,0,0, 27,0 );
                document.dispatchEvent(e);



            }catch(e){
                alert(e);
            }

        '''


        # -------------------------------------------------------------------
        self.mainFrame().evaluateJavaScript( js );
        #print("SEND_ESC: DONE");
        # -------------------------------------------------------------------

    # =======================================================================
    def event( self, _evt ):

        # -------------------------------------------------------------------
        #self.L_BTN_CLICK = False;
        #self.M_BTN_CLICK = False;
        #self.R_BTN_CLICK = False;

        # -------------------------------------------------------------------
        # http://pyqt.sourceforge.net/Docs/PyQt4/qevent.html#Type-enum
        #print( _evt.type() );
        # -------------------------------------------------------------------
        #if _evt.type() == QEvent.FocusOut:      # (QFocusEvent) == 9 == focus OUT BY CLICK
        #elif _evt.type() == QEvent.FocusIn:     # (QFocusEvent) == 8 == focus IN BY CLICK

        # -------------------------------------------------------------------
        #if _evt.type() == QEvent.ContextMenu:   # (QContextMenuEvent) == 82

        # -------------------------------------------------------------------
        #QEvent.MouseButtonDblClick  4   Mouse press again (QMouseEvent).
        #QEvent.MouseButtonRelease   3   Mouse release (QMouseEvent).
        #QPoint _evt.globalPos(); | int _evt.global[X|Y](); | QPoint _evt.pos(); | QPointF _evt.posF(); | int _evt.[x|y]()
        #_evt.button() == ( Qt.LeftButton | Qt.RightButton | Qt.MidButton )
        if _evt.type() == QEvent.MouseButtonPress: # 2   Mouse press (QMouseEvent).

            #print( "WEB_PAGE["+str(self.UID)+"].event:" );
            if _evt.button() == Qt.LeftButton:
                #print("Qt.LeftButton: "+str(Qt.LeftButton))
                self.L_BTN_CLICK = True;

            elif _evt.button() == Qt.MidButton:
                #print("Qt.MidButton: "+str(Qt.MidButton))
                self.M_BTN_CLICK = True;
            
            elif _evt.button() == Qt.RightButton:
                #print("Qt.RightButton: "+str(Qt.RightButton))
                self.R_BTN_CLICK = True;

        # -------------------------------------------------------------------
        """
        #QEvent.KeyPress 6   Key press (QKeyEvent).
        #QEvent.KeyRelease   7   Key release (QKeyEvent).
        if _evt.type() == QEvent.KeyRelease:
            print("KeyRelease: ["+str(_evt.text())+", "+str(_evt.nativeScanCode())+", "+str(_evt.key())+"]");

        int count (self)
        bool isAutoRepeat (self)
        int key (self)
        bool matches (self, QKeySequence.StandardKey key)
        Qt.KeyboardModifiers modifiers (self)
        int nativeModifiers (self)
        int nativeScanCode (self)
        int nativeVirtualKey (self)
        QString text (self)
        """

        # -------------------------------------------------------------------

        """
        if _evt.type() == QEvent.Enter:         # 10

            self.setStyleSheet( self.STL["hovered"] );
            self.HAS_FOCUS = True;

        elif _evt.type() == QEvent.Leave:       # 11 

            self.setStyleSheet( self.STL["default"] );
            self.HAS_FOCUS = False;
        """

        # -------------------------------------------------------------------
        return QWebPage.event(self, _evt);
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





