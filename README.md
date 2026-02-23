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
            padding: 0 20px;
            background-color: #00ffcc;
            color: #000;
            border: none;
            cursor: pointer;
            font-weight: bold;
            border-radius: 10px;
            transition: 0.3s;
        }
        .btn:hover { background-color: #00cca3; transform: scale(1.02); }
        .mic-btn {
            background-color: #ff3b3b;
            color: white;
            font-size: 20px;
        }
        .listening {
            animation: pulse 1s infinite;
            background-color: #ff9f43;
        }
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.1); }
            100% { transform: scale(1); }
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
        <input type="text" id="userInput" placeholder="यहाँ संदेश लिखें या बोलें..." onkeypress="handleKeyPress(event)" autocomplete="off">
        <button class="btn" onclick="sendMessage()">भेजें</button>
    </div>

    <script>
        let chatHistory = ["तुम्हारा नाम AI King है। तुम आदित्य के AI हो और हमेशा हिंदी में जवाब देते हो।"];

        // आवाज़ पहचानने का सेटअप (Speech Recognition)
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        let recognition = null;

        if (SpeechRecognition) {
            recognition = new SpeechRecognition();
            recognition.lang = 'hi-IN';
            recognition.interimResults = false;

            recognition.onstart = () => {
                document.getElementById('micBtn').classList.add('listening');
            };

            recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                document.getElementById('userInput').value = transcript;
                sendMessage(); // बोलने के बाद ऑटोमैटिक मैसेज भेजें
            };

            recognition.onerror = (event) => {
                console.error("Mic Error:", event.error);
                document.getElementById('micBtn').classList.remove('listening');
                if(event.error === 'not-allowed') alert("माइक की अनुमति (Permission) दें!");
            };

            recognition.onend = () => {
                document.getElementById('micBtn').classList.remove('listening');
            };
        }

        function startRecognition() {
            if (recognition) {
                try {
                    recognition.start();
                } catch(e) {
                    recognition.stop();
                }
            } else {
                alert("आपका ब्राउज़र माइक्रोफ़ोन सपोर्ट नहीं करता। Chrome का उपयोग करें।");
            }
        }

        // आवाज़ में जवाब देने का सेटअप (Text to Speech)
        function speak(text) {
            // बोलने से पहले पुरानी आवाज़ रोकें
            window.speechSynthesis.cancel();
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = 'hi-IN';
            utterance.rate = 1.0;
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

                // AI का जवाब बोलकर सुनाना
                speak(aiReply);

                chatHistory.push("AI: " + aiReply);

                if (chatHistory.length > 10) {
                    chatHistory.splice(1, 1);
                }

            } catch (error) {
                document.getElementById(loadingId).innerText = "कनेक्शन एरर!";
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
