# 4.2.6 User Interfaces

SmartDoc's user-facing components translate the technical architecture into accessible, pedagogically effective interfaces. The design philosophy prioritizes **cognitive focus** over visual complexity—students should concentrate on clinical reasoning rather than navigating complex software. This section describes the two primary interfaces: the simulation environment for students and the administrative dashboard for educators.

## 4.2.6.1 Simulation Interface

The simulation interface presents as a single-page web application accessible through any modern browser. The design deliberately avoids medical record system mimicry, instead providing a clean, distraction-free environment that foregrounds diagnostic thinking.

### Layout and Core Components

**Three-Panel Organization:**

1. **Patient Information Panel** (left, 25% width)

   - Case title and chief complaint
   - Basic demographics and presenting context
   - Always visible for quick reference
   - Styled as a persistent sidebar

2. **Interaction Panel** (center, 50% width)

   - Chat-based conversation with the patient's son
   - Scrollable conversation history with visual distinction between student queries (right-aligned, blue) and system responses (left-aligned, gray)
   - Input field with suggestion buttons for common query types ("Ask about medications", "Request vital signs", "Order imaging")
   - Real-time typing indicators during LLM processing

3. **Discovery Panel** (right, 25% width)
   - Running list of revealed information organized by category
   - Visual indicators for critical findings (amber icon) and contradictory evidence (purple icon)
   - Bias warnings appear here as persistent cards
   - Collapsible sections to manage information density

### Tabbed Investigation Views

Below the main conversation panel, three tabs organize different types of clinical information:

**Anamnesis Tab**

- History of present illness
- Past medical history
- Current medications
- Social history
- Review of systems

Each piece of information appears only after the student asks the relevant question, with timestamps showing when it was revealed.

**Physical Examination Tab**

- Vital signs
- General appearance
- System-by-system examination findings

Examination findings populate dynamically based on student requests, mirroring real clinical workflow where you see only what you examine.

**Diagnostic Results Tab**

- Laboratory values
- Imaging reports
- Special tests (echocardiogram, etc.)

Results appear in chronological order of request, not grouped by type, reinforcing the temporal nature of diagnostic investigation.

### Bias Warning Display

When the bias detection system identifies a concerning pattern, a **bias warning card** appears in the Discovery Panel with the following structure:

```
⚠️ COGNITIVE BIAS DETECTED

Type: Anchoring Bias

Pattern: You have focused heavily on the cardiac hypothesis
after the initial chest X-ray interpretation suggested
pulmonary vascular congestion. Consider whether you are
giving sufficient weight to contradictory evidence (e.g.,
normal cardiac examination) or alternative explanations
for the patient's symptoms.

Recommendation: Before proceeding, explicitly list
evidence that DOES NOT support your current leading
diagnosis.
```

The warning remains visible but non-blocking—students can continue investigating without dismissing it. This design choice reflects the pedagogical goal of making bias awareness metacognitively salient without punishing learners or creating frustration.

### Diagnosis Submission Interface

When the student feels ready to conclude the case, clicking "Submit Diagnosis" reveals a structured form with five metacognitive prompts:

1. **What is your diagnosis?**
   Free text, allowing students to express diagnostic certainty or uncertainty naturally.

2. **What evidence most strongly supports your diagnosis?**
   Forces explicit articulation of reasoning, preventing "gut feeling" diagnoses.

3. **What evidence argues against your diagnosis?**
   Prompts consideration of contradictory data, engaging System 2 deliberation.

4. **What alternative diagnoses did you consider?**
   Assesses differential diagnosis breadth and systematic thinking.

5. **How would you rule in or rule out these alternatives?**
   Evaluates understanding of diagnostic test characteristics and clinical decision-making.

Upon submission, the interface transitions to the evaluation results view (described below).

## 4.2.6.2 Evaluation Results Interface

After diagnosis submission, students receive comprehensive feedback organized into three sections:

### Overall Performance Summary

A prominent score display shows:

- **Overall Score:** Large number (e.g., 81/100) with color coding (red <60, yellow 60-79, green ≥80)
- **Dimensional Breakdown:** Three sub-scores for Information Gathering, Diagnostic Accuracy, and Cognitive Bias Awareness
- **Performance Tier:** Text label (e.g., "Strong Performance", "Needs Improvement")

### Detailed Evaluation

**Strengths Section:**

- Bulleted list of specific things the student did well
- Quotes from their reflection responses highlighting good reasoning
- Recognition of correct diagnostic conclusions or systematic approaches

**Areas for Improvement:**

- Specific, actionable feedback on what to do differently
- Identification of missed critical findings
- Analysis of bias patterns observed in the session

**Key Recommendations:**

- 1-2 concrete strategies for future cases
- Emphasis on generalizable skills (e.g., "Implement structured medication reconciliation") rather than case-specific facts

### Session Summary Statistics

A data table showing:

- Total interactions: 17
- Information blocks revealed: 18
- Critical findings discovered: 2/2 (100%)
- Bias warnings triggered: 1
- Session duration: 18 minutes
- Average response time: <2 seconds

This quantitative summary helps students understand their investigation pattern and efficiency.

## 4.2.6.3 Administrative Dashboard

The administrative interface provides educators and researchers with comprehensive system management capabilities. Access is restricted via authentication (simple password protection in the research prototype, designed for easy extension to institutional SSO). The dashboard is organized into six primary functional areas.

### Database Backup and Management

**Database Download:**

- One-click download of complete SQLite database file
- Includes all user sessions, conversations, diagnoses, and evaluations
- Enables offline analysis and data archival
- Critical for research data preservation and institutional backup policies

This backup capability ensures that research data remains accessible even if the hosted instance becomes unavailable, supporting reproducibility requirements for academic research.

### System Configuration

**Bias Warning and Discovery Counter Visibility:**

A critical feature for research studies is the ability to control the visibility of metacognitive scaffolding elements:

- **Hide Bias Warnings:** Checkbox to suppress real-time cognitive bias alerts
- **Hide Discovery Counters:** Checkbox to conceal information revelation tracking

**Implementation:**

```html
<input type="checkbox" id="hide-bias-warnings" /> Hide Bias Warnings (for
research studies)
```

When enabled, the configuration is stored server-side via `/api/v1/config` endpoint and retrieved by the simulation interface on load. The frontend then:

1. Hides all elements with class `bias-related` (discovery counters, bias warning cards)
2. Prevents bias warning popups from appearing
3. Logs all suppressed warnings to browser console for debugging
4. Continues recording bias events in the database for analysis

**Research Rationale:**
This feature enables controlled experiments comparing diagnostic performance with and without metacognitive scaffolding. By hiding bias warnings from a control group while maintaining identical case difficulty, researchers can isolate the educational impact of real-time bias feedback. All bias events remain logged in the database regardless of visibility, ensuring complete data collection for both experimental conditions.

### Users Management

**User Creation:**

- Form-based user registration with required fields:
  - Display name and email
  - Age and sex (for demographic analysis)
  - Role (user/admin)
  - Medical experience level (student, resident, attending)
  - Label/cohort identifier (e.g., "pilot", "cohort-2024")
- Automatic generation of unique access code for authentication
- Access code displayed once immediately after creation

**User Administration:**

- Table view showing all registered users with:
  - User ID, name, email, and role
  - Account status (active/inactive)
  - Usage statistics (number of sessions completed)
  - Creation timestamp
- Actions: View details, deactivate/reactivate, delete user
- Sortable and filterable by any column

**Purpose:**
This management interface supports both educational deployment (creating student accounts) and research administration (organizing participants into cohorts, tracking completion rates).

### LLM Profile Configuration

**Profile Creation:**

- Define multiple LLM configurations for different use cases
- Configuration parameters:
  - Profile name (e.g., "Default GPT-4", "Research Gemma")
  - Provider selection (Ollama, OpenAI, Anthropic)
  - Model specification (e.g., "gemma3:4b-it-q4_K_M")
  - Temperature (0.0-2.0, controlling response creativity)
  - Top-p sampling parameter (0.0-1.0)
  - Max tokens (optional response length limit)
  - Default profile designation

**Profile Management:**

- Table view showing all configured LLM profiles
- Displays: ID, name, provider, model, temperature, top-p settings
- Indicates which profile is currently default
- Actions: Edit parameters, set as default, delete profile

**Use Cases:**

- **Production:** Stable, tested model configuration
- **Experimentation:** Testing new models or parameter combinations
- **A/B Testing:** Comparing different LLM configurations with identical prompts
- **Cost Optimization:** Switching between local (Ollama) and cloud providers

### Agent Prompt Management

**Prompt Creation:**

- Select agent type (Son/Patient Translator, Resident/Medical Assistant, Exam/Objective Findings)
- Associate with specific LLM profile or leave as "Default/Any"
- Text area for complete system prompt definition
- Automatic versioning of prompt iterations

**Prompt Administration:**

- Table view showing all agent prompts with:
  - Prompt ID and agent type
  - Associated LLM profile
  - Version number (automatically incremented)
  - Status (active/inactive)
  - Creation and last update timestamps
- Actions: View full prompt text, edit, activate/deactivate, delete

**Prompt Viewer Modal:**

- Detailed view displaying:
  - Agent type, LLM profile, version, status
  - Complete prompt text with syntax highlighting
  - Creation and update history
- Enables comparison between prompt versions for iterative refinement

**Research Application:**
This feature enables systematic evaluation of different prompt engineering strategies. Researchers can test how variations in agent instructions affect response quality, maintaining version control of all prompt iterations used in published studies.

### Recent Activity Log

**Activity Monitoring:**

- Chronological table of recent administrative actions
- Logged events include:
  - User creation, modification, deletion
  - LLM profile configuration changes
  - Agent prompt updates
  - System configuration modifications
- Each entry shows:
  - Timestamp of action
  - Administrator user who performed action
  - Action type and description
  - Relevant details (e.g., which user was modified)

**Purpose:**
Provides audit trail for research governance, troubleshooting system issues, and understanding usage patterns. Critical for institutional review board (IRB) compliance and research reproducibility documentation.

## 4.2.6.4 Design Rationale

### Minimalist Aesthetic

SmartDoc deliberately avoids elaborate graphics, animations, or complex navigation. This **cognitive minimalism** reflects educational research showing that extraneous visual elements can increase cognitive load and distract from learning objectives (Mayer's Coherence Principle, multimedia learning research).

**Design Choices:**

- White background with subtle gray panels
- Single clear font (system default sans-serif)
- Minimal color use (blue for user, gray for system, amber/purple for warnings)
- No background images or decorative elements

### Conversation-Centric Interaction

The chat-based interface mirrors familiar messaging applications, reducing the cognitive cost of learning to use the system. Students focus on **what to ask** rather than **how to ask it**, aligning with the pedagogical goal of improving clinical reasoning rather than software proficiency.

**Affordances:**

- Natural language input (no rigid command syntax)
- Suggestion buttons for common queries (scaffolding for novices)
- Persistent conversation history (supports System 2 reflection)
- Real-time feedback (maintains immersion)

### Transparent Discovery Tracking

Unlike traditional case simulations where students might wonder "did I miss something?", SmartDoc's Discovery Panel provides immediate feedback about information revelation. This transparency serves two educational purposes:

1. **Reduces anxiety:** Students know when they've discovered new information
2. **Encourages persistence:** Visual accumulation of discoveries rewards thorough investigation

The design makes **what you know** and **what you still need to learn** explicit, supporting metacognitive monitoring.

### Non-Punitive Bias Warnings

The bias warning system could have been designed to penalize students (e.g., score deductions) or block progression (e.g., forced acknowledgment). Instead, warnings appear as **informational advisories** that remain visible but non-blocking.

**Rationale:**

- Bias awareness is developmental—students need multiple exposures to recognize patterns
- Punishment could discourage hypothesis formation (reducing bias by eliminating thinking)
- Persistent visibility allows students to reflect on warnings after the fact

This design reflects a **formative assessment philosophy** where mistakes are learning opportunities rather than failures to be avoided.

### Structured Reflection Prompts

The five-question diagnosis submission form operationalizes metacognitive reflection without requiring students to understand cognitive psychology theory. Each prompt targets a specific aspect of diagnostic reasoning:

- **Question 1** (diagnosis): Decision-making
- **Question 2** (supporting evidence): Evidence integration
- **Question 3** (contradictory evidence): Bias awareness
- **Question 4** (alternatives): Differential diagnosis
- **Question 5** (ruling in/out): Diagnostic strategy

This structure ensures students engage System 2 deliberation regardless of their natural reflective tendency, addressing the problem that unreflective practitioners often don't know they need to reflect.

## 4.2.6.5 Implementation Details

### Frontend Technology

The simulation interface is implemented as a **static single-page application** using vanilla JavaScript (ES6 modules), HTML5, and CSS3. This architecture choice prioritizes:

- **Simplicity:** No build step or framework dependencies
- **Portability:** Runs on any web server (including `python -m http.server`)
- **Transparency:** Source code is human-readable for educational inspection
- **Performance:** Minimal bundle size, fast load times

**Module Organization:**

```
js/
├── config.js          # API endpoint configuration
├── api.js             # Backend communication layer
├── state.js           # Application state management
├── main.js            # Initialization and routing
└── ui/
    ├── chat.js        # Conversation interface
    ├── patient-info.js # Case presentation panel
    ├── discoveries.js  # Information tracking panel
    ├── results.js      # Evaluation display
    └── tabs.js         # Anamnesis/Exam/Labs tabs
```

### Responsive Design

The interface adapts to different screen sizes:

- **Desktop (≥1200px):** Three-panel layout as described
- **Tablet (768-1199px):** Two-panel layout with collapsible patient info
- **Mobile (<768px):** Single-panel stacked layout with tab navigation

This responsiveness supports both classroom use (desktop monitors) and remote learning (laptops, tablets).

### Accessibility Considerations

While not the primary focus of the research prototype, basic accessibility features include:

- Semantic HTML (proper heading hierarchy, ARIA labels)
- Keyboard navigation support (tab order, enter to submit)
- High-contrast text (WCAG AA compliance)
- Screen reader compatibility for core content

Future production deployment would require comprehensive accessibility audit and remediation to meet institutional standards.

---

The user interface design reflects SmartDoc's core pedagogical philosophy: **make cognitive processes visible, support metacognitive reflection, and minimize extraneous cognitive load**. These principles translate technical capability into educational impact, completing the bridge between AI-powered backend systems and meaningful learning experiences for medical students.
