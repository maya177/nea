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
const AudioContext = window.AudioContext || window.webkitAudioContext;

var audios = document.getElementsByClassName("audio");

//audio1.addEventListener('loadedmetadata', () => {
 // duration1 = audio1.duration;

//})

//var playbtns = document.getElementsByClassName("btn btn-play");
//var pausebtns = document.getElementsByClassName("btn btn-pause");

//for (var i = 0; i < playbtns.length; i++) {
 //   playbtns[i].onclick = () => {
  //      for (var x = 0; x < playbtns.length; x++) {
   //         if (x != i){
    //            playbtns[x].disabled = true;
     //       }
     //   pausebtns[i].disabled = false;
      //  audios[i].play();
//}}}

//for (var i = 0; i < playbtns.length; i++) {
//    playbtns[i].onclick = () => {
 //      audios[i].play()
  //     console.log(i)
   //    playbtns[0].disable = true;
      // pausebtns[i].disable = false;

//var buttons = document.getElementsByTagName('play');
//for (var i = 0, len = buttons.length; i < len; i++) {
 //   buttons[i].onclick = function (){
  //      console.log(i);
   // }
//}

playBtn1.onclick = () => {
    //document.getElementbyClass("btn btn-play").disabled = true;
    //var plays = document.getElementsByClassName('btn btn-play');
    //console.log();
   // plays.setAttribute("disabled","true");
   
    plays.disabled = true;
    pauseBtn1.disabled = false;
    audio1.play();
  }

for (var i = 0; i < pausebtns.length; i++) {
    pausebtns[i].onclick = () => {
        console.log("pause btn")
        pausebtns.disabled = true;
        playbtns[i].disabled = false;
        audios[i].play();
}}

//pauseBtn1.onclick = () => {
 // pauseBtn1.disabled = true;
  //playBtn1.disabled = false;
  //audio1.pause();
//}


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
