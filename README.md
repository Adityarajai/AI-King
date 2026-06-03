<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI King - Home</title>
    <script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@latest"></script>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #0b132b; /* Dark blue matching the logo background */
            color: #ffffff;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
        }

        .brand-container {
            text-align: center;
            margin-bottom: 30px;
        }

        .logo {
            max-width: 180px;
            height: auto;
            border-radius: 12px;
            box-shadow: 0 0 20px rgba(0, 212, 255, 0.2);
        }

        .container {
            max-width: 450px;
            width: 90%;
            background: #1c2541; /* Slightly lighter contrast background */
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

        input[type="number"] {
            width: calc(100% - 24px);
            padding: 10px;
            margin-top: 10px;
            border-radius: 6px;
            border: 1px solid #5c677d;
            background-color: #0b132b;
            color: white;
            font-size: 16px;
            text-align: center;
        }

        #training-status {
            margin-top: 12px;
            font-size: 14px;
            color: #a3b18a;
        }

        #output {
            margin-top: 25px;
            font-size: 18px;
            font-weight: bold;
            color: #00f5d4;
            padding: 10px;
            border-radius: 6px;
            background: rgba(0, 245, 212, 0.1);
            display: none; /* Hidden until prediction is made */
        }
    </style>
</head>
<body>

<div class="brand-container">
    <img src="image.png" alt="AI King Logo" class="logo">
</div>

<div class="container">
    <h2>AI King Engine</h2>
    <p>Train the core intelligence model:</p>
    <button id="train-btn" onclick="trainModel()">Initialize Model</button>
    <div id="training-status">Status: Awaiting Initialization</div>
    
    <hr style="margin: 25px 0; border: 0; border-top: 1px solid #3a506b;">
    
    <p>Predict Outputs ($y = 2x - 1$):</p>
    <input type="number" id="input-x" value="10" disabled>
    <button id="predict-btn" onclick="predict()" disabled>Run Prediction</button>

    <div id="output"></div>
</div>

<script>
    let model;

    async function trainModel() {
        const trainBtn = document.getElementById('train-btn');
        const statusDiv = document.getElementById('training-status');
        
        trainBtn.disabled = true;
        statusDiv.style.color = "#ffb703";
        statusDiv.innerText = "Model optimization in progress...";

        model = tf.sequential();
        model.add(tf.layers.dense({units: 1, inputShape: [1]}));
        model.compile({loss: 'meanSquaredError', optimizer: 'sgd'});

        const xs = tf.tensor2d([-1, 0, 1, 2, 3, 4], [6, 1]);
        const ys = tf.tensor2d([-3, -1, 1, 3, 5, 7], [6, 1]);

        await model.fit(xs, ys, {epochs: 250});

        xs.dispose();
        ys.dispose();
        
        statusDiv.style.color = "#00f5d4";
        statusDiv.innerText = "System Ready.";
        document.getElementById('input-x').disabled = false;
        document.getElementById('predict-btn').disabled = false;
    }

    function predict() {
        const xValue = parseFloat(document.getElementById('input-x').value);
        const outputDiv = document.getElementById('output');
        
        tf.tidy(() => {
            const inputTensor = tf.tensor2d([xValue], [1, 1]);
            const outputTensor = model.predict(inputTensor);
            const result = outputTensor.dataSync()[0];
            
            outputDiv.style.display = "block";
            outputDiv.innerText = `Result: X = ${xValue} → Y ≈ ${result.toFixed(2)}`;
        });
    }
</script>

</body>
</html>
