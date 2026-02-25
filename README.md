<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <title>AI King - Mobile Master</title>
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <style>
        /* मोबाइल रिस्पॉन्सिव बेस सेटिंग्स */
        * { box-sizing: border-box; margin: 0; padding: 0; -webkit-tap-highlight-color: transparent; }
        
        html, body { 
            height: 100%; 
            width: 100%; 
            background-color: #000; 
            color: #fff; 
            font-family: -apple-system, system-ui, sans-serif;
            display: flex;
            flex-direction: column;
            overflow: hidden; /* स्क्रीन को हिलने से रोकने के लिए */
        }

        header { 
            padding: 15px; 
            text-align: center; 
            background: #111; 
            border-bottom: 1px solid #333;
            z-index: 10;
        }
        h2 { color: #00ffcc; font-size: 20px; text-transform: uppercase; }

        /* मोबाइल स्क्रॉल के लिए मुख्य बदलाव */
        #chat-container { 
            flex: 1; 
            overflow-y: scroll; /* मोबाइल पर स्क्रॉल सक्षम करने के लिए */
            -webkit-overflow-scrolling: touch; /* iOS के लिए स्मूथ स्क्रॉल */
            padding: 15px; 
            display: flex; 
            flex-direction: column; 
            gap: 15px; 
            background: #000;
            overscroll-behavior-y: contain; /* पुल-टू-रिफ्रेश को रोकने के लिए */
        }
        
        .message { padding: 12px 16px; border-radius: 18px; line-height: 1.5; max-width: 85%; word-wrap: break-word; font-size: 16px; }
        .user-msg { background-color: #2b2b2b; align-self: flex-end; border-bottom-right-radius: 4px; }
        .ai-msg { background-color: #1a1a1a; align-self: flex-start; border: 1px solid #333; border-left: 4px solid #00ffcc; border-bottom-left-radius: 4px; }

        .input-area { 
            padding: 10px 10px 30px 10px; /* मोबाइल बॉटम बार के लिए एक्स्ट्रा पैडिंग */
            background: #111; 
            display: flex; 
            gap: 8px; 
            align-items: center; 
            border-top: 1px solid #333;
        }
        
        input { flex: 1; padding: 12px 18px; border-radius: 25px; border: 1px solid #444; background: #1a1a1a; color: #fff; outline: none; font-size: 16px; }

        .btn { border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; border-radius: 50%; width: 42px; height: 42px; }
        .cam-btn { background: #333; color: #fff; border: 1px solid #444; }
        .mic-btn { background: #ff4b2b; color: #fff; }
        .send-btn { background: #00ffcc; color: #000; border-radius: 20px; width: auto; padding: 0 18px; font-weight: bold; font-size: 14px; }
        
        .listening { animation: pulse 1s infinite; background: #00ffcc; color: #000; }

        #cam-modal { display: none; position: fixed; inset: 0; background: #000; z-index: 1000; flex-direction: column; align-items: center; justify-content: center; }
        video { width: 100%; max-height: 70%; object-fit: cover; }

        @keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(0, 255, 204, 0.7); } 70% { box-shadow: 0 0 0 10px rgba(0, 255, 204, 0); } 100% { box-shadow: 0 0 0 0 rgba(0, 255, 204, 0); } }
    </style>
</head>
<body>

    <header><h2>AI King</h2></header>

    <div id="chat-container">
        <div class="message ai-msg">मैं आदित्य का AI हूँ, मैं आपके लिए क्या कर सकता हूँ?</div>
    </div>

    <div id="cam-modal">
        <video id="video" autoplay playsinline></video>
        <div style="padding: 20px; display: flex; gap: 20px;">
            <button class="send-btn" style="background:#ff4b2b; color:#fff;" onclick="closeCam()">बंद करें</button>
            <button class="send-btn" onclick="takeShot()">फोटो लें</button>
        </div>
        <canvas id="canvas" style="display:none;"></canvas>
    </div>

    <div class="input-area">
        <button class="btn cam-btn" onclick="openCam()">📷</button>
        <button id="micBtn" class="btn mic-btn" onclick="startVoice()">🎤</button>
        <input type="text" id="userInput" placeholder="संदेश लिखें..." onkeydown="if(event.key==='Enter') send()">
        <button class="btn send-btn" onclick="send()">भेजें</button>
    </div>

    <script>
        let history = ["तुम आदित्य के AI हो। हमेशा हिंदी में जवाब दो।"];
        const chatBox = document.getElementById('chat-container');

        // ऑटो स्क्रॉल फंक्शन
        function scrollToBottom() {
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        // कैमरा फंक्शन
        async function openCam() {
            try {
                const s = await navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } });
                document.getElementById('video').srcObject = s;
                document.getElementById('cam-modal').style.display = 'flex';
            } catch (e) { alert("Camera access problem!"); }
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
            const data = c.toDataURL('image/png');
            appendImg(data);
            closeCam();
            send("मैंने एक फोटो भेजी है।");
        }

        // आवाज फंक्शन
        const rec = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        rec.lang = 'hi-IN';
        function startVoice() { try { rec.start(); document.getElementById('micBtn').classList.add('listening'); } catch(e){} }
        rec.onresult = (e) => { document.getElementById('userInput').value = e.results[0][0].transcript; send(); };
        rec.onend = () => document.getElementById('micBtn').classList.remove('listening');

        // मैसेज भेजना
        async function send(overrideText) {
            const input = document.getElementById('userInput');
            const val = overrideText || input.value.trim();
            if (!val) return;

            if(!overrideText) appendMsg(val, 'user-msg');
            input.value = "";
            history.push("User: " + val);

            const id = "ai-" + Date.now();
            appendMsg("AI King सोच रहा है...", 'ai-msg', id);
            scrollToBottom();

            try {
                const r = await fetch(`https://text.pollinations.ai/${encodeURIComponent(history.join("\n"))}?model=openai`);
                const d = await r.text();
                const box = document.getElementById(id);
                box.innerHTML = `<div>${d}</div>`;
                if (window.MathJax) MathJax.typesetPromise([box]);
                history.push("AI: " + d);
            } catch (e) { document.getElementById(id).innerText = "सर्वर एरर!"; }
            
            scrollToBottom();
        }

        function appendMsg(t, c, id) {
            const d = document.createElement('div');
            d.className = "message " + c; if(id) d.id = id; d.innerText = t;
            chatBox.appendChild(d);
            scrollToBottom();
        }

        function appendImg(src) {
            const d = document.createElement('div');
            d.className = "message user-msg";
            d.innerHTML = `<img src="${src}" style="max-width:100%; border-radius:10px; display:block;">`;
            chatBox.appendChild(d);
            scrollToBottom();
        }
    </script>
</body>
</html>
