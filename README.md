<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI King - Pro Fix</title>
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <style>
        * { box-sizing: border-box; }
        body { font-family: 'Segoe UI', sans-serif; background-color: #000; color: #fff; margin: 0; padding: 0; display: flex; flex-direction: column; height: 100vh; }
        
        header { padding: 15px; text-align: center; border-bottom: 1px solid #333; background: #111; position: sticky; top: 0; z-index: 10; }
        h2 { color: #00ffcc; margin: 0; font-size: 22px; }

        /* Scroll Fix: overflow-y auto zaroori hai */
        #chat-container { flex: 1; overflow-y: auto; padding: 20px; display: flex; flex-direction: column; gap: 15px; background: #000; scroll-behavior: smooth; }
        
        .message { padding: 12px 16px; border-radius: 15px; line-height: 1.5; max-width: 85%; word-wrap: break-word; font-size: 16px; }
        .user-msg { background-color: #2b2b2b; align-self: flex-end; border-bottom-right-radius: 2px; }
        .ai-msg { background-color: #1a1a1a; align-self: flex-start; border-left: 4px solid #00ffcc; border-bottom-left-radius: 2px; border: 1px solid #333; }

        /* Image Display Style */
        .chat-img { max-width: 100%; border-radius: 10px; margin-top: 5px; border: 1px solid #444; }

        .input-area { padding: 10px; background: #111; display: flex; gap: 8px; align-items: center; border-top: 1px solid #333; position: sticky; bottom: 0; }
        
        input { flex: 1; padding: 12px; border-radius: 20px; border: 1px solid #444; background: #1a1a1a; color: #fff; outline: none; }

        .btn { border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; border-radius: 50%; width: 45px; height: 45px; transition: 0.2s; }
        .send-btn { background: #00ffcc; color: #000; border-radius: 20px; width: auto; padding: 0 15px; font-weight: bold; }
        .cam-btn { background: #333; color: #fff; border: 1px solid #444; }
        .mic-btn { background: #ff4b2b; color: #fff; }
        .listening { animation: pulse 1s infinite; background: #00ffcc; color: #000; }

        #cam-modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: #000; z-index: 100; flex-direction: column; align-items: center; justify-content: center; }
        video { width: 90%; border-radius: 10px; border: 2px solid #00ffcc; }
        .speak-btn { background: #222; color: #00ffcc; border: 1px solid #444; padding: 5px 10px; border-radius: 10px; font-size: 12px; margin-top: 8px; cursor: pointer; }

        @keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(0, 255, 204, 0.7); } 70% { box-shadow: 0 0 0 10px rgba(0, 255, 204, 0); } 100% { box-shadow: 0 0 0 0 rgba(0, 255, 204, 0); } }
    </style>
</head>
<body>

    <header><h2>AI King</h2></header>

    <div id="chat-container">
        <div class="message ai-msg">नमस्ते आदित्य! अब मैं फोटो को देख भी सकता हूँ। 📷 दबाएँ और फोटो खींचें।</div>
    </div>

    <div id="cam-modal">
        <video id="video" autoplay playsinline></video>
        <div style="margin-top:20px; display:flex; gap:15px;">
            <button class="send-btn" style="background:#ff4b2b; color:#fff;" onclick="closeCam()">बंद करें</button>
            <button class="send-btn" onclick="takeShot()">फोटो लें</button>
        </div>
        <canvas id="canvas" style="display:none;"></canvas>
    </div>

    <div class="input-area">
        <button class="btn cam-btn" onclick="openCam()">📷</button>
        <button id="micBtn" class="btn mic-btn" onclick="startVoice()">🎤</button>
        <input type="text" id="userInput" placeholder="यहाँ लिखें..." onkeydown="if(event.key==='Enter') send()">
        <button class="btn send-btn" onclick="send()">भेजें</button>
    </div>

    <script>
        let history = ["तुम AI King हो। आदित्य ने तुम्हें बनाया है। फोटो को देखकर उसका जवाब दो।"];

        // 1. Camera & Image Preview
        async function openCam() {
            try {
                const s = await navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } });
                document.getElementById('video').srcObject = s;
                document.getElementById('cam-modal').style.display = 'flex';
            } catch (e) { alert("Camera access denied!"); }
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
            
            // Photo Chat mein dikhana
            appendImg(data);
            closeCam();
            
            // AI ko hint dena ki photo aayi hai
            send("Maine ek photo bheji hai, isme kya hai?");
        }

        // 2. Voice
        const rec = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        rec.lang = 'hi-IN';
        function startVoice() { rec.start(); document.getElementById('micBtn').classList.add('listening'); }
        rec.onresult = (e) => { document.getElementById('userInput').value = e.results[0][0].transcript; send(); };
        rec.onend = () => document.getElementById('micBtn').classList.remove('listening');

        // 3. Speaker
        function speak(t) {
            window.speechSynthesis.cancel();
            const m = new SpeechSynthesisUtterance(t); m.lang = 'hi-IN';
            window.speechSynthesis.speak(m);
        }

        // 4. Send Message
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
                box.innerHTML = `<div>${d}</div><button class="speak-btn" onclick="speak(\`${d.replace(/['"`]/g, '')}\`)">🔊 सुनें</button>`;
                if (window.MathJax) MathJax.typesetPromise([box]);
                history.push("AI: " + d);
            } catch (e) { document.getElementById(id).innerText = "Error!"; }
        }

        function appendMsg(t, c, id) {
            const cont = document.getElementById('chat-container');
            const d = document.createElement('div');
            d.className = "message " + c; if(id) d.id = id; d.innerText = t;
            cont.appendChild(d); cont.scrollTop = cont.scrollHeight;
        }

        function appendImg(src) {
            const cont = document.getElementById('chat-container');
            const d = document.createElement('div');
            d.className = "message user-msg";
            d.innerHTML = `<img src="${src}" class="chat-img">`;
            cont.appendChild(d); cont.scrollTop = cont.scrollHeight;
        }
    </script>
</body>
</html>
