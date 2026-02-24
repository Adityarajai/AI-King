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
        .message { margin-bottom: 15px; padding: 12px 16px; border-radius: 10px; line-height: 1.6; max-width: 85%; position: relative; word-wrap: break-word; }
        .user-msg { background-color: #005c4b; align-self: flex-end; color: white; border-bottom-right-radius: 2px; }
        .ai-msg { background-color: #2c2c2c; align-self: flex-start; border-left: 4px solid #00ffcc; border-bottom-left-radius: 2px; }
        .input-area { margin-top: 15px; display: flex; width: 100%; max-width: 600px; gap: 8px; }
        input { flex: 1; padding: 15px; border-radius: 10px; border: 1px solid #444; background: #252525; color: white; outline: none; font-size: 16px; }
        .btn { padding: 12px 18px; border-radius: 10px; border: none; cursor: pointer; font-weight: bold; transition: 0.3s; }
        .send-btn { background-color: #00ffcc; color: #000; }
        .mic-btn { background-color: #ff4757; color: white; font-size: 1.2rem; display: flex; align-items: center; justify-content: center; width: 50px; }
        .mic-btn.listening { background-color: #ffa502; animation: pulse 1s infinite; }
        .speak-btn { background: #333; border: 1px solid #00ffcc; color: #00ffcc; cursor: pointer; font-size: 12px; margin-top: 10px; padding: 5px 10px; border-radius: 5px; display: inline-block; }
        @keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.1); } 100% { transform: scale(1); } }
    </style>
</head>
<body>

    <h2>--- AI King ---</h2>

    <div id="chat-container">
        <div class="message ai-msg">नमस्ते! मैं AI King हूँ। मैं आपकी क्या मदद कर सकता हूँ?</div>
    </div>

    <div class="input-area">
        <button id="micBtn" class="btn mic-btn" onclick="toggleMic()">🎤</button>
        <input type="text" id="userInput" placeholder="यहाँ लिखें या बोलें..." onkeypress="if(event.key==='Enter') sendMessage()" autocomplete="off">
        <button class="btn send-btn" onclick="sendMessage()">भेजें</button>
    </div>

    <script>
        let chatHistory = ["तुम्हारा नाम AI King है। तुम आदित्य के AI हो। हमेशा साफ और सीधे हिंदी में जवाब दो।"];

        // 1. माइक (Speech to Text) फिक्स
        const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = 'hi-IN';
        recognition.continuous = false;
        let isListening = false;

        function toggleMic() {
            if (!isListening) {
                recognition.start();
            } else {
                recognition.stop();
            }
        }

        recognition.onstart = () => {
            isListening = true;
            document.getElementById('micBtn').classList.add('listening');
        };

        recognition.onresult = (event) => {
            const text = event.results[0][0].transcript;
            document.getElementById('userInput').value = text;
            sendMessage();
        };

        recognition.onend = () => {
            isListening = false;
            document.getElementById('micBtn').classList.remove('listening');
        };

        // 2. आवाज़ (Speech) फिक्स
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
            appendMsg("AI King सोच रहा है...", 'ai-msg', tempId);

            try {
                // API कॉल में सुधार ताकि JSON कचरा न आए
                const res = await fetch(`https://text.pollinations.ai/${encodeURIComponent(chatHistory.join("\n"))}?model=openai&system=You are AI King, created by Aditya. Always answer in clear Hindi. Do not use JSON formatting.`);
                let data = await res.text();

                const aiBox = document.getElementById(tempId);
                // स्पीकर बटन जोड़ना
                aiBox.innerHTML = `<div>${data}</div><button class="speak-btn" onclick="speak(\`${data.replace(/[`'"]/g, '')}\`)">🔊 जवाब सुनें</button>`;
                
                // मैथ रेंडरिंग
                if (window.MathJax) MathJax.typesetPromise([aiBox]);
                
                chatHistory.push("AI: " + data);
            } catch (err) {
                document.getElementById(tempId).innerText = "नेटवर्क की समस्या है।";
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
