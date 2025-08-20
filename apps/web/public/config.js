// API Configuration for SmartDoc Frontend
// Use legacy routes for backward compatibility during migration
window.APP_CONFIG = {
    API_BASE_URL: "http://localhost:8000",  // Legacy routes (no /api/v1 prefix)
    USE_NEW_API: false  // Set to true when frontend is updated for v1 routes
};
