<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Offline AI - Sab Sawal Ka Jawab</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: #1a1a1a;
            color: #e0e0e0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        #chat-container {
            width: 95%;
            max-width: 600px;
            height: 90vh;
            background-color: #252525;
            border-radius: 12px;
            box-shadow: 0 4px 30px rgba(0,0,0,0.5);
            display: flex;
            flex-direction: column;
            overflow: hidden;
            border: 1px solid #333;
        }
        #header {
            padding: 15px;
            background-color: #333;
            text-align: center;
            font-weight: bold;
            border-bottom: 1px solid #444;
        }
        #status {
            font-size: 12px;
            color: #aaa;
            margin-top: 4px;
        }
        #chat-box {
            flex-grow: 1;
            padding: 20px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
       .message {
            padding: 12px 16px;
            border-radius: 18px;
            max-width: 80%;
            line-height: 1.5;
            white-space: pre-wrap;
        }
       .user-message {
            background-color: #007bff;
            color: white;
            align-self: flex-end;
            border-bottom-right-radius: 4px;
        }
       .bot-message {
            background-color: #3a3a3a;
            color: #e0e0e0;
            align-self: flex-start;
            border-bottom-left-radius: 4px;
        }
        #input-area {
            display: flex;
            border-top: 1px solid #444;
            padding: 12px;
            background-color: #333;
        }
        #user-input {
            flex-grow: 1;
            border: 1px solid #555;
            background-color: #2a2a2a;
            color: white;
            border-radius: 20px;
            padding: 12px 18px;
            font-size: 16px;
            outline: none;
        }
        #user-input:focus {
            border-color: #007bff;
        }
        #send-btn {
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 50%;
            width: 48px;
            height: 48px;
            margin-left: 10px;
            font-size: 20px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        #send-btn:disabled {
            background-color: #555;
            cursor: not-allowed;
        }
    </style>
    <!-- WebLLM library - ye browser me AI chalata hai -->
    <script type="module">
        import * as webllm from "https://esm.run/@mlc-ai/web-llm";

        const chatBox = document.getElementById('chat-box');
        const userInput = document.getElementById('user-input');
        const sendBtn = document.getElementById('send-btn');
        const status = document.getElementById('status');

        let engine;
        let messages = [
            { role: "system", content: "Tum ek helpful AI assistant ho. Hindi aur English dono me jawab do." }
        ];

        // Model load karo (pehli baar download hoga, phir cache se chalega)
        async function init() {
            status.textContent = "AI model load ho raha hai... (pehli baar 1-2 min lagega)";
            sendBtn.disabled = true;
            userInput.disabled = true;

            try {
                engine = await webllm.CreateMLCEngine(
                    "Phi-3-mini-4k-instruct-q4f16_1-MLC", // chhota, fast model ~500MB
                    {
                        initProgressCallback: (report) => {
                            status.textContent = report.text;
                        }
                    }
                );
                status.textContent = "Ready! Kuch bhi pucho";
                sendBtn.disabled = false;
                userInput.disabled = false;
                appendMessage("Namaste! Main taiyar hu. Ab aap koi bhi sawaal puch sakte ho.", 'bot-message');
            } catch (e) {
                status.textContent = "Error: " + e.message;
                appendMessage("Model load nahi ho paya. Internet check karo aur page reload karo.", 'bot-message');
            }
        }

        async function sendMessage() {
            const messageText = userInput.value.trim();
            if (messageText === '' || sendBtn.disabled) return;

            appendMessage(messageText, 'user-message');
            messages.push({ role: "user", content: messageText });
            userInput.value = '';
            sendBtn.disabled = true;
            status.textContent = "Soch raha hu...";

            // Bot reply
            const botMsgElement = appendMessage("", 'bot-message');
            let reply = "";

            try {
                const chunks = await engine.chat.completions.create({
                    messages,
                    stream: true,
                });

                for await (const chunk of chunks) {
                    const delta = chunk.choices[0]?.delta?.content || "";
                    reply += delta;
                    botMsgElement.textContent = reply;
                    chatBox.scrollTop = chatBox.scrollHeight;
                }

                messages.push({ role: "assistant", content: reply });
                status.textContent = "Ready!";
            } catch (e) {
                botMsgElement.textContent = "Error: " + e.message;
                status.textContent = "Error";
            }
            sendBtn.disabled = false;
        }

        function appendMessage(text, className) {
            const messageElement = document.createElement('div');
            messageElement.classList.add('message', className);
            messageElement.textContent = text;
            chatBox.appendChild(messageElement);
            chatBox.scrollTop = chatBox.scrollHeight;
            return messageElement;
        }

        window.sendMessage = sendMessage;
        window.handleKey = (event) => {
            if (event.key === 'Enter') sendMessage();
        };

        init();
    </script>
</head>
<body>

<div id="chat-container">
    <div id="header">
        Offline AI Chatbot
        <div id="status">Loading...</div>
    </div>
    <div id="chat-box"></div>
    <div id="input-area">
        <input type="text" id="user-input" placeholder="Koi bhi sawaal pucho..." onkeydown="handleKey(event)" disabled>
        <button id="send-btn" onclick="sendMessage()" disabled>&#x27A4;</button>
    </div>
</div>

</body>
</html>
