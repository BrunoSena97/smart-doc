import { API_BASE_URL, V1_BASE_URL, USE_LEGACY, DEBUG } from "./config.js";

function log(...args) {
  if (DEBUG) console.log("[API]", ...args);
}

async function request(url, options = {}) {
  log("Request:", url, options);

  const res = await fetch(url, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`HTTP ${res.status}: ${text}`);
  }

  const data = await res.json();
  log("Response:", data);
  return data;
}

// Legacy endpoints (no prefix)
export async function getBotResponse({ message, context, session_id }) {
  const url = `${API_BASE_URL}/get_bot_response`;
  return request(url, {
    method: "POST",
    body: JSON.stringify({ message, context, session_id })
  });
}

export async function submitDiagnosis(payload) {
  const url = `${API_BASE_URL}/submit_diagnosis`;
  return request(url, { method: "POST", body: JSON.stringify(payload) });
}

export async function submitDiagnosisWithReflection(payload) {
  const url = `${API_BASE_URL}/submit_diagnosis_with_reflection`;
  return request(url, { method: "POST", body: JSON.stringify(payload) });
}

// New v1 endpoints (keep ready for the switch)
export async function chatV1({ message }) {
  const url = `${V1_BASE_URL}/chat`;
  return request(url, { method: "POST", body: JSON.stringify({ message }) });
}

export async function healthCheck() {
  const url = `${API_BASE_URL}/health`;
  return request(url, { method: "GET" });
}
