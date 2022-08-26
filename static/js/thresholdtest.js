//.querySelector is a method of the Element interface and returns the first element within the document that matches the selectors
//.getElementById references HTML elements in DOM
const durationIndicator = document.querySelector('.audio-duration-indicator');

const audio1 = document.getElementById('audio1');
const audio2 = document.getElementById('audio2');
const audio3 = document.getElementById('audio3');
const audio4 = document.getElementById('audio4');
const audio5 = document.getElementById('audio5');


const durationToggler1 = document.getElementById('duration-toggler1');
const durationToggler2 = document.getElementById('duration-toggler2');
const durationToggler3 = document.getElementById('duration-toggler3');
const durationToggler4 = document.getElementById('duration-toggler4');
const durationToggler5 = document.getElementById('duration-toggler5');

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
const AudioContext = window.AudioContext || window.webkitAudioContext;

audio1.addEventListener('loadedmetadata', () => {
  duration1 = audio1.duration;
})

const setCurrentTime = (currentTime) => {
  audio1.currentTime = currentTime;
}

const getAudioProgress = (currentTime) => {
  const progress1 = currentTime / duration * 100
  durationIndicator.style.width = progress1 + '%';
  durationToggler1.value = progress1;
  return progress1;
}

audio1.addEventListener('timeupdate', (e) => {
  const currentTime = e.target.currentTime;
  getAudioProgress(currentTime);
});

playBtn1.onclick = () => {
    console.log("play btn")
    playBtn1.disabled = true;
    pauseBtn1.disabled = false;
    audio1.play();
}

pauseBtn1.onclick = () => {
  pauseBtn1.disabled = true;
  playBtn1.disabled = false;
  audio1.pause();
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

durationToggler1.addEventListener('input', (e) => {
  const progress1 = parseInt(e.target.value);
  const time1 = progress1 / 100 * duration;
  setCurrentTime(time1);
  getAudioProgress(time1, duration);
})
