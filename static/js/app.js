//|| means logical or
//sets URL to current page address (current URL)
URL = window.URL || window.webkitURL;

//to stream audio from getUserMedia() from MediaStream Recording API https://developer.mozilla.org/en-US/docs/Web/API/MediaStream_Recording_API
var gumStream;
//this creates mediarecorder object
var rec; 
//this is the media stream audio source node to record
var input; 

//shim for AudioContext (shim corrects the existing audio context code) for when it is not available
var AudioContext = window.AudioContext || window.webkitAudioContext;
//variable defining audio context
var audioContext

//variables for the record/pause/stop buttons
var recordButton = document.getElementById("recordButton");
var stopButton = document.getElementById("stopButton");
var pauseButton = document.getElementById("pauseButton");

//add events to buttons upon being clicked
recordButton.addEventListener("click", startRecording);
stopButton.addEventListener("click", stopRecording);
pauseButton.addEventListener("click", pauseRecording);

function startRecording() {
    console.log("recordButton clicked");
    var constraints = { audio: true, video:false }

    //disable record button until success/fail is received from getUserMedia() so that user cannot record whilst recording already happening
    recordButton.disabled = true;
    stopButton.disabled = false;
    pauseButton.disabled = false;


    navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
        //success in obtaining stream, so create audio context as sample rate may change after getUserMedia is called (eg. in macOS when recording using AirPods, sound rate defaults to one set in OS for playback device)
        console.log("getUserMedia() success, stream created, initializing Recorder.js ...");
        audioContext = new AudioContext();
        //update the sr format 
        document.getElementById("formats").innerHTML="Format: 1 channel pcm @ "+audioContext.sampleRate/1000+"kHz"
        gumStream = stream;
        input = audioContext.createMediaStreamSource(stream);

        //create recorded object and configure to record mono sound (1 channel),no need to record 2 channels as this will double file size and not improve quality of sound
        rec = new Recorder(input,{numChannels:1})

        //start the recording process
        rec.record()
        console.log("Recording started");

    }).catch(function(err) {
        //enable the record button if getUserMedia() fails
        recordButton.disabled = false;
        stopButton.disabled = true;
        pauseButton.disabled = true
    });
}

function pauseRecording(){
    console.log("pauseButton clicked rec.recording=",rec.recording );
    if (rec.recording){
        //pause
        rec.stop();
        pauseButton.innerHTML="Resume";
    }else{
        //resume
        rec.record()
        pauseButton.innerHTML="Pause";
    }
}

function stopRecording() {
    console.log("stopButton clicked");

    //disable the stop button, enable the record to allow for new recordings
    stopButton.disabled = true;
    recordButton.disabled = false;
    pauseButton.disabled = true;

    //reset pause button in case the recording is stopped while paused
    pauseButton.innerHTML="Pause";

    //tell the recorder to stop the recording
    rec.stop();

    //stop microphone access
    gumStream.getAudioTracks()[0].stop();

    //create the wav blob and pass it on to createDownloadLink
    console.log("exporting data")
    rec.exportWAV(sendData);
}

function sendData(blob) {
    fetch("/recorder", {
    method: "POST",
    body: blob,
    success: function(response) {
        console.log("success")
        window.location.href = "/home";
      }    }).then(response => response.json()
      ).then(json => {
          console.log(json)
          location.href = '/compare';
      });
}