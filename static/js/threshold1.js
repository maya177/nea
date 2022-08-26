
const durationIndicator = document.querySelector('.audio-duration-indicator');
const volumeIndicator = document.querySelector('.volume-indicator');

const audio = document.getElementById('audio1');
const audio2 = document.getElementById('audio2');
const audio3 = document.getElementById('audio3');
const audio4 = document.getElementById('audio4');
const audio5 = document.getElementById('audio5');

const durationToggler = document.getElementById('duration-toggler1');
const durationToggler2 = document.getElementById('duration-toggler2');
const durationToggler3 = document.getElementById('duration-toggler3');
const durationToggler4 = document.getElementById('duration-toggler4');
const durationToggler5 = document.getElementById('duration-toggler5');

const playBtn = document.getElementById('play-btn1');
const playBtn2 = document.getElementById('play-btn2');
const playBtn3 = document.getElementById('play-btn3');
const playBtn4 = document.getElementById('play-btn4');
const playBtn5 = document.getElementById('play-btn5');

const pauseBtn = document.getElementById('pause-btn1');
const pauseBtn2 = document.getElementById('pause-btn2');
const pauseBtn3 = document.getElementById('pause-btn3');
const pauseBtn4 = document.getElementById('pause-btn4');
const pauseBtn5 = document.getElementById('pause-btn5');

const submitBtn = document.getElementById('submit1');
const submitBtn2 = document.getElementById('submit2');
const submitBtn3 = document.getElementById('submit3');
const submitBtn4 = document.getElementById('submit4');
const submitBtn5 = document.getElementById('submit5');


let duration;
const AudioContext = window.AudioContext || window.webkitAudioContext;


//use for loop
//for (var i = 0; i < elements.length; i++) {
 //   audio[i].addEventListener('loadedmetadata', () => {
 //   duration[i] = audio[i].duration;
 // })
//}


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
    audioCtx = new (window.AudioContext || window.webkitAudioContext)();
  
    const value = e.target.value;
    console.log(value)
    audio.webiktPreservesPitch = false;
    
    //cannot use const in if statements
    if (value < 50){
      var pitch = (value/100)/1.5;
    } else if (value > 50){
      var pitch = 1.5*(1 + value/100);
    } else if (value < 10){
      var pitch = 1.5*(1 + value/100);
    }
  
    //const semitones = value / 100;
    //var semitoneRatio = Math.pow(2, 1/12);
    //audio.playbackRate = Math.pow(semitoneRatio, semitones);
    audio.playbackRate = pitch;
    //audio.detune.value = pitch*100;
    audio.loop = true;
    volumeIndicator.style.width = value + '';
  })
  //would need to use diff API to loop 
  //add in diagram showing bar and -50% and +50% scaled to -100% and +100%
  
  //https://www.oreilly.com/library/view/web-audio-api/9781449332679/ch04.html
  //https://stackoverflow.com/questions/31274895/changing-speed-of-audio-using-the-web-audio-api-without-changing-pitch
  //https://stackoverflow.com/questions/25157513/javascript-pitch-shift-with-time-stretch
  
  const v = e.tar.get.value;
    console.log(value)
    const pitch = value / 100;
    console.log(pitch)
    audio.mozPreservesPitch = false;
    audio.playbackRate = pitch;
  
  
    volumeIndicator.style.width = pitch + '%';
  
  //
  //const source = context.createBufferSource();
  //source.buffer = sample;
  //source.playbackRate.value = rate;
  //source.connect(context.destination);
  //source.start(0);
  ///