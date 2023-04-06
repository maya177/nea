//setting up constants and AudioContext
const AudioContext = window.AudioContext || window.webkitAudioContext;
const audio1 = document.getElementById('audio1');
const audioContext = new AudioContext();
const source = audioContext.createMediaElementSource(audio1);
source.connect(audioContext.destination);
const durationToggler1 = document.getElementById('duration-toggler1');
const playBtn1 = document.getElementById('play-btn1');
const pauseBtn1 = document.getElementById('pause-btn1');
const submitBtn1 = document.getElementById('submit1');
let duration;
var audios = document.getElementsByClassName("audio");

//functionality of play button
playBtn1.onclick = () => {
    audioContext.resume();
    playBtn1.disabled = true;
    pauseBtn1.disabled = false;
    audio1.play();
    audio1.loop = true;
  }
//functionality of pause button
pauseBtn1.onclick = () => {
  playBtn1.disabled = false;
  playBtn2.disabled = false;
  pauseBtn1.disabled = true;
  audio1.pause();
}

var submitBtns = document.querySelectorAll( "submit" );
var audios = document.querySelectorAll( "audio" );

//submitting the selected audio to the Flask app using ajax
submitBtn1.onclick = () => {
  console.log(audio1.src);

  $.ajax({
    type: "POST",
    url: "/threshold1",
    data: JSON.stringify(audio1.getAttribute('src')),
    contentType: "application/json",
    dataType: 'json',
    success: function(response) {
      localStorage.setItem('src', audio1.getAttribute('src'));
      window.location.href = "/threshold2";
    }
  });
}
