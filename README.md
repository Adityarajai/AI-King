<html lang="hi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>AI King - Mobile Master</title>

<script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
<script async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>

<style>

*{
box-sizing:border-box;
margin:0;
padding:0;
-webkit-tap-highlight-color:transparent;
}

html,body{
height:100%;
background:#000;
color:#fff;
font-family:system-ui,sans-serif;
display:flex;
flex-direction:column;
}

/* मोबाइल height FIX */
body{
min-height:100dvh;
}

header{
padding:15px;
text-align:center;
background:#111;
border-bottom:1px solid #333;
}

h2{
color:#00ffcc;
font-size:20px;
}

/* ⭐⭐⭐ REAL MOBILE SCROLL FIX ⭐⭐⭐ */
#chat-container{
flex:1 1 auto;
min-height:0;          /* MOST IMPORTANT */
overflow-y:auto;
-webkit-overflow-scrolling:touch;

padding:15px;
display:flex;
flex-direction:column;
gap:15px;
background:#000;
}

.message{
padding:12px 16px;
border-radius:18px;
line-height:1.5;
max-width:85%;
word-wrap:break-word;
font-size:16px;
}

.user-msg{
background:#2b2b2b;
align-self:flex-end;
border-bottom-right-radius:4px;
}

.ai-msg{
background:#1a1a1a;
align-self:flex-start;
border:1px solid #333;
border-left:4px solid #00ffcc;
border-bottom-left-radius:4px;
}

/* sticky input */
.input-area{
position:sticky;
bottom:0;
padding:10px;
background:#111;
display:flex;
gap:8px;
align-items:center;
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

.cam-btn{background:#333;color:#fff;border:1px solid #444;}
.mic-btn{background:#ff4b2b;color:#fff;}

.send-btn{
background:#00ffcc;
color:#000;
border-radius:20px;
width:auto;
padding:0 18px;
font-weight:bold;
}

.listening{
animation:pulse 1s infinite;
background:#00ffcc;
color:#000;
}

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

video{
width:100%;
max-height:70%;
object-fit:cover;
}

@keyframes pulse{
0%{box-shadow:0 0 0 0 rgba(0,255,204,.7);}
70%{box-shadow:0 0 0 10px rgba(0,255,204,0);}
100%{box-shadow:0 0 0 0 rgba(0,255,204,0);}
}

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
<button class="send-btn" style="background:#ff4b2b;color:#fff;" onclick="closeCam()">बंद करें</button>
<button class="send-btn" onclick="takeShot()">फोटो लें</button>
</div>

<canvas id="canvas" style="display:none;"></canvas>
</div>

<div class="input-area">
<button class="btn cam-btn" onclick="openCam()">📷</button>
<button id="micBtn" class="btn mic-btn" onclick="startVoice()">🎤</button>

<input id="userInput" placeholder="संदेश लिखें..."
onkeydown="if(event.key==='Enter')send()">

<button class="btn send-btn" onclick="send()">भेजें</button>
</div>

<script>

let history=["तुम आदित्य के AI हो। हमेशा हिंदी में जवाब दो।"];
const chatBox=document.getElementById('chat-container');

function scrollToBottom(){
requestAnimationFrame(()=>{
chatBox.scrollTop=chatBox.scrollHeight;
});
}

/* CAMERA */

async function openCam(){
try{
const s=await navigator.mediaDevices.getUserMedia({video:{facingMode:"environment"}});
video.srcObject=s;
cam-modal.style.display='flex';
}catch(e){alert("Camera problem");}
}

function closeCam(){
const s=video.srcObject;
if(s)s.getTracks().forEach(t=>t.stop());
cam-modal.style.display='none';
}

function takeShot(){
const c=canvas;
c.width=video.videoWidth;
c.height=video.videoHeight;
c.getContext('2d').drawImage(video,0,0);
appendImg(c.toDataURL());
closeCam();
send("मैंने फोटो भेजी है");
}

/* VOICE */

const rec=new(window.SpeechRecognition||window.webkitSpeechRecognition)();
rec.lang='hi-IN';

function startVoice(){
try{
rec.start();
micBtn.classList.add('listening');
}catch{}
}

rec.onresult=e=>{
userInput.value=e.results[0][0].transcript;
send();
};

rec.onend=()=>micBtn.classList.remove('listening');

/* CHAT */

async function send(overrideText){

const input=userInput;
const val=overrideText||input.value.trim();
if(!val)return;

if(!overrideText)appendMsg(val,'user-msg');

input.value="";
history.push("User:"+val);

const id="ai-"+Date.now();
appendMsg("AI सोच रहा है...","ai-msg",id);

scrollToBottom();

try{
const r=await fetch(`https://text.pollinations.ai/${encodeURIComponent(history.join("\n"))}?model=openai`);
const d=await r.text();

const box=document.getElementById(id);
box.innerHTML=d;

if(window.MathJax)MathJax.typesetPromise([box]);

history.push("AI:"+d);

}catch{
document.getElementById(id).innerText="Server error";
}

scrollToBottom();
}

function appendMsg(t,c,id){
const d=document.createElement('div');
d.className="message "+c;
if(id)d.id=id;
d.innerText=t;
chatBox.appendChild(d);
scrollToBottom();
}

function appendImg(src){
const d=document.createElement('div');
d.className="message user-msg";
d.innerHTML=`<img src="${src}" style="max-width:100%;border-radius:10px">`;
chatBox.appendChild(d);
scrollToBottom();
}

</script>
</body>
</html>