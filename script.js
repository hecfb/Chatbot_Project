async function sendMessage() {
    const userInput = document.getElementById('user-input').value;
    const response = await fetch('https://53l2z7756j.execute-api.us-east-1.amazonaws.com/dev', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_input: userInput }),
    });
    const data = await response.json();
    const chatBox = document.getElementById('chat-box');
    chatBox.innerHTML += `<div>User: ${userInput}</div>`;
    chatBox.innerHTML += `<div>Bot: ${data.ChatGPT_reply}</div>`;
    document.getElementById('user-input').value = '';
}