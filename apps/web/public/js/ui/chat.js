import {
  sendChat,
  submitDiagnosis,
  submitDiagnosisWithReflection,
} from "../api.js";
import {
  state,
  addDiscovery,
  setTotalAvailableInfo,
  incBiasWarnings,
} from "../state.js";
import {
  redrawCategory,
  updateProgress,
  updateBiasCount,
} from "./patientInfo.js";
import { V1_BASE_URL } from "../config.js";

export function initChatHandlers() {
  // Hook up chat forms for each context
  hookForm("anamnesis");
  hookForm("exam");
  hookForm("labs");

  // Hook up diagnosis submission
  const submitBtn = document.getElementById("submit-diagnosis");
  if (submitBtn) {
    submitBtn.addEventListener("click", () => {
      const dx = document.getElementById("diagnosis-input")?.value.trim();
      if (!dx) {
        alert("Please enter your diagnosis.");
        return;
      }
      showMetacognitiveCheckpoint();
    });
  }

  // Hook up reflection submission
  const reflectionBtn = document.getElementById("submit-reflection");
  if (reflectionBtn) {
    reflectionBtn.addEventListener("click", async () => {
      const dx = document.getElementById("diagnosis-input")?.value.trim();
      const reflection = collectReflection();
      if (!validateReflection(reflection)) {
        alert("Please complete all reflection questions before submitting.");
        return;
      }

      await handleSubmitDiagnosisWithReflection(dx, reflection);
    });
  }

  console.log("[CHAT] Chat handlers initialized");
}

function hookForm(context) {
  const form = document.getElementById(`${context}-form`);
  if (!form) {
    console.warn("[CHAT] Form not found for context:", context);
    return;
  }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    await handleChat(context);
  });

  console.log("[CHAT] Form hooked for context:", context);
}

async function handleChat(context) {
  const input = document.getElementById(`${context}-input`);
  const chatboxId = `${context}-chatbox`;

  if (!input) {
    console.error("[CHAT] Input not found for context:", context);
    return;
  }

  const text = input.value.trim();
  if (!text) return;

  // Add user message to chat
  addMsg(chatboxId, text, "user");

  // Clear input and reset height
  input.value = "";
  input.style.height = "auto";

  try {
    console.log("[CHAT] Sending message:", {
      text,
      context,
      sessionId: state.sessionId,
    });

    const data = await sendChat(text, context);

    // Save session ID to localStorage for persistence
    if (state.sessionId) {
      localStorage.setItem("smartdoc_session_id", state.sessionId);
    }

    // Add bot response
    addMsg(chatboxId, data.response, "bot");

    // Process discovery events
    if (Array.isArray(data.discovery_events)) {
      for (const ev of data.discovery_events) {
        const cat = mapCategory(ev.category);
        if (cat) {
          addDiscovery(cat, ev.field, ev.value);
          redrawCategory(cat);
        }
      }
    }

    // Update discovery stats
    if (
      data.discovery_stats &&
      typeof data.discovery_stats.total === "number"
    ) {
      setTotalAvailableInfo(data.discovery_stats.total);
      updateProgress();
    }

    // Handle bias warnings
    if (Array.isArray(data.bias_warnings) && data.bias_warnings.length) {
      for (const w of data.bias_warnings) {
        addBiasWarning(chatboxId, w);
      }
      incBiasWarnings(data.bias_warnings.length);
      updateBiasCount();
    }

    // Log if using real SmartDoc engine
    if (data.smartdoc_engine) {
      console.log("[CHAT] ✅ Response from real SmartDoc engine");
    } else {
      console.log("[CHAT] ⚠️ Response from mock engine");
    }
  } catch (err) {
    console.error("[CHAT] Error:", err);
    addMsg(
      chatboxId,
      "Sorry, I encountered an error. Please try again.",
      "bot"
    );
  }
}

function addMsg(chatboxId, text, role) {
  console.log("[CHAT] addMsg called with:", {
    chatboxId,
    text: text.substring(0, 50) + "...",
    role,
  });

  const box = document.getElementById(chatboxId);
  if (!box) {
    console.error("[CHAT] Chatbox not found:", chatboxId);
    return;
  }

  const card = document.createElement("div");
  card.className = `message ${role === "assistant" ? "bot" : role}-message`;

  const avatar = document.createElement("div");
  avatar.className = `avatar ${role === "assistant" ? "bot" : role}-avatar`;

  if (role === "bot" || role === "assistant") {
    // Create avatar elements programmatically instead of using innerHTML
    const img = document.createElement("img");
    const fallback = document.createElement("i");

    // Set image properties
    img.className = "avatar-image";
    img.alt = getBotAltText(chatboxId);

    // Set fallback icon properties
    fallback.className = getBotFallbackClass(chatboxId);
    fallback.style.display = "none";

    // Handle image load errors with retry logic
    img.onerror = function () {
      console.error("[CHAT] Failed to load avatar image:", this.src);
      console.log("[CHAT] Attempting fallback to icon for chatbox:", chatboxId);
      this.style.display = "none";
      fallback.style.display = "flex";
    };

    // Handle successful image load
    img.onload = function () {
      console.log("[CHAT] Successfully loaded avatar image:", this.src);
      this.style.display = "block";
      fallback.style.display = "none";
    };

    // Set the image source AFTER setting up event handlers
    img.src = getBotImageUrl(chatboxId);

    avatar.appendChild(img);
    avatar.appendChild(fallback);
  } else {
    avatar.innerHTML = '<i class="fas fa-user-md"></i>';
  }

  const bubble = document.createElement("div");
  bubble.className = "message-bubble";
  bubble.innerHTML = `<span>${text}</span>`;

  card.appendChild(avatar);
  card.appendChild(bubble);
  box.appendChild(card);
  box.scrollTop = box.scrollHeight;
}

function getBotImageUrl(chatboxId) {
  console.log("[CHAT] Using V1_BASE_URL for assets:", V1_BASE_URL);
  console.log("[CHAT] Getting image URL for chatboxId:", chatboxId);

  let imageUrl;
  if (chatboxId.includes("anamnesis")) {
    imageUrl = `${V1_BASE_URL}/assets/son_image.png`;
  } else if (chatboxId.includes("exam")) {
    imageUrl = `${V1_BASE_URL}/assets/patient_image.png`;
  } else if (chatboxId.includes("labs")) {
    imageUrl = `${V1_BASE_URL}/assets/resident_image.png`;
  } else {
    imageUrl = `${V1_BASE_URL}/assets/resident_image.png`;
  }

  console.log("[CHAT] Resolved image URL:", imageUrl);
  return imageUrl;
}

function getBotAltText(chatboxId) {
  if (chatboxId.includes("anamnesis")) return "Son";
  if (chatboxId.includes("exam")) return "Patient";
  if (chatboxId.includes("labs")) return "Resident";
  return "Resident";
}

function getBotFallbackClass(chatboxId) {
  if (chatboxId.includes("anamnesis")) return "fas fa-user avatar-fallback";
  if (chatboxId.includes("exam")) return "fas fa-stethoscope avatar-fallback";
  if (chatboxId.includes("labs")) return "fas fa-user-md avatar-fallback";
  return "fas fa-user-md avatar-fallback";
}

function addBiasWarning(chatboxId, warning) {
  const box = document.getElementById(chatboxId);
  if (!box) return;

  const div = document.createElement("div");
  div.className = "bias-warning";
  div.innerHTML = `
    <div class="bias-warning-header">
      <i class="fas fa-exclamation-triangle"></i>
      Cognitive Bias Alert: ${warning.bias_type || "Unknown"}
    </div>
    <div class="bias-warning-content">${
      warning.description || warning.message || "Bias detected"
    }</div>
  `;
  box.appendChild(div);
  box.scrollTop = box.scrollHeight;
}

function mapCategory(c) {
  const m = {
    "Clinical History": "hpi",
    "Medical History": "hpi",
    History: "hpi",
    HPI: "hpi",
    "Presenting Symptoms": "hpi",
    medical_history: "hpi",
    presenting_symptoms: "hpi",
    clinical_assessment: "hpi",
    hpi: "hpi",
    history: "hpi",
    general: "hpi",

    "Current Medications": "medications",
    Medications: "medications",
    current_medications: "medications",
    medications: "medications",

    "Physical Examination": "exam",
    "Physical Exam": "exam",
    Examination: "exam",
    physical_examination: "exam",
    physical_exam: "exam",
    examination: "exam",
    exam: "exam",

    Laboratory: "labs",
    Labs: "labs",
    "Diagnostic Results": "labs",
    diagnostic_results: "labs",
    laboratory: "labs",
    labs: "labs",

    Imaging: "imaging",
    imaging: "imaging",
  };

  return m[c] || null;
}

function showMetacognitiveCheckpoint() {
  const submitBtn = document.getElementById("submit-diagnosis");
  const checkpoint = document.getElementById("metacognitive-checkpoint");

  if (submitBtn) submitBtn.style.display = "none";
  if (checkpoint) {
    checkpoint.style.display = "block";
    checkpoint.scrollIntoView({ behavior: "smooth" });
  }
}

function collectReflection() {
  return {
    "What is the single most compelling piece of evidence that supports your chosen diagnosis?":
      document.getElementById("supporting-evidence")?.value.trim() || "",
    "What is one piece of evidence that might argue against your diagnosis?":
      document.getElementById("contradicting-evidence")?.value.trim() || "",
    "What else could this be? List at least two reasonable alternative diagnoses.":
      document.getElementById("alternative-diagnoses")?.value.trim() || "",
    "For one of your alternative diagnoses, what specific information would help rule it in or out?":
      document.getElementById("additional-testing")?.value.trim() || "",
    "Have you considered and ruled out any potential must-not-miss or life-threatening conditions?":
      document.getElementById("critical-conditions")?.value.trim() || "",
  };
}

function validateReflection(obj) {
  // Minimal validation for research study - only check basic completion
  return Object.values(obj).every((v) => v && v.trim().length > 0);
}

async function handleSubmitDiagnosisWithReflection(diagnosis, reflection) {
  const btn = document.getElementById("submit-reflection");
  if (!btn) return;

  const originalText = btn.innerHTML;
  btn.innerHTML =
    '<i class="fas fa-spinner fa-spin"></i> Processing Evaluation...';
  btn.disabled = true;

  try {
    const data = await submitDiagnosisWithReflection({
      diagnosis,
      metacognitive_responses: reflection,
      session_data: {
        discovered_count: state.discoveredCount,
        total_available: state.totalAvailableInfo,
        bias_warnings: state.biasWarningCount,
        discovered_info: state.discoveredInfo,
      },
    });

    // Import and use results renderer
    const { renderResults, renderAdvancedResults } = await import(
      "./results.js"
    );

    if (data.llm_evaluation?.evaluation) {
      renderAdvancedResults(data);
    } else {
      renderResults(data);
    }

    // Switch to results tab
    const resultsTab = document.querySelector('[data-tab="results"]');
    if (resultsTab) resultsTab.click();
  } catch (error) {
    console.error("[CHAT] Diagnosis submission error:", error);
    alert("Error submitting diagnosis. Please try again.");
  } finally {
    btn.innerHTML = originalText;
    btn.disabled = false;
  }
}

// Export addMsg and mapCategory for session restoration
export { addMsg, mapCategory };
