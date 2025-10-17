# 4.2 Part II: Technical Implementation

This section presents the technical implementation of SmartDoc. While Part I focused on the architectural principles and modular design, this section details how the components were executed in practice, including runtime configuration, large language model integration, database architecture, deployment configuration, and production refinements.

## 4.2.1 Overview and Execution Pipeline

The SmartDoc pipeline follows a sequence of phases that mirror the cognitive processes of a clinical encounter. Each phase is encapsulated in a dedicated module, enabling independent testing and future extension.

### System Startup and Configuration

Upon initialization, the system loads:

- **Case definitions** from structured JSON files (symptoms, information blocks, bias triggers)
- **Intent taxonomy** with descriptions, examples, and context availability rules
- **LLM provider configuration** (model selection, temperature settings, timeout thresholds)
- **Database connection** for persistent storage of sessions and reasoning traces

### Request Processing Flow

When a learner submits a query (e.g., "What are the patient's vital signs?"), the system processes it through six sequential phases:

**1. Query Initiation and Routing**

The system captures both the input text and its context (session ID, current diagnostic phase, previously revealed information). The request is passed to the Intent-Driven Disclosure Manager, the central orchestrator.

**2. Intent Classification**

The system determines what the learner is trying to accomplish. This operationalizes **System 1 pattern recognition** (rapid, intuitive categorization) while maintaining hooks for **System 2 monitoring** (deliberate oversight of the reasoning process).

The classification pipeline:

- Filters intents by current diagnostic phase (context awareness)
- Submits query + available intents to LLM with structured prompt
- Receives classification with confidence score and explanation
- Falls back to keyword matching if LLM classification fails

Low-confidence classifications trigger clarification requests rather than potentially incorrect information disclosure.

**3. Discovery Processing**

Once the intent is identified, the Discovery Processor determines what information to reveal:

```
identified_intent = "exam_cardiovascular"
↓
mapped_blocks = get_blocks_triggered_by(intent)
↓
eligible_blocks = filter_by_prerequisites(mapped_blocks, revealed_history)
↓
reveal(eligible_blocks)
```

This implements **progressive disclosure**, ensuring students must actively seek evidence rather than receive it passively. Prerequisites enforce logical clinical sequencing (e.g., cannot order CT scan before obtaining history).

**4. Response Generation**

Contextually appropriate responses are generated based on the diagnostic phase:

- **Anamnesis phase**: `AnamnesisSonResponder` generates family member dialogue, modeling uncertainty ("I think...", "I'm not sure...") and using simplified medical terminology.

- **Physical examination**: `ExamObjectiveResponder` provides descriptive clinical findings using standardized medical language.

- **Investigations**: `LabsResidentResponder` delivers laboratory or imaging results in professional format, with direct responses for unavailable tests.

When no information exists for a classified intent (WITH_DATA = false), responders generate appropriate fallback responses that maintain immersion without revealing that the information doesn't exist in the case.

**5. Bias Detection and Session Logging**

In parallel with response generation, the Bias Analyzer monitors interaction patterns:

```python
if focus_on_single_hypothesis > 70%:
    trigger_bias_warning("anchoring")
    prompt = "You seem focused on a single diagnosis. What else could explain these findings?"
    log_bias_event(type="anchoring", timestamp=now(), prompt=prompt)
```

Detected events are logged with full context, creating a traceable record for both real-time intervention and post-session analysis.

**6. Assembly and Delivery**

The system compiles:

- The virtual patient's response (dialogue or results)
- Newly revealed information (clinical facts added to student's knowledge)
- Any bias warnings or metacognitive prompts
- Progress indicators (% of case completed, critical findings status)

This complete package is returned to the learner's interface and persisted to the database.

### Handling of Uncertainty and Edge Cases

The pipeline includes multiple safeguards for unexpected situations:

**Ambiguous Queries**: When intent classification confidence falls below threshold (0.3), the system requests clarification rather than making potentially incorrect assumptions.

**Unavailable Information**: When a classified intent has no corresponding information blocks, responders generate contextually appropriate responses (e.g., "That test hasn't been performed at this time").

**LLM Failures**: When LLM inference fails (timeout, parsing error), the system falls back to keyword-based intent matching and deterministic response templates, ensuring educational functionality is maintained.

**Session Interruptions**: All state changes are immediately persisted to the database, allowing sessions to be resumed even after abrupt termination.

This modular execution pipeline ensures controlled information flow (supporting debiasing strategies), authentic immersion, and reproducibility—directly addressing pedagogical requirements and gaps identified in Chapter 3.

## Algorithm 1: Intent-Driven Progressive Disclosure

The core algorithm that orchestrates information revelation:

```
Input: user_query, session_context, revealed_blocks
Output: information_blocks, educational_hints, bias_warnings

1:  diagnostic_phase ← session_context.current_phase
2:  available_intents ← filter_intents_by_phase(diagnostic_phase)
3:
4:  classification ← LLM_classify(user_query, available_intents)
5:  if classification.confidence < 0.3 then
6:      return request_clarification(query, available_intents)
7:  end if
8:
9:  intent ← classification.intent_id
10: mapped_blocks ← get_intent_block_mappings(intent, case)
11: eligible_blocks ← filter_by_prerequisites(mapped_blocks, revealed_blocks)
12:
13: // Educational scaffolding logic
14: if intent == "meds_ra_specific_initial_query" then
15:     query_count ← count_previous_queries(intent, session)
16:     if query_count > 1 AND "critical_infliximab" NOT revealed then
17:         hint ← "Maybe you could check her previous hospital records?"
18:         return (eligible_blocks, hint, None)
19:     end if
20: end if
21:
22: // Bias detection logic
23: hypothesis_focus ← calculate_focus(revealed_blocks, working_diagnosis)
24: if hypothesis_focus > 0.70 then
25:     contradictory ← detect_contradictions(revealed_blocks, working_diagnosis)
26:     if contradictory exists then
27:         warning ← create_bias_warning("anchoring")
28:         prompt ← "What else could explain these findings?"
29:         return (eligible_blocks, None, (warning, prompt))
30:     end if
31: end if
32:
33: return (eligible_blocks, None, None)
```

This algorithm integrates intent classification, progressive disclosure, educational scaffolding, and bias detection into a unified decision process that executes on every learner query.

## Algorithm 2: Bias Detection and Warning System

The bias monitoring algorithm that runs continuously during diagnostic sessions:

```
Input: session_history, current_hypothesis, revealed_information
Output: bias_warning or None

1:  recent_queries ← get_last_n_queries(session_history, n=5)
2:  hypothesis_mentions ← count_hypothesis_keywords(recent_queries, current_hypothesis)
3:  total_mentions ← count_total_keywords(recent_queries)
4:  focus_ratio ← hypothesis_mentions / total_mentions
5:
6:  // Anchoring bias detection
7:  if focus_ratio > 0.70 then
8:      contradictory_info ← detect_contradictions(revealed_information, current_hypothesis)
9:      if contradictory_info is not empty then
10:         log_bias_event(type="anchoring", evidence=contradictory_info)
11:         prompt ← "You seem focused on " + current_hypothesis + ". What else could explain these findings?"
12:         return BiasWarning(type="anchoring", prompt=prompt, severity="moderate")
13:     end if
14: end if
15:
16: // Confirmation bias detection
17: supporting_queries ← count_queries_seeking_confirmation(recent_queries, current_hypothesis)
18: refuting_queries ← count_queries_seeking_refutation(recent_queries, current_hypothesis)
19: if supporting_queries > 0 AND refuting_queries == 0 then
20:     if length(recent_queries) >= 4 then
21:         log_bias_event(type="confirmation", pattern="seeking only supporting evidence")
22:         prompt ← "Consider evidence that might contradict your working diagnosis"
23:         return BiasWarning(type="confirmation", prompt=prompt, severity="low")
24:     end if
25: end if
26:
27: // Premature closure detection
28: critical_blocks ← get_critical_blocks(case)
29: revealed_critical ← filter_revealed(critical_blocks, revealed_information)
30: if length(revealed_critical) < 0.6 * length(critical_blocks) then
31:     if diagnosis_submitted then
32:         log_bias_event(type="premature_closure", coverage=length(revealed_critical))
33:         // Note: warning after diagnosis, used in evaluation
34:         return BiasWarning(type="premature_closure", prompt=None, severity="high")
35:     end if
36: end if
37:
38: return None
```

This algorithm operationalizes the bias taxonomy from Chapter 2 into computational detection rules, enabling real-time identification of bias-prone reasoning patterns.
