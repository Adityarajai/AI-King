export default async function handler(req, res) {
    // 1. Allow your GitHub Pages website to talk to this backend
    res.setHeader('Access-Control-Allow-Credentials', true);
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS,PATCH,DELETE,POST,PUT');
    res.setHeader('Access-Control-Allow-Headers', 'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version');

    // Handle browser preflight checks
    if (req.method === 'OPTIONS') {
        res.status(200).end();
        return;
    }

    // 2. Only allow POST requests (sending questions)
    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Method not allowed' });
    }

    const { question } = req.body;
    if (!question) {
        return res.status(400).json({ error: 'Question is required' });
    }

    // 3. Grab your secret token hidden inside Vercel's settings
    const apiKey = process.env.HF_TOKEN; 
    const modelUrl = "https://api-inference.huggingface.co/models/MistralAI/Mistral-7B-Instruct-v0.3";
    const systemPrompt = `You are the AI King, a grand, wise, and regal monarch. Respond to the user's question majestically, keeping answers clear and under 4 sentences. Question: ${question}`;

    try {
        // 4. Safely ask Hugging Face for the answer using your hidden key
        const response = await fetch(modelUrl, {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${apiKey}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                inputs: systemPrompt,
                parameters: { max_new_tokens: 150, return_full_text: false }
            })
        });

        const data = await response.json();
        const kingReply = data[0]?.generated_text || "The King remains silent. Please try again.";
        
        // 5. Send the answer back to the user's phone
        return res.status(200).json({ reply: kingReply.trim() });

    } catch (error) {
        return res.status(500).json({ error: 'Failed to reach the royal chamber' });
    }
}
