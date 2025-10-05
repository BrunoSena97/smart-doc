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
      const category = discovery.category || "hpi";
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

  console.log("[STATE] Session restored:", {
    sessionId: state.sessionId,
    discoveries: state.discoveredCount,
    biasWarnings: state.biasWarningCount,
  });
}

export function hasExistingSession() {
  return state.sessionId !== null && state.discoveredCount > 0;
}
