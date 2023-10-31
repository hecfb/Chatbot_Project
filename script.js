async function fetchAPI(url, data) {
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });

    if (!response.ok) {
        throw new Error(`Network response was not ok ${response.statusText}`);
    }

    return response.json();
}

async function generateContent() {
    try {
        const inputText = document.getElementById('inputText').value;
        const outputDiv = document.getElementById('output');

        // Step 1: Generate Content
        const generateUrl = 'https://117iyqsjq8.execute-api.us-east-1.amazonaws.com/dev/generate';
        const generatedData = await fetchAPI(generateUrl, { input: inputText });
        const generatedContent = generatedData.content;

        // Step 2: Manage Content
        const manageUrl = 'https://117iyqsjq8.execute-api.us-east-1.amazonaws.com/dev/manage';
        const managedData = await fetchAPI(manageUrl, { content: generatedContent });
        const managedContent = managedData.content;

        // Step 3: Publish Content
        const publishUrl = 'https://117iyqsjq8.execute-api.us-east-1.amazonaws.com/dev/publish';
        const publishedData = await fetchAPI(publishUrl, { content: managedContent });
        const publishedMessage = publishedData.message;

        // Display published message and managed content
        outputDiv.innerHTML = `<p>${publishedMessage}</p><p>${managedContent}</p>`;
    } catch (error) {
        console.error('Error:', error);
        outputDiv.innerHTML = `<p style="color:red;">Error: ${error.message}</p>`;
    }
}