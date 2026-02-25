<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI King - Pro</title>
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/tesseract.js@4/dist/tesseract.min.js"></script>
    <style>
        * { box-sizing: border-box; }
        body { font-family: 'Segoe UI', Roboto, sans-serif; background-color: #000; color: #fff; margin: 0; padding: 0; display: flex; flex-direction: column; height: 100vh; overflow: hidden; }
        
        header { padding: 15px; text-align: center; border-bottom: 1px solid #333; background: #111; }
        h2 { color: #00ffcc; margin: 0; font-size: 24px; letter-spacing: 1px; }

        #chat-container { flex: 1; overflow-y: auto; padding: 20px; display: flex; flex-direction: column; gap: 15px; background: #000; }
        
        .message { padding: 14px 18px; border-radius: 18px; line-height: 1.6; max-width: 85%; word-wrap: break-word; font-size: 16px; position: relative; }
        .user-msg { background-color: #2b2b2b; align-self: flex-end; color: #fff; border-bottom-right-radius: 4px; }
        .ai-msg { background-color: #1a1a1a; align-self: flex-start; color: #e0e0e0; border-left: 4px solid #00ffcc; border-bottom-left-radius: 4px; border: 1px solid #333; }

        .input-area { padding: 15px; background: #111; display: flex; gap: 10px; align-items: center; border-top: 1px solid #333; }
        
        input { flex: 1; padding: 14px; border-radius: 25px; border: 1px solid #444; background: #1a1a1a; color: #fff; outline: none; font-size: 16px; }

        .btn { border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: 0.2s; }
        .send-btn { background: #00ffcc; color: #000; padding: 12px 20px; border-radius: 25px; font-weight: bold; min-width: 80px; }
        .icon-btn { background: #333; color: #fff; min-width: 45px; height: 45px; border-radius: 50%; font-size: 20px; border: 1px solid #444; }
        .mic-btn { background: #ff4b2b; }
        .listening { animation: pulse 1.5s infinite; background: #00ffcc; color: #000; }

        .speak-btn { background: #222; color: #00ffcc; border: 1px solid #444; padding: 6px 12px; border-radius: 15px; font-size: 12px; margin-top: 10px; cursor: pointer; }

        /* Camera Modal */
        #cam-modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: #000; z-index: 9999; flex-direction: column; align-items: center; justify-content: center; }
        video { width: 90%; max-width: 450px; border-radius: 15px; border: 2px solid #00ffcc; margin-bottom: 20px; }
        .cam-btns { display: flex; gap: 15px; }
        
        @keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(0, 255, 204, 0.7); } 70% { box-shadow: 0 0 0 15px rgba(0, 255, 204, 0); } 100% { box-shadow: 0 0 0 0 rgba(0, 255, 204, 0); } }
    </style>
</head>
<body>

    <header>
        <h2>AI King</h2>
    </header>

    <div id="chat-container">
        <div class="message ai-msg">प्रणाम आदित्य! मैं आपका AI King हूँ। फोटो खींचने के लिए 📷 दबाएँ, बोलने के लिए 🎤।</div>
    </div>

    <div id="cam-modal">
        <video id="video" autoplay playsinline></video>
        <div class="cam-btns">
            <button class="send-btn" style="background: #ff4b2b; color: #fff;" onclick="stopCamera()">रद्द करें</button>
            <button class="send-btn" onclick="capturePhoto()">फोटो लें</button>
        </div>
        <canvas id="canvas" style="display:none;"></canvas>
    </div>

    <div class="input-area">
        <button class="btn icon-btn" onclick="startCamera()">📷</button>
        <input type="file" id="fileInput" accept="image/*" capture="environment" style="display:none" onchange="handleFile(event)">
        
        <button id="micBtn" class="btn icon-btn mic-btn" onclick="toggleMic()">🎤</button>
        <input type="text" id="userInput" placeholder="यहाँ लिखें..." onkeydown="if(event.key==='Enter') sendMessage()">
        <button class="btn send-btn" onclick="sendMessage()">भेजें</button>
    </div>

    <script>
        let chatHistory = ["तुम AI King हो, जिसे आदित्य ने बनाया है। हमेशा स्पष्ट हिंदी में जवाब दो।"];

        // 1. कैमरा एक्सेस (With Fallback)
        const video = document.getElementById('video');
        const modal = document.getElementById('cam-modal');

        async function startCamera() {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } });
                video.srcObject = stream;
                modal.style.display = 'flex';
            } catch (err) {
                console.log("Direct cam failed, opening file picker...");
                document.getElementById('fileInput').click(); // अगर कैमरा ब्लॉक है तो गैलरी/कैमरा ऐप खुलेगा
            }
        }

        function stopCamera() {
            const stream = video.srcObject;
            if (stream) stream.getTracks().forEach(t => t.stop());
            modal.style.display = 'none';
        }

        function capturePhoto() {
            const canvas = document.getElementById('canvas');
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            canvas.getContext('2d').drawImage(video, 0, 0);
            processImage(canvas.toDataURL());
            stopCamera();
        }

        function handleFile(e) {
            const file = e.target.files[0];
            if (!file) return;
            const reader = new FileReader();
            reader.onload = (event) => processImage(event.target.result);
            reader.readAsDataURL(file);
        }

        function processImage(imgData) {
            appendMsg("फोटो से टेक्स्ट पढ़ रहा हूँ...", 'ai-msg', 'ocr-load');
            Tesseract.recognize(imgData, 'hin+eng').then(({ data: { text } }) => {
                document.getElementById('ocr-load').remove();
                document.getElementById('userInput').value = text.trim();
                appendMsg("फोटो का टेक्स्ट: " + text.trim(), 'user-msg');
            });
        }

        // 2. माइक्रोफोन (Smart Fix)
        const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = 'hi-IN';
        let listening = false;

        function toggleMic() {
            if (!listening) { recognition.start(); } else { recognition.stop(); }
        }
        recognition.onstart = () => { listening = true; document.getElementById('micBtn').classList.add('listening'); };
        recognition.onend = () => { listening = false; document.getElementById('micBtn').classList.remove('listening'); };
        recognition.onresult = (e) => { document.getElementById('userInput').value = e.results[0][0].transcript; sendMessage(); };

        // 3. आवाज (Speaker)
        function speak(text) {
            window.speechSynthesis.cancel();
            const msg = new SpeechSynthesisUtterance(text);
            msg.lang = 'hi-IN';
            window.speechSynthesis.speak(msg);
        }

        // 4. मैसेज भेजना (Fixed UI & Logic)
        async function sendMessage() {
            const input = document.getElementById('userInput');
            const text = input.value.trim();
            if (!text) return;

            appendMsg(text, 'user-msg');
            input.value = "";
            chatHistory.push("User: " + text);

            const aiId = "ai-" + Date.now();
            appendMsg("AI King सोच रहा है...", 'ai-msg', aiId);

            try {
                const res = await fetch(`https://text.pollinations.ai/${encodeURIComponent(chatHistory.join("\n"))}?model=openai`);
                const data = await res.text();
                const aiBox = document.getElementById(aiId);
                aiBox.innerHTML = `<div>${data}</div><button class="speak-btn" onclick="speak(\`${data.replace(/['"`]/g, '')}\`)">🔊 जवाब सुनें</button>`;
                if (window.MathJax) MathJax.typesetPromise([aiBox]);
                chatHistory.push("AI: " + data);
            } catch (err) { document.getElementById(aiId).innerText = "सर्वर एरर!"; }
        }

        function appendMsg(text, cls, id) {
            const container = document.getElementById('chat-container');
            const div = document.createElement('div');
            div.className = "message " + cls;
            if (id) div.id = id;
            div.innerText = text;
            container.appendChild(div);
            container.scrollTop = container.scrollHeight;
        }
    </script>
</body>
</html>
