function simulateKeyPress() {
    var evt = document.createEvent("KeyboardEvent");
    
    evt.initKeyEvent (
        "keypress", true, true, window, 0, 0, 0, 0, 0, 27 // <= 27 == ESCAPE
    );

    var canceled = !body.dispatchEvent(evt);

    if(canceled) {
        // A handler called preventDefault
        alert("canceled");
    } else {
        // None of the handlers called preventDefault
        alert("not canceled");
    }
}

function simulateKeyPress();
