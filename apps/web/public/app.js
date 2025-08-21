const API = window.APP_CONFIG.API_BASE_URL;

let questionCount = 0;

// DOM elements
const messageInput = document.getElementById('messageInput');
const messagesContainer = document.getElementById('messages');
const questionCountElement = document.getElementById('questionCount');
const sessionStatusElement = document.getElementById('sessionStatus');

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    messageInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    // Test API connection
    testApiConnection();
});

async function testApiConnection() {
    try {
        const response = await fetch(`${API}/health`);
        if (response.ok) {
            sessionStatusElement.textContent = 'Connected';
            sessionStatusElement.style.color = '#28a745';
        } else {
            throw new Error('API not responding');
        }
    } catch (error) {
        sessionStatusElement.textContent = 'Disconnected';
        sessionStatusElement.style.color = '#dc3545';
        addMessage('system', '⚠️ Unable to connect to SmartDoc API. Please check if the server is running on port 8000.');
    }
}

async function sendMessage() {
    const message = messageInput.value.trim();
    if (!message) return;

    // Clear input and disable
    messageInput.value = '';
    messageInput.disabled = true;

    // Add user message
    addMessage('user', message);

    // Update question count
    questionCount++;
    questionCountElement.textContent = questionCount;

    // Show loading
    const loadingElement = addMessage('assistant', 'Processing your question...');
    loadingElement.classList.add('loading');

    try {
        const response = await fetch(`${API}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();

        // Remove loading message
        loadingElement.remove();

        // Add AI response
        addMessage('assistant', data.reply || 'No response received');

    } catch (error) {
        console.error('Error:', error);

        // Remove loading message
        loadingElement.remove();

        // Add error message
        addMessage('error', `❌ Error: ${error.message}. Please check the API server.`);
    } finally {
        // Re-enable input
        messageInput.disabled = false;
        messageInput.focus();
    }
}

function addMessage(type, content) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';

    if (type === 'user') {
        contentDiv.innerHTML = `<strong>You:</strong> ${escapeHtml(content)}`;
    } else if (type === 'assistant') {
        contentDiv.innerHTML = `<strong>SmartDoc:</strong> ${escapeHtml(content)}`;
    } else if (type === 'system') {
        contentDiv.innerHTML = content; // System messages can have HTML
    } else if (type === 'error') {
        contentDiv.innerHTML = content; // Error messages can have HTML
    }

    messageDiv.appendChild(contentDiv);
    messagesContainer.appendChild(messageDiv);

    // Scroll to bottom
    messagesContainer.scrollTop = messagesContainer.scrollHeight;

    return messageDiv;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Add some demo functionality
function addDemoMessage() {
    const demoMessages = [
        "What brings the patient here today?",
        "Can you tell me about the patient's current medications?",
        "What are the patient's vital signs?",
        "Does the patient have any allergies?",
        "What is the patient's past medical history?"
    ];

    const randomMessage = demoMessages[Math.floor(Math.random() * demoMessages.length)];
    messageInput.value = randomMessage;
}
