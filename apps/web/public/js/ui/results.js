export function renderResults(data) {
  const el = document.getElementById("results-content");
  if (!el) {
    console.error("[RESULTS] Results content container not found");
    return;
  }

  el.innerHTML = `
    <div class="results-summary">
      <div class="score-card">
        <h3><i class="fas fa-star"></i> Overall Score</h3>
        <div class="score-value">${data.score || "N/A"}</div>
      </div>

      <div class="performance-metrics">
        <h3><i class="fas fa-chart-bar"></i> Performance Breakdown</h3>
        <div class="metric-grid">
          <div class="metric-item">
            <span class="metric-label">Information Discovery</span>
            <span class="metric-value">${data?.performance_summary?.information_discovery || "N/A"}</span>
          </div>
          <div class="metric-item">
            <span class="metric-label">Bias Awareness</span>
            <span class="metric-value">${data?.performance_summary?.bias_awareness || "N/A"}</span>
          </div>
          <div class="metric-item">
            <span class="metric-label">Diagnostic Accuracy</span>
            <span class="metric-value">${data?.performance_summary?.diagnostic_accuracy || "N/A"}</span>
          </div>
        </div>
      </div>

      <div class="feedback-section">
        <h3><i class="fas fa-comment-medical"></i> Clinical Feedback</h3>
        <div class="feedback-content">${data.feedback || "No feedback available."}</div>
      </div>
    </div>
  `;

  console.log("[RESULTS] Basic results rendered");
}

export function renderAdvancedResults(data) {
  const el = document.getElementById("results-content");
  if (!el) {
    console.error("[RESULTS] Results content container not found");
    return;
  }

  const ev = data.llm_evaluation?.evaluation;
  if (!ev) {
    console.warn("[RESULTS] No evaluation data found, falling back to basic results");
    renderResults(data);
    return;
  }

  el.innerHTML = `
    <div class="results-summary advanced-results">
      <div class="score-card">
        <h3><i class="fas fa-star"></i> Overall Clinical Performance</h3>
        <div class="score-value">${ev.overall_score || 0}/100</div>
        <div class="confidence-indicator">
          <small>Confidence: ${ev.confidence_assessment || "N/A"}%</small>
        </div>
      </div>

      <div class="performance-metrics">
        <h3><i class="fas fa-chart-bar"></i> Detailed Performance Metrics</h3>
        <div class="metric-grid">
          ${renderMetricItems(ev)}
        </div>
      </div>

      <div class="feedback-section">
        <h3><i class="fas fa-comment-medical"></i> Comprehensive Clinical Feedback</h3>
        <div class="feedback-content">
          ${renderDetailedFeedback(ev)}
        </div>
      </div>

      ${ev.recommendations ? `
        <div class="recommendations-section">
          <h3><i class="fas fa-lightbulb"></i> Recommendations for Improvement</h3>
          <div class="recommendations-content">
            ${renderRecommendations(ev.recommendations)}
          </div>
        </div>
      ` : ''}
    </div>
  `;

  console.log("[RESULTS] Advanced results rendered");
}

function renderMetricItems(evaluation) {
  const metrics = [
    { label: "Information Discovery", key: "information_discovery_score" },
    { label: "Diagnostic Accuracy", key: "diagnostic_accuracy" },
    { label: "Clinical Reasoning", key: "clinical_reasoning_score" },
    { label: "Bias Awareness", key: "bias_awareness_score" },
    { label: "Metacognitive Reflection", key: "metacognitive_score" },
  ];

  return metrics.map(metric => {
    const value = evaluation[metric.key];
    const displayValue = value !== undefined ? `${value}/100` : "N/A";
    return `
      <div class="metric-item">
        <span class="metric-label">${metric.label}</span>
        <span class="metric-value">${displayValue}</span>
      </div>
    `;
  }).join('');
}

function renderDetailedFeedback(evaluation) {
  let feedback = "";

  if (evaluation.strengths) {
    feedback += `<div class="feedback-section-item">
      <h4><i class="fas fa-thumbs-up"></i> Strengths</h4>
      <p>${evaluation.strengths}</p>
    </div>`;
  }

  if (evaluation.areas_for_improvement) {
    feedback += `<div class="feedback-section-item">
      <h4><i class="fas fa-arrow-up"></i> Areas for Improvement</h4>
      <p>${evaluation.areas_for_improvement}</p>
    </div>`;
  }

  if (evaluation.clinical_reasoning_feedback) {
    feedback += `<div class="feedback-section-item">
      <h4><i class="fas fa-brain"></i> Clinical Reasoning</h4>
      <p>${evaluation.clinical_reasoning_feedback}</p>
    </div>`;
  }

  return feedback || "<p>No detailed feedback available.</p>";
}

function renderRecommendations(recommendations) {
  if (Array.isArray(recommendations)) {
    return `<ul class="recommendations-list">
      ${recommendations.map(rec => `<li>${rec}</li>`).join('')}
    </ul>`;
  } else if (typeof recommendations === 'string') {
    return `<p>${recommendations}</p>`;
  } else {
    return "<p>No specific recommendations available.</p>";
  }
}

export function initResults() {
  const resultsContent = document.getElementById("results-content");
  if (resultsContent && !resultsContent.innerHTML.trim()) {
    resultsContent.innerHTML = `
      <div class="results-placeholder">
        <div class="placeholder-content">
          <i class="fas fa-chart-line" style="font-size: 3rem; color: var(--text-muted); margin-bottom: 1rem;"></i>
          <h3>Complete Your Clinical Assessment</h3>
          <p>Submit your diagnosis and reflection to see detailed performance results.</p>
        </div>
      </div>
    `;
  }
}
