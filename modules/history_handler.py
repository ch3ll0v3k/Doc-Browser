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

class History_List_Item( QListWidgetItem ):

    # =======================================================================
    def __init__(self, _data, parent=None):

        # -------------------------------------------------------------------
        QListWidgetItem.__init__(self, parent);

        # -------------------------------------------------------------------
        self.LOG_TAG                                = str(self.__class__.__name__).upper();
        self.DEBUG                                  = False;

        #self.setBackground(QBrush brush);
        #self.setBackgroundColor( QColor("#000") );
        #self.setTextColor( QColor("#FFF") );
        self.setText( _data );
        #self.setIcon( QIcon( parent.PARENT.ICON ) );

        #self.setStyleSheet( "QListWidget{ font: 12px 'monospace'; color: #000; background-color: rbga(0,0,0, 220); border-style: solid; border-width: 5px; border-color: #FFF; }" );


        # -------------------------------------------------------------------

    # =======================================================================

###################################################################################################
class History_Handler( QListWidget ):

    # =======================================================================
    def __init__(self, parent=None):

        # -------------------------------------------------------------------
        QListWidget.__init__(self, parent);

        # -------------------------------------------------------------------
        self.PARENT                                 = parent;
        self.DEBUG                                  = False;
        self.LOG_TAG                                = str(self.__class__.__name__).upper();


        self.FOUND_ITEMS                            = 0;
        self.WIDTH                                  = 800;
        self.MAX_FOUND_ITEMS_DISPLAY                = 20;

        self.ITEMS                                  = [

            "__exec:home",
        ];

        self.ITEMS_TTL_AVAILABLE                    = len( self.ITEMS );


        self.setGeometry(155, 31, self.WIDTH, 300);
        #self.setStyleSheet( 'QListWidget{ background-color: #000: color: #fff; }' );        
        #self.setStyleSheet( 'QListWidget::Item{ background-color: rgba(0,0,0, 170): color: #fff; margin-top: 2px; }' );

        self.setStyleSheet( """ 


                QListView {

                    /* make the selection span the entire width of the view */
                    show-decoration-selected: 1; 
                    background-color: #333; color: #FFffFF;
                    /*
                    border-style: solid; border-width: 4px; border-color: #fff;
                    */

                }

                QListView::item {
                    border-top-style: solid; border-width: 1px; border-color: #555;
                    padding-top: 2px; padding-bottom: 2px; 
                }

                QListView::item:selected {
                    background-color: #000; color: #F00;
                }
                
                QListView::item:selected:active {
                    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #6a6ea9, stop: 1 #888dd9);
                    background-color: #000; color: #0F0;
                }

                /*
                QListView::item:hover {
                    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #FAFBFE, stop: 1 #DCDEF1);
                    background-color: #000; color: #0F0;
                }
                */

                /*
                QListView::item:alternate { }
                QListView::item:selected:!active { background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ABAFE5, stop: 1 #8588B2); }
                */

        """ );

        # -------------------------------------------------------------------

        # events
        #self.returnPressed.connect (self.GO_TO_URL );
        #self.textChanged.connect( self.SEARCH_IN_HISTIRY );
        #self.itemSelectionChanged.connect( self.SELECT_SEACH_VALUE );
        #self.itemClicked.connect( self.SELECT_SEACH_VALUE );

        self.UPDATE_TIMER                       = QTimer();
        self.HAS_FOCUS                          = False;

        # -------------------------------------------------------------------
        self.PARENT.SPLASH.STATUS( self.LOG_TAG+": [INIT]" );

        # -------------------------------------------------------------------
        self.hide();
        # -------------------------------------------------------------------

    # =======================================================================
    def ON_ITEM_CHANGED( self ):

        # -------------------------------------------------------------------
        self.HAS_FOCUS = True;
        selected_value = str(self.currentItem().text()).strip();
        self.PARENT.URL_BAR.SET_TEXT( selected_value );

        # -------------------------------------------------------------------

    # =======================================================================
    def ON_ITEM_SELECTED( self ):

        # -------------------------------------------------------------------
        self.HAS_FOCUS                 = False;
        self.PARENT.URL_BAR.HAS_FOCUS  = False;
        selected_value = str(self.currentItem().text()).strip();

        self.PARENT.URL_BAR.SET_TEXT( selected_value );
        self.clearFocus();
        self.PARENT.GO_TO_URL( );

        # -------------------------------------------------------------------

    # =======================================================================
    def SEARCH(self):

        # -------------------------------------------------------------------
        if self.HAS_FOCUS:
            return;

        self.clear();
        self.FOUND_ITEMS = 0;

        _url_bar_value = str(self.PARENT.URL_BAR.text()).strip().replace("file://", "");

        if _url_bar_value == "":
                return;

        for item in self.ITEMS:
            #print("item: "+item)
            if _url_bar_value in item:
                History_List_Item( item, self );
                self.FOUND_ITEMS += 1;

            if self.FOUND_ITEMS > self.MAX_FOUND_ITEMS_DISPLAY:
                break;

        # -------------------------------------------------------------------
        if self.FOUND_ITEMS > 1:
            self.setGeometry( 155, 31, self.WIDTH, 22*self.FOUND_ITEMS );
            self.show();
            return;
    
        elif self.FOUND_ITEMS == 1:
            self.setGeometry( 155, 31, self.WIDTH, 38 );
            self.show();
            return;
        self.hide();

        # -------------------------------------------------------------------

    # =======================================================================
    def ADD ( self, _item ):

        # -------------------------------------------------------------------
        if unicode(_item) not in self.ITEMS:
            self.ITEMS.append( unicode(_item) );
            return True;

        return False;
        # -------------------------------------------------------------------

    # =======================================================================
    def event(self, event):

        # -------------------------------------------------------------------
        try:

            if event.type() == QEvent.KeyPress:

                _key = str(event.key());

                if _key == "16777235": # |16777235| == arrow_up
                    self.UPDATE_TIMER.singleShot( 10, self.DELAYED_METHOD_CALL );

                elif _key == "16777237": # |16777237| == arrow_down
                    self.UPDATE_TIMER.singleShot( 10, self.DELAYED_METHOD_CALL );

                elif _key == "16777220": # ENTER
                    self.clearFocus();
                    self.ON_ITEM_SELECTED();
                    return True;

            elif event.type() == QEvent.MouseButtonRelease:

                self.ON_ITEM_SELECTED();
                self.clearFocus();
                return True;

            return QListWidget.event(self, event)

        except Exception as _err:
            self.LOCAL_ERROR_LOG( str(_err) );
            return QListWidget.event(self, event)

        # -------------------------------------------------------------------

    # =======================================================================
    def DELAYED_METHOD_CALL( self ):

        # -------------------------------------------------------------------
        # Qlist need some time to set item;
        # Otherwise wrong ITEM-INDEX IS SELECTED
        self.ON_ITEM_CHANGED();

        # -------------------------------------------------------------------

    # =======================================================================
    def mouseReleaseEvent(self, _evt):
        
        # -------------------------------------------------------------------
        #print("mouseReleaseEvent");
        self.ON_ITEM_SELECTED();
        self.clearFocus();
        #return True;
        # -------------------------------------------------------------------

    # =======================================================================
    """
    def focusInEvent (self,  _evt):

        # -------------------------------------------------------------------
        print("focus_IN_Event");
        
        #return QListWidget.event(self, _evt)
        # -------------------------------------------------------------------

    # =======================================================================
    def focusOutEvent (self, _evt):

        # -------------------------------------------------------------------
        print("focus_OUT_Event");
        #return QListWidget.event(self, _evt)
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









