export const state = {
  sessionId: null,

  discoveredInfo: {
    hpi: {},           // label -> { label, value, timestamp }
    medications: {},
    exam: {},
    labs: {},
    imaging: {}
  },

  totalAvailableInfo: 0,
  discoveredCount: 0,
  biasWarningCount: 0,
};

export function newSession() {
  state.sessionId = "SESS_" + Math.random().toString(36).substr(2, 9).toUpperCase();
  console.log("[STATE] New session created:", state.sessionId);
  return state.sessionId;
}

export function addDiscovery(category, label, value) {
  if (!state.discoveredInfo[category]) state.discoveredInfo[category] = {};
  const isNew = !state.discoveredInfo[category][label];
  state.discoveredInfo[category][label] = { label, value, timestamp: Date.now() };
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
  return { ...state };
}
