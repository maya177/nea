const data = localStorage.getItem('src');
var audio = document.getElementById('audio');
audio.src=data;
audio.load();
let duration;
const AudioContext = window.AudioContext || window.webkitAudioContext;

const durationIndicator = document.querySelector('.audio-duration-indicator');
const volumeIndicator = document.querySelector('.volume-indicator');
const freqIndicator = document.querySelector('.freq-indicator');

const durationToggler = document.getElementById('duration-toggler');
const volumeToggler = document.getElementById('volume-toggler');
const freqToggler = document.getElementById('freq-toggler');

const playBtn = document.getElementById('play-btn');
const pauseBtn = document.getElementById('pause-btn');
const muteBtn = document.getElementById('mute-btn');
const submitBtn = document.getElementById('submit');

//get audio duration from audio metadata
audio.addEventListener('loadedmetadata', () => {
  duration = audio.duration;
})

//set current time to indicate progress through audio on progress bar
const setCurrentTime = (currentTime) => {
  audio.currentTime = currentTime;
}

//get current duration of audio elapsed
const getAudioProgress = (currentTime) => {
  const progress = currentTime / duration * 100
  durationIndicator.style.width = progress + '%';
  durationToggler.value = progress;
  return progress;
}

//update current time as audio plays
audio.addEventListener('timeupdate', (e) => {
  const currentTime = e.target.currentTime;
  getAudioProgress(currentTime);
});

//show progress on progress bar using duration toggler
durationToggler.addEventListener('input', (e) => {
  const progress = parseInt(e.target.value);
  const time = progress / 100 * duration;
  setCurrentTime(time);
  getAudioProgress(time, duration);
})

//allows the user to adjust the volume of audio playing
volumeToggler.addEventListener('input', (e) => {
  const value = e.target.value;
  const volume = value / 100;
  audio.volume = volume;
  volumeIndicator.style.width = value + '%';
})

//allows the user to adjust the frequency of audio by changing audio playback rate
//playback rate range is x0.25 to x4
freqToggler.addEventListener('input', (e) => {
  audioCtx = new (window.AudioContext || window.webkitAudioContext)();

  const value = e.target.value;
  console.log(value)
  audio.webiktPreservesPitch = false;
  
  if (value < 50){
    var pitch = ((value*2)/100);
  } else if (value > 50){
    var pitch = 1 + ((value/2)/100);
  }
    else if (value < 30){
    var pitch = 0.6
  }

  audio.playbackRate = pitch;
  audio.loop = true;
  volumeIndicator.style.width = value + '';
})

//plays audio
playBtn.onclick = () => {
  console.log("play btn")
  playBtn.disabled = true;
  pauseBtn.disabled = false;
  audio.play();
}

//pauses audio
pauseBtn.onclick = () => {
pauseBtn.disabled = true;
playBtn.disabled = false;
audio.pause();
}

//mutes audio
muteBtn.onclick = () => {
if (audio.muted) {
  audio.muted = false;
  muteBtn.innerText = 'Mute';
} else {
  audio.muted = true;
  muteBtn.innerText = 'Unmute';
}
}