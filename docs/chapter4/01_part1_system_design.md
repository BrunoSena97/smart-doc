# 4.1 Part I: System Design

This first part presents the architectural principles and conceptual design of SmartDoc.

## 4.1.1 Overview

The SmartDoc system was inspired directly by the principles of progressive disclosure and metacognitive scaffolding outlined in Chapter 2. The system adopts a modular, rule-guided approach aligned with large language model capabilities. Unlike traditional virtual patients that follow predetermined branching scripts, SmartDoc enables free-form clinical inquiry while maintaining pedagogical control through intent-driven information revelation.

The platform implements three core pedagogical principles:

1. **Authenticity** — Realistic patient interactions through conversational interfaces that mimic genuine anamnesis, physical examination, and investigation ordering, bridging the theory-practice gap identified in Chapter 3.

2. **Bias Awareness** — Real-time detection of reasoning patterns associated with anchoring, confirmation bias, or premature closure, with targeted interventions that encourage reflection without disrupting immersion.

3. **Structured Reflection** — Embedded metacognitive checkpoints that support deliberate reflection and consolidation of diagnostic reasoning skills, operationalizing the debiasing strategies discussed in Chapter 2.

The architecture separates responsibilities into distinct layers:

- **Domain logic** — the reasoning engine and pedagogical rules that govern information disclosure and bias detection.
- **API layer** — orchestrating communication, state management, and coordination between modules.
- **Presentation layer** — the learner-facing interface for interacting with the virtual patient and receiving feedback.

At the core of the system lies the **Intent-Driven Disclosure Manager**, which orchestrates three essential processes:

1. **Understanding learner input** via an LLM-powered Intent Classifier that maps natural language queries to clinical intents,
2. **Controlling information flow** through a Discovery Processor that releases case data incrementally based on query specificity,
3. **Monitoring reasoning patterns** through a Bias Analyzer that detects bias-prone behaviors in real time and triggers metacognitive prompts.

This architecture ensures that the simulation reflects authentic diagnostic practice (as emphasized in Chapter 3) while embedding cognitive safeguards to mitigate common reasoning errors (Chapter 2). The modular design allows independent testing and validation of each component, addressing reproducibility concerns raised in the literature review.

## 4.1.2 Core Components

SmartDoc's architecture comprises seven interrelated modules, each responsible for a specific aspect of the educational simulation.

### Intent Classifier

Learner utterances are mapped to a predefined taxonomy of 33 diagnostic intents (e.g., `pmh_general`, `exam_cardiovascular`, `imaging_chest_xray`, `meds_ra_specific_initial_query`). Rather than relying on rigid question trees or template matching, SmartDoc leverages natural language classification through an LLM, allowing students to phrase queries naturally. The classifier is context-aware, filtering available intents based on the current diagnostic phase (anamnesis, examination, or investigations), which improves accuracy and reduces ambiguity.

This module operationalizes **System 1 pattern recognition** while maintaining pathways for **System 2 monitoring**, as learners can freely explore hypotheses while the system tracks their reasoning trajectory.

### Discovery Processor

Clinical information is released progressively, linked directly to learner queries and their classified intents. Information is organized into modular **information blocks**, each representing a discrete clinical fact (e.g., vital signs, medication history, laboratory results). Blocks are annotated with metadata including:

- **Level** — depth of inquiry required (Level 1 = basic, Level 2+ = detailed follow-up),
- **Prerequisites** — other blocks that must be revealed first,
- **Critical flag** — whether the information is essential for correct diagnosis,
- **Intent triggers** — which clinical intents reveal this block.

This implements the principle of **progressive disclosure**, ensuring that data emerges as a result of active inquiry rather than passive reception. The design aligns with constructivist learning theory, promoting deep engagement over rote information consumption.

### Simulation Engine

The Simulation Engine orchestrates the entire learning loop, coordinating between all other modules:

> Student query → Intent classified → Discovery processing → Bias analysis → Response generation → Feedback assembly

It integrates reasoning traces with pedagogical scaffolds, ensuring each interaction is both educationally meaningful and technically coherent. The engine maintains session state, tracks revealed information, monitors hypothesis focus, and determines when educational interventions (hints, bias warnings, reflection prompts) should be deployed.

### Bias Analyzer

Bias detection is achieved through a combination of rule-based heuristics and LLM-based reasoning analysis. The module is directly grounded in the bias taxonomy presented in Section 2.2.2, with detection mechanisms for:

- **Anchoring bias** — persistence on initial hypotheses despite contradictory evidence,
- **Confirmation bias** — selective pursuit of supporting evidence while ignoring refuting information,
- **Premature closure** — stopping investigation too early before adequate data gathering.

Detection triggers are parameterized with thresholds calibrated during pilot testing. For example:

> IF hypothesis_focus > 70% on single diagnosis
> AND contradictory_evidence revealed
> THEN trigger anchoring_warning("What else could explain these findings?")

This transforms abstract debiasing strategies into actionable, in-the-moment coaching that guides learners toward more systematic reasoning without revealing the diagnosis.

### Clinical Evaluator

SmartDoc employs a simplified, single-LLM evaluation architecture that assesses diagnostic performance across three dimensions:

1. **Information gathering** — thoroughness of history-taking, appropriate test ordering, recognition of critical findings,
2. **Diagnostic accuracy** — correctness of final diagnosis, quality of differential reasoning, integration of evidence,
3. **Cognitive bias awareness** — quality of metacognitive reflection, recognition of bias-prone moments, mitigation strategies employed.

Unlike earlier multi-agent approaches that proved unreliable, this streamlined evaluator uses structured prompts with explicit scoring rubrics. It includes quality detection mechanisms that identify inadequate responses (nonsense answers, minimal effort) and assign appropriately low scores, ensuring fairness and educational validity.

### Response Generation System

Contextually appropriate responses are generated through specialized **responder modules** that adapt language and information density to the current diagnostic phase:

- **AnamnesisSonResponder** — simulates family member dialogue with uncertainty modeling ("I think...", "I'm not sure..."), uses simplified medical terminology, and includes educational hints when learners exhibit signs of being stuck.

- **LabsResidentResponder** — delivers investigation results in professional medical language, provides direct responses for unavailable tests without unnecessary verbosity.

- **ExamObjectiveResponder** — reports physical examination findings with clinical precision and standardized terminology.

This multi-responder architecture maintains immersion while ensuring pedagogically appropriate information delivery at each phase.

### Session Management

All interactions are logged with high-resolution timestamps, creating comprehensive **reasoning traces** that capture:

- Learner queries with classified intents and confidence scores,
- Information blocks revealed and their revelation sequence,
- Bias warnings triggered and their timing,
- Reflection responses to metacognitive prompts,
- Diagnosis submissions with evaluation scores and feedback.

This provides a complete record for both formative feedback (personalized debriefs) and summative assessment (diagnostic performance evaluation). The logs also enable empirical research on interaction patterns, addressing the call in Chapter 3 for more transparent evaluation of AI-powered educational systems.

Together, these components implement a learning cycle where action, feedback, and reflection are tightly coupled, addressing the shortcomings of both traditional scripted simulations and unguided clinical encounters.
