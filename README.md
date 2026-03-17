<html lang="hi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI King Pro</title>
<link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&family=Noto+Sans+Devanagari:wght@400;500;600&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box;margin:0;padding:0}

:root{
  --bg:#060a0f;
  --surface:#0d1117;
  --surface2:#111820;
  --border:#1e2d3d;
  --accent:#00e5ff;
  --accent2:#7b61ff;
  --text:#e8edf2;
  --text-dim:#8899aa;
  --user-bg:#132233;
  --ai-bg:#0d1a1f;
  --danger:#ff4466;
  --success:#00ffaa;
}

body{
  height:100vh;
  display:flex;
  flex-direction:column;
  background:var(--bg);
  color:var(--text);
  font-family:'Noto Sans Devanagari',system-ui;
  overflow:hidden;
}

/* animated bg grid */
body::before{
  content:'';
  position:fixed;
  inset:0;
  background-image:
    linear-gradient(rgba(0,229,255,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,229,255,0.03) 1px, transparent 1px);
  background-size:40px 40px;
  pointer-events:none;
  z-index:0;
}

/* HEADER */
header{
  position:relative;
  z-index:10;
  padding:12px 18px;
  display:flex;
  align-items:center;
  justify-content:space-between;
  background:linear-gradient(135deg, #0d1117 0%, #0a1520 100%);
  border-bottom:1px solid var(--border);
  box-shadow:0 2px 20px rgba(0,229,255,0.08);
}

.logo{
  display:flex;
  align-items:center;
  gap:10px;
}

.logo-icon{
  width:36px;height:36px;
  background:linear-gradient(135deg,var(--accent),var(--accent2));
  border-radius:10px;
  display:flex;align-items:center;justify-content:center;
  font-size:18px;
  box-shadow:0 0 15px rgba(0,229,255,0.3);
}

.logo-text{
  font-family:'Rajdhani',sans-serif;
  font-size:22px;
  font-weight:700;
  background:linear-gradient(90deg,var(--accent),var(--accent2));
  -webkit-background-clip:text;
  -webkit-text-fill-color:transparent;
  letter-spacing:1px;
}

.logo-badge{
  font-size:10px;
  background:var(--accent2);
  color:#fff;
  padding:2px 6px;
  border-radius:6px;
  font-family:'Rajdhani',sans-serif;
  font-weight:600;
}

.header-actions{
  display:flex;
  gap:8px;
}

.hbtn{
  background:var(--surface2);
  border:1px solid var(--border);
  color:var(--text-dim);
  padding:7px 12px;
  border-radius:10px;
  cursor:pointer;
  font-size:13px;
  transition:all .2s;
  display:flex;align-items:center;gap:5px;
}
.hbtn:hover{
  border-color:var(--accent);
  color:var(--accent);
  box-shadow:0 0 10px rgba(0,229,255,0.1);
}

/* STATUS BAR */
#status-bar{
  background:rgba(0,229,255,0.05);
  border-bottom:1px solid var(--border);
  padding:6px 18px;
  font-size:11px;
  color:var(--text-dim);
  display:flex;
  align-items:center;
  gap:6px;
  position:relative;
  z-index:9;
}

#status-dot{
  width:7px;height:7px;
  border-radius:50%;
  background:var(--success);
  box-shadow:0 0 6px var(--success);
  animation:pulse 2s infinite;
}

@keyframes pulse{
  0%,100%{opacity:1}
  50%{opacity:.4}
}

/* CAMERA PREVIEW */
#camera-container{
  display:none;
  position:relative;
  z-index:9;
  background:#000;
  border-bottom:2px solid var(--accent);
  max-height:200px;
  overflow:hidden;
}

#camera-container video{
  width:100%;
  max-height:200px;
  object-fit:cover;
  opacity:.85;
}

#camera-overlay{
  position:absolute;
  inset:0;
  border:2px solid rgba(0,229,255,.3);
  pointer-events:none;
}

#camera-overlay::before,#camera-overlay::after{
  content:'';
  position:absolute;
  width:20px;height:20px;
  border-color:var(--accent);
  border-style:solid;
}
#camera-overlay::before{top:8px;left:8px;border-width:2px 0 0 2px;}
#camera-overlay::after{bottom:8px;right:8px;border-width:0 2px 2px 0;}

.camera-controls{
  position:absolute;
  bottom:8px;
  right:8px;
  display:flex;
  gap:6px;
}

.cam-btn{
  background:rgba(0,0,0,.7);
  border:1px solid var(--accent);
  color:var(--accent);
  padding:6px 12px;
  border-radius:8px;
  cursor:pointer;
  font-size:12px;
  backdrop-filter:blur(4px);
}

/* CHAT AREA */
#chat{
  flex:1;
  overflow-y:auto;
  padding:18px;
  display:flex;
  flex-direction:column;
  gap:14px;
  position:relative;
  z-index:1;
  scroll-behavior:smooth;
}

#chat::-webkit-scrollbar{width:4px}
#chat::-webkit-scrollbar-track{background:transparent}
#chat::-webkit-scrollbar-thumb{background:var(--border);border-radius:4px}

/* MESSAGE */
.msg{
  padding:13px 17px;
  border-radius:16px;
  max-width:82%;
  word-wrap:break-word;
  line-height:1.6;
  font-size:14.5px;
  animation:msgIn .3s ease-out;
  position:relative;
}

@keyframes msgIn{
  from{opacity:0;transform:translateY(10px)}
  to{opacity:1;transform:translateY(0)}
}

.user{
  background:linear-gradient(135deg,var(--user-bg),#1a2f42);
  align-self:flex-end;
  border:1px solid rgba(0,229,255,.15);
  border-bottom-right-radius:4px;
}

.ai{
  background:var(--ai-bg);
  border:1px solid var(--border);
  border-left:3px solid var(--accent);
  border-bottom-left-radius:4px;
  align-self:flex-start;
}

.ai.thinking{
  border-left-color:var(--accent2);
}

/* typing dots */
.dots span{
  display:inline-block;
  width:6px;height:6px;
  background:var(--accent);
  border-radius:50%;
  margin:0 2px;
  animation:dotBounce .9s infinite;
}
.dots span:nth-child(2){animation-delay:.15s}
.dots span:nth-child(3){animation-delay:.3s}

@keyframes dotBounce{
  0%,80%,100%{transform:translateY(0)}
  40%{transform:translateY(-6px)}
}

/* typing cursor */
.typing-cursor::after{
  content:'▋';
  color:var(--accent);
  animation:blink .7s infinite;
}
@keyframes blink{0%,100%{opacity:1}50%{opacity:0}}

/* IMAGE in chat */
.msg img.snap{
  max-width:100%;
  border-radius:10px;
  margin-top:8px;
  border:1px solid var(--border);
}

/* copy btn */
.copy-btn{
  position:absolute;
  top:8px;right:8px;
  background:var(--surface2);
  border:1px solid var(--border);
  color:var(--text-dim);
  padding:3px 8px;
  border-radius:6px;
  font-size:11px;
  cursor:pointer;
  opacity:0;
  transition:opacity .2s;
}
.msg:hover .copy-btn{opacity:1}
.copy-btn:hover{color:var(--accent);border-color:var(--accent);}

/* history panel */
#history-panel{
  display:none;
  position:fixed;
  top:0;right:0;
  width:300px;height:100vh;
  background:var(--surface);
  border-left:1px solid var(--border);
  z-index:100;
  flex-direction:column;
  box-shadow:-10px 0 30px rgba(0,0,0,.5);
}

#history-panel.open{display:flex}

.history-header{
  padding:16px;
  border-bottom:1px solid var(--border);
  display:flex;
  justify-content:space-between;
  align-items:center;
  font-family:'Rajdhani',sans-serif;
  font-size:16px;
  font-weight:700;
  color:var(--accent);
}

#history-list{
  flex:1;
  overflow-y:auto;
  padding:12px;
}

.history-item{
  padding:10px 12px;
  border-radius:10px;
  border:1px solid var(--border);
  margin-bottom:8px;
  cursor:pointer;
  font-size:12px;
  color:var(--text-dim);
  transition:.2s;
}
.history-item:hover{border-color:var(--accent);color:var(--text);}
.history-item .h-time{font-size:10px;color:var(--accent2);margin-bottom:4px;}

/* INPUT AREA */
.bottom{
  position:relative;
  z-index:10;
  background:linear-gradient(0deg,var(--surface) 0%,rgba(13,17,23,.95) 100%);
  border-top:1px solid var(--border);
  padding:12px 14px;
}

/* voice wave */
#voice-wave{
  display:none;
  height:36px;
  align-items:center;
  justify-content:center;
  gap:3px;
  margin-bottom:10px;
}

#voice-wave.active{display:flex}

#voice-wave span{
  display:block;
  width:3px;
  background:var(--accent);
  border-radius:3px;
  animation:wave 1s ease-in-out infinite;
}
#voice-wave span:nth-child(1){height:10px;animation-delay:0s}
#voice-wave span:nth-child(2){height:20px;animation-delay:.1s}
#voice-wave span:nth-child(3){height:30px;animation-delay:.2s}
#voice-wave span:nth-child(4){height:20px;animation-delay:.3s}
#voice-wave span:nth-child(5){height:14px;animation-delay:.4s}
#voice-wave span:nth-child(6){height:26px;animation-delay:.15s}
#voice-wave span:nth-child(7){height:18px;animation-delay:.25s}
#voice-wave span:nth-child(8){height:10px;animation-delay:.35s}

@keyframes wave{
  0%,100%{transform:scaleY(1)}
  50%{transform:scaleY(1.8)}
}

.input-row{
  display:flex;
  gap:8px;
  align-items:flex-end;
}

#input{
  flex:1;
  padding:13px 16px;
  border-radius:14px;
  border:1px solid var(--border);
  background:var(--surface2);
  color:var(--text);
  font-size:14px;
  font-family:'Noto Sans Devanagari',system-ui;
  resize:none;
  outline:none;
  transition:border-color .2s, box-shadow .2s;
  min-height:48px;
  max-height:120px;
}

#input:focus{
  border-color:var(--accent);
  box-shadow:0 0 0 3px rgba(0,229,255,.08);
}

.action-btn{
  border:none;
  border-radius:12px;
  width:48px;height:48px;
  display:flex;align-items:center;justify-content:center;
  cursor:pointer;
  transition:all .2s;
  font-size:18px;
  flex-shrink:0;
}

#send-btn{
  background:linear-gradient(135deg,var(--accent),var(--accent2));
  color:#000;
  box-shadow:0 4px 15px rgba(0,229,255,.2);
}
#send-btn:hover{transform:scale(1.05);box-shadow:0 4px 20px rgba(0,229,255,.35);}
#send-btn:active{transform:scale(.96);}

#mic-btn{
  background:var(--surface2);
  border:1px solid var(--border);
  color:var(--text-dim);
}
#mic-btn.recording{
  background:rgba(255,68,102,.15);
  border-color:var(--danger);
  color:var(--danger);
  animation:micPulse 1s infinite;
}
@keyframes micPulse{
  0%,100%{box-shadow:0 0 0 0 rgba(255,68,102,.3)}
  50%{box-shadow:0 0 0 8px rgba(255,68,102,0)}
}

#cam-btn{
  background:var(--surface2);
  border:1px solid var(--border);
  color:var(--text-dim);
}
#cam-btn.active{
  border-color:var(--accent);
  color:var(--accent);
}

/* SPEAK indicator */
#speak-indicator{
  display:none;
  align-items:center;
  gap:6px;
  font-size:11px;
  color:var(--accent2);
  padding:4px 0;
}
#speak-indicator.active{display:flex}

/* Toast */
#toast{
  position:fixed;
  bottom:90px;
  left:50%;
  transform:translateX(-50%) translateY(20px);
  background:var(--surface2);
  border:1px solid var(--accent);
  color:var(--text);
  padding:8px 18px;
  border-radius:20px;
  font-size:13px;
  opacity:0;
  transition:.3s;
  z-index:200;
  pointer-events:none;
}
#toast.show{opacity:1;transform:translateX(-50%) translateY(0)}
</style>
</head>

<body>

<header>
  <div class="logo">
    <div class="logo-icon">👑</div>
    <span class="logo-text">AI KING</span>
    <span class="logo-badge">PRO</span>
  </div>
  <div class="header-actions">
    <button class="hbtn" onclick="toggleHistory()">📋 History</button>
    <button class="hbtn" onclick="clearChat()">🗑️ Clear</button>
  </div>
</header>

<div id="status-bar">
  <div id="status-dot"></div>
  <span id="status-text">AI King तैयार है</span>
</div>

<!-- Camera Preview -->
<div id="camera-container">
  <video id="camera-feed" autoplay playsinline muted></video>
  <div id="camera-overlay"></div>
  <div class="camera-controls">
    <button class="cam-btn" onclick="capturePhoto()">📸 Capture</button>
    <button class="cam-btn" onclick="closeCamera()">✕ बंद</button>
  </div>
</div>

<!-- Chat -->
<div id="chat">
  <div class="msg ai">
    नमस्ते! 🙏 मैं Aditya Raj का AI हूँ, लेकिन मैं आपकी कैसे सहायता कर सकता हूँ?
  </div>
</div>

<!-- History Panel -->
<div id="history-panel">
  <div class="history-header">
    <span>📋 Chat History</span>
    <button class="hbtn" onclick="toggleHistory()">✕</button>
  </div>
  <div id="history-list"></div>
  <div style="padding:12px;border-top:1px solid var(--border)">
    <button class="hbtn" style="width:100%;justify-content:center;" onclick="clearHistory()">🗑️ सब Delete करो</button>
  </div>
</div>

<!-- Bottom Input -->
<div class="bottom">
  <div id="voice-wave">
    <span></span><span></span><span></span><span></span>
    <span></span><span></span><span></span><span></span>
  </div>

  <div id="speak-indicator">
    <span>🔊</span> AI बोल रहा है...
  </div>

  <div class="input-row">
    <button class="action-btn" id="mic-btn" onclick="toggleMic()" title="Voice Input">🎤</button>
    <button class="action-btn" id="cam-btn" onclick="toggleCamera()" title="Camera">📷</button>
    <textarea id="input" placeholder="लिखो या माइक से बोलो..." rows="1"></textarea>
    <button class="action-btn" id="send-btn" onclick="send()">➤</button>
  </div>
</div>

<div id="toast"></div>

<script>
const chat = document.getElementById("chat");
const input = document.getElementById("input");
const statusText = document.getElementById("status-text");
const voiceWave = document.getElementById("voice-wave");
const speakIndicator = document.getElementById("speak-indicator");

// ─── AUTO RESIZE TEXTAREA ───────────────────────────────────
input.addEventListener("input", () => {
  input.style.height = "auto";
  input.style.height = Math.min(input.scrollHeight, 120) + "px";
});

// ─── SCROLL ──────────────────────────────────────────────────
function nearBottom(){ return chat.scrollHeight - chat.scrollTop - chat.clientHeight < 150; }
function scrollBottom(){ chat.scrollTop = chat.scrollHeight; }

// ─── TOAST ───────────────────────────────────────────────────
function showToast(msg){
  const t = document.getElementById("toast");
  t.textContent = msg;
  t.classList.add("show");
  setTimeout(() => t.classList.remove("show"), 2500);
}

// ─── ADD MESSAGE ─────────────────────────────────────────────
function addMsg(text, cls, imgSrc = null){
  const should = nearBottom();
  const d = document.createElement("div");
  d.className = "msg " + cls;

  if(imgSrc){
    const img = document.createElement("img");
    img.className = "snap";
    img.src = imgSrc;
    d.appendChild(img);
    if(text){ const p = document.createElement("p"); p.style.marginTop="8px"; p.textContent=text; d.appendChild(p); }
  } else {
    d.textContent = text;
  }

  // copy button
  const cb = document.createElement("button");
  cb.className = "copy-btn";
  cb.textContent = "Copy";
  cb.onclick = () => { navigator.clipboard.writeText(d.innerText.replace("Copy","")); showToast("✅ Copied!"); };
  d.appendChild(cb);

  chat.appendChild(d);
  if(should) scrollBottom();
  return d;
}

// ─── TYPING ANIMATION ────────────────────────────────────────
async function typeText(el, text, speed = 18){
  el.classList.add("typing-cursor");
  el.textContent = "";

  // remove copy btn during typing, add back after
  const cb = el.querySelector(".copy-btn");
  if(cb) cb.remove();

  for(let i = 0; i < text.length; i++){
    el.textContent += text[i];
    if(nearBottom()) scrollBottom();
    await new Promise(r => setTimeout(r, speed));
  }

  el.classList.remove("typing-cursor");

  const newCb = document.createElement("button");
  newCb.className = "copy-btn";
  newCb.textContent = "Copy";
  newCb.onclick = () => { navigator.clipboard.writeText(el.innerText.replace("Copy","")); showToast("✅ Copied!"); };
  el.appendChild(newCb);
}

// ─── HISTORY ─────────────────────────────────────────────────
let chatHistory = JSON.parse(localStorage.getItem("aiking_history") || "[]");

function saveToHistory(userMsg, aiMsg){
  const entry = {
    time: new Date().toLocaleString("hi-IN"),
    user: userMsg.substring(0, 60) + (userMsg.length > 60 ? "..." : ""),
    ai: aiMsg.substring(0, 80) + (aiMsg.length > 80 ? "..." : ""),
    full_user: userMsg,
    full_ai: aiMsg
  };
  chatHistory.unshift(entry);
  if(chatHistory.length > 50) chatHistory = chatHistory.slice(0, 50);
  localStorage.setItem("aiking_history", JSON.stringify(chatHistory));
}

function renderHistory(){
  const list = document.getElementById("history-list");
  list.innerHTML = "";
  if(!chatHistory.length){
    list.innerHTML = '<div style="color:var(--text-dim);text-align:center;padding:30px;font-size:13px;">कोई history नहीं</div>';
    return;
  }
  chatHistory.forEach((h, i) => {
    const d = document.createElement("div");
    d.className = "history-item";
    d.innerHTML = `<div class="h-time">${h.time}</div><b>आप:</b> ${h.user}<br><span style="color:var(--text-dim)">AI: ${h.ai}</span>`;
    d.onclick = () => {
      input.value = h.full_user;
      toggleHistory();
    };
    list.appendChild(d);
  });
}

function toggleHistory(){
  const p = document.getElementById("history-panel");
  if(p.classList.toggle("open")) renderHistory();
}

function clearHistory(){
  chatHistory = [];
  localStorage.removeItem("aiking_history");
  renderHistory();
  showToast("🗑️ History delete हुई");
}

function clearChat(){
  const msgs = chat.querySelectorAll(".msg:not(:first-child)");
  msgs.forEach(m => m.remove());
  showToast("✅ Chat साफ़ हुई");
}

// ─── VOICE INPUT (Speech Recognition) ────────────────────────
let recognition = null;
let isRecording = false;

function toggleMic(){
  if(!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)){
    showToast("❌ यह browser voice support नहीं करता");
    return;
  }

  if(isRecording){
    recognition.stop();
    return;
  }

  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  recognition = new SpeechRecognition();
  recognition.lang = "hi-IN";
  recognition.continuous = false;
  recognition.interimResults = true;

  recognition.onstart = () => {
    isRecording = true;
    document.getElementById("mic-btn").classList.add("recording");
    voiceWave.classList.add("active");
    setStatus("🎤 सुन रहा हूँ...", true);
  };

  recognition.onresult = (e) => {
    const transcript = Array.from(e.results).map(r => r[0].transcript).join("");
    input.value = transcript;
  };

  recognition.onend = () => {
    isRecording = false;
    document.getElementById("mic-btn").classList.remove("recording");
    voiceWave.classList.remove("active");
    setStatus("AI King तैयार है");
    if(input.value.trim()) send();
  };

  recognition.onerror = (e) => {
    isRecording = false;
    document.getElementById("mic-btn").classList.remove("recording");
    voiceWave.classList.remove("active");
    showToast("❌ Voice error: " + e.error);
    setStatus("AI King तैयार है");
  };

  recognition.start();
}

// ─── CAMERA ──────────────────────────────────────────────────
let cameraStream = null;
let capturedImage = null;

async function toggleCamera(){
  const btn = document.getElementById("cam-btn");
  const container = document.getElementById("camera-container");

  if(cameraStream){
    closeCamera();
    return;
  }

  try{
    cameraStream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" }, audio: false });
    document.getElementById("camera-feed").srcObject = cameraStream;
    container.style.display = "block";
    btn.classList.add("active");
    btn.textContent = "📷";
    setStatus("📷 Camera चालू है");
  } catch(err){
    showToast("❌ Camera access नहीं मिला");
  }
}

function closeCamera(){
  if(cameraStream){
    cameraStream.getTracks().forEach(t => t.stop());
    cameraStream = null;
  }
  document.getElementById("camera-container").style.display = "none";
  document.getElementById("cam-btn").classList.remove("active");
  setStatus("AI King तैयार है");
}

function capturePhoto(){
  const video = document.getElementById("camera-feed");
  const canvas = document.createElement("canvas");
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  canvas.getContext("2d").drawImage(video, 0, 0);
  capturedImage = canvas.toDataURL("image/jpeg", 0.8);
  closeCamera();
  showToast("📸 Photo लिया गया! अब message भेजो");

  // show preview in input area
  const prev = document.getElementById("img-preview");
  if(prev) prev.remove();
  const preview = document.createElement("div");
  preview.id = "img-preview";
  preview.style.cssText = "display:flex;align-items:center;gap:8px;padding:6px 0;font-size:12px;color:var(--accent)";
  preview.innerHTML = `<img src="${capturedImage}" style="height:40px;border-radius:6px;border:1px solid var(--accent)"> 
    <span>Photo ready</span> 
    <button onclick="removeCaptured()" style="background:none;border:none;color:var(--danger);cursor:pointer;font-size:16px">✕</button>`
