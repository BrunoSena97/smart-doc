// API Configuration for SmartDoc Frontend

// Detect if we're running in development (localhost:3000) or production
const isLocalDevelopment =
  (window.location.hostname === "localhost" ||
    window.location.hostname === "127.0.0.1") &&
  window.location.port === "3000";

// Debug logging
console.log("SmartDoc Config Debug:", {
  hostname: window.location.hostname,
  port: window.location.port,
  isLocalDevelopment,
  fullUrl: window.location.href,
});

// In production or when NOT on localhost:3000, use relative URLs (nginx proxy handles routing)
// Only in local development (localhost:3000), use absolute URLs to the API server
export const API_BASE_URL = isLocalDevelopment
  ? "http://localhost:8000" // Development: direct to API server
  : ""; // Production: relative URL - nginx will proxy /api to API server

export const V1_BASE_URL = isLocalDevelopment
  ? "http://localhost:8000/api/v1" // Development: direct to API server
  : "/api/v1"; // Production: relative URL - nginx will proxy to API server

// Debug the final URLs
console.log("SmartDoc API URLs:", {
  API_BASE_URL,
  V1_BASE_URL,
});
