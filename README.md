<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI King</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background-color: #0f0f0f; color: #e0e0e0; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 100vh; margin: 0; padding: 10px; }
        /* Green AI King Title Style */
        h2 { color: #00ffcc; text-shadow: 0 0 10px rgba(0, 255, 204, 0.5); margin-bottom: 20px; font-size: 28px; letter-spacing: 2px; }
        #chat-container { width: 100%; max-width: 600px; background: #1a1a1a; border-radius: 15px; padding: 20px; box-shadow: 0 8px 32px rgba(0,0,0,0.8); height: 450px; overflow-y: auto; border: 1px solid #333; display: flex; flex-direction: column; }
        .message { margin-bottom: 15px; padding: 12px 16px; border-radius: 10px; line-height: 1.5; max-width: 85%; word-wrap: break-word; font-size: 15px; }
        .user-msg { background-color: #005c4b; align-self: flex-end; border-bottom-right-radius: 2px; color: white; }
        .ai-msg { background-color: #2c2c2c; align-self: flex-start; border-bottom-left-radius: 2px; border-left: 3px solid #00ffcc; }
        .input-area { margin-top: 15px; display: flex; width: 100%; max-width: 600px; gap: 10px; }
        input { flex: 1; padding: 15px; border-radius: 10px; border: 1px solid #444; background: #252525; color: white; outline: none; font-size: 16px; }
        input:focus { border-color: #00ffcc; }
        button { padding: 0 25px; background-color: #00ffcc; color: #000; border: none; cursor: pointer; font-weight: bold; border-radius: 10px; transition: 0.3s; }
        button:hover { background-color: #00cca3; transform: scale(1.02); }
    </style>
</head>
<body>

    <h2>--- AI King ---</h2>

    <div id="chat-container">
        <div class="message ai-msg">मैं आदित्य का AI हूँ, आपकी क्या मदद कर सकता हूँ?</div>
    </div>

    <div class="input-area">
        <input type="text" id="userInput" placeholder="यहाँ संदेश लिखें..." onkeypress="handleKeyPress(event)" autocomplete="off">
        <button onclick="sendMessage()">भेजें</button>
    </div>

    <script>
        async function sendMessage() {
            const inputField = document.getElementById('userInput');
            const message = inputField.value.trim();
            if (message === "") return;

            appendMessage(message, 'user-msg');
            inputField.value = "";

            const loadingId = "id-" + Date.now();
            appendMessage("AI King सोच रहा है...", 'ai-msg', loadingId);

            try {
                const response = await fetch(`https://text.pollinations.ai/${encodeURIComponent(message)}?system=${encodeURIComponent("तुम आदित्य के AI हो, तुम्हारा नाम AI King है और तुम हमेशा हिंदी में जवाब देते हो")}`);
                const aiReply = await response.text();
                document.getElementById(loadingId).innerText = aiReply;
            } catch (error) {
                document.getElementById(loadingId).innerText = "सर्वर से संपर्क नहीं हो पाया।";
            }
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
