<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <title>AI King - Full Screen</title>
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        
        /* Full Screen Setup */
        html, body { 
            height: 100%; 
            width: 100%; 
            background-color: #000; 
            color: #fff; 
            overflow: hidden; 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }

        body { display: flex; flex-direction: column; }
        
        header { 
            width: 100%; 
            padding: 12px; 
            text-align: center; 
            background: #111; 
            border-bottom: 1px solid #333; 
            flex-shrink: 0;
        }
        h2 { color: #00ffcc; font-size: 18px; text-transform: uppercase; letter-spacing: 1.5px; }

        /* Scrollable Chat Area */
        #chat-container { 
            flex: 1; 
            overflow-y: auto; 
            padding: 15px; 
            display: flex; 
            flex-direction: column; 
            gap: 12px; 
            background: #000;
            width: 100%;
            -webkit-overflow-scrolling: touch;
        }
        
        .message { padding: 12px 16px; border-radius: 20px; line-height: 1.5; max-width: 85%; word-wrap: break-word; font-size: 16px; }
        .user-msg { background-color: #2b2b2b; align-self: flex-end; border-bottom-right-radius: 4px; }
        .ai-msg { background-color: #1a1a1a; align-self: flex-start; border: 1px solid #333; border-left: 4px solid #00ffcc; border-bottom-left-radius: 4px; }

        .chat-img { max-width: 100%; border-radius: 12px; display: block; margin-top: 5px; border: 1px solid #444; }

        /* Input Area at Bottom */
        .input-area { 
            width: 100%; 
            padding: 10px 15px 25px 15px; /* Bottom padding for mobile home bars */
            background: #111; 
            display: flex; 
            gap: 10px; 
            align-items: center; 
            border-top: 1px solid #333;
            flex-shrink: 0;
        }
        
        input { flex: 1; padding: 12px 18px; border-radius: 25px; border: 1px solid #444; background: #1a1a1a; color: #fff; outline: none; font-size: 16px; }

        .btn { border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; border-radius: 50%; }
        .icon-btn { width: 42px; height: 42px; background: #333; color: #fff; border: 1px solid #444; font-size: 18px; }
        .mic-btn { background: #ff4b2b; color: #fff; width: 42px; height: 42px; }
        .send-btn { background: #00ffcc; color: #000; border-radius: 20px; padding: 0 15px; font-weight: bold; height: 40px; font-size: 14px; }
        .listening { animation: pulse 1s infinite; background: #00ffcc; color: #000; }

        /* Camera View */
        #cam-modal { display: none; position: fixed; inset: 0; background: #000; z-index: 1000; flex-direction: column; align-items: center; justify-content: center; }
        video { width: 100%; max-height: 80%; object-fit: cover; }
        
        .speak-btn { background: #222; color: #00ffcc; border: 1px solid #444; padding: 5px 10px; border-radius: 12px; font-size: 12px; margin-top: 8px; cursor: pointer; }

        @keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(0, 255, 204, 0.7); } 70% { box-shadow: 0 0 0 10px rgba(0, 255, 204, 0); } 100% { box-shadow: 0 0 0 0 rgba(0, 255, 204, 0); } }
    </style>
</head>
<body>

    <header><h2>AI King</h2></header>

    <div id="chat-container">
        <div class="message ai-msg">नमस्ते आदित्य! अब मैं पूरी स्क्रीन पर हूँ। आप आसानी से ऊपर-नीचे स्क्रॉल कर सकते हैं।</div>
    </div>

    <div id="cam-modal">
        <video id="video" autoplay playsinline></video>
        <div style="padding: 20px; display: flex; gap: 20px; width: 100%; justify-content: center; background: rgba(0,0,0,0.8);">
            <button class="send-btn" style="background:#ff4b2b; color:#fff;" onclick="closeCam()">बंद करें</button>
            <button class="send-btn" onclick="takeShot()">फोटो खींचें</button>
        </div>
        <canvas id="canvas" style="display:none;"></canvas>
    </div>

    <div class="input-area">
        <button class="btn icon-btn" onclick="openCam()">📷</button>
        <button id="micBtn" class="btn mic-btn" onclick="startVoice()">🎤</button>
        <input type="text" id="userInput" placeholder="संदेश..." onkeydown="if(event.key==='Enter') send()">
        <button class="btn send-btn" onclick="send()">भेजें</button>
    </div>

    <script>
        let history = ["तुम AI King हो। आदित्य ने तुम्हें बनाया है। हिंदी में संक्षिप्त जवाब दो।"];
        const chatBox = document.getElementById('chat-container');

        // Camera
        async function openCam() {
            try {
                const s = await navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } });
                document.getElementById('video').srcObject = s;
                document.getElementById('cam-modal').style.display = 'flex';
            } catch (e) { alert("Camera Access Denied"); }
        }

        function closeCam() {
            const s = document.getElementById('video').srcObject;
            if (s) s.getTracks().forEach(t => t.stop());
            document.getElementById('cam-modal').style.display = 'none';
        }

        function takeShot() {
            const c = document.getElementById('canvas');
            const v = document.getElementById('video');
            c.width = v.videoWidth; c.height = v.videoHeight;
            c.getContext('2d').drawImage(v, 0, 0);
            appendImg(c.toDataURL('image/png'));
            closeCam();
            send("मैंने एक फोटो भेजी है।");
        }

        // Voice
        const rec = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        rec.lang = 'hi-IN';
        function startVoice() { try { rec.start(); document.getElementById('micBtn').classList.add('listening'); } catch(e){} }
        rec.onresult = (e) => { document.getElementById('userInput').value = e.results[0][0].transcript; send(); };
        rec.onend = () => document.getElementById('micBtn').classList.remove('listening');

        // Speaker
        function speak(t) {
            window.speechSynthesis.cancel();
            const m = new SpeechSynthesisUtterance(t); m.lang = 'hi-IN';
            window.speechSynthesis.speak(m);
        }

        // Messaging
        async function send(overrideText) {
            const input = document.getElementById('userInput');
            const val = overrideText || input.value.trim();
            if (!val) return;

            if(!overrideText) appendMsg(val, 'user-msg');
            input.value = "";
            history.push("User: " + val);

            const id = "ai-" + Date.now();
            appendMsg("AI King सोच रहा है...", 'ai-msg', id);

            try {
                const r = await fetch(`https://text.pollinations.ai/${encodeURIComponent(history.join("\n"))}?model=openai`);
                const d = await r.text();
                const box = document.getElementById(id);
                box.innerHTML = `<div>${d}</div><button class="speak-btn" onclick="speak(\`${d.replace(/['"`]/g, '')}\`)">🔊 जवाब सुनें</button>`;
                if (window.MathJax) MathJax.typesetPromise([box]);
                history.push("AI: " + d);
            } catch (e) { document.getElementById(id).innerText = "सर्वर एरर!"; }
            
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        function appendMsg(t, c, id) {
            const d = document.createElement('div');
            d.className = "message " + c; if(id) d.id = id; d.innerText = t;
            chatBox.appendChild(d);
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        function appendImg(src) {
            const d = document.createElement('div');
            d.className = "message user-msg";
            d.innerHTML = `<img src="${src}" class="chat-img">`;
            chatBox.appendChild(d);
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    </script>
</body>
</html>
