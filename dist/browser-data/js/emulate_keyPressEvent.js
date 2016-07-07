function test() {
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

}


function simulateKeyPress() {
    
    var evt = document.createEvent("KeyboardEvent");
    
    evt.initKeyEvent (
        "keypress", true, true, window, 0, 0, 0, 0, 27, 0
    );

    var canceled = document.body.dispatchEvent(evt);

    if(canceled) {
        // A handler called preventDefault
        alert("canceled");
    } else {
        // None of the handlers called preventDefault
        alert("not canceled");
    }
}

simulateKeyPress();

// ===========================================================================================
document.createEvent("KeyBoardEvent").initKeyEvent("keypress",true, true, window, false, false, false, false, 40, 0);
// ===========================================================================================
var event = document.createEvent('KeyboardEvent'); // create a key event

// define the event
event.initKeyEvent(
                    "keypress",  // typeArg,                                                           
                    true,        // canBubbleArg,                                                        
                    true,        // cancelableArg,                                                       
                    null,        // viewArg,  Specifies UIEvent.view. This value may be null.     
                    false,       // ctrlKeyArg,                                                               
                    false,       // altKeyArg,                                                        
                    false,       // shiftKeyArg,                                                      
                    false,       // metaKeyArg,                                                       
                    9,           // keyCodeArg,                                                      
                    0            // charCodeArg);
                );

document.getElementById('blah').dispatchEvent(event);

// ===========================================================================================
CORRECT-WAY: ===>>>

var e = document.createEvent('KeyboardEvent');
e.initKeyboardEvent("keyup", true, true, window, 0,0,0,0,0, 27,0 );
document.dispatchEvent(e);

// ===========================================================================================
var element = document.getElementById("elementID");

// END KEY
var e = document.createEvent('KeyboardEvent');
e.initKeyEvent('keydown', true, true, window, false, false, false, false, 35, 0);
document.dispatchEvent(e);

var e = document.createEvent('KeyboardEvent');
e.initKeyEvent('keyup', true, true, window, false, false, false, false, 35, 0);
element.dispatchEvent(e);

// ARROW DOWN KEY
var e = document.createEvent('KeyboardEvent');
e.initKeyEvent('keydown', true, true, window, false, false, false, false, 40, 0);
element.dispatchEvent(e);

var e = document.createEvent('KeyboardEvent');
e.initKeyEvent('keyup', true, true, window, false, false, false, false, 40, 0);
element.dispatchEvent(e);

//ENTER KEY
var e = document.createEvent('KeyboardEvent');
e.initKeyEvent('keydown', true, true, window, false, false, false, false, 13, 0);
element.dispatchEvent(e);

var e = document.createEvent('KeyboardEvent');
e.initKeyEvent('keyup', true, true, window, false, false, false, false, 13, 0);
element.dispatchEvent(e);
// ===========================================================================================
