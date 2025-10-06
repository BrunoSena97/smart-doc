// API Configuration for SmartDoc Frontend

// Detect if we're running in development (localhost:3000) or production
const isProduction =
  !window.location.hostname.includes("localhost") &&
  !window.location.hostname.includes("127.0.0.1");

// In production, use relative URLs (nginx proxy handles routing)
// In development, use absolute URLs to the API server
export const API_BASE_URL = isProduction
  ? "" // Relative URL - nginx will proxy /api to API server
  : "http://localhost:8000"; // Development: direct to API server

export const V1_BASE_URL = isProduction
  ? "/api/v1" // Relative URL - nginx will proxy to API server
  : "http://localhost:8000/api/v1"; // Development: direct to API server

// Default: try v1 first, then fallback to legacy
export const PREFER_V1 = true;

// Debug logging (disable in production)
export const DEBUG = !isProduction;
