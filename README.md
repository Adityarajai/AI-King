<html lang="hi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI King 👑 - Illusion AI</title>
<style>
:root {--bg:#0a0b0f; --surface:#12141a; --border:#252836; --accent:#6c63ff; --text:#e8eaf0;}
*{margin:0;padding:0;box-sizing:border-box;}
body{height:100vh;background:var(--bg);color:var(--text);font-family:sans-serif;display:flex;flex-direction:column;}
.header{padding:15px;background:var(--surface);text-align:center;font-size:18px;font-weight:bold;border-bottom:2px solid var(--accent);}
.topics-bar{display:flex;gap:10px;padding:10px;overflow-x:auto;background:var(--surface);}
.topic-chip{padding:8px 15px;border-radius:20px;background:#1a1d26;cursor:pointer;font-size:12px;}
.chat-area{flex:1;overflow-y:auto;padding:15px;display:flex;flex-direction:column;}
.input-area{padding:10px;background:var(--surface);display:flex;flex-direction:column;gap:5px;}
textarea{width:100%;padding:10px;border-radius:10px;border:none;outline:none;}
button{padding:10px 15px;border:none;border-radius:10px;background:var(--accent);color:var(--text);cursor:pointer;font-size:14px;transition:0.2s;}
button:hover{background:#574fd1;}
.message{background:#1a1d26;padding:10px 12px;border-radius:10px;margin:5px 0;align-self:flex-start;}
.message.user{background:#6c63ff;color:#fff;align-self:flex-end;}
.qa-item{margin-bottom:10px;padding:10px;border:1px solid var(--border);border-radius:10px;}
.qa-q{color:var(--accent);font-weight:bold;}
.qa-a{font-size:13px;}
</style>
</head>
<body>

<div class="header">👑 AI King - Illusion AI</div>
<div class="topics-bar" id="topicsBar"></div>
<div class="chat-area" id="chat"><div style="text-align:center">👑 Welcome to AI King (Illusion)</div></div>
<div class="input-area">
<textarea id="input" placeholder="कुछ लिखें..."></textarea>
<button onclick="sendMessage()">Send</button>
</div>

<script>
// Sample Q&A offline
const sampleData={
"विज्ञान":[
{q:"कोशिका क्या है?",a:"जीवन की सबसे छोटी इकाई।"},
{q:"गुरुत्वाकर्षण क्या है?",a:"दो पिंडों के बीच आकर्षण बल।"}
],
"गणित":[
{q:"पाई का मान?",a:"22/7 या 3.14"},
{q:"वर्ग क्या है?",a:"समान भुजाओं वाला चतुर्भुज"}
],
"हिंदी":[
{q:"संज्ञा क्या है?",a:"नाम को संज्ञा कहते हैं"},
{q:"क्रिया क्या है?",a:"कार्य बताने वाले शब्द"}
],
"अंग्रेज़ी":[
{q:"What is noun?",a:"Name of person/place/thing"},
{q:"What is verb?",a:"Action word"}
],
"सामाजिक विज्ञान":[
{q:"लोकतंत्र क्या है?",a:"जनता द्वारा शासन"},
{q:"संविधान क्या है?",a:"देश का सर्वोच्च कानून"}
]
};

// Topics buttons
const subjects=Object.keys(sampleData);
const topicsBar=document.getElementById('topicsBar');
subjects.forEach(sub=>{
  let btn=document.createElement('div');
  btn.className='topic-chip';
  btn.innerText=sub;
  btn.onclick=()=>showSampleQ(sub);
  topicsBar.appendChild(btn);
});
let letterBtn=document.createElement('div');
letterBtn.className='topic-chip';
letterBtn.innerText='✉️ पत्र';
letterBtn.onclick=showLetter;
topicsBar.appendChild(letterBtn);

// Show sample Q&A
function showSampleQ(sub){
  let html=`<h3>${sub} - Sample Questions</h3>`;
  sampleData[sub].forEach((item,i)=>{
    html+=`<div class="qa-item"><div class="qa-q">${i+1}. ${item.q}</div><div class="qa-a">उत्तर: ${item.a}</div></div>`;
  });
  document.getElementById("chat").innerHTML=html;
  scrollChat();
}

// Letters
function showLetter(){
  let txt=`<b>पिता जी को पत्र:</b><br><br>आदरणीय पिताजी,<br>सादर प्रणाम। मैं यहाँ कुशल हूँ। आशा है आप भी स्वस्थ होंगे।<br>मुझे 2 दिन की छुट्टी चाहिए क्योंकि मैं बीमार हूँ।<br><br>आपका पुत्र<br>नाम<br><br>
<b>माता जी को पत्र:</b><br><br>प्रिय माताजी,<br>सादर प्रणाम। मैं ठीक हूँ। आप कैसी हैं?<br>मैं जल्द घर आऊंगा।<br><br>आपका बेटा`;
  document.getElementById("chat").innerHTML=txt;
  scrollChat();
}

// Chat
function sendMessage(){
  let input=document.getElementById('input');
  let msg=input.value.trim();
  if(msg==="") return;
  addMessage(msg,'user');
  input.value='';
  generateIllusionAnswer(msg);
}

function addMessage(text,sender){
  let div=document.createElement('div');
  div.className='message';
  if(sender==='user') div.classList.add('user');
  div.innerHTML=text;
  document.getElementById('chat').appendChild(div);
  scrollChat();
}

function scrollChat(){
  const chat=document.getElementById('chat');
  chat.scrollTop=chat.scrollHeight;
}

// Illusion AI logic
function generateIllusionAnswer(msg){
  msg=msg.toLowerCase();
  // Check sample Q&A
  for(let sub in sampleData){
    for(let item of sampleData[sub]){
      if(msg.includes(item.q.toLowerCase().split(" ")[0])){
        addMessage(`<b>${item.q}</b><br>उत्तर: ${item.a}`,'ai');
        return;
      }
    }
  }
  // Unknown question → generate smart-sounding generic answer
  const genericAnswers=[
    "यह एक महत्वपूर्ण प्रश्न है। इसका उत्तर कुछ इस प्रकार हो सकता है।",
    "मैं इसे समझा रहा हूँ, ध्यान से देखें।",
    "यह प्रश्न दिलचस्प है। इसका उत्तर खोजा जा रहा है।",
    "आपके सवाल पर विचार किया गया। इसका उत्तर निम्न है।",
    "मैंने आपके प्रश्न का विश्लेषण किया और यह उत्तर सुझाया।"
  ];
  let randomAnswer=genericAnswers[Math.floor(Math.random()*genericAnswers.length)];
  addMessage(randomAnswer,'ai');
}
</script>
</body>
</html>
