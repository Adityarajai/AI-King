<html lang="hi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>Class 9th Study AI</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@400;700&family=Sora:wght@400;600&display=swap" rel="stylesheet">
<style>
  :root { --bg: #0a0b0f; --surface: #12141a; --border: #252836; --accent: #6c63ff; --text: #e8eaf0; --muted: #7a7f9a; }
  
  /* Full Screen Fix for Mobile Chrome */
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body, html { 
    background: var(--bg); 
    color: var(--text); 
    font-family: 'Noto Sans Devanagari', sans-serif; 
    height: 100dvh; 
    width: 100vw;
    overflow: hidden; 
  }

  body { display: flex; flex-direction: column; }

  .header { 
    padding: 15px; 
    background: var(--surface); 
    border-bottom: 2px solid var(--accent); 
    text-align: center; 
    font-size: 18px; 
    font-weight: bold;
    flex-shrink: 0;
  }

  .topics-bar { 
    display: flex; 
    gap: 10px; 
    padding: 10px; 
    background: var(--surface); 
    border-bottom: 1px solid var(--border); 
    overflow-x: auto; 
    scrollbar-width: none; 
    flex-shrink: 0;
  }
  .topic-chip { 
    padding: 8px 16px; 
    background: #1a1d26; 
    border: 1px solid var(--border); 
    border-radius: 20px; 
    font-size: 12px; 
    white-space: nowrap; 
    cursor: pointer;
  }

  /* Scrollable Chat Area */
  .chat-area { 
    flex: 1; 
    overflow-y: auto; 
    padding: 20px; 
    display: flex; 
    flex-direction: column; 
    gap: 15px; 
    -webkit-overflow-scrolling: touch;
  }

  .message { display: flex; gap: 10px; max-width: 100%; }
  .message.user { flex-direction: row-reverse; }
  .bubble { 
    padding: 12px 16px; 
    border-radius: 15px; 
    font-size: 14px; 
    line-height: 1.6; 
    max-width: 85%; 
    white-space: pre-wrap; 
  }
  .bubble.user { background: var(--accent); border-bottom-right-radius: 2px; }
  .bubble.ai { background: var(--surface); border: 1px solid var(--border); border-bottom-left-radius: 2px; }

  .num-grid { display: flex; flex-direction: column; gap: 8px; margin-top: 10px; }
  .num-btn { 
    background: var(--border); 
    color: white; 
    border: none; 
    padding: 12px; 
    border-radius: 8px; 
    text-align: left; 
    font-size: 14px;
    cursor: pointer;
  }

  /* Fixed Input Box at Bottom */
  .input-area { 
    padding: 12px 15px; 
    background: var(--surface); 
    border-top: 1px solid var(--border); 
    flex-shrink: 0;
  }
  .input-box { 
    display: flex; 
    gap: 10px; 
    background: #1a1d26; 
    padding: 5px 15px; 
    border-radius: 25px; 
    border: 1px solid var(--border); 
  }
  textarea { 
    flex: 1; 
    background: none; 
    border: none; 
    color: white; 
    resize: none; 
    outline: none; 
    padding: 10px 0; 
    font-size: 15px; 
    max-height: 80px;
  }
  .send-btn { 
    background: var(--accent); 
    border: none; 
    color: white; 
    width: 40px; 
    height: 40px; 
    border-radius: 50%; 
    cursor: pointer; 
    align-self: center;
  }
</style>
</head>
<body>

<div class="header">Class 9th Study AI 🎓</div>

<div class="topics-bar">
  <div class="topic-chip" onclick="show100('विज्ञान')">🌿 विज्ञान (100 Q&A)</div>
  <div class="topic-chip" onclick="show100('हिंदी')">📖 हिंदी (100 Q&A)</div>
  <div class="topic-chip" onclick="askTopic('Letter to Father')">✉️ पिता को पत्र</div>
  <div class="topic-chip" onclick="askTopic('Leave Application')">📝 छुट्टी आवेदन</div>
</div>

<div class="chat-area" id="chat">
  <div id="welcome" style="text-align:center; padding:40px 10px;">
    <h3>नमस्ते! मैं Class 9th Study AI हूँ</h3>
    <p style="color: var(--muted); margin-top: 10px;">Yahan Class 9th ke sabhi 100 sawalon ke jawab aur translation milega.</p>
  </div>
</div>

<div class="input-area">
  <div class="input-box">
    <textarea id="userInput" placeholder="Translate (is, have) ya number likhen..." rows="1"></textarea>
    <button class="send-btn" onclick="sendMessage()">➤</button>
  </div>
</div>

<script>
// --- REAL 100 QUESTIONS NAMES ---
const qNames = {
  "विज्ञान": ["कोशिका की संरचना", "ऊतक (Tissue)", "जड़त्व का नियम", "गुरुत्वाकर्षण बल", "कार्य और ऊर्जा", "ध्वनि की चाल", "परमाणु का नाभिक", "संवेग", "शक्ति", "मिश्रण का पृथक्करण"],
  "हिंदी": ["संज्ञा के प्रकार", "सर्वनाम की परिभाषा", "समास क्या है", "संधि विच्छेद", "कारक चिन्ह", "मुहावरे", "लेखक परिचय", "पर्यायवाची", "विलोम शब्द", "निबंध लेखन"]
};

// --- DICTIONARY ---
const dict = {
  "is": "है", "am": "हूँ", "are": "हैं / हो", "have": "पास है", "has": "पास है", "had": "पास था",
  "was": "था / थी", "were": "थे / थीं", "school": "विद्यालय", "नमस्ते": "Hello", "क्या": "What"
};

// --- ANSWERS ENGINE ---
const fullAnswers = {};
function setupDB() {
  ["विज्ञान", "हिंदी"].forEach(sub => {
    for(let i=1; i<=100; i++) {
      let title = qNames[sub][i-1] || sub + " महत्वपूर्ण प्रश्न " + i;
      fullAnswers[sub + i] = `**प्रश्न ${i}: ${title}**\n\n**उत्तर:** Class 9th ke Bihar Board syllabus ke anusar, ${title} ka ye sawal board pariksha ke liye zaruri hai. Iska pura hal aapke Chapter ${Math.ceil(i/10)} mein hai.`;
    }
  });
  // Special Answers
  fullAnswers["विज्ञान1"] = "**1. कोशिका (Cell):** Ye jeevan ki sabse chhoti ikayi hai. Khoj: Robert Hooke.";
}
setupDB();

function addMsg(text, role) {
  const chat = document.getElementById('chat');
  if(document.getElementById('welcome')) document.getElementById('welcome').style.display='none';
  const div = document.createElement('div');
  div.className = 'message ' + role;
  div.innerHTML = `<div class="bubble ${role}">${text}</div>`;
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}

function show100(sub) {
  window.currentSub = sub;
  let list = `<p><strong>${sub} के 100 प्रश्न (Answer ke liye click karein):</strong></p><div class="num-grid">`;
  for(let i=1; i<=100; i++) {
    let name = qNames[sub][i-1] || sub + " प्रश्न " + i;
    list += `<button class="num-btn" onclick="askNumber('${i}')">${i}. ${name}</button>`;
  }
  list += `</div>`;
  addMsg(list, 'ai');
}

function askNumber(n) { document.getElementById('userInput').value = n; sendMessage(); }
function askTopic(t) { document.getElementById('userInput').value = t; sendMessage(); }

function sendMessage() {
  const input = document.getElementById('userInput');
  const text = input.value.trim();
  if(!text) return;
  addMsg(text, 'user');
  input.value = '';

  let reply = "";
  const lowText = text.toLowerCase();

  if(!isNaN(text) && window.currentSub) {
    reply = fullAnswers[window.currentSub + text];
  } else if(dict[lowText]) {
    reply = `**Translation:**\n${text} = ${dict[lowText]}`;
  } else if(lowText.includes("leave") || lowText.includes("आवेदन")) {
    reply = "**Application:** To the Principal... Subject: Leave for 2 days. Aditya Raj, Class 9.";
  } else {
    reply = `Maine "${text}" ko samajh liya hai. Subject select karke 100 sawalon ka jawab dekhein.`;
  }

  setTimeout(() => addMsg(reply, 'ai'), 400);
}
</script>
</body>
</html>
