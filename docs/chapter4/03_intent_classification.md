# 4.1.4 Intent Classification System

The Intent Classifier is a foundational component of SmartDoc's architecture, responsible for translating natural language queries into structured clinical intents that drive information disclosure. Unlike template-matching or keyword-based systems, SmartDoc employs a hybrid LLM-powered approach that balances linguistic flexibility with reliability.

## Intent Taxonomy

SmartDoc employs a comprehensive taxonomy of 33 clinical intents organized across three diagnostic phases. This taxonomy was developed through analysis of clinical reasoning literature and iterative refinement during pilot testing.

**Table 4.1: Intent Categories by Diagnostic Phase**

| Phase                | Intent Category            | Example Intents                                                                                                        | Count |
| -------------------- | -------------------------- | ---------------------------------------------------------------------------------------------------------------------- | ----- |
| Anamnesis            | Past Medical History       | `pmh_general`, `pmh_family_history`, `pmh_surgical_history`                                                            | 3     |
| Anamnesis            | History of Present Illness | `hpi_chief_complaint`, `hpi_onset_duration_primary`, `hpi_fever`, `hpi_chills`, `hpi_chest_pain`, `hpi_weight_changes` | 9     |
| Anamnesis            | Medications                | `meds_current_known`, `meds_ra_specific_initial_query`, `meds_full_reconciliation_query`                               | 3     |
| Anamnesis            | Social History             | `social_smoking`, `social_alcohol`, `social_occupation`                                                                | 3     |
| Physical Examination | General Exam               | `exam_vital`, `exam_general_appearance`                                                                                | 2     |
| Physical Examination | System-Specific            | `exam_cardiovascular`, `exam_respiratory`                                                                              | 2     |
| Investigations       | Laboratory                 | `labs_general`, `labs_specific_cbc`, `labs_specific_bnp`                                                               | 5     |
| Investigations       | Imaging                    | `imaging_chest_xray`, `imaging_ct_chest`, `imaging_echo`                                                               | 6     |

Each intent is defined with:

- **Intent ID** — unique identifier used for mapping to information blocks
- **Description** — semantic definition of what the intent represents
- **Examples** — sample queries that should trigger this intent
- **Negative examples** — queries that should NOT trigger this intent
- **Context availability** — which diagnostic phases permit this intent

This structured taxonomy enables both accurate classification and systematic case design.

## Classification Pipeline

The intent classification process follows a multi-stage pipeline designed to maximize accuracy while maintaining responsiveness:

### Stage 1: Context Filtering

Before classification begins, the system determines which intents are currently available based on the diagnostic phase:

- **Anamnesis phase** → only history, medication, and social intents available
- **Examination phase** → only physical examination intents available
- **Investigations phase** → only laboratory and imaging intents available

This context-aware filtering reduces ambiguity and improves accuracy by constraining the classification space. For example, the query "vital signs" during anamnesis would be rejected, prompting the learner to transition to the examination phase.

### Stage 2: LLM-Based Classification

The filtered set of intents is passed to an LLM with a structured prompt that includes:

- The learner's query
- The current diagnostic context
- Definitions and examples for each available intent
- Instructions to return the most appropriate intent with confidence score

Example prompt structure:

```
You are a clinical reasoning assistant. Classify the following doctor's query into one of the available intents.

Context: anamnesis
Query: "What brings you here today?"

Available intents:
- pmh_general: Questions about past medical history, diseases, conditions, diagnoses. Does NOT include medications.
  Examples: "What is her medical history?", "Any chronic conditions?"

- hpi_chief_complaint: Questions about the main presenting complaint or reason for visit.
  Examples: "What brings you here?", "Why did you come to the clinic?"

Return: intent_id, confidence (0-1), explanation
```

The LLM returns structured output:

```json
{
  "intent_id": "hpi_chief_complaint",
  "confidence": 0.95,
  "explanation": "The doctor is asking what brings the patient to the clinic, which directly addresses the chief complaint within the anamnesis phase."
}
```

### Stage 3: Confidence Thresholding

Classification results are evaluated against a confidence threshold (default: 0.3):

- **High confidence (≥ 0.7)** — intent accepted, information disclosure proceeds
- **Medium confidence (0.3-0.7)** — intent accepted with caution, logged for review
- **Low confidence (< 0.3)** — classification rejected, system requests clarification

This threshold was calibrated through pilot testing to balance false positives (incorrect intent) against false negatives (missing valid queries).

### Stage 4: Keyword Fallback

If LLM classification fails (timeout, parsing error, low confidence) or returns unexpected results, the system employs keyword-based fallback matching:

```python
fallback_mappings = {
    "vital signs|vitals|temperature|blood pressure|heart rate": "exam_vital",
    "past medical history|medical history|chronic conditions": "pmh_general",
    "chest x-ray|chest xray|cxr": "imaging_chest_xray",
    "complete blood count|CBC|hemoglobin": "labs_specific_cbc",
    ...
}
```

This hybrid approach ensures reliability even when LLM inference is unavailable or produces invalid output.

## Intent Specificity and Semantic Precision

A key design principle of SmartDoc's intent taxonomy is rewarding **semantic precision** in clinical questioning. This is particularly evident in the medication intent hierarchy:

- `meds_current_known` — generic query about current medications
  → "Any regular medication?", "What does she take?"

- `meds_ra_specific_initial_query` — specific query about rheumatoid arthritis treatment
  → "Medications for rheumatoid arthritis?", "Any biologics?"

- `meds_full_reconciliation_query` — expert-level query for comprehensive medication review
  → "Can you get her complete medication list from previous hospitalizations?"

Each intent maps to progressively more detailed information blocks, operationalizing the concept that expert clinicians ask more targeted questions. This design resists the common educational pitfall of rewarding generic, unfocused inquiry.

## Production Refinements and Accuracy Improvements

The intent classification system underwent iterative refinement through production testing with medical students. Two significant issues were identified and resolved:

### Issue 1: PMH vs. Medications Confusion

**Initial observation**: The query "What is her past medical history?" was frequently misclassified as `meds_current_known` (confidence 0.95), despite medications being explicitly excluded from the PMH intent definition.

**Root cause**: Insufficient negative examples in intent descriptions, leading the LLM to conflate "medical history" with "everything about the patient."

**Solution**: Enhanced both intents with explicit examples and negative constraints:

```python
pmh_general: {
  "description": "Questions about past medical history, diseases, conditions, and diagnoses. Does NOT include medications.",
  "examples": [
    "What is her medical history?",
    "What is her past medical history?",
    "Any chronic conditions?",
    "What problems does she have?"
  ],
  "negative_examples": [
    "What medications does she take?" (→ meds_current_known)
  ]
}

meds_current_known: {
  "description": "Questions about current medications. Must explicitly mention 'medication', 'drug', 'pill', 'prescription' or similar terms. NOT for medical history or diagnoses.",
  "examples": [
    "Any regular medication?",
    "What drugs does she take?",
    "Is she on any prescriptions?"
  ],
  "negative_examples": [
    "What is her medical history?" (→ pmh_general)
  ]
}
```

**Result**: Classification accuracy for PMH queries improved from 57% to >95% in production testing.

### Issue 2: Context-Inappropriate Intent Acceptance

**Initial observation**: During physical examination, queries like "Any medications?" were being accepted and classified, causing confusion about diagnostic phase progression.

**Solution**: Implemented strict context filtering that rejects intents not available in the current phase, with explicit feedback:

> "That question is more appropriate for the history-taking phase. You are currently in the physical examination phase."

**Result**: Eliminated cross-phase classification errors and improved learner awareness of diagnostic workflow structure.

**Table 4.2: Intent Classification Accuracy Improvements**

| Configuration                   | PMH vs. Meds Accuracy | Cross-Phase Errors | Overall Accuracy |
| ------------------------------- | --------------------- | ------------------ | ---------------- |
| Baseline (generic descriptions) | 57%                   | 23%                | 78%              |
| Enhanced descriptions           | 95%                   | 18%                | 87%              |
| + Context filtering             | 95%                   | 0%                 | 96%              |

These improvements demonstrate the importance of iterative refinement based on actual learner interactions, a key finding that will inform the discussion of educational design in Chapter 5.

## Handling Ambiguity and Uncertainty

The classification system is designed to acknowledge and handle ambiguous queries rather than forcing inappropriate classifications:

### Clarification Requests

When confidence falls below threshold or multiple intents appear equally valid, the system requests clarification:

> "I'm not sure I understood your question. Are you asking about [interpretation A] or [interpretation B]?"

This models good clinical communication practice and prevents incorrect information disclosure.

### Intent Logging and Analysis

All classification decisions are logged with full context:

```json
{
  "query": "What is her past medical history?",
  "context": "anamnesis",
  "classified_intent": "pmh_general",
  "confidence": 0.95,
  "explanation": "...",
  "timestamp": "2025-10-13T22:47:52Z"
}
```

These logs enable:

1. **Quality assurance** — manual review of classification decisions
2. **System improvement** — identification of recurring misclassifications
3. **Educational research** — analysis of learner questioning patterns

This comprehensive logging addresses the call in Chapter 3 for more transparent and auditable AI-powered educational systems.

## Integration with Case Design

The intent taxonomy is tightly coupled with case design through the intent-block mapping system described in Section 4.1.3. Each information block specifies which intents can reveal it, creating a bidirectional relationship:

- **Case designers** specify which clinical questions should reveal each piece of information
- **The intent classifier** determines which clinical question the learner is asking
- **The discovery processor** matches classified intents to available blocks

This architecture enables case-specific pedagogical control while maintaining conversational flexibility, a key innovation of the SmartDoc platform.
