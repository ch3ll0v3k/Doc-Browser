// ================================================================================
/*
lib v1.0.0

*/
// ================================================================================
window.addEventListener('load', function(){

    _log("temax-main.js: loaded");

});

// ================================================================================
function pageLoader(){

    // ----------------------------------------------------------------------------
    // Page Loader
    setTimeout(function(){

        _getById('page_loader_bol').style.display = 'none'; 
        _getById('page_loader_box').style.display = 'none'; 

        try{
            _getById('level_editor_wrapper').style.display  = 'block';
        }catch(e){}

        try{
            _getById('animation_editor_wrapper').style.display  = 'block';
        }catch(e){}
        
        PAGE_LOADET();

    }, 500);
    // ----------------------------------------------------------------------------
    /*
    <div id="page_loader_bol"></div>
    <div id="page_loader_box">
        <div id="page_loader_img"></div>
        <div id="page_loader_text"></div>
        <div id="page_loader_white_balk_"></div>
    </div>
    */
    // ----------------------------------------------------------------------------
}

// ================================================================================
function _log(toLog){ console.log(toLog); }
function _dir(method){ console.log(console.dir(method)); }
function _byId(id){ return document.getElementById(id); }
function _byName(name){ return document.getElementsByName(name); }
function _byClass(className){ return document.getElementsByClassName(className); }
function _byTag(tagName){ return document.getElementsByTagName(tagName); }
function _newElem(type){ return document.createElement(type); }
function _randInt(min, max){ return Math.floor(Math.random() * (max - min + 1)) + min;  }

// ================================================================================
function getRandomID(L){

    var ID = '';
    var L = L ? L : 12;
    var data = new Array('a', 'b', 'c', 'd', 'e', 'f', 'A', 'B', 'C', 'D','F', 'F', 'O', 'B', 'e', '9', '0', '7', '6', '3', '2', '5', '8', '1', '4' );
    for(var i=0; i<L;i++){
        ID += data[__GRIT(0, 24)];
    }
    return ID+'_';
}

// ================================================================================
function simulateKeyPress() {
    try{

        var e = document.createEvent('KeyboardEvent');
        e.initKeyboardEvent("keyup", true, true, window, 0,0,0,0,0, 27,0 ); // <= 27 == ESC
        document.dispatchEvent(e);

        var e = document.createEvent('KeyboardEvent');
        e.initKeyboardEvent("keydown", true, true, window, 0,0,0,0,0, 27,0 ); // <= 27 == ESC
        document.dispatchEvent(e);

        var e = document.createEvent('KeyboardEvent');
        e.initKeyboardEvent("keypress", true, true, window, 0,0,0,0,0, 27,0 ); // <= 27 == ESC
        document.dispatchEvent(e);

    }catch(e){
        alert(e);
    }

}

// ================================================================================
function getXmlHttp(){

    var xmlHTTH;

    try{ 
        xmlHTTH = new ActiveXObject("MSXML2.XMLHTTP");

    }catch (e){

        try { 
            xmlHTTH = new ActiveXObject("Microsoft.XMLHTTP"); 

        }catch (e){ 
            xmlHTTH = new XMLHttpRequest(); 

        } 
    }

    return xmlHTTH;

}

// ================================================================================
function ajaxPOST(PostData){
    // -------------------------------------------
    var PostData = '';
        PostData += 'login=name';
        PostData += '&password=12345';

        //PostData = encodeURIComponent(PostData);
        //alert(encodeURIComponent(PostData));
        //alert(encodeURI(PostData));    
    // -------------------------------------------
    var _AJAX_ = getXmlHttp();
    // -------------------------------------------
    _AJAX_.open('POST',url, true); // false ASYNC         
    // -------------------------------------------
    //_AJAX_.setRequestHeader("Custom_name", "custom_data");
    //_AJAX_.setRequestHeader("Content-Type", "multipart/form-data");
    _AJAX_.setRequestHeader("Content-Type", "text/html");
    _AJAX_.setRequestHeader("Content-length", PostData.length);
    _AJAX_.setRequestHeader('Content-type','application/x-www-form-urlencoded');
    // -------------------------------------------
    _AJAX_.onreadystatechange = function () {
        if(_AJAX_.readyState == 4 && _AJAX_.status == 200){
            // ---------------------------------------------------------
            // var seconds = new Date().getTime() / 1000;
            // var time = new Date().getTime();

            // _AJAX_.getAllResponseHeaders();      // 
            // _AJAX_.getResponseHeader('name');    // 
            // _AJAX_.readyState                    // == 4
            // _AJAX_.status                        // == 200
            // _AJAX_.responseText                  // == text response
            // ---------------------------------------------------------
        }
    }
    // -------------------------------------------
    _AJAX_.send(PostData);
}
// ================================================================================
function ajaxGET(url) {
    // -------------------------------------------
    var _AJAX_ = getXmlHttp();
    // -------------------------------------------
    _AJAX_.open('GET',url, true); // false SYNC
    _AJAX_.setRequestHeader('_status_', 'custom-data');
    // -------------------------------------------
    _AJAX_.onreadystatechange = function () {
        if(_AJAX_.readyState == 4 && _AJAX_.status == 200){
            // ---------------------------------------------------------
            // var seconds = new Date().getTime() / 1000;
            // var time = new Date().getTime();

            // _AJAX_.getAllResponseHeaders();      // 
            // _AJAX_.getResponseHeader('name');    // 
            // _AJAX_.readyState                    // == 4
            // _AJAX_.status                        // == 200
            // _AJAX_.responseText                  // == text response
            // ---------------------------------------------------------
        }
    }
    // -------------------------------------------
    _AJAX_.send(null);
}
// ================================================================================