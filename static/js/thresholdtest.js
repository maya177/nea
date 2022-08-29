//.querySelector is a method of the Element interface and returns the first element within the document that matches the selectors
//.getElementById references HTML elements in DOM
//const data = JSON.parse(localStorage.getItem('src'));

//playback rate range is x0.25 to x4
const data = localStorage.getItem('src');
var audio = document.getElementById('audio');
audio.src=data;
audio.load();

const durationIndicator = document.querySelector('.audio-duration-indicator');
const volumeIndicator = document.querySelector('.volume-indicator');
const freqIndicator = document.querySelector('.freq-indicator');

console.log("data")
console.log(data)
console.log(typeof(data))

//not working w var but works hardcoded
//workaround
//var str = "<audio controls><source src=' "+$scope.data+" ' type='audio/wav'></audio>";

//var str = "<audio id='audio' "+"./static/audiobuzz.mp3"+" '</audio>";
//document.getElementById('audio').innerHTML = str;
//console.log(audio.getAttribute('src'));

const durationToggler = document.getElementById('duration-toggler');
const volumeToggler = document.getElementById('volume-toggler');
const freqToggler = document.getElementById('freq-toggler');

const playBtn = document.getElementById('play-btn');
const pauseBtn = document.getElementById('pause-btn');
const muteBtn = document.getElementById('mute-btn');
const submitBtn = document.getElementById('submit');

let duration;
const audioCtx = new AudioContext();

//set up the different audio nodes we will use for the app
const analyser = audioCtx.createAnalyser();
const distortion = audioCtx.createWaveShaper();
const gainNode = audioCtx.createGain();
const biquadFilter = audioCtx.createBiquadFilter();
const convolver = audioCtx.createConvolver();

// connect the nodes together

source = audio.createMediaStreamSource(stream);
source.connect(analyser);
analyser.connect(distortion);
distortion.connect(biquadFilter);
biquadFilter.connect(convolver);
convolver.connect(gainNode);
gainNode.connect(audioCtx.destination);

// Manipulate the Biquad filter

audio.addEventListener('loadedmetadata', () => {
  duration = audio.duration;
})

const setCurrentTime = (currentTime) => {
  audio.currentTime = currentTime;
}

const getAudioProgress = (currentTime) => {
  const progress = currentTime / duration * 100
  durationIndicator.style.width = progress + '%';
  durationToggler.value = progress;
  return progress;
}

audio.addEventListener('timeupdate', (e) => {
  const currentTime = e.target.currentTime;
  getAudioProgress(currentTime);
});

durationToggler.addEventListener('input', (e) => {
  const progress = parseInt(e.target.value);
  const time = progress / 100 * duration;
  setCurrentTime(time);
  getAudioProgress(time, duration);
})

volumeToggler.addEventListener('input', (e) => {
  const value = e.target.value;
  const volume = value / 100;
  audio.volume = volume;
  volumeIndicator.style.width = value + '%';
})

freqToggler.addEventListener('input', (e) => {

  biquadFilter.type = "lowshelf";
  biquadFilter.frequency.value = 1000;
  biquadFilter.gain.value = 25;

  const value = e.target.value;
  console.log(value)
  audio.webiktPreservesPitch = false;
  

  biquadFilter.frequency.setTargetAtTime(1000, audioCtx.currentTime, 0)


  //const semitones = value / 100;
  //var semitoneRatio = Math.pow(2, 1/12);
  //audio.playbackRate = Math.pow(semitoneRatio, semitones);
  
  //audio.playbackRate = pitch;
  
  //audio.detune.value = pitch*100;
  audio.loop = true;
  volumeIndicator.style.width = value + '';
})


playBtn.onclick = () => {
  console.log("play btn")
  playBtn.disabled = true;
  pauseBtn.disabled = false;
  audio.play();
}

pauseBtn.onclick = () => {
pauseBtn.disabled = true;
playBtn.disabled = false;
audio.pause();
}

muteBtn.onclick = () => {
if (audio.muted) {
  audio.muted = false;
  muteBtn.innerText = 'Mute';
} else {
  audio.muted = true;
  muteBtn.innerText = 'Unmute';
}
}

submitBtn.onclick = () => {
  console.log(audio.volume)
  console.log(audio.playbackRate)

  let data = {'src': audio.getAttribute('src'), 'volume': audio.volume, 'pitch': audio.playbackRate};
  $.ajax({
    type: "POST",
    url: "/threshold2",
    data: JSON.stringify(data),
    contentType: "application/json",
    dataType: 'json',
    success: function(response) {
      window.location.href = "/home";
    }
  });

}

