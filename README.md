<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI King</title>
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background-color: #0f0f0f; color: #e0e0e0; display: flex; flex-direction: column; align-items: center; min-height: 100vh; margin: 0; padding: 10px; }
        h2 { color: #00ffcc; margin-bottom: 20px; }
        #chat-container { width: 100%; max-width: 600px; background: #1a1a1a; border-radius: 15px; padding: 20px; height: 500px; overflow-y: auto; border: 1px solid #333; display: flex; flex-direction: column; box-shadow: 0 8px 32px rgba(0,0,0,0.5); }
        .message { margin-bottom: 15px; padding: 12px 16px; border-radius: 10px; line-height: 1.6; max-width: 85%; position: relative; }
        .user-msg { background-color: #005c4b; align-self: flex-end; color: white; border-bottom-right-radius: 2px; }
        .ai-msg { background-color: #2c2c2c; align-self: flex-start; border-left: 4px solid #00ffcc; border-bottom-left-radius: 2px; }
        .input-area { margin-top: 15px; display: flex; width: 100%; max-width: 600px; gap: 8px; }
        input { flex: 1; padding: 15px; border-radius: 10px; border: 1px solid #444; background: #252525; color: white; outline: none; }
        .btn { padding: 12px 18px; border-radius: 10px; border: none; cursor: pointer; font-weight: bold; transition: 0.3s; }
        .send-btn { background-color: #00ffcc; color: #000; }
        .mic-btn { background-color: #ff4757; color: white; font-size: 1.2rem; }
        .mic-btn.listening { background-color: #ffa502; animation: pulse 1s infinite; }
        .speak-btn { background: none; border: none; color: #00ffcc; cursor: pointer; font-size: 14px; margin-top: 5px; display: block; }
        @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }
    </style>
</head>
<body>

    <h2>--- AI King ---</h2>

    <div id="chat-container" id="chatContainer">
        <div class="message ai-msg">नमस्ते! मैं AI King हूँ। मैं आपकी क्या मदद कर सकता हूँ?</div>
    </div>

    <div class="input-area">
        <button id="micBtn" class="btn mic-btn" onclick="startMic()">🎤</button>
        <input type="text" id="userInput" placeholder="यहाँ लिखें या बोलें..." onkeypress="if(event.key==='Enter') sendMessage()" autocomplete="off">
        <button class="btn send-btn" onclick="sendMessage()">भेजें</button>
    </div>

    <script>
        let chatHistory = ["तुम्हारा नाम AI King है। तुम आदित्य के AI हो और हमेशा हिंदी में जवाब देते हो।"];

        // 1. माइक सेटअप
        const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = 'hi-IN';
        
        function startMic() {
            try {
                recognition.start();
                document.getElementById('micBtn').classList.add('listening');
            } catch (e) { recognition.stop(); }
        }

        recognition.onresult = (event) => {
            document.getElementById('userInput').value = event.results[0][0].transcript;
            sendMessage();
        };

        recognition.onend = () => document.getElementById('micBtn').classList.remove('listening');

        // 2. आवाज़ (Speech) सेटअप
        function speak(text) {
            window.speechSynthesis.cancel();
            const msg = new SpeechSynthesisUtterance(text);
            msg.lang = 'hi-IN';
            window.speechSynthesis.speak(msg);
        }

        // 3. मैसेज भेजने का फंक्शन
        async function sendMessage() {
            const input = document.getElementById('userInput');
            const chat = document.getElementById('chat-container');
            const val = input.value.trim();
            if (!val) return;

            appendMsg("You: " + val, 'user-msg');
            input.value = "";
            chatHistory.push("User: " + val);

            const tempId = "ai-" + Date.now();
            appendMsg("सोच रहा हूँ...", 'ai-msg', tempId);

            try {
                const res = await fetch(`https://text.pollinations.ai/${encodeURIComponent(chatHistory.join(" "))}`);
                let data = await res.text();

                // JSON सफाई (अगर API गलती से JSON भेज दे)
                try {
                    const json = JSON.parse(data);
                    data = json.choices ? json.choices[0].message.content : (json.content || data);
                } catch(e) {}

                const aiBox = document.getElementById(tempId);
                aiBox.innerHTML = `<div>${data}</div><button class="speak-btn" onclick="speak(\`${data.replace(/`/g, '')}\`)">🔊 सुनें</button>`;
                
                // गणित रेंडर करें
                if (window.MathJax) MathJax.typesetPromise([aiBox]);
                
                chatHistory.push("AI: " + data);
            } catch (err) {
                document.getElementById(tempId).innerText = "नेटवर्क एरर!";
            }
            chat.scrollTop = chat.scrollHeight;
        }

        function appendMsg(text, cls, id) {
            const div = document.createElement('div');
            div.className = "message " + cls;
            if(id) div.id = id;
            div.innerText = text;
            document.getElementById('chat-container').appendChild(div);
            document.getElementById('chat-container').scrollTop = document.getElementById('chat-container').scrollHeight;
        }
    </script>
</body>
</html>
