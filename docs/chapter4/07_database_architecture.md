# 4.2.4 Database Architecture and State Management

To support both responsive simulation and robust research analytics, SmartDoc adopts a dual-layer state management architecture:

1. **In-memory session state** — ensures real-time responsiveness during the learner's interaction with the virtual patient
2. **Persistent database storage** — captures full reasoning traces, bias events, and reflection data for subsequent analysis

This separation allows the system to deliver immediate educational feedback while also creating durable records for evaluation and research.

## Conceptual Schema

The underlying schema is organized around educational workflows rather than technical implementation details. Key entities represent the pedagogical concepts central to diagnostic reasoning education:

**Core Entities:**

- **Users** — learners and administrators with role-based access control
- **Conversations** — the main unit of analysis, representing complete diagnostic sessions
- **Messages** — full history of learner queries and system responses with classified intents
- **SimulationSessions** — metadata about the diagnostic case, status, and performance statistics
- **DiscoveryEvents** — when and how clinical information was revealed, operationalizing progressive disclosure
- **BiasWarnings** — logged instances of anchoring, confirmation, or premature closure detection
- **DiagnosisSubmissions** — final diagnostic hypotheses with reasoning and evaluation scores
- **ReflectionResponses** — learner answers to structured metacognitive prompts
- **AuditLogs** — comprehensive system event logging for reproducibility and security

**Figure 4.X: Conceptual Database Schema**

```
┌──────────────┐
│    Users     │
│──────────────│
│ id (PK)      │
│ email        │
│ role         │
└──────┬───────┘
       │
       │ 1:N
       │
┌──────▼────────────┐        ┌──────────────────┐
│  Conversations    │◄───────┤    Messages      │
│───────────────────│  1:N   │──────────────────│
│ id (PK)           │        │ id (PK)          │
│ user_id (FK)      │        │ conversation_id  │
│ title             │        │ role             │
│ created_at        │        │ content          │
└──────┬────────────┘        │ context          │
       │                     │ meta (JSON)      │
       │ 1:1                 │ created_at       │
       │                     └──────────────────┘
┌──────▼──────────────────┐
│  SimulationSessions     │
│─────────────────────────│
│ id (PK)                 │
│ conversation_id (FK)    │
│ case_id                 │
│ status                  │
│ stats (JSON)            │
│ created_at, ended_at    │
└──────┬──────────────────┘
       │
       ├──────► DiscoveryEvents (1:N)
       │        ├─ category, label, value
       │        ├─ block_id, confidence
       │        └─ created_at
       │
       ├──────► BiasWarnings (1:N)
       │        ├─ bias_type
       │        ├─ description
       │        └─ created_at
       │
       └──────► DiagnosisSubmissions (1:N)
                ├─ diagnosis_text
                ├─ score_overall, score_breakdown
                ├─ feedback (text)
                └─┬─ created_at
                  │
                  └──► ReflectionResponses (1:N)
                       ├─ question, answer
                       └─ created_at
```

This design ensures that each learner session produces a rich, analyzable dataset that links behavior (intents, queries, revealed information) with outcomes (diagnosis accuracy, bias awareness, metacognitive reflection quality).

## State Management Architecture

During an active simulation, the **Progressive Disclosure Store** maintains session-level state in memory:

```python
class SessionState:
    session_id: str
    case_id: str
    current_phase: DiagnosticPhase  # anamnesis, exam, labs
    revealed_blocks: Set[str]        # IDs of disclosed information
    query_history: List[Query]       # All student queries
    working_hypothesis: Optional[str]  # Current diagnostic focus
    bias_warnings_triggered: List[BiasWarning]
    start_time: datetime
```

This in-memory state enables rapid decision-making during interactions (milliseconds, not database query latency). However, key pedagogical events trigger immediate database writes through event hooks:

```python
@on_reveal
def handle_information_revealed(block: InformationBlock):
    update_session_state(block)
    log_to_database(
        event="discovery",
        category=block.category,
        label=block.label,
        value=block.content,
        block_id=block.id,
        timestamp=now()
    )

@on_bias_detected
def handle_bias_detected(bias_type: str, description: str):
    issue_warning(bias_type)
    log_to_database(
        event="bias_warning",
        bias_type=bias_type,
        description=description,
        timestamp=now()
    )
```

This event-driven design ensures that cognitive bias detection (Chapter 2) and reflection prompts are not only experienced by the learner but also captured for empirical study (addressing gaps identified in Chapter 3).

## Choice of Database Technology

For research purposes, **portability and reproducibility** were prioritized over scalability. SQLite was selected because it:

- **Allows easy sharing** of complete simulation datasets for replication studies (single-file database)
- **Eliminates external dependencies** for participants in multi-site trials
- **Guarantees data integrity** even during abrupt session terminations (ACID compliance)
- **Simplifies deployment** — no separate database server required
- **Ensures reproducibility** — exact database state can be versioned and shared

Although SQLite does not support massive concurrency, SmartDoc's use case involves individual or small-cohort learning sessions, making this a pragmatic and effective choice. The abstraction layer (SQLAlchemy) ensures that the system can migrate to enterprise-grade databases (PostgreSQL, MySQL) if future large-scale deployments require it.

## Logging and Reproducibility

SmartDoc implements structured logging for both technical and pedagogical events. For each session, the following are captured:

**Interaction Traces:**

- Learner queries with exact timestamps
- Classified intents with confidence scores and explanations
- Information blocks revealed with revelation sequences
- Response content from each responder module

**Pedagogical Events:**

- Discovery events organized by category (presenting_symptoms, physical_examination, diagnostic_results, current_medications, imaging)
- Bias warnings with type, timing, and contextual triggers
- Reflection prompt presentations and student responses
- Diagnosis submissions with complete evaluation breakdowns

**Technical Metrics:**

- LLM inference times and token counts
- Classification confidence distributions
- Fallback mechanism activations
- Error occurrences and recovery strategies

These logs create a **complete reasoning trace**, enabling:

1. **Formative feedback** — personalized debriefs showing learners their questioning patterns, revealed information sequence, and bias-prone moments

2. **Summative evaluation** — objective assessment of diagnostic accuracy, information gathering thoroughness, and bias awareness

3. **Research analytics** — large-scale studies of interaction patterns, identification of common reasoning errors, and evaluation of pedagogical interventions

By embedding reproducibility at the data layer, SmartDoc ensures that each learning session doubles as a research opportunity. This addresses the call in Chapter 3 for more transparent and empirically grounded evaluation of AI-powered virtual patients.

## Example: Reasoning Trace from Real Session

The following excerpt demonstrates the richness of captured data from Session SESS_0W451OZEJ:

```json
{
  "session_id": "SESS_0W451OZEJ",
  "case_id": "mull_case",
  "conversation_id": 8,
  "created_at": "2025-10-13T22:47:43Z",

  "messages": [
    {
      "id": 153,
      "role": "user",
      "content": "First, what is her past medical history?",
      "context": "anamnesis",
      "meta": {
        "intent_id": "pmh_general",
        "intent_confidence": 0.95,
        "intent_explanation": "The doctor is asking about past medical history..."
      },
      "created_at": "2025-10-13T22:47:52Z"
    },
    {
      "id": 154,
      "role": "assistant",
      "content": "Uh, she has a history of morbid obesity, diabetes, hypertension, and rheumatoid arthritis.",
      "context": "anamnesis",
      "created_at": "2025-10-13T22:47:52Z"
    }
  ],

  "discoveries": [
    {
      "id": 57,
      "category": "presenting_symptoms",
      "label": "Past Medical History",
      "value": "Morbid obesity, diabetes, hypertension, rheumatoid arthritis",
      "confidence": 0.95,
      "block_id": "pmh_comorbidities",
      "created_at": "2025-10-13T22:47:52Z"
    }
  ],

  "bias_warnings": [
    {
      "id": 3,
      "bias_type": "anchoring",
      "description": "Focus on cardiac hypothesis after chest X-ray interpretation",
      "created_at": "2025-10-13T22:53:42Z"
    }
  ],

  "diagnosis_submissions": [
    {
      "id": 9,
      "diagnosis_text": "miliary tuberculosis",
      "score_overall": 81,
      "score_breakdown": {
        "information_gathering": 75,
        "diagnostic_accuracy": 88,
        "cognitive_bias_awareness": 80
      },
      "feedback": "Correct diagnosis, avoided heart failure trap...",
      "created_at": "2025-10-13T23:08:40Z"
    }
  ],

  "statistics": {
    "total_messages": 34,
    "total_discoveries": 18,
    "total_bias_warnings": 1,
    "discoveries_by_category": {
      "presenting_symptoms": 6,
      "current_medications": 3,
      "physical_examination": 3,
      "imaging": 3,
      "diagnostic_results": 3
    },
    "session_duration_minutes": 20.7
  }
}
```

This structured capture enables both immediate educational use (student review, instructor feedback) and downstream research analysis (pattern mining, intervention effectiveness studies).

## Data Privacy and Security Considerations

Although SmartDoc is a research prototype, data protection principles were embedded from initial design:

**Access Control:**

- Role-based authentication (students, instructors, administrators)
- Session isolation — learners access only their own data
- Instructor dashboards with aggregated analytics

**Data Minimization:**

- No personally identifiable medical information
- Simulated cases only (no real patient data)
- Optional anonymization for research datasets

**Audit Trails:**

- All data access logged with timestamps and user IDs
- Administrative actions (user creation, data export) fully traced
- Modification history preserved for critical records

**Local Storage:**

- All data stored locally, no external transmission
- LLM processing entirely local (Ollama), no cloud API calls
- Database backups encrypted at rest

These safeguards align with educational research ethics requirements and demonstrate that pedagogical innovation need not compromise learner privacy.
