//.querySelector is a method of the Element interface and returns the first element within the document that matches the selectors
//.getElementById references HTML elements in DOM
const durationIndicator = document.querySelector('.audio-duration-indicator');
const volumeIndicator = document.querySelector('.volume-indicator');
const freqIndicator = document.querySelector('.freq-indicator');
const audio = document.getElementById('audio');
const durationToggler = document.getElementById('duration-toggler');
const volumeToggler = document.getElementById('volume-toggler');
const freqToggler = document.getElementById('freq-toggler');
const playBtn = document.getElementById('play-btn');
const pauseBtn = document.getElementById('pause-btn');
const muteBtn = document.getElementById('mute-btn');
const submitBtn = document.getElementById('submit');

let duration;

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
    pass_to_python = audio.volume
    console.log(pass_to_python)

    /*$.ajax({
        url:'/threshold',
        type: 'POST',
        data: JSON.stringify(pass_to_python)
      });
*/
}

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
    const freq = e.target.value;
    audio.pitch = freq
    volumeIndicator.style.width = value + '%';

    },
    false
  );