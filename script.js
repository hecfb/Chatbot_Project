async function generateContent() {
    const inputText = document.getElementById('inputText').value;
    const outputDiv = document.getElementById('output');

    // Step 1: Generate Content
    let response = await fetch('https://117iyqsjq8.execute-api.us-east-1.amazonaws.com/dev/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ input: inputText })
    });
    let data = await response.json();
    let generatedContent = data.content;

    // Step 2: Manage Content
    response = await fetch('https://117iyqsjq8.execute-api.us-east-1.amazonaws.com/dev/manage', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ content: generatedContent })
    });
    data = await response.json();
    let managedContent = data.content;

    // Step 3: Publish Content
    response = await fetch('https://117iyqsjq8.execute-api.us-east-1.amazonaws.com/dev/publish', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ content: managedContent })
    });
    data = await response.json();
    let publishedMessage = data.message;

    // Display published message and managed content
    outputDiv.innerHTML = `<p>${publishedMessage}</p><p>${managedContent}</p>`;
}
