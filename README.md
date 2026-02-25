<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <title>AI King - Smart Vision</title>
    <script src="https://cdn.jsdelivr.net/npm/tesseract.js@4/dist/tesseract.min.js"></script>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { background: #000; color: #fff; font-family: sans-serif; display: flex; flex-direction: column; height: 100vh; overflow: hidden; }
        header { padding: 15px; text-align: center; border-bottom: 1px solid #333; background: #111; }
        #chat-container { flex: 1; overflow-y: auto; padding: 15px; display: flex; flex-direction: column; gap: 12px; }
        .message { padding: 12px 16px; border-radius: 18px; max-width: 85%; font-size: 16px; line-height: 1.5; }
        .user-msg { background: #2b2b2b; align-self: flex-end; }
        .ai-msg { background: #1a1a1a; border: 1px solid #333; border-left: 4px solid #00ffcc; align-self: flex-start; }
        .chat-img { max-width: 100%; border-radius: 10px; margin-bottom: 5px; border: 1px solid #444; }
        .input-area { padding: 10px; background: #111; display: flex; gap: 10px; align-items: center; border-top: 1px solid #333; }
        input { flex: 1; padding: 12px 18px; border-radius: 25px; border: 1px solid #444; background: #1a1a1a; color: #fff; outline: none; }
        .btn { border: none; cursor: pointer; border-radius: 50%; width: 42px; height: 42px; display: flex; align-items: center; justify-content: center; }
        .cam-btn { background: #333; color: #fff; }
        .mic-btn { background: #ff4b2b; color: #fff; }
        .send-btn { background: #00ffcc; color: #000; width: auto; padding: 0 15px; border-radius: 20px; font-weight: bold; }
        #cam-modal { display: none; position: fixed; inset: 0; background: #000; z-index: 1000; flex-direction: column; align-items: center; justify-content: center; }
        video { width: 100%; max-height: 70%; object-fit: cover; }
        .speak-btn { background: #222; color: #00ffcc; border: 1px solid #444; padding: 5px 10px; border-radius: 10px; font-size: 12px; margin-top: 5px; cursor: pointer; }
    </style>
</head>
<body>

<header><h2 style="color:#00ffcc;">AI King</h2></header>

<div id="chat-container">
    <div class="message ai-msg">प्रणाम! अब मैं फोटो के शब्दों को पढ़कर जवाब दे सकता हूँ। 📷 दबाकर फोटो खींचें।</div>
</div>

<div id="cam-modal">
    <video id="video" autoplay playsinline></video>
    <div style="padding:20px; display:flex; gap:20px;">
        <button class="send-btn" style="background:#ff4b2b; color:#fff;" onclick="closeCam()">बंद करें</button>
        <button class="send-btn" onclick="takeShot()">फोटो लें</button>
    </div>
    <canvas id="canvas" style="display:none;"></canvas>
</div>

<div class="input-area">
    <button class="btn cam-btn" onclick="openCam()">📷</button>
    <button id="micBtn" class="btn mic-btn" onclick="startVoice()">🎤</button>
    <input type="text" id="userInput" placeholder="संदेश या फोटो का सवाल...">
    <button class="btn send-btn" onclick="send()">भेजें</button>
</div>

<script>
    let chatHistory = ["तुम AI King हो। फोटो से मिले टेक्स्ट का हिंदी में सटीक जवाब दो।"];
    const chatContainer = document.getElementById('chat-container');

    // Camera + OCR Fix
    async function openCam() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } });
            document.getElementById('video').srcObject = stream;
            document.getElementById('cam-modal').style.display = 'flex';
        } catch (e) { alert("कैमरा एक्सेस नहीं मिला!"); }
    }

    function closeCam() {
        const stream = document.getElementById('video').srcObject;
        if (stream) stream.getTracks().forEach(t => t.stop());
        document.getElementById('cam-modal').style.display = 'none';
    }

    async function takeShot() {
        const canvas = document.getElementById('canvas');
        const video = document.getElementById('video');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        canvas.getContext('2d').drawImage(video, 0, 0);
        const dataUrl = canvas.toDataURL('image/png');
        
        appendImg(dataUrl);
        closeCam();
        
        appendMsg("फोटो से सवाल पढ़ रहा हूँ... कृपया रुकें।", 'ai-msg', 'ocr-status');

        // OCR: Photo se text nikalna
        Tesseract.recognize(dataUrl, 'hin+eng').then(({ data: { text } }) => {
            document.getElementById('ocr-status').remove();
            if(text.trim()) {
                appendMsg("मैंने यह पढ़ा: " + text.trim(), 'user-msg');
                send(text);
            } else {
                appendMsg("माफी चाहता हूँ, फोटो साफ नहीं है। कृपया दोबारा खींचें।", 'ai-msg');
            }
        });
    }

    // Voice & Messaging
    const rec = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    rec.lang = 'hi-IN';
    function startVoice() { rec.start(); }
    rec.onresult = (e) => { document.getElementById('userInput').value = e.results[0][0].transcript; send(); };

    async function send(customText) {
        const input = document.getElementById('userInput');
        const val = customText || input.value.trim();
        if (!val) return;

        if(!customText) appendMsg(val, 'user-msg');
        input.value = "";
        chatHistory.push("User: " + val);

        const aiId = "ai-" + Date.now();
        appendMsg("AI King सोच रहा है...", 'ai-msg', aiId);

        try {
            const res = await fetch(`https://text.pollinations.ai/${encodeURIComponent(chatHistory.join("\n"))}?model=openai`);
            const data = await res.text();
            document.getElementById(aiId).innerHTML = `<div>${data}</div><button class="speak-btn" onclick="speak(\`${data.replace(/['"`]/g, '')}\`)">🔊 सुनें</button>`;
            chatHistory.push("AI: " + data);
        } catch (e) { document.getElementById(aiId).innerText = "सर्वर एरर!"; }
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    function appendMsg(t, c, id) {
        const d = document.createElement('div');
        d.className = "message " + c; if(id) d.id = id; d.innerText = t;
        chatContainer.appendChild(d);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    function appendImg(src) {
        const d = document.createElement('div');
        d.className = "message user-msg";
        d.innerHTML = `<img src="${src}" class="chat-img">`;
        chatContainer.appendChild(d);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    function speak(t) {
        window.speechSynthesis.cancel();
        const m = new SpeechSynthesisUtterance(t); m.lang = 'hi-IN';
        window.speechSynthesis.speak(m);
    }
</script>
</body>
</html>
