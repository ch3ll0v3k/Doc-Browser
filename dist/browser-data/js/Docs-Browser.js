// Docs-Browser.js
// =================================================================================
var BODY;
var quick_link_box;
var mDate = new Date();

// =================================================================================
window.addEventListener('load', function(){

    //var x = document.getElementById("elem");
    BODY = document.body;
    quick_link_box = _byId("quick-link-box");

    var LINKS =[
        "/m-sys/",
        "https://stackoverflow.com/",
        "https://youtube.com/",
        "http://pyqt.sourceforge.net/Docs/PyQt4/qlineedit.html",
        "http://programmersforum.ru",
        "http://habrahabr.ru/",
        "http://geektimes.ru",
        "https://www.exploit-db.com/exploits/15684/",
        "http://www.radiolibrary.ru/reference/transistor/kt315g.html",
        "http://www.md4u.ru/viewtopic.php?f=80&t=3156",
        "https://news.ycombinator.com/news",
        "http://forum.cxem.net/index.php?showtopic=163780#entry2419524",
        "http://4pda.ru/forum/index.php?showtopic=533229&st=40#entry49774993",
        "http://radiokot.ru/forum/viewtopic.php?f=11&t=54135&sid=b65263b7bc269c5bf21ae102f899211f&start=20",
        "http://pdalife.ru",
    ];

    var link = 
        '<a id="LINK_ID" href="LINK_HREF" title="LINK_TITLE">'
            +'<div class="quick-link-holder">'
                +'<div class="quick-link">'
                    +'<img class="quick-link-img" src="./data/LINK_IMAGE"/>'
                +'</div>'

                //+'<div class="quick-link-descr">title</div>'

            +'</div>'
        +'</a>';

    var html = "";
    var i = 0;

    for( ; i<LINKS.length; i++ ){

        html += link
            .replace( "LINK_ID", "link_"+i )
            .replace( "LINK_HREF", LINKS[i] )
            .replace( "LINK_IMAGE", "LINK_"+i+".png?t="+mDate.getTime() )
            .replace( "LINK_TITLE", LINKS[i] );

    }


    if( i < 23){

        html += link
            .replace( "ADD", "" )
            .replace( "LINK_HREF", "file:///__exec:home_page:favorites:add" )
            .replace( "LINK_IMAGE", "plus.png?t="+mDate.getTime() )
            .replace( "LINK_TITLE", "Add New" );
        
    }


    quick_link_box.innerHTML = html;

    /*
    BODY.style.width = WIDTH+"px";
    BODY.style.height = HEIGHT+"px";
    */
    console.log("Docs-Browser: Loadet!");

});

// =================================================================================

















// =================================================================================
