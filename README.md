<html lang="hi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>AI King</title>

<script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
<script async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>

<style>

*{box-sizing:border-box;margin:0;padding:0;-webkit-tap-highlight-color:transparent;}

html,body{
height:100%;
background:#000;
color:#fff;
font-family:system-ui;
display:flex;
flex-direction:column;
}

body{min-height:100dvh;}

header{
padding:15px;
text-align:center;
background:#111;
border-bottom:1px solid #333;
}

h2{color:#00ffcc;}

#chat-container{
flex:1 1 auto;
min-height:0;
overflow-y:auto;
-webkit-overflow-scrolling:touch;
padding:15px;
display:flex;
flex-direction:column;
gap:15px;
}

.message{
padding:12px 16px;
border-radius:18px;
max-width:85%;
word-wrap:break-word;
font-size:16px;
}

.user-msg{
background:#2b2b2b;
align-self:flex-end;
}

.ai-msg{
background:#1a1a1a;
align-self:flex-start;
border:1px solid #333;
border-left:4px solid #00ffcc;
}

.input-area{
position:sticky;
bottom:0;
padding:10px;
background:#111;
display:flex;
gap:8px;
border-top:1px solid #333;
}

input{
flex:1;
padding:12px 18px;
border-radius:25px;
border:1px solid #444;
background:#1a1a1a;
color:#fff;
outline:none;
font-size:16px;
}

.btn{
border:none;
cursor:pointer;
display:flex;
align-items:center;
justify-content:center;
border-radius:50%;
width:42px;
height:42px;
}

.cam-btn{background:#333;color:#fff;}
.mic-btn{background:#ff4b2b;color:#fff;}

.send-btn{
background:#00ffcc;
color:#000;
border-radius:20px;
width:auto;
padding:0 18px;
font-weight:bold;
}

.listening{background:#00ffcc;color:#000;}

#cam-modal{
display:none;
position:fixed;
inset:0;
background:#000;
z-index:1000;
flex-direction:column;
align-items:center;
justify-content:center;
}

video{width:100%;max-height:70%;object-fit:cover;}

</style>
</head>

<body>

<header><h2>AI King</h2></header>

<div id="chat-container">
<div class="message ai-msg">मैं आदित्य का AI हूँ, मैं आपके लिए क्या कर सकता हूँ?</div>
</div>

<div id="cam-modal">
<video id="video" autoplay playsinline></video>

<div style="padding:20px;display:flex;gap:20px;">
<button class="send-btn" style="background:#ff4b2b;color:#fff;" id="closeCamBtn">बंद करें</button>
<button class="send-btn" id="shotBtn">फोटो लें</button>
</div>

<canvas id="canvas" style="display:none;"></canvas>
</div>

<div class="input-area">
<button class="btn cam-btn" id="camBtn">📷</button>
<button class="btn mic-btn" id="micBtn">🎤</button>
<input id="userInput" placeholder="संदेश लिखें...">
<button class="btn send-btn" id="sendBtn">भेजें</button>
</div>

<script>

/* ===== ELEMENTS ===== */

const chatBox=document.getElementById('chat-container');
const video=document.getElementById('video');
const canvas=document.getElementById('canvas');
const camModal=document.getElementById('cam-modal');
const micBtn=document.getElementById('micBtn');
const userInput=document.getElementById('userInput');

const camBtn=document.getElementById('camBtn');
const sendBtn=document.getElementById('sendBtn');
const closeCamBtn=document.getElementById('closeCamBtn');
const shotBtn=document.getElementById('shotBtn');

let history=["तुम आदित्य के AI हो। हमेशा हिंदी में जवाब दो।"];

/* ===== SCROLL ===== */

function scrollBottom(){
requestAnimationFrame(()=>chatBox.scrollTop=chatBox.scrollHeight);
}

/* ===== CHAT ===== */

sendBtn.onclick=()=>send();
userInput.onkeydown=e=>{if(e.key==="Enter")send();};

async function send(override){

const val=override||userInput.value.trim();
if(!val)return;

if(!override)append(val,'user-msg');

userInput.value="";
history.push("User:"+val);

const id="ai"+Date.now();
append("AI सोच रहा है...","ai-msg",id);

scrollBottom();

try{
const r=await fetch(`https://text.pollinations.ai/${encodeURIComponent(history.join("\n"))}?model=openai`);
const t=await r.text();
document.getElementById(id).innerHTML=t;
history.push("AI:"+t);
}catch{
document.getElementById(id).innerText="Server error";
}

scrollBottom();
}

function append(t,c,id){
const d=document.createElement('div');
d.className="message "+c;
if(id)d.id=id;
d.innerText=t;
chatBox.appendChild(d);
scrollBottom();
}

function appendImg(src){
const d=document.createElement('div');
d.className="message user-msg";
d.innerHTML=`<img src="${src}" style="max-width:100%;border-radius:10px">`;
chatBox.appendChild(d);
scrollBottom();
}

/* ===== CAMERA ===== */

camBtn.onclick=openCam;
closeCamBtn.onclick=closeCam;
shotBtn.onclick=takeShot;

async function openCam(){
try{
const s=await navigator.mediaDevices.getUserMedia({video:{facingMode:"environment"}});
video.srcObject=s;
camModal.style.display='flex';
}catch{
alert("Camera permission denied");
}
}

function closeCam(){
const s=video.srcObject;
if(s)s.getTracks().forEach(t=>t.stop());
camModal.style.display='none';
}

function takeShot(){
canvas.width=video.videoWidth;
canvas.height=video.videoHeight;
canvas.getContext('2d').drawImage(video,0,0);
appendImg(canvas.toDataURL());
closeCam();
send("मैंने फोटो भेजी है");
}

/* ===== VOICE SAFE ===== */

let rec=null;

if(window.SpeechRecognition||window.webkitSpeechRecognition){
rec=new(window.SpeechRecognition||window.webkitSpeechRecognition)();
rec.lang='hi-IN';

rec.onresult=e=>{
userInput.value=e.results[0][0].transcript;
send();
};

rec.onend=()=>micBtn.classList.remove('listening');
}

micBtn.onclick=()=>{
if(!rec){alert("Voice not supported");return;}
try{
rec.start();
micBtn.classList.add('listening');
}catch{}
};

</script>

</body>
</html>