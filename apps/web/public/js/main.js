import { newSession } from "./state.js";
import { initTabs } from "./ui/tabs.js";
import { initChatHandlers } from "./ui/chat.js";
import { initPatientInfo } from "./ui/patientInfo.js";
import { initResults } from "./ui/results.js";

document.addEventListener("DOMContentLoaded", () => {
  console.log("[MAIN] SmartDoc Frontend initializing...");

  // Initialize session
  newSession();

  // Initialize UI components
  initTabs();
  initChatHandlers();
  initPatientInfo();
  initResults();

  console.log("[MAIN] ✅ SmartDoc Frontend initialized successfully!");
});
