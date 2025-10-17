# 4.1.3 Case Modeling: Intent-Driven Simulation

SmartDoc introduces a novel approach to clinical case design that embeds educational triggers and bias detection directly into the case structure itself. This intent-driven simulation model represents a significant innovation in medical education technology, moving beyond traditional linear case presentations to create dynamic, conversational learning experiences.

## Case Schema Architecture

Each SmartDoc case is defined using a structured schema that integrates progressive disclosure, bias triggers, and educational metadata directly into the case content. This ensures that diagnostic reasoning, bias awareness, and metacognition are not peripheral features but are embedded in the simulation itself.

A case definition includes four core elements:

1. **Initial Presentation** — chief complaint, basic demographic information, and contextual framing (e.g., "elderly woman with worsening dyspnea").

2. **Information Blocks** — modular clinical facts (history, examination, investigations, medications), progressively revealed through learner queries. Each block is annotated with disclosure metadata.

3. **Bias Triggers** — metadata defining when and how anchoring, confirmation, or framing biases are likely to occur, along with corrective prompts.

4. **Educational Notes** — learning objectives, clinical pearls, and structured reflection questions linked to key diagnostic moments.

Example case structure:

```json
{
  "caseId": "mull_case",
  "caseTitle": "An elderly woman with dyspnea",
  "initialPresentation": {
    "chiefComplaint": "Worsening shortness of breath",
    "historyProvider": "Son (patient is Spanish-speaking)",
    "contextualFrame": "History of 'heart failure'"
  },
  "informationBlocks": [...],
  "biasTriggers": {...},
  "educationalNotes": {...}
}
```

By embedding these components into a single schema, SmartDoc avoids the limitations of scripted, branching cases. Instead, the case itself defines when information is revealed, where bias prompts are activated, and how reflection is scaffolded.

## Information Blocks and Progressive Disclosure

Information is stored in modular **information blocks**, each annotated with structured metadata that governs its revelation:

- **blockId** — unique identifier (e.g., `critical_infliximab`, `imaging_cxr_preliminary`)
- **blockType** — category (e.g., Medications, Imaging, Labs, History)
- **content** — the actual clinical information to be revealed
- **level** — depth of inquiry required (1 = basic, 2 = detailed, 3 = comprehensive)
- **intentTriggers** — array of intent IDs that can reveal this block
- **prerequisites** — blocks that must be revealed first
- **isCritical** — boolean flag for diagnostically essential information
- **revealPolicy** — revelation strategy (`immediate`, `escalate`, `conditional`)

Example information block:

```json
{
  "blockId": "critical_infliximab",
  "blockType": "Medications",
  "content": "Records from previous hospitalizations reveal the patient has been receiving infliximab for rheumatoid arthritis for the past 3-4 months.",
  "isCritical": true,
  "intentTriggers": ["meds_full_reconciliation_query"],
  "level": 2,
  "prerequisites": ["meds_ra_uncertainty"],
  "revealPolicy": "escalate"
}
```

In this example, the infliximab information (critical for diagnosing miliary tuberculosis) is revealed only after learners probe medication history in detail and specifically request previous hospital records. This design resists **premature closure** by requiring persistence and systematic inquiry.

### Progressive Disclosure in Practice

Information revelation follows a structured ladder of inquiry depth:

- **Level 1**: Basic data disclosed with minimal inquiry (e.g., vital signs, chief complaint, known medications)
- **Level 2**: Detailed information requiring specific follow-up questions (e.g., medication reconciliation, imaging studies)
- **Level 3**: Comprehensive data requiring expert-level probing (e.g., detailed medication history from external records)

This mechanism operationalizes:

- **Anchoring bias** — learners who accept surface-level data (e.g., elevated BNP) without deeper investigation risk missing contradictory findings.
- **Premature closure** — learners who fail to escalate inquiries miss critical diagnostic clues.
- **Framing bias** — the initial presentation label influences which information blocks learners pursue.

## Intent-Block Mapping Architecture

Each information block can be revealed through multiple intent pathways, enabling flexible yet pedagogically meaningful interactions. SmartDoc employs two mapping strategies:

### Direct Block Mapping

Used when semantic specificity in questioning should be rewarded. The learner's precise phrasing determines which information is revealed:

- `meds_ra_specific_initial_query` → `meds_ra_uncertainty`
- `meds_full_reconciliation_query` → `critical_infliximab`
- `imaging_echo` → `critical_echo`

This design rewards targeted clinical inquiry over generic questioning.

### Group-Based Escalation

Used when repeated probing of the same domain should progressively reveal more detail:

- First labs inquiry → `labs_general` (CBC, basic chemistry)
- Second labs inquiry → `labs_cardiac` (BNP, troponin)
- Third labs inquiry → `labs_specialized` (additional markers)

### Design Rationale

The choice between direct mapping and group escalation is pedagogically motivated. For medication history, SmartDoc intentionally uses **direct block mapping** rather than pure escalation counting. This rewards semantic precision in questioning ("Can you get her complete medication list from previous hospitalizations?") rather than mere repetition of generic queries.

Example from production data:

1. "Any regular medication?" → reveals basic list (lisinopril, atenolol, glipizide, metformin)
2. "Medications for rheumatoid arthritis?" → reveals uncertainty block ("I'm not sure about her RA medications")
3. "Can you get her complete medication list from previous hospitalizations?" → reveals infliximab

This mapping strategy operationalizes the distinction between surface-level and deep clinical reasoning, directly addressing the pedagogical goals outlined in Chapter 2.

## Educational Scaffolding Within Progressive Disclosure

Beyond simple information gating, SmartDoc implements dynamic educational hints when learners exhibit signs of being stuck. This addresses a key limitation of purely discovery-based learning: learners may become frustrated when unable to progress, but providing direct answers undermines the learning experience.

### Example: Medication Reconciliation Scaffolding

When a learner repeatedly asks about rheumatoid arthritis medications without progressing to full reconciliation:

1. **First query** (`meds_ra_specific_initial_query`):
   → "I'm not sure about her rheumatoid arthritis medications, I'm sorry."

2. **Second identical query**:
   → "Like I said, I'm not sure. Maybe you could check her previous hospital records? I know she's had some treatments at other facilities."

This just-in-time guidance models expert clinical reasoning (consulting external records for medication history) without revealing the answer directly. The hint emerges naturally from the virtual patient's dialogue, maintaining immersion while providing pedagogical scaffolding.

This dynamic scaffolding mechanism was developed iteratively through production testing with medical students and addresses findings from Chapter 3 regarding the need for adaptive support in AI-powered learning environments.

## Embedded Bias Triggers

Bias triggers are encoded directly in case metadata, allowing real-time monitoring of learner reasoning patterns. Each trigger specifies:

- The **anchor information** that may mislead learners,
- The **contradictory evidence** that should prompt reconsideration,
- The **bias type** being demonstrated,
- The **intervention prompt** to encourage metacognition.

Example bias trigger (anchoring):

```json
"biasTriggers": {
  "anchoring": {
    "anchorInfoId": "imaging_cxr_preliminary",
    "contradictoryInfoId": "critical_echo",
    "description": "Anchoring on preliminary chest X-ray interpretation ('pulmonary vascular congestion') delays recognition of normal echocardiogram, leading to incorrect heart failure diagnosis.",
    "interventionPrompt": "You seem focused on a cardiac explanation. What else could explain dyspnea with this pattern?"
  }
}
```

### Bias Detection Logic

The system monitors learner behavior patterns and triggers warnings based on configurable thresholds:

```
IF recent_queries.focus_on("cardiac|heart|failure") > 70%
AND contradictory_echo_revealed
AND hypothesis_unchanged
THEN trigger_bias_warning("anchoring")
     prompt_reflection("What else could explain these findings?")
```

This transforms abstract debiasing strategies (e.g., cognitive forcing, described in Chapter 2) into concrete, in-the-moment educational interventions.

## Educational Notes and Reflection Support

Each case embeds learning objectives, clinical pearls, and structured reflection prompts that guide post-diagnosis review:

```json
"educationalNotes": {
  "learningPoints": [
    "Medication reconciliation is crucial in patients with multimorbidity",
    "TNF-alpha inhibitors substantially increase tuberculosis reactivation risk",
    "Normal echocardiogram effectively rules out heart failure as primary etiology"
  ],
  "clinicalPearls": [
    "Miliary pattern on chest CT: innumerable 1-2mm nodules",
    "Always verify medication history from multiple sources"
  ],
  "biasAwareness": [
    "Anchoring on initial 'heart failure' framing delays alternative diagnoses",
    "Confirmation bias: seeking cardiac evidence while ignoring pulmonary clues"
  ]
}
```

At diagnostic closure, learners are presented with structured reflection prompts:

- What evidence supports your diagnosis?
- What evidence contradicts it?
- What alternative explanations remain plausible?
- What was the single most compelling piece of evidence?
- What biases might have influenced your reasoning?

This operationalizes **deliberate reflection** (Chapter 2) and ensures that metacognition is not optional but embedded in the workflow.

## Application: The Mull Case

The prototype case adapts Mull et al.'s published case of diagnostic error, in which an elderly woman with dyspnea was repeatedly misdiagnosed with heart failure due to cognitive biases. SmartDoc encodes this case by:

- **Framing** the initial presentation as "elderly patient with history of heart failure",
- **Embedding anchoring triggers** around chest X-ray interpretation and elevated BNP,
- **Requiring medication reconciliation** to reveal immunosuppressant use,
- **Providing contradictory evidence** through normal echocardiogram,
- **Revealing critical findings** only through persistent, specific questioning.

This case demonstrates how SmartDoc transforms published case reports of diagnostic error into interactive learning experiences that make cognitive bias tangible and addressable.

## Innovation Summary

The intent-driven case design provides several key innovations:

1. **Conversational learning** — natural dialogue replaces scripted question trees, enabling authentic clinical inquiry.
2. **Embedded bias education** — bias triggers built into case metadata enable real-time detection and intervention.
3. **Progressive disclosure** — learners earn critical clues by resisting bias-prone shortcuts and pursuing systematic investigation.
4. **Dynamic scaffolding** — educational hints emerge when learners are stuck, maintaining challenge without causing frustration.
5. **Research-ready design** — interaction logs capture complete reasoning traces for empirical analysis.

In this way, SmartDoc transforms case-based learning from passive fact recall to active, bias-aware clinical reasoning practice, directly addressing gaps identified in both the cognitive psychology literature (Chapter 2) and AI-powered virtual patient research (Chapter 3).
