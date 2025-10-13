# Comprehensive Prompt Improvements Across All Contexts

**Date**: October 13, 2025
**Status**: ✅ Implemented and Tested
**Scope**: Anamnesis, Physical Exam, and Labs/Imaging Contexts

---

## Overview

Updated all context prompts and fallback handling to provide appropriate, context-specific responses for:

1. **Nonsense/unclear queries** - Proper acknowledgment of confusion
2. **Unavailable information** - Clear indication when information doesn't exist
3. **Context-appropriate personas** - Natural language tailored to each clinical context

## Changes by Context

### 1. Anamnesis (Patient's Son) - LLM-Powered

**File**: `/packages/core/src/smartdoc_core/simulation/prompts/patient_default.py`

**Approach**: **LLM-generated** responses for natural, in-character communication

**Updated Prompt**:

```python
persona = (
    "You are the English-speaking son of an elderly Spanish-speaking woman in the emergency department.\n"
    "You are translating for your mother who only speaks Spanish. You are concerned but trying to be helpful.\n"
    "You speak naturally to the doctor, providing information based on what you know about your mother's condition.\n"
    "Answer naturally without inventing new medical facts.\n\n"
    "IMPORTANT RULES:\n"
    "- If the question is nonsense or unclear: Say \"I'm not sure I can answer that particular question, I didn't understand.\"\n"
    "- If asked about information you don't have: Say \"I'm not sure I have information about that specifically.\"\n"
    "- Stay in character as a concerned but helpful son\n"
    "- Be natural and conversational\n"
    "- Use hesitation markers (\"Uh\", \"you know\") when appropriate"
)
```

**Example Responses**:

**Nonsense Query** ("blah blah nonsense?"):

> "Uh, sorry, Doctor. Mom… she didn't quite understand what you said about the 'blah blah nonsense.' I'm not sure I can answer that particular question, I didn't understand. Could you maybe… could you explain it a little differently?"

**Unavailable Information** ("What's her favorite color?"):

> "Uh, Doctor, I'm not sure I have information about that specifically. My… my mother, she doesn't really talk about favorite colors. It's… it's a little difficult to ask her, you know?"

**Benefits**:

- Natural, authentic conversation
- Maintains educational realism
- Appropriate hesitation and concern
- Context-aware and persona-consistent

---

### 2. Physical Exam (Objective Findings) - Simple Message

**File**: `/packages/core/src/smartdoc_core/simulation/responders/exam_objective.py`

**Approach**: **No LLM generation** - Direct objective findings or simple unavailable message

**Implementation**:

```python
def respond(self, *, intent_id: str, doctor_question: str, clinical_data: List[Dict], context: str) -> str:
    findings = []
    for data in clinical_data:
        content = data.get("content") or data.get("summary")
        if content:
            findings.append(content)

    if findings:
        return " ".join(findings)  # Direct objective findings
    else:
        return "That examination finding is not available in this case."  # Simple message
```

**Fallback Response**:

```python
def _generate_exam_fallback_response(self, intent_result: Dict, session) -> str:
    return "That examination finding is not available in this case."
```

**Example Responses**:

**Available Finding** ("Check vital signs"):

> "Vital signs: Temperature 99.9°F (37.7°C), HR 105, BP 140/70, RR 24, O2 sat 89% on room air."

**Unavailable Finding** ("Examine the patient's aura"):

> "That examination finding is not available in this case."

**Nonsense Query** ("asdfgh nonsense exam?"):

> "That examination finding is not available in this case."

**Benefits**:

- Objective and factual
- No unnecessary embellishment
- Fast response (no LLM latency)
- Clear and clinical

---

### 3. Labs/Imaging (Medical Resident) - LLM-Powered

**File**: `/packages/core/src/smartdoc_core/simulation/prompts/resident_default.py`

**Approach**: **LLM-generated** professional responses maintaining resident persona

**Updated Prompt**:

```python
persona = (
    "You are a medical resident working in the emergency department.\n"
    "You are professional, knowledgeable, and helpful. You can order tests, review results, and provide clinical information.\n"
    "You speak directly and professionally to the attending physician, providing clear medical information and recommendations.\n"
    "Be concise, professional, and factual. Do not make up names or refer to specific doctors by name.\n"
    "Present laboratory and imaging results objectively without adding fictional details.\n\n"
    "IMPORTANT RULES:\n"
    "- If the question is nonsense or unclear: Say \"I'm not sure I understand that question. Could you clarify what you're asking?\"\n"
    "- If asked about a test/imaging that cannot be obtained or doesn't exist: Say \"That test/imaging isn't available\" or \"We can't perform that examination\" (be professional and context-appropriate)\n"
    "- If asked about a test that hasn't been ordered yet: Offer to order it professionally\n"
    "- Stay professional and clinical in your language\n"
    "- Be direct and factual"
)
```

**Example Responses**:

**Available Test** ("What are the BNP results?"):

> "BNP is elevated at 1,250 pg/mL, which is significantly abnormal and suggests heart failure."

**Nonsense Query** ("xyz abc nonsense test?"):

> "I'm not sure I understand that question. Could you clarify what you're asking?"

**Unavailable Test** ("Can we get a PET scan?"):

> "That test isn't available. What other studies would you like me to order?"

**Benefits**:

- Professional medical language
- Maintains resident-attending dynamic
- Offers alternatives when appropriate
- Clear about limitations

---

## Implementation Details

### Context Configuration

Added `clarification` intent to all contexts:

```python
def _is_intent_valid_for_context(self, intent_id: str, context: str) -> bool:
    context_intents = {
        "anamnesis": [
            # ... history intents ...
            "clarification",  # Allow clarification in anamnesis
        ],
        "exam": [
            # ... exam intents ...
            "clarification",  # Allow clarification in exam
        ],
        "labs": [
            # ... labs intents ...
            "clarification",  # Allow clarification in labs
        ],
    }
    return intent_id in context_intents.get(context, [])
```

### Fallback Methods

**Anamnesis** - LLM-powered clarification:

```python
def _generate_clarification_response(self, intent_result: Dict, session) -> str:
    # Uses LLM with patient's son prompt
    # Returns natural, context-aware response
```

**Exam** - Simple message:

```python
def _generate_exam_fallback_response(self, intent_result: Dict, session) -> str:
    return "That examination finding is not available in this case."
```

**Labs** - LLM-powered professional response:

```python
def _generate_labs_fallback_response(self, intent_result: Dict, session) -> str:
    # Uses LLM with resident prompt
    # Returns professional, clinical response
```

---

## Design Rationale

### Why Different Approaches?

1. **Anamnesis (LLM)**:

   - Natural conversation is crucial for educational realism
   - Patient's son persona requires authentic hesitation and concern
   - Benefits from LLM's natural language understanding

2. **Exam (Simple)**:

   - Objective findings should be factual, not embellished
   - Fast response time important for examination workflow
   - Clear binary: finding exists or doesn't exist
   - No need for natural language generation

3. **Labs (LLM)**:
   - Professional medical communication expected
   - Can offer to order tests not yet available
   - Maintains resident-attending relationship
   - Benefits from contextual understanding

---

## Testing

**Test File**: `/dev-tools/test_all_contexts_fallback.py`

**Results**: ✅ All tests passing

```
ANAMNESIS CONTEXT:
✅ Nonsense query → LLM response with "didn't understand"
✅ Unavailable info → LLM response with "don't have information"

EXAM CONTEXT:
✅ Nonsense exam → "That examination finding is not available in this case"
✅ Non-existent finding → "That examination finding is not available in this case"

LABS CONTEXT:
✅ Nonsense test → LLM response with clarification request
✅ Unavailable test → LLM response (offers alternatives or states unavailable)
```

**Integration Tests**: ✅ All passing

- Medication escalation: 100% accuracy maintained
- No regression in existing functionality

---

## Benefits Summary

### Educational Value

1. **Authentic Simulation**: Each context feels realistic and appropriate
2. **Clear Boundaries**: Students understand information limitations
3. **Professional Standards**: Maintains clinical communication norms

### Technical Quality

1. **Context-Appropriate**: Right tool for each job (LLM vs simple message)
2. **Performance**: Fast for exam, rich for anamnesis/labs
3. **Maintainable**: Clear separation of concerns

### User Experience

1. **Natural Flow**: Conversations feel authentic
2. **Appropriate Feedback**: Clear when information unavailable
3. **Professional Communication**: Maintains clinical realism

---

## Files Modified

### Prompts

- `/packages/core/src/smartdoc_core/simulation/prompts/patient_default.py` - Added IMPORTANT RULES for anamnesis
- `/packages/core/src/smartdoc_core/simulation/prompts/resident_default.py` - Added IMPORTANT RULES for labs
- `/packages/core/src/smartdoc_core/simulation/prompts/exam_default.py` - Updated (though not actively used)

### Responders

- `/packages/core/src/smartdoc_core/simulation/responders/exam_objective.py` - Simplified to no LLM
- `/packages/core/src/smartdoc_core/simulation/responders/anamnesis_son.py` - No changes (already LLM-powered)
- `/packages/core/src/smartdoc_core/simulation/responders/labs_resident.py` - No changes (already LLM-powered)

### Engine

- `/packages/core/src/smartdoc_core/simulation/engine.py`:
  - Updated `_is_intent_valid_for_context()` to include clarification in all contexts
  - Updated `_generate_exam_fallback_response()` to simple message
  - Updated `_generate_labs_fallback_response()` to use LLM
  - `_generate_clarification_response()` already LLM-powered for anamnesis

### Testing

- `/dev-tools/test_all_contexts_fallback.py` - NEW comprehensive test across all contexts
- `/dev-tools/test_clarification_response.py` - Anamnesis-specific test

---

## Conclusion

The comprehensive prompt improvements provide:

- **Context-appropriate responses** tailored to each clinical scenario
- **Educational realism** maintaining authentic medical communication
- **Performance optimization** using LLM only where natural language adds value
- **Clear information boundaries** helping students understand case limitations

This three-pronged approach (LLM for anamnesis, simple for exam, LLM for labs) balances educational value, technical performance, and clinical authenticity.

---

**Related Documentation:**

- [LLM-Powered Clarification](./LLM_POWERED_CLARIFICATION.md) - Detailed anamnesis implementation
- [Intent Simplification and Storage](./INTENT_SIMPLIFICATION_AND_STORAGE.md) - Intent system improvements
- [Session Management](../development/session-management.md) - Session handling
- [Architecture Overview](../architecture/README.md) - System architecture
