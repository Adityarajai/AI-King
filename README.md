<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<script src="https://cdn.jsdelivr.net/npm/tesseract.js@5/dist/tesseract.min.js"></script>

<style>
body{margin:0;background:#000;color:#fff;font-family:system-ui;display:flex;flex-direction:column;height:100vh}
#chat{flex:1;overflow:auto;padding:15px;display:flex;flex-direction:column;gap:10px}
.msg{padding:12px;border-radius:16px;max-width:85%}
.user{background:#2b2b2b;align-self:flex-end}
.ai{background:#1a1a1a;border-left:4px solid #00ffcc}
.bottom{display:flex;padding:10px;background:#111;gap:8px}
button{border:none;border-radius:20px;padding:10px 14px;font-weight:bold;cursor:pointer}
#modal{display:none;position:fixed;inset:0;background:#000;flex-direction:column;justify-content:center}
video{width:100%}
</style>
</head>

<body>

<div id="chat">
<div class="msg ai">📷 फोटो भेजो — मैं टेक्स्ट पढ़ दूँगा (NO API 🙂)</div>
</div>

<div id="modal">
<video id="video" autoplay playsinline></video>
<button onclick="closeCam()">बंद</button>
<button onclick="shot()">फोटो लें</button>
<canvas id="canvas" style="display:none"></canvas>
</div>

<div class="bottom">
<button onclick="openCam()">📷 कैमरा</button>
</div>

<script>

const chat=document.getElementById("chat");
const video=document.getElementById("video");
const canvas=document.getElementById("canvas");
const modal=document.getElementById("modal");

function add(t,c="ai"){
const d=document.createElement("div");
d.className="msg "+c;
d.innerText=t;
chat.appendChild(d);
chat.scrollTop=chat.scrollHeight;
}

/* CAMERA */

async function openCam(){
const s=await navigator.mediaDevices.getUserMedia({video:true});
video.srcObject=s;
modal.style.display="flex";
}

function closeCam(){
const s=video.srcObject;
if(s)s.getTracks().forEach(t=>t.stop());
modal.style.display="none";
}

/* ⭐ PHOTO OCR */

async function shot(){

canvas.width=video.videoWidth;
canvas.height=video.videoHeight;
canvas.getContext("2d").drawImage(video,0,0);

const img=canvas.toDataURL("image/jpeg");

closeCam();

/* show image */
const d=document.createElement("div");
d.className="msg user";
d.innerHTML=`<img src="${img}" style="max-width:100%">`;
chat.appendChild(d);

add("📖 फोटो पढ़ रहा हूँ...");

/* REAL TEXT READING (NO API) */

const { data } = await Tesseract.recognize(
img,
'eng+hin',
{ logger:m=>console.log(m) }
);

add("📄 मिला टेक्स्ट:\n\n"+data.text);

}

</script>
</body>
</html>