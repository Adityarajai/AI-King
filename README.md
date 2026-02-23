<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI King</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #0f0f0f;
            color: #e0e0e0;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            margin: 0;
            padding: 10px;
        }
        h2 {
            color: #00ffcc;
            text-shadow: 0 0 10px rgba(0, 255, 204, 0.3);
            margin-bottom: 20px;
        }
        #chat-container {
            width: 100%;
            max-width: 600px;
            background: #1a1a1a;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.8);
            height: 450px;
            overflow-y: auto;
            border: 1px solid #333;
            display: flex;
            flex-direction: column;
        }
        .message {
            margin-bottom: 15px;
            padding: 12px 16px;
            border-radius: 10px;
            line-height: 1.5;
            max-width: 85%;
            word-wrap: break-word;
        }
        .user-msg {
            background-color: #005c4b;
            align-self: flex-end;
            border-bottom-right-radius: 2px;
            color: white;
        }
        .ai-msg {
            background-color: #2c2c2c;
            align-self: flex-start;
            border-bottom-left-radius: 2px;
            border-left: 3px solid #00ffcc;
        }
        .input-area {
            margin-top: 15px;
            display: flex;
            width: 100%;
            max-width: 600px;
            gap: 10px;
        }
        input {
            flex: 1;
            padding: 15px;
            border-radius: 10px;
            border: 1px solid #444;
            background: #252525;
            color: white;
            outline: none;
            font-size: 16px;
        }
        input:focus { border-color: #00ffcc; }
        .btn {
            padding: 12px;
            background-color: #00ffcc;
            color: #000;
            border: none;
            cursor: pointer;
            font-weight: bold;
            border-radius: 10px;
            transition: 0.3s;
        }
        .btn:hover { background-color: #00cca3; transform: scale(1.05); }
        .mic-btn { background-color: #ff3b3b; color: white; }
        .mic-btn.listening { background-color: #ff9f43; animation: pulse 1s infinite; }

        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
    </style>
</head>
<body>

    <h2>--- AI King ---</h2>

    <div id="chat-container">
        <div class="message ai-msg">मैं आदित्य का AI हूँ, आपकी क्या मदद कर सकता हूँ?</div>
    </div>

    <div class="input-area">
        <button id="micBtn" class="btn mic-btn" onclick="startRecognition()">🎤</button>
        <input type="text" id="userInput" placeholder="यहाँ लिखें या बोलें..." onkeypress="handleKeyPress(event)" autocomplete="off">
        <button class="btn" onclick="sendMessage()">भेजें</button>
    </div>

    <script>
        let chatHistory = ["तुम्हारा नाम AI King है। तुम आदित्य के AI हो और हमेशा हिंदी में जवाब देते हो।"];

        // आवाज़ पहचानने के लिए (Speech Recognition)
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = SpeechRecognition ? new SpeechRecognition() : null;

        if (recognition) {
            recognition.lang = 'hi-IN';
            recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                document.getElementById('userInput').value = transcript;
                document.getElementById('micBtn').classList.remove('listening');
                sendMessage(); // बोलने के बाद अपने आप मैसेज भेज दें
            };
            recognition.onend = () => {
                document.getElementById('micBtn').classList.remove('listening');
            };
        }

        function startRecognition() {
            if (recognition) {
                recognition.start();
                document.getElementById('micBtn').classList.add('listening');
            } else {
                alert("आपका ब्राउज़र माइक्रोफ़ोन सपोर्ट नहीं करता।");
            }
        }

        // आवाज़ में बोलने के लिए (Text to Speech)
        function speak(text) {
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = 'hi-IN';
            window.speechSynthesis.speak(utterance);
        }

        async function sendMessage() {
            const inputField = document.getElementById('userInput');
            const chatContainer = document.getElementById('chat-container');
            const message = inputField.value.trim();

            if (message === "") return;

            appendMessage("You: " + message, 'user-msg');
            inputField.value = "";
            chatHistory.push("User: " + message);

            const loadingId = "loading-" + Date.now();
            appendMessage("सोच रहा हूँ...", 'ai-msg', loadingId);

            try {
                const fullConversation = encodeURIComponent(chatHistory.join(" "));
                const response = await fetch(`https://text.pollinations.ai/${fullConversation}`);
                const aiReply = await response.text();

                const loadingDiv = document.getElementById(loadingId);
                loadingDiv.innerText = aiReply;

                // AI का जवाब बोलने के लिए
                speak(aiReply);

                chatHistory.push("AI: " + aiReply);
                if (chatHistory.length > 10) chatHistory.splice(1, 1);

            } catch (error) {
                document.getElementById(loadingId).innerText = "सर्वर एरर!";
            }

            chatContainer.scrollTop = chatContainer.scrollHeight;
        }

        function appendMessage(text, className, id = null) {
            const chatContainer = document.getElementById('chat-container');
            const div = document.createElement('div');
            div.className = "message " + className;
            if(id) div.id = id;
            div.innerText = text;
            chatContainer.appendChild(div);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }

        function handleKeyPress(e) {
            if (e.key === 'Enter') sendMessage();
        }
    </script>
</body>
</html>
