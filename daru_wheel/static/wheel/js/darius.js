    // Correctly decide between ws:// and wss://
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var ws_path = ws_scheme + '://' + window.location.host + "/ispin_wheel/";
    console.log("Connecting to " + ws_path);


    const spinSocket = new WebSocket(ws_path);

    spinSocket.onmessage = function(e) {
        
        const data = JSON.parse(e.data);

        // console.log(data.ipointer)
        if (data.ipointer == 777){
            alert('Place a Bet to Spin!Select RED or YELLOW, Enter amount and click BET.Click on Real Cash button to use real money.Finally click SPIN.');
        }

        if (data.ipointer<30){
            startSpinB(data.ipointer);
        } 
    };

    spinSocket.onclose = function(e) {
        console.error('spin socket closed unexpectedly');
    };


    document.querySelector('#spin_button').onclick = function(e) {
        // const pointerInputDom = document.querySelector('#spin-pointer-input');
        const ipointer = '';
        spinSocket.send(JSON.stringify({
            'ipointer': ipointer
        }));
        // pointerInputDom.value = '';
    };

// Create new wheel object specifying the parameters at creation time.
let theWheel = new Winwheel({
    'outerRadius'     : 212,        // Set outer radius so wheel fits inside the background.
    'innerRadius'     : 45,   
    'responsive'      : false, // Make wheel hollow so segments don't go all way to center.
    'textFontSize'    : 24,         // Set default font size for the segments.
    'textOrientation' : 'vertical', // Make text vertial so goes down from the outside of wheel.
    'textAlignment'   : 'outer',    // Align text to outside of wheel.
    'numSegments'     : 28,         // Specify number of segments.
    'segments'        :             // Define segments including colour and text.
    [                               // font size and test colour overridden on backrupt segments.

        {'fillStyle' : '#fff200', 'text' : ''},
        {'fillStyle' : '#ee1c24', 'text' : ''},
        {'fillStyle' : '#fff200', 'text' : ''},
        {'fillStyle' : '#ee1c24', 'text' : ''},
        {'fillStyle' : '#fff200', 'text' : ''},

        {'fillStyle' : '#ee1c24', 'text' : ''},
        {'fillStyle' : '#fff200', 'text' : ''},
        {'fillStyle' : '#ee1c24', 'text' : ''},
        {'fillStyle' : '#fff200', 'text' : ''},
        {'fillStyle' : '#ee1c24', 'text' : ''},

        {'fillStyle' : '#fff200', 'text' : ''},
        {'fillStyle' : '#ee1c24', 'text' : ''},
        {'fillStyle' : '#ffffff', 'text' :  'Big Win', 'textFontSize' : 16, 'textFillStyle' : '#00000'},// WHITE
        {'fillStyle' : '#ee1c24', 'text' : ''},
        {'fillStyle' : '#fff200', 'text' : ''},

        {'fillStyle' : '#ee1c24', 'text' : ''},
        {'fillStyle' : '#fff200', 'text' : ''},
        {'fillStyle' : '#ee1c24', 'text' : ''},
        {'fillStyle' : '#fff200', 'text' : ''},
        {'fillStyle' : '#ee1c24', 'text' : '', 'textFontSize' : 12, 'textFillStyle' : '#e70697'},

        {'fillStyle' : '#fff200', 'text' : '', 'textFontSize' : 16, 'textFillStyle' : '#3cb878'},
        {'fillStyle' : '#ee1c24', 'text' : ''},                  
        {'fillStyle' : '#fff200', 'text' : ''},
        {'fillStyle' : '#ee1c24', 'text' : ''},
        {'fillStyle' : '#fff200', 'text' : ''},

        {'fillStyle' : '#ee1c24', 'text' : ''},
        {'fillStyle' : '#fff200', 'text' : ''},
        
        {'fillStyle' : '#000000', 'text' : 'LOOSE TURN', 'textFontSize' : 12, 'textFillStyle' : '#3cb878'},


    ],
    'animation' :           // Specify the animation to use.
    {
        'type'     : 'spinToStop',
        'duration' : 15,    // Duration in seconds.
        'spins'    : 6,     // Default number of complete spins.
        // 'callbackFinished' : alertPrize,
        'callbackSound'    : playSound,   // Function to call when the tick sound is to be triggered.
        'soundTrigger'     : 'pin'   ,     // Specify pins are to trigger the sound, the other option is 'segment'.
        // 'callbackAfter' : 'drawTriangle()'
    },
    'pins' :				// Turn pins on.
    {
        'number'     : 28,
        'fillStyle'  : 'silver',
        'outerRadius': 4,
    }
});

// Loads the tick audio sound in to an audio object.
let audio = new Audio('/static/wheel/sounds/ticko.mp3');

// This function is called when the sound is to be played.
function playSound()
{
    // Stop and rewind the sound if it already happens to be playing.
    audio.pause();
    audio.currentTime = 0;

    // Play the sound.
    audio.play();
}

// Vars used by the code in this page to do power controls.
let wheelPower    = 10;
let wheelSpinning = false;


function startSpin()
{ 
    if (wheelSpinning == false) {
    // Stop any current animation.
    theWheel.stopAnimation(false);
    // Reset the rotation angle to less than or equal to 360 so spinning again
    // works as expected. Setting to modulus (%) 360 keeps the current position.
    theWheel.rotationAngle = 0;//theWheel.rotationAngle % 360;
    // Start animation.
    theWheel.startAnimation();
    wheelSpinning = true;
    }

}

function startSpinB(seg){
    if (wheelSpinning == false) {

    theWheel.stopAnimation(false);
    theWheel.rotationAngle = 0;
    segmentNumber = seg;
    let stopAt = theWheel.getRandomForSegment(segmentNumber);
    theWheel.animation.stopAngle = stopAt;

    theWheel.startAnimation();
    wheelSpinning = true;

    }
    }
