import { state } from "../state.js";

export function updateSessionBadge() {
  const el = document.getElementById("current-session");
  if (el) el.textContent = state.sessionId || "N/A";
}

export function updateProgress() {
  const { discoveredCount, totalAvailableInfo } = state;
  const pct = totalAvailableInfo > 0 ? Math.round((discoveredCount / totalAvailableInfo) * 100) : 0;

  const progressEl = document.getElementById("discovery-progress");
  const countEl = document.getElementById("discovery-count");

  if (progressEl) progressEl.style.width = `${pct}%`;
  if (countEl) countEl.textContent = `${discoveredCount}/${totalAvailableInfo}`;

  console.log("[PATIENT-INFO] Progress updated:", { discoveredCount, totalAvailableInfo, pct });
}

export function updateBiasCount() {
  const el = document.getElementById("bias-count");
  if (el) el.textContent = state.biasWarningCount;
}

export function redrawCategory(category) {
  const container = document.getElementById(`${category}-info`);
  const info = state.discoveredInfo[category];

  if (!container) {
    console.warn("[PATIENT-INFO] Container not found for category:", category);
    return;
  }

  if (!info || Object.keys(info).length === 0) {
    container.innerHTML = `<p class="no-info">No ${category} information discovered yet</p>`;
    return;
  }

  const entries = Object.entries(info).sort((a, b) => a[1].timestamp - b[1].timestamp);
  container.innerHTML = "";

  entries.forEach(([_, d]) => {
    const item = document.createElement("div");
    item.className = "info-item";
    item.innerHTML = `
      <span class="info-item-label">${d.label}:</span>
      <span class="info-item-value">${d.value}</span>
    `;
    container.appendChild(item);
  });

  console.log("[PATIENT-INFO] Category redrawn:", category, "entries:", entries.length);
}

export function initPatientInfo() {
  // Initialize all patient info sections
  const categories = ['hpi', 'medications', 'exam', 'labs', 'imaging'];
  categories.forEach(category => redrawCategory(category));

  updateSessionBadge();
  updateProgress();
  updateBiasCount();
}
