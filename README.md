<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI King - The Global Omniscient Engine</title>
    <script type="module">
        import { pipeline } from 'https://cdn.jsdelivr.net/npm/@xenova/transformers@2.6.0';
        window.pipeline = pipeline;
    </script>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #0b132b; 
            color: #ffffff;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
        }

        .brand-container {
            text-align: center;
            margin-bottom: 20px;
        }

        .logo {
            max-width: 150px;
            height: auto;
            border-radius: 12px;
            box-shadow: 0 0 20px rgba(0, 212, 255, 0.2);
            display: block;
            margin: 0 auto;
        }

        .logo-fallback {
            font-size: 28px;
            font-weight: bold;
            color: #ffb703;
            text-shadow: 0 0 10px rgba(255, 183, 3, 0.5);
        }

        .container {
            max-width: 550px;
            width: 90%;
            background: #1c2541; 
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
            text-align: center;
        }

        h2 {
            margin-top: 0;
            color: #48cae4;
        }

        button {
            width: 100%;
            padding: 12px;
            background: linear-gradient(135deg, #00b4d8, #0077b6);
            color: white;
            border: none;
            border-radius: 6px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: opacity 0.2s;
            margin-top: 10px;
        }

        button:hover {
            opacity: 0.9;
        }

        button:disabled {
            background: #5c677d;
            cursor: not-allowed;
        }

        input[type="text"] {
            width: calc(100% - 24px);
            padding: 12px;
            margin-top: 10px;
            border-radius: 6px;
            border: 1px solid #5c677d;
            background-color: #0b132b;
            color: white;
            font-size: 16px;
            text-align: center;
        }

        #status-box {
            font-size: 14px;
            color: #00f5d4;
            margin-bottom: 15px;
            background: rgba(0, 245, 212, 0.05);
            padding: 8px;
            border-radius: 4px;
        }

        #output {
            margin-top: 25px;
            font-size: 16px;
            color: #ffb703;
            padding: 15px;
            border-radius: 6px;
            background: rgba(255, 183, 3, 0.05);
            border: 1px solid rgba(255, 183, 3, 0.2);
            display: none;
            text-align: left;
            line-height: 1.5;
            max-height: 250px;
            overflow-y: auto;
        }
    </style>
</head>
<body>

<div class="brand-container">
    <img src="image.png" alt="👑 AI KING" class="logo" onerror="this.style.display='none'; this.nextElementSibling.style.display='block';">
    <div class="logo-fallback" style="display: none;">👑 AI KING</div>
</div>

<div class="container">
    <h2>AI King Grand Court</h2>
    <div id="status-box">Status: Preparing Royal Court...</div>
    
    <p>Ask the King any question in the universe:</p>
    <input type="text" id="user-question" placeholder="Ask me anything..." value="What is the capital of France?">
    <button id="send-btn" onclick="askTheKing()" disabled>Load AI Engine</button>

    <div id="output"></div>
</div>

<script>
    let generator = null;

    // Automatically load the light AI model inside the browser engine
    window.addEventListener('DOMContentLoaded', async () => {
        const statusBox = document.getElementById('status-box');
        const sendBtn = document.getElementById('send-btn');
        
        try {
            statusBox.innerText = "Status: Summoning AI King (Downloading engine)...";
            // Using a tiny text-generation model optimized for browsers
            generator = await window.pipeline('text2text-generation', 'Xenova/LaMini-Flan-T5-78M');
            
            statusBox.innerText = "Status: AI King is on the Throne!";
            statusBox.style.color = "#00f5d4";
            sendBtn.innerText = "Consult the King";
            sendBtn.disabled = false;
        } catch (e) {
            console.error(e);
            statusBox.innerText = "Status: Failed to build local engine.";
            statusBox.style.color = "#ff4d4d";
        }
    });

    async function askTheKing() {
        if(!generator) return;

        const inputField = document.getElementById('user-question');
        const sendBtn = document.getElementById('send-btn');
        const outputDiv = document.getElementById('output');
        
        const question = inputField.value.trim();
        if (!question) return;

        sendBtn.disabled = true;
        sendBtn.innerText = "The King is thinking...";
        outputDiv.style.display = "block";
        outputDiv.innerHTML = "<em>The King is preparing his decree...</em>";

        // Instruct the local engine to speak like royalty
        const prompt = `You are a majestic king. Answer this question regally: ${question}`;

        try {
            const result = await generator(prompt, { 
                max_new_tokens: 100,
                temperature: 0.7 
            });
            
            let kingReply = result[0].generated_text;
            outputDiv.innerHTML = `👑 <strong>AI King:</strong> ${kingReply.trim()}`;

        } catch (error) {
            console.error(error);
            outputDiv.innerHTML = "<span style='color: #ff4d4d;'>Error: Core processing failure in the royal chambers.</span>";
        } finally {
            sendBtn.disabled = false;
            sendBtn.innerText = "Consult the King";
        }
    }
</script>

</body>
</html>
