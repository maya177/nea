//have hardcoded btns because for some reason loops aren't working, neither are .getelementbyclassname it won't let me disable multiple at once

const AudioContext = window.AudioContext || window.webkitAudioContext;

const audio1 = document.getElementById('audio1');
const audio2 = document.getElementById('audio2');
const audio3 = document.getElementById('audio3');
const audio4 = document.getElementById('audio4');
const audio5 = document.getElementById('audio5');

const audioContext = new AudioContext();
const source = audioContext.createMediaElementSource(audio1);
source.connect(audioContext.destination);


const durationToggler1 = document.getElementById('duration-toggler1');
const durationToggler2 = document.getElementById('duration-toggler2');
const durationToggler3 = document.getElementById('duration-toggler3');
const durationToggler4 = document.getElementById('duration-toggler4');
const durationToggler5 = document.getElementById('duration-toggler5');

const plays = document.getElementsByClassName("btn btn-play")
const playBtn1 = document.getElementById('play-btn1');
const playBtn2 = document.getElementById('play-btn2');
const playBtn3 = document.getElementById('play-btn3');
const playBtn4 = document.getElementById('play-btn4');
const playBtn5 = document.getElementById('play-btn5');

const pauseBtn1 = document.getElementById('pause-btn1');
const pauseBtn2 = document.getElementById('pause-btn2');
const pauseBtn3 = document.getElementById('pause-btn3');
const pauseBtn4 = document.getElementById('pause-btn4');
const pauseBtn5 = document.getElementById('pause-btn5');

const submitBtn1 = document.getElementById('submit1');
const submitBtn2 = document.getElementById('submit2');
const submitBtn3 = document.getElementById('submit3');
const submitBtn4 = document.getElementById('submit4');
const submitBtn5 = document.getElementById('submit5');

let duration;

var audios = document.getElementsByClassName("audio");



//const analyzer = Meyda.createMeydaAnalyzer({
//  audioContext: audioContext,
//  source: source,
//  bufferSize: 512,
//  featureExtractors: ["rms"],
//  callback: (features) => {
//    console.log(features);
//  },
//});


playBtn1.onclick = () => {
  audioContext.resume();

  playBtn1.disabled = true;
  playBtn2.disabled = true;
  playBtn3.disabled = true;
  playBtn4.disabled = true;
  playBtn5.disabled = true;

  pauseBtn1.disabled = false;
  audio1.play();
  audio1.loop = true;
}
pauseBtn1.onclick = () => {
  
  playBtn1.disabled = false;
  playBtn2.disabled = false;
  playBtn3.disabled = false;
  playBtn4.disabled = false;
  playBtn5.disabled = false;

  pauseBtn1.disabled = true;

  audio1.pause();
}

playBtn2.onclick = () => {
  audioContext.resume();

  playBtn1.disabled = true;
  playBtn2.disabled = true;
  playBtn3.disabled = true;
  playBtn4.disabled = true;
  playBtn5.disabled = true;

  pauseBtn2.disabled = false;
  audio2.play();
  audio2.loop = true;
}
pauseBtn2.onclick = () => {
  audioContext.resume();

  playBtn1.disabled = false;
  playBtn2.disabled = false;
  playBtn3.disabled = false;
  playBtn4.disabled = false;
  playBtn5.disabled = false;

  pauseBtn2.disabled = true;

  audio2.pause();
}

playBtn3.onclick = () => {
  audioContext.resume();

  playBtn1.disabled = true;
  playBtn2.disabled = true;
  playBtn3.disabled = true;
  playBtn4.disabled = true;
  playBtn5.disabled = true;

  pauseBtn3.disabled = false;
  audio3.play();
  audio3.loop = true;
}
pauseBtn3.onclick = () => {
  playBtn1.disabled = false;
  playBtn2.disabled = false;
  playBtn3.disabled = false;
  playBtn4.disabled = false;
  playBtn5.disabled = false;

  pauseBtn3.disabled = true;
  audio3.pause();
}


playBtn4.onclick = () => {
  audioContext.resume();

  playBtn1.disabled = true;
  playBtn2.disabled = true;
  playBtn3.disabled = true;
  playBtn4.disabled = true;
  playBtn5.disabled = true;

  pauseBtn4.disabled = false;
  audio4.play();
  audio4.loop = true;
}
pauseBtn4.onclick = () => {
  playBtn1.disabled = false;
  playBtn2.disabled = false;
  playBtn3.disabled = false;
  playBtn4.disabled = false;
  playBtn5.disabled = false;

  pauseBtn4.disabled = true;

  audio4.pause();
}


playBtn5.onclick = () => {
  audioContext.resume();

  playBtn1.disabled = true;
  playBtn2.disabled = true;
  playBtn3.disabled = true;
  playBtn4.disabled = true;
  playBtn5.disabled = true;

  pauseBtn5.disabled = false;
  audio5.play();
  audio5.loop = true;
}

pauseBtn5.onclick = () => {
  playBtn1.disabled = false;
  playBtn2.disabled = false;
  playBtn3.disabled = false;
  playBtn4.disabled = false;
  playBtn5.disabled = false;

  pauseBtn5.disabled = false;

  audio4.pause();
}

var submitBtns = document.querySelectorAll( "submit" );
var audios = document.querySelectorAll( "audio" );

//for ( var i = 0; i < submitBtns.length; i++){}

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

submitBtn2.onclick = () => {
  console.log(audio2.src);

  $.ajax({
    type: "POST",
    url: "/threshold1",
    data: JSON.stringify(audio2.getAttribute('src')),
    contentType: "application/json",
    dataType: 'json',
    success: function(response) {
      localStorage.setItem('src', audio2.getAttribute('src'));
      window.location.href = "/threshold2";
    }
  });
}
submitBtn3.onclick = () => {
  console.log(audio3.src);

  $.ajax({
    type: "POST",
    url: "/threshold1",
    data: JSON.stringify(audio3.getAttribute('src')),
    contentType: "application/json",
    dataType: 'json',
    success: function(response) {
      localStorage.setItem('src', audio3.getAttribute('src'));
      window.location.href = "/threshold2";
    }
  });
}
submitBtn4.onclick = () => {
  console.log(audio4.src);

  $.ajax({
    type: "POST",
    url: "/threshold1",
    data: JSON.stringify(audio4.getAttribute('src')),
    contentType: "application/json",
    dataType: 'json',
    success: function(response) {
      localStorage.setItem('src', audio4.getAttribute('src'));
      window.location.href = "/threshold2";
    }
  });
}
//can take out ajax because src carried to threshold2 and all submitted there
submitBtn5.onclick = () => {
  console.log(audio5.src);

  $.ajax({
    type: "POST",
    url: "/threshold1",
    data: JSON.stringify(audio5.getAttribute('src')),
    contentType: "application/json",
    dataType: 'json',
    success: function(response) {
      localStorage.setItem('src', audio5.getAttribute('src'));
      window.location.href = "/threshold2";
    }
  });
}
//wasn't working because local storage data was json stringified