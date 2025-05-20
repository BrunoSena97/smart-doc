**Project Documentation: SmartDoc - Virtual Patient Simulation for Medical Education**

- **Project Title:** SmartDoc
- **Version:** 0.1 (Initial Working Prototype with SBERT NLU)
- **Date:** May 20, 2025
- **Overall Thesis Goal:** To develop and evaluate an AI-powered system (SmartDoc) to simulate clinical scenarios, primarily for first-year medical specialization students. The system aims to assess and provide feedback on cognitive biases during medical interviews and promote metacognitive skills, leveraging Natural Language Processing and potentially Large Language Models (LLMs).

---

**I. Current Project Status & Achievements (as of Version 0.1)**

- **Functional Command-Line Prototype:** A Python-based prototype capable of simulating a turn-based clinical interview via a command-line interface (e.g., Git Bash) has been successfully developed and tested.
- **Modular Architecture:** The system is built with distinct, interacting modules for knowledge management, natural language understanding, dialogue management, and logging.
- **Semantic NLU Implemented:** Natural Language Understanding (NLU) leverages the Sentence Transformers (SBERT) library to understand student queries based on semantic similarity to a predefined set of canonical questions, inspired by approaches like OSCEBot[cite: 2, 3]. This allows for more flexible query interpretation than simple keyword spotting.
- **Structured Knowledge Base:** A detailed clinical case ("Elderly Woman with 'Heart Failure'" from Mull_DiagnosticError.pdf, now `case01.json`) has been formalized into a structured JSON format. The `KnowledgeBaseManager` can load and serve this information.
- **Dialogue Flow Management:** A Finite State Machine (FSM) defined in `DialogueState` guides the basic flow of the clinical interview (e.g., Introduction, HPI, PMH, Investigations). The `DialogueManager` implements this FSM.
- **Discoverable Information Mechanism:** The system can withhold and later reveal critical "discoverable" pieces of information based on student queries that semantically match triggers for these items.
- **Interaction Logging:** A `SystemLogger` is in place to record conversation turns, NLU outputs, and dialogue states for debugging and future analysis.
- **Canonical Question Mapping:** A comprehensive list of `canonical_question_mappings` has been created, linking natural language questions to specific data points in the knowledge base or system actions. This list is central to the SBERT-based NLU.

---

**II. Current System Capabilities (Version 0.1)**

- **Simulate Clinical Interview:** The system can engage in a text-based dialogue, playing the role of a Virtual Standardized Patient (VSP) whose information is provided by a family member (the son in `case01.json`).
- **Understand Student Queries Semantically:** Using SBERT, the system can interpret a variety of student phrasings and map them to the most relevant piece of information or VSP action.
- **Provide Case-Specific Information:** Responds to queries by fetching relevant data from the `case01.json` knowledge base (e.g., patient history, symptoms, initial lab/exam findings).
- **Manage Dialogue Flow:** Transitions through predefined stages of a clinical interview (Introduction, HPI, PMH, etc.).
- **Reveal Critical Findings:** If the student asks questions that semantically align with triggers for "discoverable" information (e.g., Infliximab use, Echo results), the system can provide this information.
- **Handle Basic Misunderstandings:** If a student's query does not achieve a sufficient similarity score with any canonical question, the VSP can ask the student to rephrase.
- **Log Interactions:** All turns of the conversation, along with NLU confidence and dialogue state, are logged for review.

---

**III. Module Breakdown (Version 0.1)**

1.  **`case01.json` (Knowledge Base Content):**
    - **Purpose:** Stores all data for the specific clinical scenario.
    - **Key Content:** Patient profile, initial presentation (HPI, meds, exam, labs, imaging), discoverable information (with triggers), cognitive bias examples, metacognitive prompts.
2.  **`dialogue_fsm_data.py` (NLU Mapping Data):**
    - **Purpose:** Stores the `canonical_question_mappings` list.
    - **Key Content:** A list of dictionaries, where each entry maps `canonical_question`(s) (and `variations`) to an `id`, `action_type` (e.g., `Workspace_from_kb`, `trigger_discoverable`), and `target_details` (for `KnowledgeBaseManager` or `DialogueManager` actions). This data drives the SBERT NLU.
3.  **`dialogue_state.py` (FSM Definitions):**
    - **Purpose:** Defines the explicit states of the clinical interview's Finite State Machine.
    - **Key Content:** `DialogueState` class with constants like `INTRODUCTION`, `HPI_GATHERING`, `INVESTIGATIONS_QUERY`, `CLOSING`, etc.
4.  **`knowledge_base_manager.py` (`KnowledgeBaseManager` class):**
    - **Purpose:** Loads, manages, and provides structured access to `case01.json`.
    - **Key Functionalities:** Loads JSON at initialization; provides getter methods for specific data points (e.g., `get_chief_complaints()`, `get_specific_lab_result_initial()`, `get_discoverable_item_details()`). Abstracts the raw JSON structure from other modules.
5.  **`nlu_service.py` (`NLUService` class):**
    - **Purpose:** Processes student's free-text input to determine intent and target information using SBERT.
    - **Key Functionalities:** Loads a pre-trained SBERT model; pre-computes embeddings for all canonical questions (from `dialogue_fsm_data.py`); compares student query embedding against canonical embeddings using cosine similarity; returns a structured output (intent ID, action type, target details, score) if similarity exceeds a cutoff, or an "intent_not_understood" otherwise.
6.  **`dialogue_manager.py` (`DialogueManager` class):**
    - **Purpose:** The "brain" of the VSP; manages conversation flow, state transitions, response generation, and logic for revealing information.
    - **Key Functionalities:** Maintains current dialogue state (FSM); processes NLU output; uses `action_type` to interact with `KnowledgeBaseManager` or trigger scripted responses; implements logic for revealing discoverable items (currently basic, needs refinement); determines next dialogue state.
7.  **`system_logger.py` (`SystemLogger` class):**
    - **Purpose:** Logs interactions to a file for debugging, testing, and future analysis.
    - **Key Functionalities:** Initializes a log file; provides a method to log student input, VSP response, timestamp, current dialogue state, and NLU output details (intent, score).
8.  **`main.py` (Main Application Script):**
    - **Purpose:** Orchestrates the system, initializes modules, and runs the command-line user interaction loop.
    - **Key Functionalities:** Sets up all services; takes student input; passes input to NLU; passes NLU output to DM; prints VSP response; calls logger; handles session exit.

---

**IV. Planned Immediate Next Steps (Prototype Refinement - Phase 2B)**

The current working prototype is a strong foundation. The immediate next steps focus on refining its core functionalities before layering on the more complex cognitive evaluation features:

1.  **NLU Robustness & SBERT Performance Tuning:**
    - Systematically test and optimize the SBERT similarity `cutoff_value`.
    - Expand and refine `canonical_question_mappings` (add more `variations`, ensure clarity of canonical questions) based on test conversations and log analysis to improve match accuracy.
    - Improve handling of truly out-of-scope or ambiguous questions beyond a simple "I don't understand."
2.  **Dialogue Management (DM) Enhancements:**
    - Develop comprehensive state transition logic in the `DialogueManager` for all defined `DialogueState`s, ensuring smooth and logical progression through the interview.
    - Refine and make more robust the logic for revealing "discoverable" information, potentially incorporating multi-step reveals or checks based on conversation history (e.g., student has to ask a follow-up after an initial evasive answer).
    - Explore adding simple contextual memory to the DM (e.g., remembering the last entity discussed) to handle simple follow-up clarifications more naturally.
3.  **Interaction Flow & Basic Usability Testing:**
    - Conduct thorough self-testing by role-playing as a student through the entire `case01.json` scenario.
    - Recruit 1-2 peers (fellow students) for informal usability testing, observe their interactions, and gather feedback on clarity, ease of use, and perceived naturalness.
    - Use logs to identify common points of failure, confusion, or awkward interactions.
4.  **Introduction of Basic Metacognitive Prompts:**
    - Integrate 1-2 simple, pre-defined metacognitive prompts (from the list in `case01.json`, e.g., "What else can this be?") to be triggered by the `DialogueManager` at specific, logical points in the conversation (e.g., after initial data gathering is complete). This is a preliminary step towards the full metacognition goal.

---

**V. Long-Term Goal: Cognitive Bias & Metacognition Module Integration**

The ultimate aim of the "SmartDoc" thesis project is to evaluate cognitive biases and provide metacognitive support. The refined prototype (after Phase 2B) will serve as the platform for this.

**A. Vision for Cognitive Bias Evaluation & Metacognitive Support:**

- **Bias Identification:** The system aims to identify patterns in student interaction that may suggest the influence of common cognitive biases (e.g., anchoring, confirmation bias, premature closure). This would be based on the sequence of questions asked, information ignored, timing of queries relative to information revealed, and potentially direct articulations of thought if prompted.
- **Metacognitive Prompting:** Beyond simple pre-defined prompts, the system will aim to provide tailored metacognitive questions or feedback to encourage students to reflect on their diagnostic process, consider alternatives, and identify potential flaws in their reasoning.
- **Feedback Mechanism:** Provide students with insights into their decision-making process, highlighting moments where biases might have played a role or where metacognitive reflection could have been beneficial. This could be a post-simulation report initially.

**B. Plan for Integrating Cognitive Bias & Metacognition Modules:**

1.  **Prerequisite: Rich Data Collection & Feature Engineering (from refined prototype logs):**

    - The detailed logs from the refined prototype (Phase 2B) are crucial. These logs (student query, NLU intent/score, DM state, VSP response, timestamps, revealed info) will be the primary data source.
    - **Feature Engineering:** Identify specific features from the logs that could indicate biases. Examples:
      - _Anchoring:_ Student repeatedly asks questions related to an initial (possibly incorrect) hypothesis, even after conflicting data is presented.
      - _Confirmation Bias:_ Student primarily seeks data confirming their working hypothesis and neglects questions that might refute it.
      - _Premature Closure:_ Student attempts to conclude the interview or offer a diagnosis very early, before sufficient data (especially discoverable items) has been gathered.
      - Ratio of questions about confirming vs. disconfirming evidence.
      - Sequence of information access.

2.  **Bias Detection Module(s) - Iterative Approach:**

    - **Initial Rule-Based Heuristics:** Start by implementing rules based on known patterns from the literature and the specific `case01.json` scenario. For example: "IF student asks <3 questions about alternative diagnoses after initial data suggests 'heart failure' AND Pro-BNP is high AND CXR suggests congestion, THEN flag potential anchoring."
    - **Machine Learning / LLM Integration (Thesis Core):**
      - **Supervised Learning (if data can be annotated):** If you can collect and annotate a dataset of student interactions (labeling segments with potential biases), you could train a classifier.
      - **LLM for Transcript Analysis:** Use an LLM (e.g., fine-tuned or with sophisticated prompting) to analyze the full dialogue transcript (from logs) or segments of it. The LLM could be asked to:
        - Identify if the student's questioning pattern aligns with known definitions of specific cognitive biases.
        - Assess if the student adequately explored critical information paths.
        - Determine if the student responded appropriately to new (especially conflicting) information.
      - This LLM module would take the interaction log as input and output a "bias score" or a qualitative assessment.

3.  **Metacognitive Prompting & Feedback Generation Module:**

    - **Dynamic Prompt Generation:** Based on the output of the Bias Detection Module, an LLM could be used to generate more context-specific and nuanced metacognitive prompts in real-time (advanced) or for a post-simulation report.
      - _Example:_ If potential anchoring is detected, instead of a generic "What else?", the LLM could help craft: "You've gathered strong evidence for X. Given that the patient also presented with Y (which is less typical for X), what other possibilities might explain the full picture?"
    - **Feedback Report:** Develop a module to synthesize findings (from bias detection, information gathered, etc.) into a structured feedback report for the student post-simulation.

4.  **Integration with `DialogueManager`:**
    - The `DialogueManager` might need to be enhanced to:
      - Send interaction data to the Bias Detection Module periodically or at the end of the session.
      - Receive signals or flags from the Bias Detection Module.
      - Trigger specific metacognitive prompts (either pre-defined or dynamically generated by the Feedback Generation Module) at appropriate times based on these signals or pre-defined triggers in the FSM.

---

**VI. Evolution Towards Thesis Goals**

This phased approach, starting with a robust rule-based VSP (now enhanced with SBERT NLU) and iteratively improving it, directly supports the core thesis objectives. The refined prototype will:

- Provide a reliable platform for collecting high-quality student interaction data.
- Serve as a baseline against which LLM-driven enhancements (for NLU, DM, bias detection, or feedback) can be compared and evaluated.
- Allow for the systematic and controlled introduction of LLM components into specific modules, making the development and evaluation process more manageable.
