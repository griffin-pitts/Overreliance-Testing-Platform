document.addEventListener('DOMContentLoaded', function() {
    console.log("Chat.js loaded");
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const chatHistory = document.getElementById('chat-history');

    chatForm.addEventListener('submit', function(e) {
        console.log("Chat form submitted");
        e.preventDefault();
        const message = chatInput.value.trim();
        if (message) {
            console.log("Sending message:", message);
            appendMessage('User', message);
            chatInput.value = '';
            fetchBotResponse(message);
        }
    });

    function appendMessage(sender, message) {
        console.log("Appending message:", sender, message);
        const messageElement = document.createElement('p');
        messageElement.innerHTML = `<strong>${sender}:</strong> ${message}`;
        chatHistory.appendChild(messageElement);
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }

    function fetchBotResponse(message) {
        console.log("Fetching bot response for:", message);
        appendMessage('Bot', 'Thinking...');
        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message }),
        })
        .then(response => {
            console.log("Received response from server");
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log("Parsed response data:", data);
            // Remove the "Thinking..." message
            chatHistory.removeChild(chatHistory.lastChild);
            if (data.error) {
                appendMessage('Bot', `Error: ${data.error}`);
            } else {
                appendMessage('Bot', data.response);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            // Remove the "Thinking..." message
            chatHistory.removeChild(chatHistory.lastChild);
            appendMessage('Bot', `An error occurred: ${error.message}. Please try again or contact support if the problem persists.`);
        });
    }
});