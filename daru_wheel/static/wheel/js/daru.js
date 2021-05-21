 // Correctly decide between ws:// and wss://
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var ws_path = ws_scheme + '://' + window.location.host + "/daru_wheel/";
    console.log("Connecting to " + ws_path);


    const spinSocket = new WebSocket(ws_path);    


        spinSocket.onmessage = function(e) {
            
            const data = JSON.parse(e.data);


            if (data.pointer){
                
                // console.log(data.pointer)

                startSpinB(data.pointer);
   
            }
            if (data.secondvalu){
                
                // console.log(data.secondvalu)
                var minn = (data.secondvalu/60).toPrecision(1);
                var secc = minn*60
                var secc = data.secondvalu;

                document.getElementById('dtim').textContent =data.secondvalu;
                document.getElementById('dmin').textContent =minn;
                // document.getElementById('dsec').textContent = data.secondvalu -secc;   
 
            }
            if (data.market){
              //  console.log(data.mssg);
               const mrkt = data.market;
               document.getElementById('market').textContent = mrkt;
            }

                 
            // document.querySelector('#spin-log').value += (data.pointer + '\n');
        };

        spinSocket.onclose = function(e) {
            console.error('spin socket closed unexpectedly');
        };

        // document.querySelector('#spin-pointer-input').focus();
        
        // document.querySelector('#spin-pointer-input').onkeyup = function(e) {
        //     if (e.keyCode === 13) {  // enter, return
        //         document.querySelector('#spin-pointer-submit').click();
        //     }
        // };

        // document.querySelector('#spin-pointer-submit').onclick = function(e) {
        //     const pointerInputDom = document.querySelector('#spin-pointer-input');
        //     const pointer = pointerInputDom.value;
        //     spinSocket.send(JSON.stringify({
        //         'pointer': pointer
        //     }));
        //     pointerInputDom.value = '';
        // };

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

            {'fillStyle' : '#fff200', 'text' : 'x2'},
            {'fillStyle' : '#ee1c24', 'text' : 'x2'},
            {'fillStyle' : '#fff200', 'text' : 'x2'},
            {'fillStyle' : '#ee1c24', 'text' : 'x2'},
            {'fillStyle' : '#fff200', 'text' : 'x2'},

            {'fillStyle' : '#ee1c24', 'text' : 'x2'},
            {'fillStyle' : '#fff200', 'text' : 'x2'},
            {'fillStyle' : '#ee1c24', 'text' : 'x2'},
            {'fillStyle' : '#fff200', 'text' : 'x2'},
            {'fillStyle' : '#ee1c24', 'text' : 'x2'},

            {'fillStyle' : '#fff200', 'text' : 'x2'},
            {'fillStyle' : '#ee1c24', 'text' : 'x2'},
            {'fillStyle' : '#ffffff', 'text' :  'AVARAGE', 'textFontSize' : 16, 'textFillStyle' : '#00000'},// WHITE
            {'fillStyle' : '#ee1c24', 'text' : 'x2'},
            {'fillStyle' : '#fff200', 'text' : 'x2'},

            {'fillStyle' : '#ee1c24', 'text' : 'x2'},
            {'fillStyle' : '#fff200', 'text' : 'x2'},
            {'fillStyle' : '#ee1c24', 'text' : 'x2'},
            {'fillStyle' : '#fff200', 'text' : 'x2'},
            {'fillStyle' : '#ee1c24', 'text' : 'x2'},

            {'fillStyle' : '#fff200', 'text' : 'x2'},
            {'fillStyle' : '#ee1c24', 'text' : 'x2'},                  
            {'fillStyle' : '#fff200', 'text' : 'x2'},
            {'fillStyle' : '#ee1c24', 'text' : 'x2'},
            {'fillStyle' : '#fff200', 'text' : 'x2'},

            {'fillStyle' : '#ee1c24', 'text' : 'x2'},
            {'fillStyle' : '#fff200', 'text' : 'x2'},
            
            {'fillStyle' : '#000000', 'text' : 'BLACK HOLE', 'textFontSize' : 12, 'textFillStyle' : '#ffffff'},
            

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
    let audio = new Audio('/static/wheel/sounds/tick.mp3');

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
        // Stop any current animation.
        theWheel.stopAnimation(false);
        // Reset the rotation angle to less than or equal to 360 so spinning again
        // works as expected. Setting to modulus (%) 360 keeps the current position.
        theWheel.rotationAngle = 0;//theWheel.rotationAngle % 360;
        // Start animation.
        theWheel.startAnimation();

    }

    function startSpinB(seg){
        theWheel.stopAnimation(false);
        theWheel.rotationAngle = 0;
        segmentNumber = seg;
        let stopAt = theWheel.getRandomForSegment(segmentNumber);
        theWheel.animation.stopAngle = stopAt;

        theWheel.startAnimation();
        
        }