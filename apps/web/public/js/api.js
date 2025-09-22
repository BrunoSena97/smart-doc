import { API_BASE_URL, V1_BASE_URL, PREFER_V1, DEBUG } from "./config.js";
import { state } from "./state.js";

function log(...args) {
  if (DEBUG) console.debug("[API]", ...args);
}

// Auth helper functions
export function authHeaders() {
  const token = localStorage.getItem("smartdoc_token");
  return token ? { Authorization: `Bearer ${token}` } : {};
}

export function isAuthenticated() {
  return !!localStorage.getItem("smartdoc_token");
}

export function clearAuth() {
  localStorage.removeItem("smartdoc_token");
}

async function request(url, options = {}) {
  log("Request:", url, options);

  const headers = {
    "Content-Type": "application/json",
    ...authHeaders(),
    ...(options.headers || {}),
  };

  const res = await fetch(url, {
    headers,
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

// Helper function to try v1 first, then fallback to legacy
async function tryThenFallback(tryFn, fallbackFn) {
  try {
    const result = await tryFn();
    log("✅ Used v1 endpoint successfully");
    return result;
  } catch (error) {
    log("⚠️ v1 endpoint failed, falling back to legacy:", error.message);
    try {
      const result = await fallbackFn();
      log("✅ Used legacy endpoint successfully");
      return result;
    } catch (fallbackError) {
      log("❌ Both v1 and legacy endpoints failed");
      throw fallbackError;
    }
  }
}

// Health check (always at root)
export async function healthCheck() {
  const url = `${API_BASE_URL}/health`;
  return request(url, { method: "GET" });
}

// Chat with automatic fallback
export async function sendChat(message, context = "anamnesis") {
  if (!PREFER_V1) {
    // Use legacy directly if v1 is disabled
    log("Using legacy endpoint by configuration");
    return legacyChatRequest(message, context);
  }

  return tryThenFallback(
    () => v1ChatRequest(message, context),
    () => legacyChatRequest(message, context)
  );
}

// V1 chat request
async function v1ChatRequest(message, context = "anamnesis") {
  const url = `${V1_BASE_URL}/chat`;
  return request(url, {
    method: "POST",
    body: JSON.stringify({
      message,
      context,
      session_id: state.sessionId,
    }),
  });
}

// Legacy chat request
async function legacyChatRequest(message, context = "anamnesis") {
  const url = `${API_BASE_URL}/get_bot_response`;
  return request(url, {
    method: "POST",
    body: JSON.stringify({
      message,
      context, // Now properly passes the context
      session_id: "web_session",
    }),
  });
}

// Diagnosis submission with fallback
export async function submitDiagnosis(payload) {
  if (!PREFER_V1) {
    return legacySubmitDiagnosis(payload);
  }

  return tryThenFallback(
    () => v1SubmitDiagnosis(payload),
    () => legacySubmitDiagnosis(payload)
  );
}

// V1 diagnosis submission (placeholder for when backend is ready)
async function v1SubmitDiagnosis(payload) {
  const url = `${V1_BASE_URL}/diagnosis`;
  return request(url, {
    method: "POST",
    body: JSON.stringify({
      ...payload,
      session_id: state.sessionId,
    }),
  });
}

// Legacy diagnosis submission
async function legacySubmitDiagnosis(payload) {
  const url = `${API_BASE_URL}/submit_diagnosis`;
  return request(url, {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

// Diagnosis with reflection submission with fallback
export async function submitDiagnosisWithReflection(payload) {
  if (!PREFER_V1) {
    return legacySubmitDiagnosisWithReflection(payload);
  }

  return tryThenFallback(
    () => v1SubmitDiagnosisWithReflection(payload),
    () => legacySubmitDiagnosisWithReflection(payload)
  );
}

// V1 diagnosis with reflection using new evaluation system
async function v1SubmitDiagnosisWithReflection(payload) {
  const url = `${V1_BASE_URL}/evaluation/submit`;
  return request(url, {
    method: "POST",
    body: JSON.stringify({
      diagnosis: payload.diagnosis,
      metacognitive_responses: payload.metacognitive_responses,
      session_id: payload.session_data?.session_id,
      case_context: {},
    }),
  });
}

// Legacy diagnosis with reflection
async function legacySubmitDiagnosisWithReflection(payload) {
  const url = `${API_BASE_URL}/submit_diagnosis_with_reflection`;
  return request(url, {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

// Legacy compatibility exports (for gradual migration)
export async function getBotResponse({ message, context, session_id }) {
  return legacyChatRequest(message, context);
}

// Auth API endpoints
export async function login(code) {
  const url = `${V1_BASE_URL}/auth/login`;
  return request(url, {
    method: "POST",
    body: JSON.stringify({ code }),
  });
}

export async function logout() {
  const url = `${V1_BASE_URL}/auth/logout`;
  try {
    await request(url, { method: "POST" });
  } finally {
    clearAuth();
  }
}

export async function getProfile() {
  const url = `${V1_BASE_URL}/auth/me`;
  return request(url, { method: "GET" });
}
