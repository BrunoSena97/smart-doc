// API Configuration for SmartDoc Frontend

// Detect if we're running in local development vs production
const isLocalDevelopment =
  window.location.hostname === "localhost" ||
  window.location.hostname === "127.0.0.1";

// In production (any domain that's not localhost), use relative URLs
// In local development, use absolute URLs to the API server
export const API_BASE_URL = isLocalDevelopment
  ? "http://localhost:8000" // Development: direct to API server
  : ""; // Production: relative URL - traefik/nginx will handle routing

export const V1_BASE_URL = isLocalDevelopment
  ? "http://localhost:8000/api/v1" // Development: direct to API server
  : "/api/v1"; // Production: relative URL - traefik/nginx will handle routing

// Default: try v1 first, then fallback to legacy
export const PREFER_V1 = true;

// Debug logging (disable in production)
export const DEBUG = !isLocalDevelopment;
