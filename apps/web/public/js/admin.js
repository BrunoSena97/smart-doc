// SmartDoc Admin Panel JavaScript
const API_BASE = "/api/v1";
let authToken = "";

// =============================================================================
// Utility Functions
// =============================================================================

function showError(message) {
  alert("Error: " + message);
}

function showSuccess(message) {
  console.log("Success:", message);
}

function formatDate(dateString) {
  if (!dateString) return "Never";
  return new Date(dateString).toLocaleString();
}

function getAuthHeaders() {
  return authToken ? { Authorization: `Bearer ${authToken}` } : {};
}

async function apiCall(endpoint, options = {}) {
  const url = `${API_BASE}${endpoint}`;
  const config = {
    headers: {
      "Content-Type": "application/json",
      ...getAuthHeaders(),
      ...options.headers,
    },
    ...options,
  };

  try {
    const response = await fetch(url, config);
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || `HTTP ${response.status}`);
    }

    return data;
  } catch (error) {
    console.error("API call failed:", error);
    throw error;
  }
}

// =============================================================================
// Authentication
// =============================================================================

async function login() {
  const code = document.getElementById("access-code").value.trim();
  if (!code) {
    showError("Please enter an access code");
    return;
  }

  try {
    const response = await apiCall("/auth/login", {
      method: "POST",
      body: JSON.stringify({ code }),
    });

    authToken = response.token;
    showAuthenticatedState();
    loadAllData();
    showSuccess("Logged in successfully");
  } catch (error) {
    showError("Login failed: " + error.message);
  }
}

function logout() {
  authToken = "";
  showUnauthenticatedState();
  document.getElementById("access-code").value = "";
}

function showAuthenticatedState() {
  document.getElementById("login-form").classList.add("hidden");
  document.getElementById("auth-status").classList.remove("hidden");
  document.getElementById("auth-section").classList.add("logged-in");
  document.getElementById("admin-content").classList.remove("hidden");
}

function showUnauthenticatedState() {
  document.getElementById("login-form").classList.remove("hidden");
  document.getElementById("auth-status").classList.add("hidden");
  document.getElementById("auth-section").classList.remove("logged-in");
  document.getElementById("admin-content").classList.add("hidden");
}

// =============================================================================
// Users Management
// =============================================================================

async function loadUsers() {
  try {
    const users = await apiCall("/admin/users");
    displayUsers(users);
  } catch (error) {
    showError("Failed to load users: " + error.message);
  }
}

function displayUsers(users) {
  const tbody = document.querySelector("#users-table tbody");
  tbody.innerHTML = "";

  users.forEach((user) => {
    const row = document.createElement("tr");
    row.innerHTML = `
            <td>${user.id}</td>
            <td>${user.display_name || "N/A"}</td>
            <td>${user.email || "N/A"}</td>
            <td>${user.role}</td>
            <td>
                <span class="status-indicator ${
                  user.is_active ? "status-active" : "status-inactive"
                }">
                    ${user.is_active ? "Active" : "Inactive"}
                </span>
            </td>
            <td>${user.usage_count}${
      user.usage_limit ? `/${user.usage_limit}` : ""
    }</td>
            <td>${formatDate(user.created_at)}</td>
            <td>
                <button class="btn btn-danger" onclick="deleteUser(${user.id})"
                        ${
                          user.role === "admin"
                            ? 'disabled title="Cannot delete admin"'
                            : ""
                        }>
                    🗑️
                </button>
            </td>
        `;
    tbody.appendChild(row);
  });
}

async function createUser() {
  const userData = {
    display_name: document.getElementById("user-name").value.trim(),
    email: document.getElementById("user-email").value.trim(),
    age: parseInt(document.getElementById("user-age").value) || null,
    sex: document.getElementById("user-sex").value || null,
    medical_experience:
      document.getElementById("user-experience").value.trim() || null,
    role: document.getElementById("user-role").value,
    code_label: document.getElementById("user-label").value.trim() || null,
    is_active: true,
  };

  if (!userData.display_name) {
    showError("Display name is required");
    return;
  }

  try {
    const response = await apiCall("/admin/users", {
      method: "POST",
      body: JSON.stringify(userData),
    });

    // Show the access code
    document.getElementById("new-user-code").textContent = response.access_code;
    document.getElementById("user-code-display").classList.remove("hidden");

    // Clear form
    clearUserForm();

    // Reload users
    loadUsers();
    showSuccess("User created successfully");
  } catch (error) {
    showError("Failed to create user: " + error.message);
  }
}

function clearUserForm() {
  document.getElementById("user-name").value = "";
  document.getElementById("user-email").value = "";
  document.getElementById("user-age").value = "";
  document.getElementById("user-sex").value = "";
  document.getElementById("user-experience").value = "";
  document.getElementById("user-role").value = "user";
  document.getElementById("user-label").value = "";
}

async function deleteUser(userId) {
  if (!confirm("Are you sure you want to delete this user?")) {
    return;
  }

  try {
    await apiCall(`/admin/users/${userId}`, { method: "DELETE" });
    loadUsers();
    showSuccess("User deleted successfully");
  } catch (error) {
    showError("Failed to delete user: " + error.message);
  }
}

// =============================================================================
// LLM Profiles Management
// =============================================================================

async function loadProfiles() {
  try {
    const profiles = await apiCall("/admin/llm-profiles");
    displayProfiles(profiles);
    updateProfileSelects(profiles);
  } catch (error) {
    showError("Failed to load profiles: " + error.message);
  }
}

function displayProfiles(profiles) {
  const tbody = document.querySelector("#profiles-table tbody");
  tbody.innerHTML = "";

  profiles.forEach((profile) => {
    const row = document.createElement("tr");
    row.innerHTML = `
            <td>${profile.id}</td>
            <td>${profile.name}</td>
            <td>${profile.provider}</td>
            <td>${profile.model}</td>
            <td>${profile.temperature}</td>
            <td>${profile.top_p}</td>
            <td>
                <span class="status-indicator ${
                  profile.is_default ? "status-active" : "status-inactive"
                }">
                    ${profile.is_default ? "Yes" : "No"}
                </span>
            </td>
            <td>${formatDate(profile.created_at)}</td>
            <td>
                <button class="btn btn-danger" onclick="deleteProfile(${
                  profile.id
                })">🗑️</button>
            </td>
        `;
    tbody.appendChild(row);
  });
}

function updateProfileSelects(profiles) {
  const select = document.getElementById("prompt-profile");
  const currentValue = select.value;

  // Clear existing options except first
  while (select.children.length > 1) {
    select.removeChild(select.lastChild);
  }

  profiles.forEach((profile) => {
    const option = document.createElement("option");
    option.value = profile.id;
    option.textContent = profile.name;
    select.appendChild(option);
  });

  // Restore selection if possible
  if (currentValue) {
    select.value = currentValue;
  }
}

async function createProfile() {
  const profileData = {
    name: document.getElementById("profile-name").value.trim(),
    provider: document.getElementById("profile-provider").value,
    model: document.getElementById("profile-model").value.trim(),
    temperature: parseFloat(
      document.getElementById("profile-temperature").value
    ),
    top_p: parseFloat(document.getElementById("profile-top-p").value),
    max_tokens:
      parseInt(document.getElementById("profile-max-tokens").value) || null,
    is_default: document.getElementById("profile-default").checked,
  };

  if (!profileData.name || !profileData.model) {
    showError("Name and model are required");
    return;
  }

  try {
    await apiCall("/admin/llm-profiles", {
      method: "POST",
      body: JSON.stringify(profileData),
    });

    clearProfileForm();
    loadProfiles();
    showSuccess("Profile created successfully");
  } catch (error) {
    showError("Failed to create profile: " + error.message);
  }
}

function clearProfileForm() {
  document.getElementById("profile-name").value = "";
  document.getElementById("profile-provider").value = "ollama";
  document.getElementById("profile-model").value = "";
  document.getElementById("profile-temperature").value = "0.1";
  document.getElementById("profile-top-p").value = "0.9";
  document.getElementById("profile-max-tokens").value = "";
  document.getElementById("profile-default").checked = false;
}

async function deleteProfile(profileId) {
  if (!confirm("Are you sure you want to delete this profile?")) {
    return;
  }

  try {
    await apiCall(`/admin/llm-profiles/${profileId}`, { method: "DELETE" });
    loadProfiles();
    showSuccess("Profile deleted successfully");
  } catch (error) {
    showError("Failed to delete profile: " + error.message);
  }
}

// =============================================================================
// Agent Prompts Management
// =============================================================================

async function loadPrompts() {
  try {
    const prompts = await apiCall("/admin/prompts");
    displayPrompts(prompts);
  } catch (error) {
    showError("Failed to load prompts: " + error.message);
  }
}

function displayPrompts(prompts) {
  const tbody = document.querySelector("#prompts-table tbody");
  tbody.innerHTML = "";

  // Store prompts data globally for modal access
  window.promptsData = {};

  prompts.forEach((prompt) => {
    // Store full prompt data
    window.promptsData[prompt.id] = prompt;

    const row = document.createElement("tr");
    row.innerHTML = `
            <td>${prompt.id}</td>
            <td>${prompt.agent_key}</td>
            <td>${prompt.profile_name || "Default"}</td>
            <td>${prompt.version}</td>
            <td>
                <span class="status-indicator ${
                  prompt.is_active ? "status-active" : "status-inactive"
                }">
                    ${prompt.is_active ? "Active" : "Inactive"}
                </span>
            </td>
            <td>${formatDate(prompt.created_at)}</td>
            <td>
                <div class="action-buttons">
                    <button class="btn btn-secondary" onclick="viewPrompt(${
                      prompt.id
                    })">👁️ View</button>
                    <button class="btn ${
                      prompt.is_active ? "btn-secondary" : "btn"
                    }" onclick="togglePromptStatus(${prompt.id}, '${
      prompt.agent_key
    }')" title="${prompt.is_active ? "Deactivate" : "Activate"}">
                        ${prompt.is_active ? "🔄 Deactivate" : "✅ Activate"}
                    </button>
                    <button class="btn btn-danger" onclick="deletePrompt(${
                      prompt.id
                    })">🗑️</button>
                </div>
            </td>
        `;
    tbody.appendChild(row);
  });
}

async function createPrompt() {
  const promptData = {
    agent_key: document.getElementById("prompt-agent").value,
    profile_id:
      parseInt(document.getElementById("prompt-profile").value) || null,
    prompt_text: document.getElementById("prompt-text").value.trim(),
    version: 1,
    is_active: true,
  };

  if (!promptData.prompt_text) {
    showError("Prompt text is required");
    return;
  }

  try {
    await apiCall("/admin/prompts", {
      method: "POST",
      body: JSON.stringify(promptData),
    });

    clearPromptForm();
    loadPrompts();
    showSuccess("Prompt created successfully");
  } catch (error) {
    showError("Failed to create prompt: " + error.message);
  }
}

function clearPromptForm() {
  document.getElementById("prompt-agent").value = "son";
  document.getElementById("prompt-profile").value = "";
  document.getElementById("prompt-text").value = "";
}

async function deletePrompt(promptId) {
  if (!confirm("Are you sure you want to delete this prompt?")) {
    return;
  }

  try {
    await apiCall(`/admin/prompts/${promptId}`, { method: "DELETE" });
    loadPrompts();
    showSuccess("Prompt deleted successfully");
  } catch (error) {
    showError("Failed to delete prompt: " + error.message);
  }
}

async function togglePromptStatus(promptId, agentKey) {
  const prompt = window.promptsData[promptId];
  if (!prompt) {
    showError("Prompt data not found");
    return;
  }

  const action = prompt.is_active ? "deactivate" : "activate";
  const confirmMessage = prompt.is_active
    ? "Are you sure you want to deactivate this prompt?"
    : `Are you sure you want to activate this prompt? This will deactivate any other active prompts for the ${agentKey} agent.`;

  if (!confirm(confirmMessage)) {
    return;
  }

  try {
    const response = await apiCall(`/admin/prompts/${promptId}/toggle-status`, {
      method: "POST",
    });

    loadPrompts(); // Reload to show updated statuses
    showSuccess(response.message || `Prompt ${action}d successfully`);
  } catch (error) {
    showError(`Failed to ${action} prompt: ` + error.message);
  }
}

// =============================================================================
// System Configuration
// =============================================================================

async function loadConfiguration() {
  try {
    const config = await apiCall("/admin/config");
    document.getElementById("hide-bias-warnings").checked =
      config.hide_bias_warnings || false;
    showSuccess("Configuration loaded");
  } catch (error) {
    showError("Failed to load configuration: " + error.message);
  }
}

async function saveConfiguration() {
  const config = {
    hide_bias_warnings: document.getElementById("hide-bias-warnings").checked,
  };

  try {
    await apiCall("/admin/config", {
      method: "POST",
      body: JSON.stringify(config),
    });
    showSuccess("Configuration saved successfully");
  } catch (error) {
    showError("Failed to save configuration: " + error.message);
  }
}

// =============================================================================
// Audit Logs
// =============================================================================

async function loadAuditLogs() {
  try {
    const logs = await apiCall("/admin/audit-logs");
    displayAuditLogs(logs);
  } catch (error) {
    showError("Failed to load audit logs: " + error.message);
  }
}

function displayAuditLogs(logs) {
  const tbody = document.querySelector("#logs-table tbody");
  tbody.innerHTML = "";

  logs.forEach((log) => {
    const row = document.createElement("tr");
    const payload = log.payload ? JSON.stringify(log.payload) : "";

    row.innerHTML = `
            <td>${formatDate(log.created_at)}</td>
            <td>${log.actor_name || "System"}</td>
            <td>${log.action}</td>
            <td title="${payload}">${payload.substring(0, 50)}${
      payload.length > 50 ? "..." : ""
    }</td>
        `;
    tbody.appendChild(row);
  });
}

// =============================================================================
// Data Loading
// =============================================================================

async function loadAllData() {
  try {
    await Promise.all([
      loadUsers(),
      loadProfiles(),
      loadPrompts(),
      loadAuditLogs(),
      loadConfiguration(),
    ]);
  } catch (error) {
    console.error("Failed to load some data:", error);
  }
}

// =============================================================================
// Event Listeners
// =============================================================================

document.addEventListener("DOMContentLoaded", function () {
  // Auth events
  document.getElementById("login-btn").addEventListener("click", login);
  document.getElementById("logout-btn").addEventListener("click", logout);

  // Enter key for login
  document
    .getElementById("access-code")
    .addEventListener("keypress", function (e) {
      if (e.key === "Enter") {
        login();
      }
    });

  // Refresh buttons
  document.getElementById("refresh-users").addEventListener("click", loadUsers);
  document
    .getElementById("refresh-profiles")
    .addEventListener("click", loadProfiles);
  document
    .getElementById("refresh-prompts")
    .addEventListener("click", loadPrompts);
  document
    .getElementById("refresh-logs")
    .addEventListener("click", loadAuditLogs);

  // Create buttons
  document.getElementById("create-user").addEventListener("click", createUser);
  document
    .getElementById("create-profile")
    .addEventListener("click", createProfile);
  document
    .getElementById("create-prompt")
    .addEventListener("click", createPrompt);

  // Hide user code display when clicking anywhere
  document.addEventListener("click", function (e) {
    if (
      !e.target.closest("#user-code-display") &&
      !e.target.closest("#create-user")
    ) {
      document.getElementById("user-code-display").classList.add("hidden");
    }
  });
});

// Export functions for inline onclick handlers
window.deleteUser = deleteUser;
window.deleteProfile = deleteProfile;
window.deletePrompt = deletePrompt;
window.togglePromptStatus = togglePromptStatus;
window.viewPrompt = viewPrompt;
window.closePromptModal = closePromptModal;
window.loadConfiguration = loadConfiguration;
window.saveConfiguration = saveConfiguration;
window.saveConfiguration = saveConfiguration;

// =============================================================================
// Prompt Modal Functions
// =============================================================================

function viewPrompt(id) {
  const prompt = window.promptsData[id];
  if (!prompt) {
    showError("Prompt data not found");
    return;
  }

  // Populate modal data
  document.getElementById("modal-agent").textContent = prompt.agent_key;
  document.getElementById("modal-profile").textContent =
    prompt.profile_name || "Default";
  document.getElementById("modal-version").textContent = prompt.version;
  document.getElementById("modal-status").innerHTML = `
    <span class="status-indicator ${
      prompt.is_active ? "status-active" : "status-inactive"
    }">
      ${prompt.is_active ? "Active" : "Inactive"}
    </span>
  `;
  document.getElementById("modal-created").textContent = formatDate(
    prompt.created_at
  );
  document.getElementById("modal-updated").textContent = formatDate(
    prompt.updated_at || prompt.created_at
  );
  document.getElementById("modal-prompt-text").textContent = prompt.prompt_text;

  // Show modal
  document.getElementById("prompt-modal").style.display = "block";
}

function closePromptModal() {
  document.getElementById("prompt-modal").style.display = "none";
}

// Close modal when clicking outside of it
window.onclick = function (event) {
  const modal = document.getElementById("prompt-modal");
  if (event.target === modal) {
    closePromptModal();
  }
};
