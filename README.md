<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI King</title>
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <style>
        * { box-sizing: border-box; }
        body { font-family: 'Segoe UI', Roboto, sans-serif; background-color: #000; color: #fff; margin: 0; padding: 0; display: flex; flex-direction: column; height: 100vh; }
        
        header { padding: 15px; text-align: center; border-bottom: 1px solid #333; background: #000; }
        h2 { color: #00ffcc; margin: 0; font-size: 24px; letter-spacing: 2px; }

        #chat-container { flex: 1; overflow-y: auto; padding: 20px; display: flex; flex-direction: column; gap: 15px; background: #000; }
        
        .message { padding: 14px 18px; border-radius: 18px; line-height: 1.5; max-width: 90%; word-wrap: break-word; font-size: 16px; }
        .user-msg { background-color: #2b2b2b; align-self: flex-end; color: #fff; border-bottom-right-radius: 4px; }
        .ai-msg { background-color: #1a1a1a; align-self: flex-start; color: #e0e0e0; border-left: 4px solid #00ffcc; border-bottom-left-radius: 4px; border: 1px solid #333; }

        .input-area { padding: 15px; background: #000; display: flex; gap: 10px; align-items: center; border-top: 1px solid #333; }
        
        input { flex: 1; padding: 14px; border-radius: 25px; border: 1px solid #444; background: #1a1a1a; color: #fff; outline: none; font-size: 16px; }
        input:focus { border-color: #00ffcc; }

        .btn { border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: 0.2s; }
        .send-btn { background: #00ffcc; color: #000; padding: 12px 20px; border-radius: 25px; font-weight: bold; }
        .mic-btn { background: #ff4b2b; color: #fff; width: 50px; height: 50px; border-radius: 50%; font-size: 22px; }
        .listening { animation: pulse 1.5s infinite; background: #00ffcc; color: #000; }

        .speak-btn { background: #333; color: #00ffcc; border: 1px solid #444; padding: 6px 12px; border-radius: 15px; font-size: 12px; margin-top: 10px; cursor: pointer; }

        @keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(0, 255, 204, 0.7); } 70% { box-shadow: 0 0 0 15px rgba(0, 255, 204, 0); } 100% { box-shadow: 0 0 0 0 rgba(0, 255, 204, 0); } }
    </style>
</head>
<body>

    <header>
        <h2>AI King</h2>
    </header>

    <div id="chat-container">
        <div class="message ai-msg">नमस्ते! मैं आदित्य का AI King हूँ। पूछिए, मैं आज आपकी क्या मदद कर सकता हूँ?</div>
    </div>

    <div class="input-area">
        <button id="micBtn" class="btn mic-btn" onclick="toggleMic()">🎤</button>
        <input type="text" id="userInput" placeholder="यहाँ लिखें..." onkeydown="if(event.key==='Enter') sendMessage()">
        <button class="btn send-btn" onclick="sendMessage()">भेजें</button>
    </div>

    <script>
        let chatHistory = ["तुम AI King हो, जिसे आदित्य ने बनाया है। हमेशा स्पष्ट हिंदी में जवाब दो।"];

        // 1. Mic Fix
        const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = 'hi-IN';
        let isListening = false;

        function toggleMic() {
            if (!isListening) {
                try { recognition.start(); } catch(e) {}
            } else {
                recognition.stop();
            }
        }

        recognition.onstart = () => {
            isListening = true;
            document.getElementById('micBtn').classList.add('listening');
        };
        recognition.onresult = (e) => {
            document.getElementById('userInput').value = e.results[0][0].transcript;
            sendMessage();
        };
        recognition.onend = () => {
            isListening = false;
            document.getElementById('micBtn').classList.remove('listening');
        };

        // 2. Speaker Fix
        function speak(text) {
            window.speechSynthesis.cancel();
            const msg = new SpeechSynthesisUtterance(text);
            msg.lang = 'hi-IN';
            window.speechSynthesis.speak(msg);
        }

        // 3. Send Function Fix
        async function sendMessage() {
            const input = document.getElementById('userInput');
            const chat = document.getElementById('chat-container');
            const text = input.value.trim();
            
            if (!text) return;

            appendMsg(text, 'user-msg');
            input.value = "";
            chatHistory.push("User: " + text);

            const aiId = "ai-" + Date.now();
            appendMsg("AI King सोच रहा है...", 'ai-msg', aiId);

            try {
                // Simplified API URL to avoid breaking
                const res = await fetch(`https://text.pollinations.ai/${encodeURIComponent(chatHistory.join("\n"))}?model=openai`);
                const data = await res.text();

                const aiBox = document.getElementById(aiId);
                aiBox.innerHTML = `<div>${data}</div><button class="speak-btn" onclick="speak(\`${data.replace(/['"`]/g, '')}\`)">🔊 जवाब सुनें</button>`;
                
                // Math rendering
                if (window.MathJax) MathJax.typesetPromise([aiBox]);
                
                chatHistory.push("AI: " + data);
            } catch (err) {
                document.getElementById(aiId).innerText = "माफी चाहता हूँ, सर्वर में समस्या है।";
            }
            chat.scrollTop = chat.scrollHeight;
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
