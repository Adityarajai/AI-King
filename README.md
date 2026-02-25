<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <title>AI King - Fixed Scroll</title>
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <style>
        /* Base Setup */
        * { box-sizing: border-box; margin: 0; padding: 0; }
        html, body { 
            height: 100%; 
            width: 100%; 
            background-color: #000; 
            color: #fff; 
            font-family: -apple-system, sans-serif;
            overflow: hidden; /* Main body scroll block rahega */
        }

        body { display: flex; flex-direction: column; }

        header { 
            padding: 15px; 
            text-align: center; 
            background: #111; 
            border-bottom: 1px solid #333;
            flex-shrink: 0;
        }
        h2 { color: #00ffcc; font-size: 20px; letter-spacing: 1px; }

        /* SCROLL FIX: Is container ki height fix hai taaki scrolling lock na ho */
        #chat-container { 
            flex: 1; 
            overflow-y: auto; /* Sirf ye area scroll hoga */
            padding: 15px; 
            display: flex; 
            flex-direction: column; 
            gap: 15px; 
            background: #000;
            width: 100%;
            -webkit-overflow-scrolling: touch; /* iOS smooth scroll */
        }
        
        .message { padding: 12px 16px; border-radius: 20px; line-height: 1.5; max-width: 85%; word-wrap: break-word; font-size: 16px; }
        .user-msg { background-color: #2b2b2b; align-self: flex-end; border-bottom-right-radius: 4px; }
        .ai-msg { background-color: #1a1a1a; align-self: flex-start; border: 1px solid #333; border-left: 4px solid #00ffcc; border-bottom-left-radius: 4px; }

        /* Input area hamesha bottom par rahega */
        .input-area { 
            padding: 10px 10px 25px 10px; 
            background: #111; 
            display: flex; 
            gap: 8px; 
            align-items: center; 
            border-top: 1px solid #333;
            flex-shrink: 0;
        }
        
        input { flex: 1; padding: 12px 15px; border-radius: 25px; border: 1px solid #444; background: #1a1a1a; color: #fff; outline: none; font-size: 16px; }

        .btn { border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; border-radius: 50%; }
        .icon-btn { width: 40px; height: 40px; background: #333; color: #fff; font-size: 18px; }
        .mic-btn { background: #ff4b2b; width: 40px; height: 40px; }
        .send-btn { background: #00ffcc; color: #000; border-radius: 20px; padding: 0 15px; font-weight: bold; height: 38px; }
        .listening { animation: pulse 1s infinite; background: #00ffcc; color: #000; }

        #cam-modal { display: none; position: fixed; inset: 0; background: #000; z-index: 1000; flex-direction: column; align-items: center; justify-content: center; }
        video { width: 100%; max-height: 75%; object-fit: cover; }
        
        @keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(0, 255, 204, 0.7); } 70% { box-shadow: 0 0 0 10px rgba(0, 255, 204, 0); } 100% { box-shadow: 0 0 0 0 rgba(0, 255, 204, 0); } }
    </style>
</head>
<body>

    <header><h2>AI King</h2></header>

    <div id="chat-container">
        <div class="message ai-msg">Mai Aditya ka AI hu, mai aap ke liye kya kar sakta hun?</div>
    </div>

    <div id="cam-modal">
        <video id="video" autoplay playsinline></video>
        <div style="padding: 20px; display: flex; gap: 20px;">
            <button class="send-btn" style="background:#ff4b2b; color:#fff;" onclick="closeCam()">Cancel</button>
            <button class="send-btn" onclick="takeShot()">Capture</button>
        </div>
        <canvas id="canvas" style="display:none;"></canvas>
    </div>

    <div class="input-area">
        <button class="btn icon-btn" onclick="openCam()">📷</button>
        <button id="micBtn" class="btn mic-btn" onclick="startVoice()">🎤</button>
        <input type="text" id="userInput" placeholder="Message..." onkeydown="if(event.key==='Enter') send()">
        <button class="btn send-btn" onclick="send()">Bhejen</button>
    </div>

    <script>
        let history = ["Tum Aditya ke AI ho. Hamesha Hindi mein jawab do."];
        const chatBox = document.getElementById('chat-container');

        // Scroll Function: Hamesha bottom par scroll karega
        function scrollToBottom() {
            chatBox.scrollTo({
                top: chatBox.scrollHeight,
                behavior: 'smooth'
            });
        }

        // Camera
        async function openCam() {
            try {
                const s = await navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } });
                document.getElementById('video').srcObject = s;
                document.getElementById('cam-modal').style.display = 'flex';
            } catch (e) { alert("Camera Permission Blocked"); }
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
            send("Photo received.");
        }

        // Voice
        const rec = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        rec.lang = 'hi-IN';
        function startVoice() { try { rec.start(); document.getElementById('micBtn').classList.add('listening'); } catch(e){} }
        rec.onresult = (e) => { document.getElementById('userInput').value = e.results[0][0].transcript; send(); };
        rec.onend = () => document.getElementById('micBtn').classList.remove('listening');

        // Messaging
        async function send(overrideText) {
            const input = document.getElementById('userInput');
            const val = overrideText || input.value.trim();
            if (!val) return;

            if(!overrideText) appendMsg(val, 'user-msg');
            input.value = "";
            history.push("User: " + val);

            const id = "ai-" + Date.now();
            appendMsg("AI King soch raha hai...", 'ai-msg', id);

            try {
                const r = await fetch(`https://text.pollinations.ai/${encodeURIComponent(history.join("\n"))}?model=openai`);
                const d = await r.text();
                const box = document.getElementById(id);
                box.innerHTML = `<div>${d}</div>`;
                if (window.MathJax) MathJax.typesetPromise([box]);
                history.push("AI: " + d);
            } catch (e) { document.getElementById(id).innerText = "Error!"; }
            
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
            d.innerHTML = `<img src="${src}" style="max-width:100%; border-radius:10px;">`;
            chatBox.appendChild(d);
            scrollToBottom();
        }
    </script>
</body>
</html>
