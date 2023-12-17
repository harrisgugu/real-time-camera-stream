// Inside static/js/main.js
const video = document.getElementById('video');
const intervalSlider = document.getElementById('interval');
const fps = document.getElementById('fps');
const startButton = document.getElementById('startButton');
const stopButton = document.getElementById('stopButton'); 
const recordingIndicator = document.getElementById('recordingIndicator');

fps.innerHTML = intervalSlider.value;

intervalSlider.oninput = function() {
    fps.innerHTML = intervalSlider.value;
}


startButton.addEventListener('click', async function() {
    recordingIndicator.style.display = 'block'; 
    data  = {
        fps: fps.innerHTML
    }
    console.log("fps value in start button: ", data.fps)
    const response = await fetch('/start_capture', { 
        method: 'POST' ,
        mode: "cors", // no-cors, *cors, same-origin
        cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
        credentials: "same-origin", // include, *same-origin, omit
        headers: {
        "Content-Type": "application/json",
        },
        body: JSON.stringify(data), // body data type must match "Content-Type" header
    });
    return response.json();
});

stopButton.addEventListener('click', async function() {
    recordingIndicator.style.display = 'none';
    const response = await fetch('/stop_capture', { method: 'POST' });
});

var constraints = { audio: false, video: { width: 1280, height: 720 } };

if (navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(function (stream) {
            video.srcObject = stream;
            video.onloadedmetadata = function (e) {
                video.play();
            }
        })
        .catch(function (err) {
            console.log(err.name + ": " + err.message);
        });
}
