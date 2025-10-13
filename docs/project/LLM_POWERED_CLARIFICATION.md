# LLM-Powered Clarification Responses

**Date**: October 13, 2025
**Status**: ✅ Implemented and Tested
**Context**: Anamnesis (Patient's Son Persona)

---

## Overview

Replaced hardcoded, progression-based clarification responses with LLM-generated natural responses that intelligently distinguish between nonsense queries and questions about unavailable information.

## Problem Statement

Previous implementation used revelation percentage to generate different hardcoded responses:

- < 30% revealed: "I'm not sure I have information about that specifically. Is there anything else..."
- 30-70% revealed: "I'm not sure I can answer that particular question. I've told you what I know..."
- > 70% revealed: "I don't think I have information about that..."

**Issues:**

1. Responses didn't distinguish between unclear/nonsense queries and legitimate questions about unavailable info
2. Revelation percentage-based responses felt mechanical
3. Didn't leverage LLM's natural language understanding

## Solution

### LLM-Powered Clarification Generation

**Location**: `/packages/core/src/smartdoc_core/simulation/engine.py`

```python
def _generate_clarification_response(self, intent_result: Dict, session) -> str:
    """
    Generate LLM-powered clarification response for anamnesis context.

    Uses the patient's son responder to generate natural responses that:
    - Acknowledge nonsense/unclear questions: "I'm not sure I can answer that particular question, I didn't understand."
    - Acknowledge unavailable information: "I'm not sure I have information about that specifically."
    """
    confidence = intent_result.get("confidence", 0)
    original_query = intent_result.get("original_input", "")

    # Use AnamnesisSonResponder to generate natural response
    responder = self.responders.get("anamnesis")
    if not responder:
        return "I'm not sure I can answer that particular question."

    # Build prompt for clarification with guidance
    clarification_guidance = """You need to respond to a question that you either:
1. Didn't understand (nonsense or unclear) → Say: "I'm not sure I can answer that particular question, I didn't understand."
2. Don't have information about → Say: "I'm not sure I have information about that specifically."

Be natural and stay in character as the patient's son."""

    prompt = f"""You are the English-speaking son of an elderly Spanish-speaking woman in the emergency department.
You are translating for your mother who only speaks Spanish. You are concerned but trying to be helpful.

The doctor just asked: "{original_query}"

{clarification_guidance}

Your response:"""

    try:
        response = self.provider.generate(prompt, temperature=0.3)
        return self._clean_response_text(response)
    except Exception as e:
        sys_logger.log_system("warning", f"LLM clarification generation failed: {e}")
        # Fallback based on confidence
        if confidence < 0.3:
            return "I'm not sure I can answer that particular question, I didn't understand."
        else:
            return "I'm not sure I have information about that specifically."
```

### Context Configuration

Added `clarification` intent to anamnesis valid intents list:

```python
def _is_intent_valid_for_context(self, intent_id: str, context: str) -> bool:
    """Check if an intent is valid for the given context."""
    context_intents = {
        "anamnesis": [
            # ... other intents ...
            "clarification",  # Allow clarification in anamnesis
        ],
        # ... other contexts ...
    }
    return intent_id in context_intents.get(context, [])
```

## Response Examples

### Nonsense Query

**Query**: "blah blah nonsense?"

**Response**:

> Uh, sorry, Doctor. My mom… she didn't quite understand what you said about the 'blah blah nonsense.' I'm not sure I can answer that particular question, I didn't understand. Could you maybe… could you explain it a little differently? Or perhaps in Spanish?

### Single Unclear Word

**Query**: "oi?"

**Response**:

> Uh, sorry, Doctor. I'm not sure I can answer that particular question, I didn't understand. My mom… she's a little confused right now. Could you maybe… could you speak a little slower, or perhaps ask it another way?

### Irrelevant Clinical Question

**Query**: "What's her favorite color?"

**Response**:

> Uh, Doctor, I'm not sure I have information about that specifically. My mother… she doesn't really talk about favorite colors. It's… it's a little difficult to ask her, you know?

### Non-Clinical Question

**Query**: "Tell me about her hobbies"

**Response**:

> Uh, Doctor, with all due respect, my mother… she doesn't really talk about her hobbies. It's… it's a little difficult to translate, but she mostly just focuses on getting better. I'm not sure I have information about that specifically.

## Key Features

### 1. Natural Language Understanding

- LLM distinguishes between nonsense and legitimate questions
- Stays in character as the patient's son
- Uses appropriate hesitation markers ("Uh", "you know")

### 2. Appropriate Response Patterns

- **Nonsense/Unclear**: "I'm not sure I can answer that particular question, I didn't understand."
- **Unavailable Info**: "I'm not sure I have information about that specifically."

### 3. Graceful Fallback

- If LLM fails, uses confidence-based hardcoded responses
- Low confidence (< 0.3): "didn't understand" response
- Higher confidence: "don't have information" response

### 4. Scope

- **Anamnesis only**: For patient's son persona where natural conversation is critical
- **Other contexts** (exam, labs): Continue using appropriate professional responses

## Testing

**Test File**: `/dev-tools/test_clarification_response.py`

**Results**: ✅ 4/4 tests passed

```
1. Nonsense query: ✅ Contains "didn't understand" pattern
2. Single unclear word: ✅ Contains "didn't understand" pattern
3. Irrelevant clinical question: ✅ Contains "don't have information" pattern
4. Non-clinical question: ✅ Contains "don't have information" pattern
```

**Integration Tests**: ✅ All passing

- Medication escalation: 100% accuracy maintained
- No regression in other functionality

## Benefits

### Educational Value

1. **Authentic Simulation**: Natural responses enhance realism
2. **No Information Leakage**: Doesn't reveal information categories
3. **Appropriate Guidance**: Distinguishes between confusion and unavailable data

### Technical Quality

1. **LLM-Powered**: Leverages natural language understanding
2. **Fallback Strategy**: Graceful degradation on LLM failure
3. **Context-Specific**: Only for anamnesis where naturalness matters most

### User Experience

1. **Natural Conversation**: Feels like talking to a real person
2. **Appropriate Confusion**: Acknowledges unclear questions naturally
3. **Helpful Feedback**: Implicit guidance through authentic responses

## Files Modified

### Core Changes

- `/packages/core/src/smartdoc_core/simulation/engine.py`
  - `_generate_clarification_response()`: LLM-powered generation
  - `_is_intent_valid_for_context()`: Added "clarification" to anamnesis

### Testing

- `/dev-tools/test_clarification_response.py`: NEW - Comprehensive clarification testing

## Future Considerations

### Potential Enhancements

1. **Exam Context**: Consider LLM-powered objective finding clarifications
2. **Labs Context**: LLM-powered resident responses for unavailable tests
3. **Context Memory**: Use session history to inform clarification tone
4. **Multiple Languages**: Leverage LLM for multilingual clarification

### Monitoring

- Track clarification response quality in production
- Collect examples of edge cases for prompt refinement
- Monitor LLM generation latency and fallback frequency

## Conclusion

The LLM-powered clarification system successfully replaces mechanical, progression-based responses with natural, contextually appropriate responses that:

- Maintain educational value
- Enhance simulation realism
- Preserve the patient's son persona authenticity
- Intelligently handle both unclear questions and unavailable information

This improvement demonstrates the value of selective LLM application where natural conversation quality significantly impacts educational effectiveness.

---

**Related Documentation:**

- [Intent Simplification and Storage](./INTENT_SIMPLIFICATION_AND_STORAGE.md)
- [Session Management](../development/session-management.md)
- [Architecture Overview](../architecture/README.md)
