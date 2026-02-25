<html lang="hi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI King</title>

<style>
*{box-sizing:border-box;margin:0;padding:0}
body{
height:100vh;
display:flex;
flex-direction:column;
background:#000;color:#fff;font-family:system-ui;
}
header{
padding:14px;text-align:center;background:#111;color:#00ffcc;
}

/* CHAT */
#chat{
flex:1;
overflow:auto;
padding:15px;
display:flex;
flex-direction:column;
gap:12px;
}

.msg{
padding:12px 16px;border-radius:18px;max-width:80%;
word-wrap:break-word;
}
.user{background:#2b2b2b;align-self:flex-end;}
.ai{background:#1a1a1a;border-left:4px solid #00ffcc;}

/* INPUT BAR */
.bottom{
display:flex;gap:8px;padding:10px;background:#111;
}

input{
flex:1;padding:12px;border-radius:20px;
border:1px solid #444;background:#1a1a1a;color:#fff;
}

button{
border:none;cursor:pointer;border-radius:20px;
padding:10px 14px;font-weight:bold;
}

.cam{background:#333;color:#fff;}
.mic{background:#ff4b2b;color:#fff;}
.send{background:#00ffcc;color:#000;}

#camModal{
display:none;
position:fixed;inset:0;background:#000;z-index:5;
flex-direction:column;justify-content:center;
}
video{width:100%}
</style>
</head>

<body>

<header><b>AI King</b></header>

<div id="chat">
<div class="msg ai">नमस्ते आदित्य 🙂 मैं आपका AI हूँ</div>
</div>

<!-- CAMERA MODAL -->
<div id="camModal">
<video id="video" autoplay playsinline></video>
<button onclick="closeCam()">बंद</button>
<button onclick="shot()">फोटो लें</button>
<canvas id="canvas" style="display:none"></canvas>
</div>

<div class="bottom">
<button class="cam" onclick="openCam()">📷</button>
<button class="mic" onclick="voice()">🎤</button>
<input id="input" placeholder="संदेश लिखो...">
<button class="send" onclick="send()">भेजें</button>
</div>

<script>

const chat=document.getElementById("chat");
const input=document.getElementById("input");
const video=document.getElementById("video");
const canvas=document.getElementById("canvas");
const modal=document.getElementById("camModal");

/* SMART AUTO SCROLL */

function nearBottom(){
return chat.scrollHeight-chat.scrollTop-chat.clientHeight<120;
}
function smartScroll(){
if(nearBottom()) chat.scrollTop=chat.scrollHeight;
}

/* ADD MESSAGE */

function add(t,c){
const d=document.createElement("div");
d.className="msg "+c;
d.innerText=t;
chat.appendChild(d);
smartScroll();
}

/* SEND */

async function send(txt){

const v=txt||input.value.trim();
if(!v)return;

add(v,"user");
input.value="";

const load=document.createElement("div");
load.className="msg ai";
load.innerText="सोच रहा है...";
chat.appendChild(load);
chat.scrollTop=chat.scrollHeight;

try{
const r=await fetch("https://text.pollinations.ai/"+encodeURIComponent(v));
const t=await r.text();
load.innerText=t;
}catch{
load.innerText="Server error";
}

chat.scrollTop=chat.scrollHeight;
}

input.onkeydown=e=>{if(e.key==="Enter")send();};

/* CAMERA */

async function openCam(){
try{
const s=await navigator.mediaDevices.getUserMedia({video:true});
video.srcObject=s;
modal.style.display="flex";
}catch{alert("Camera permission denied")}
}

function closeCam(){
const s=video.srcObject;
if(s)s.getTracks().forEach(t=>t.stop());
modal.style.display="none";
}

function shot(){
canvas.width=video.videoWidth;
canvas.height=video.videoHeight;
canvas.getContext("2d").drawImage(video,0,0);
const img=canvas.toDataURL();
const d=document.createElement("div");
d.className="msg user";
d.innerHTML=`<img src="${img}" style="max-width:100%;border-radius:10px">`;
chat.appendChild(d);
closeCam();
smartScroll();
}

/* MIC */

let rec=null;
if(window.SpeechRecognition||window.webkitSpeechRecognition){
rec=new(window.SpeechRecognition||window.webkitSpeechRecognition)();
rec.lang="hi-IN";
rec.onresult=e=>{
input.value=e.results[0][0].transcript;
send();
};
}

function voice(){
if(!rec){alert("Voice not supported");return;}
rec.start();
}

</script>

</body>
</html>