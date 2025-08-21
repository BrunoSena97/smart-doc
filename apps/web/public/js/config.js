// API Configuration for SmartDoc Frontend
export const API_BASE_URL = "http://localhost:8000"; // for legacy (/chat, /submit_diagnosis...)
export const V1_BASE_URL = "http://localhost:8000/api/v1"; // for new API

// Default: try v1 first, then fallback to legacy
export const PREFER_V1 = true;

// Debug logging
export const DEBUG = true;
