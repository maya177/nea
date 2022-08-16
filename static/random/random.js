URL = window.URL || window.webkitURL;

var gumStream;
var rec; 
var input; 

var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext

var recordButton = document.getElementById("recordButton");
var stopButton = document.getElementById("stopButton");
var pauseButton = document.getElementById("pauseButton");

recordButton.addEventListener("click", startRecording);
stopButton.addEventListener("click", stopRecording);
pauseButton.addEventListener("click", pauseRecording);

function startRecording() {
    console.log("recordButton clicked");
    var constraints = { audio: true, video:false }
    recordButton.disabled = true;
    stopButton.disabled = false;
    pauseButton.disabled = false


    navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
        console.log("success! - initializing Recorder.js");
        audioContext = new AudioContext();
        gumStream = stream;
        input = audioContext.createMediaStreamSource(stream);

        rec = new Recorder(input,{numChannels:1})

        rec.record()
        console.log("Recording started");

    }).catch(function(err) {
        recordButton.disabled = false;
        stopButton.disabled = true;
        pauseButton.disabled = true
    });
}

function pauseRecording(){
    console.log("pauseButton clicked rec.recording=",rec.recording );
    if (rec.recording){
        rec.stop();
        pauseButton.innerHTML="Resume";
    }else{
        rec.record()
        pauseButton.innerHTML="Pause";
    }
}

function stopRecording() {
    console.log("stopButton clicked");
    stopButton.disabled = true;
    recordButton.disabled = false;
    pauseButton.disabled = true;

    pauseButton.innerHTML="Pause";

    rec.stop();

    gumStream.getAudioTracks()[0].stop();

    rec.exportWAV(append)
}

function append(blob) {
    var au = document.createElement('audio');
    var li = document.createElement('li');

    au.controls = true;
    li.appendChild(au);
    recordingsList.appendChild(li);
}

