import { addMsg } from "./ui/chat.js";

// Import mapCategory for discovery restoration
let mapCategory = null;
import("./ui/chat.js").then((module) => {
  mapCategory = module.mapCategory || ((c) => c.toLowerCase());
});
export const state = {
  sessionId: null,

  discoveredInfo: {
    hpi: {}, // label -> { label, value, timestamp }
    medications: {},
    exam: {},
    labs: {},
    imaging: {},
  },

  totalAvailableInfo: 0,
  discoveredCount: 0,
  biasWarningCount: 0,
};

export function newSession() {
  state.sessionId =
    "SESS_" + Math.random().toString(36).substr(2, 9).toUpperCase();
  console.log("[STATE] New session created:", state.sessionId);
  return state.sessionId;
}

export function addDiscovery(category, label, value) {
  if (!state.discoveredInfo[category]) state.discoveredInfo[category] = {};
  const isNew = !state.discoveredInfo[category][label];
  state.discoveredInfo[category][label] = {
    label,
    value,
    timestamp: Date.now(),
  };
  if (isNew) {
    state.discoveredCount++;
    console.log("[STATE] New discovery added:", { category, label, value });
  }
}

export function setTotalAvailableInfo(n) {
  state.totalAvailableInfo = n || 0;
  console.log("[STATE] Total available info set to:", n);
}

export function incBiasWarnings(n = 1) {
  state.biasWarningCount += n;
  console.log("[STATE] Bias warnings count:", state.biasWarningCount);
}

export function getState() {
  return state;
}

// Session restoration functions
export function restoreSessionState(sessionData) {
  // Restore session ID
  state.sessionId = sessionData.session_id;

  // Restore discoveries
  state.discoveredInfo = {
    hpi: {},
    medications: {},
    exam: {},
    labs: {},
    imaging: {},
  };

  state.discoveredCount = 0;

  if (sessionData.discoveries) {
    sessionData.discoveries.forEach((discovery) => {
      // Map the discovery category to UI category
      const rawCategory = discovery.category || "presenting_symptoms";
      const category = mapCategoryLocal(rawCategory);

      if (!state.discoveredInfo[category]) {
        state.discoveredInfo[category] = {};
      }

      state.discoveredInfo[category][discovery.label] = {
        label: discovery.label,
        value: discovery.value,
        timestamp: new Date(discovery.timestamp).getTime(),
      };

      state.discoveredCount++;
    });
  }

  // Restore bias warnings count
  state.biasWarningCount = sessionData.bias_warnings
    ? sessionData.bias_warnings.length
    : 0;

  // Restore chat messages
  if (sessionData.messages) {
    restoreChatMessages(sessionData.messages);
  }

  // Redraw discoveries in UI
  if (sessionData.discoveries) {
    import("./ui/patientInfo.js").then(({ redrawCategory }) => {
      Object.keys(state.discoveredInfo).forEach((cat) => {
        if (Object.keys(state.discoveredInfo[cat]).length > 0) {
          redrawCategory(cat);
        }
      });
    });
  }

  console.log("[STATE] Session restored:", {
    sessionId: state.sessionId,
    discoveries: state.discoveredCount,
    biasWarnings: state.biasWarningCount,
    messages: sessionData.messages ? sessionData.messages.length : 0,
  });
}

function restoreChatMessages(messages) {
  // Group messages by context
  const messagesByContext = {
    anamnesis: [],
    exam: [],
    labs: [],
  };

  messages.forEach((msg) => {
    const context = msg.context || "anamnesis";
    if (messagesByContext[context]) {
      messagesByContext[context].push(msg);
    }
  });

  // Delay message restoration to ensure DOM and images are ready
  setTimeout(() => {
    Object.entries(messagesByContext).forEach(([context, contextMessages]) => {
      if (contextMessages.length > 0) {
        const chatboxId = `${context}-chatbox`;
        contextMessages.forEach((msg) => {
          addMsg(chatboxId, msg.content, msg.role);
        });
      }
    });
  }, 100);
}

// Local category mapping function for restoration
function mapCategoryLocal(c) {
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
  return m[c] || "hpi";
}

export function hasExistingSession() {
  return state.sessionId !== null && state.discoveredCount > 0;
}
