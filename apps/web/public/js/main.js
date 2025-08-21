import { newSession } from "./state.js";
import { initTabs } from "./ui/tabs.js";
import { initChatHandlers } from "./ui/chat.js";
import { initPatientInfo } from "./ui/patientInfo.js";
import { initResults } from "./ui/results.js";
import { healthCheck } from "./api.js";

let questionCount = 0;

document.addEventListener("DOMContentLoaded", async () => {
  console.log("[MAIN] SmartDoc Frontend initializing...");

  // Initialize session
  newSession();

  // Initialize UI components
  initTabs();
  initChatHandlers();
  initPatientInfo();
  initResults();

  // Test API connection and set status
  await testApiConnection();

  // Set up legacy DOM elements compatibility (if they exist)
  setupLegacyCompatibility();

  console.log("[MAIN] ✅ SmartDoc Frontend initialized successfully!");
});

async function testApiConnection() {
  const sessionStatusElement =
    document.getElementById("sessionStatus") ||
    document.querySelector(".status-indicator span:last-child") ||
    document.getElementById("current-session");

  try {
    const response = await healthCheck();
    if (sessionStatusElement) {
      sessionStatusElement.textContent = "Connected";
      sessionStatusElement.style.color = "#28a745";
    }

    // Update session display
    const sessionDisplay = document.getElementById("current-session");
    if (sessionDisplay) {
      sessionDisplay.textContent = "Active";
    }

    console.log("[MAIN] ✅ API connection successful");
  } catch (error) {
    console.error("[MAIN] API connection failed:", error);

    if (sessionStatusElement) {
      sessionStatusElement.textContent = "Disconnected";
      sessionStatusElement.style.color = "#dc3545";
    }

    // Show system message in active chat if available
    const activeChatbox = document.querySelector(
      ".tab-content.active .chat-log"
    );
    if (activeChatbox) {
      addSystemMessage(
        activeChatbox,
        "⚠️ Unable to connect to SmartDoc API. Please check if the server is running on port 8000."
      );
    }
  }
}

function setupLegacyCompatibility() {
  // Set up compatibility for any legacy code that might reference these IDs
  const messageInput = document.getElementById("messageInput");
  const messagesContainer = document.getElementById("messages");
  const questionCountElement = document.getElementById("questionCount");

  if (messageInput) {
    messageInput.addEventListener("keypress", function (e) {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        // Find the form this input belongs to and trigger submit
        const form = messageInput.closest("form");
        if (form) {
          form.dispatchEvent(new Event("submit"));
        }
      }
    });
  }

  // Expose global functions for legacy compatibility
  window.sendMessage = function () {
    const activeInput = document.querySelector(".tab-content.active textarea");
    if (activeInput) {
      const form = activeInput.closest("form");
      if (form) {
        form.dispatchEvent(new Event("submit"));
      }
    }
  };

  window.addMessage = function (type, message) {
    const activeChatbox = document.querySelector(
      ".tab-content.active .chat-log"
    );
    if (activeChatbox) {
      addSystemMessage(activeChatbox, message);
    }
  };
}

function addSystemMessage(chatbox, message) {
  const messageDiv = document.createElement("div");
  messageDiv.className = "message system-message";
  messageDiv.innerHTML = `
    <div class="avatar bot-avatar">
      <i class="fas fa-info-circle"></i>
    </div>
    <div class="message-bubble">
      <span>${message}</span>
    </div>
  `;
  chatbox.appendChild(messageDiv);
  chatbox.scrollTop = chatbox.scrollHeight;
}

// Export functions for other modules to use
export { testApiConnection, questionCount };
