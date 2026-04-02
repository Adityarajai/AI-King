<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Offline AI Chatbot</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: #f4f4f9;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        #chat-container {
            width: 90%;
            max-width: 400px;
            height: 600px;
            background-color: #fff;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        #chat-box {
            flex-grow: 1;
            padding: 20px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }
        .message {
            padding: 10px 15px;
            border-radius: 18px;
            max-width: 75%;
            line-height: 1.4;
        }
        .user-message {
            background-color: #007bff;
            color: white;
            align-self: flex-end;
            border-bottom-right-radius: 4px;
        }
        .bot-message {
            background-color: #e9e9eb;
            color: #333;
            align-self: flex-start;
            border-bottom-left-radius: 4px;
        }
        #input-area {
            display: flex;
            border-top: 1px solid #ddd;
            padding: 10px;
        }
        #user-input {
            flex-grow: 1;
            border: 1px solid #ccc;
            border-radius: 20px;
            padding: 10px 15px;
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
            width: 44px;
            height: 44px;
            margin-left: 10px;
            font-size: 20px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
        }
    </style>
</head>
<body>

<div id="chat-container">
    <div id="chat-box">
        <div class="message bot-message">Hi there! I'm a simple AI. Ask me something!</div>
    </div>
    <div id="input-area">
        <input type="text" id="user-input" placeholder="Type a message..." onkeydown="handleKey(event)">
        <button id="send-btn" onclick="sendMessage()">&#x27A4;</button>
    </div>
</div>

<script>
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');

    function sendMessage() {
        const messageText = userInput.value.trim();
        if (messageText === '') return;

        // Display user message
        appendMessage(messageText, 'user-message');
        userInput.value = '';

        // Get and display bot response
        setTimeout(() => {
            const botResponse = getBotResponse(messageText);
            appendMessage(botResponse, 'bot-message');
        }, 500); // Simulate thinking
    }

    function appendMessage(text, className) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', className);
        messageElement.textContent = text;
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function handleKey(event) {
        if (event.key === 'Enter') {
            sendMessage();
        }
    }

    // --- The "AI" Brain ---
    // This is where you add the logic. It's a simple rule-based system.
    function getBotResponse(input) {
        const text = input.toLowerCase();

        if (text.includes('hello') || text.includes('hi')) {
            return 'Hello there! How can I help you today?';
        } else if (text.includes('how are you')) {
            return 'I am just a bunch of code, but I feel fantastic! Thanks for asking.';
        } else if (text.includes('your name')) {
            return 'I don\'t have a name. I\'m your offline AI assistant!';
        } else if (text.includes('what can you do')) {
            return 'I can have simple conversations. Try asking about my name, how I am, or tell me a joke!';
        } else if (text.includes('joke')) {
            return 'Why don’t scientists trust atoms? Because they make up everything!';
        } else if (text.includes('time')) {
            const date = new Date();
            const hours = date.getHours();
            const minutes = date.getMinutes().toString().padStart(2, '0');
            return `The current time is ${hours}:${minutes}.`;
        } else if (text.includes('bye') || text.includes('goodbye')) {
            return 'Goodbye! Have a great day!';
        } else {
            return 'I\'m not sure how to answer that. I am still learning. Try asking me to tell you a joke.';
        }
    }
</script>

</body>
</html>
