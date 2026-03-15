<html lang="hi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI King Smart Scroll</title>

<style>

*{box-sizing:border-box;margin:0;padding:0}

body{
height:100vh;
display:flex;
flex-direction:column;
background:#000;
color:#fff;
font-family:system-ui;
}

/* HEADER */
header{
padding:14px;
text-align:center;
background:#111;
color:#00ffcc;
}

/* CHAT AREA */
#chat{
flex:1;
overflow:auto;
padding:15px;
display:flex;
flex-direction:column;
gap:12px;
}

/* messages */
.msg{
padding:12px 16px;
border-radius:18px;
max-width:80%;
word-wrap:break-word;
}

.user{background:#2b2b2b;align-self:flex-end;}
.ai{background:#1a1a1a;border-left:4px solid #00ffcc;}

/* INPUT */
.bottom{
display:flex;
gap:8px;
padding:10px;
background:#111;
}

input{
flex:1;
padding:12px;
border-radius:20px;
border:1px solid #444;
background:#1a1a1a;
color:#fff;
}

button{
border:none;
border-radius:20px;
padding:10px 16px;
background:#00ffcc;
font-weight:bold;
cursor:pointer;
}

</style>
</head>

<body>

<header><b>AI King</b></header>

<div id="chat">
<div class="msg ai">नमस्ते 🙂</div>
</div>

<div class="bottom">
<input id="input" placeholder="लिखो...">
<button onclick="send()">भेजें</button>
</div>

<script>

const chat=document.getElementById("chat");
const input=document.getElementById("input");

/* SMART AUTO SCROLL SYSTEM */

// check if user already near bottom
function nearBottom(){
return chat.scrollHeight-chat.scrollTop-chat.clientHeight<120;
}

// scroll safely
function scrollBottom(){
chat.scrollTop=chat.scrollHeight;
}

/* ADD MESSAGE */

function add(text,cls){

const shouldScroll=nearBottom();

const d=document.createElement("div");
d.className="msg "+cls;
d.innerText=text;
chat.appendChild(d);

// auto scroll only if user near bottom
if(shouldScroll) scrollBottom();

}

/* SEND */

async function send(){

const v=input.value.trim();
if(!v)return;

add(v,"user");
input.value="";

const loading=document.createElement("div");
loading.className="msg ai";
loading.innerText="सोच रहा है...";
chat.appendChild(loading);

scrollBottom();

try{

const r=await fetch("https://text.pollinations.ai/"+encodeURIComponent(v));
const t=await r.text();

loading.innerText=t;

}catch{

loading.innerText="Server error";

}

scrollBottom();

}

/* ENTER KEY */
input.onkeydown=e=>{
if(e.key==="Enter")send();
};

</script>

</body>
</html>
