export function renderResults(data) {
  const el = document.getElementById("results-content");
  if (!el) {
    console.error("[RESULTS] Results content container not found");
    return;
  }

  el.innerHTML = `
    <div class="results-summary">

      <div class="feedback-section">
        <h3><i class="fas fa-comment-medical"></i> Clinical Feedback</h3>
        <div class="feedback-content">${
          data.feedback || "No feedback available."
        }</div>
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
    console.warn(
      "[RESULTS] No evaluation data found, falling back to basic results"
    );
    renderResults(data);
    return;
  }

  // Calculate overall score from the three main components
  const infoScore = ev.information_gathering?.score || 0;
  const diagScore = ev.diagnostic_accuracy?.score || 0;
  const biasScore = ev.cognitive_bias_awareness?.score || 0;
  const overallScore = Math.round((infoScore + diagScore + biasScore) / 3);

  el.innerHTML = `
    <div class="results-summary advanced-results">
      <div class="score-card">
        <h3><i class="fas fa-star"></i> Overall Clinical Performance</h3>
        <div class="score-value">${overallScore}/100</div>
        <div class="score-breakdown">
          <small>Based on three core competencies</small>
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

            <div class="recommendations-section">
        <h3><i class="fas fa-chart-bar"></i> Performance Analysis</h3>
        <div class="recommendations-content">
          ${generateImprovementAdvice(ev)
            .map((advice) => `<div class="advice-item">${advice}</div>`)
            .join("")}
        </div>
      </div>
    </div>
  `;

  console.log("[RESULTS] Advanced results rendered");
}

function renderMetricItems(evaluation) {
  const metrics = [
    { label: "Information Gathering", path: "information_gathering.score" },
    { label: "Diagnostic Accuracy", path: "diagnostic_accuracy.score" },
    {
      label: "Cognitive Bias Awareness",
      path: "cognitive_bias_awareness.score",
    },
  ];

  return metrics
    .map((metric) => {
      const value = getNestedValue(evaluation, metric.path);
      const displayValue = value !== undefined ? `${value}/100` : "N/A";
      const colorClass = getScoreColorClass(value);
      return `
      <div class="metric-item">
        <span class="metric-label">${metric.label}</span>
        <span class="metric-value ${colorClass}">${displayValue}</span>
      </div>
    `;
    })
    .join("");
}

// Helper function to get nested object values
function getNestedValue(obj, path) {
  return path.split(".").reduce((current, key) => current?.[key], obj);
}

// Helper function to get color class based on score
function getScoreColorClass(score) {
  if (score === undefined || score === null) return "";
  if (score >= 80) return "score-excellent";
  if (score >= 60) return "score-good";
  if (score >= 40) return "score-fair";
  return "score-poor";
}

function renderDetailedFeedback(evaluation) {
  let feedback = "";
  const comprehensiveFeedback = evaluation.comprehensive_feedback || {};

  if (comprehensiveFeedback.strengths) {
    feedback += `<div class="feedback-section-item">
      <h4><i class="fas fa-thumbs-up"></i> Strengths</h4>
      <p>${comprehensiveFeedback.strengths}</p>
    </div>`;
  }

  if (comprehensiveFeedback.areas_for_improvement) {
    feedback += `<div class="feedback-section-item">
      <h4><i class="fas fa-arrow-up"></i> Areas for Improvement</h4>
      <p>${comprehensiveFeedback.areas_for_improvement}</p>
    </div>`;
  }

  if (
    comprehensiveFeedback.key_recommendations &&
    comprehensiveFeedback.key_recommendations.length > 0
  ) {
    feedback += `<div class="feedback-section-item">
      <h4><i class="fas fa-lightbulb"></i> Key Recommendations</h4>
      <ul class="recommendations-list">
        ${comprehensiveFeedback.key_recommendations
          .map((rec) => `<li>${rec}</li>`)
          .join("")}
      </ul>
    </div>`;
  }

  // Add individual analysis if available
  const areas = [
    "information_gathering",
    "diagnostic_accuracy",
    "cognitive_bias_awareness",
  ];
  areas.forEach((area) => {
    const analysis = evaluation[area]?.analysis;
    if (analysis) {
      const title = area
        .replace(/_/g, " ")
        .replace(/\b\w/g, (l) => l.toUpperCase());
      feedback += `<div class="feedback-section-item">
        <h4><i class="fas fa-info-circle"></i> ${title}</h4>
        <p class="analysis-text">${analysis}</p>
      </div>`;
    }
  });

  return feedback || "<p>No detailed feedback available.</p>";
}

function renderRecommendations(recommendations) {
  if (Array.isArray(recommendations)) {
    return `<ul class="recommendations-list">
      ${recommendations.map((rec) => `<li>${rec}</li>`).join("")}
    </ul>`;
  } else if (typeof recommendations === "string") {
    return `<p>${recommendations}</p>`;
  } else {
    return "<p>No specific recommendations available.</p>";
  }
}

function generateImprovementAdvice(evaluation) {
  const advice = [];

  // Check information gathering score
  const infoScore = evaluation.information_gathering?.score || 0;
  if (infoScore < 30) {
    advice.push(
      "🔍 <strong>Information Gathering:</strong> Limited clinical information was gathered. Focus on systematic history taking and physical examination."
    );
  } else if (infoScore < 60) {
    advice.push(
      "📋 <strong>Information Gathering:</strong> Moderate clinical information was collected. Consider exploring additional relevant areas."
    );
  } else {
    advice.push(
      "🔍 <strong>Information Gathering:</strong> Good systematic approach to clinical information discovery."
    );
  }

  // Check diagnostic accuracy
  const diagScore = evaluation.diagnostic_accuracy?.score || 0;
  if (diagScore < 50) {
    advice.push(
      "🎯 <strong>Diagnostic Accuracy:</strong> Consider strengthening diagnostic reasoning and differential diagnosis skills."
    );
  } else if (diagScore < 80) {
    advice.push(
      "🎯 <strong>Diagnostic Accuracy:</strong> Reasonable diagnostic approach with room for improvement in precision."
    );
  } else {
    advice.push(
      "🎯 <strong>Diagnostic Accuracy:</strong> Strong diagnostic reasoning and clinical accuracy demonstrated."
    );
  }

  // Check cognitive bias awareness
  const biasScore = evaluation.cognitive_bias_awareness?.score || 0;
  if (biasScore < 50) {
    advice.push(
      "🧠 <strong>Cognitive Bias Awareness:</strong> Metacognitive reflection needs significant improvement. Focus on thoughtful self-analysis."
    );
  } else if (biasScore < 70) {
    advice.push(
      "🧠 <strong>Cognitive Bias Awareness:</strong> Developing awareness of cognitive biases. Continue practicing reflective thinking."
    );
  } else {
    advice.push(
      "🧠 <strong>Cognitive Bias Awareness:</strong> Good metacognitive reflection and bias awareness demonstrated."
    );
  }

  return advice;
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
