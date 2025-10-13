# Intent Simplification and Storage Enhancement

**Date:** October 13, 2025
**Status:** ✅ Completed
**Impact:** High - Improved LLM classification accuracy and added intent metadata storage

---

## Overview

This update simplified the medication intent classification system from 5 intents to 3 intents, and added storage of intent classification metadata to the database for analysis and debugging.

## Problem Statement

### 1. Intent Classification Issues

- **5 medication intents** for only **3 information blocks** created confusion
- LLM was making misclassifications:
  - "Edema?" → `meds_ra_specific_initial_query` (wrong - not about medications)
  - "oi?" → `meds_current_known` (wrong - meaningless query)
- Intent structure didn't match 1:1 with case file progressive disclosure levels

### 2. Missing Intent Metadata Storage

- LLM generated valuable classification metadata (intent_id, confidence, explanation)
- **This data was being calculated but thrown away** - not stored in database
- Impossible to debug misclassifications retroactively
- No way to audit intent classification accuracy in production

---

## Solution: Two-Part Fix

### Part 1: Simplify Medication Intents (5 → 3)

**Removed Intents:**

- `meds_uncertainty` - Merged into `meds_ra_specific_initial_query`
- `meds_other_meds_initial_query` - Merged into `meds_current_known`

**Retained Intents (1:1 mapping with case blocks):**

| Intent ID                        | Maps To               | Level | Description                                             |
| -------------------------------- | --------------------- | ----- | ------------------------------------------------------- |
| `meds_current_known`             | `meds_initial_known`  | 1     | Basic medication list (lisinopril, atenolol, etc.)      |
| `meds_ra_specific_initial_query` | `meds_ra_uncertainty` | 2     | RA-specific medications (son unsure)                    |
| `meds_full_reconciliation_query` | `critical_infliximab` | 3     | Complete medication reconciliation (reveals infliximab) |

**Example Queries Merged:**

- "Any other medications?" → Now classified as `meds_current_known` (Level 1)
- "Not sure about RA medications?" → Now classified as `meds_ra_specific_initial_query` (Level 2)

### Part 2: Store Intent Classification Metadata

**What's Now Stored:**

```json
{
  "intent_id": "meds_ra_specific_initial_query",
  "intent_confidence": 0.98,
  "intent_explanation": "The user is asking specifically about medications for rheumatoid arthritis, which maps to Level 2 of the medication escalation."
}
```

**Storage Location:** `Message.meta` JSON field in database

**When Stored:** User message is saved WITH intent metadata after LLM classification

---

## Files Modified

### Core Intent Classification

- ✅ `/packages/core/src/smartdoc_core/intent/classifier.py`
  - Removed `meds_uncertainty` and `meds_other_meds_initial_query` from `_default_intent_categories()`
  - Merged examples into remaining 3 intents
  - Updated `_valid_intents_for_context()` for anamnesis context
  - Fallback methods already correct (only referenced 3 intents)

### Case File

- ✅ `/data/raw/cases/intent_driven_case.json`
  - Removed deleted intents from `intentBlockMappings`
  - Updated `meds_ra_uncertainty` block to only trigger on `meds_ra_specific_initial_query`
  - Clean 1:1 mapping: 3 intents → 3 blocks

### Simulation Engine

- ✅ `/packages/core/src/smartdoc_core/simulation/engine.py`
  - Removed deleted intents from intent-specific responses
  - Updated context-specific intent list for anamnesis

### Development Tools

- ✅ `/dev-tools/test_enhanced_intents.py`
  - Updated medication intent list from 5 to 3
- ✅ `/dev-tools/comprehensive_test_data_extract.py`
  - Merged examples into 3 intents
  - Updated intent category mapping

### API Storage Layer

- ✅ `/apps/api/src/smartdoc_api/routes/chat.py`
  - Extract `intent_classification` from `discovery_result`
  - Store intent metadata in `Message.meta` field
  - Added debug logging for stored intent data
  - Fallback case stores user message without intent metadata

### New Testing Tool

- ✅ `/dev-tools/test_intent_storage.py`
  - Script to verify intent metadata storage
  - Queries database for recent messages with intent data
  - Displays intent_id, confidence, explanation

---

## Testing Results

### Integration Test: Medication Escalation

```bash
make test-file FILE=tests/integration/test_medication_escalation_flow.py
```

**Results:**

- ✅ Intent Classification: 6/6 correct (100% accuracy)
- ✅ Escalation Flow: All 3 levels revealed correctly
- ✅ Overall: SUCCESS 🎉

**Test Queries:**

1. "What medications is she taking?" → `meds_current_known` ✅
2. "What does she take for her arthritis?" → `meds_ra_specific_initial_query` ✅
3. "What does she take for RA?" → `meds_ra_specific_initial_query` ✅
4. "Can I see her complete medication list from previous records?" → `meds_full_reconciliation_query` ✅
5. "Any biologics or infliximab in her history?" → `meds_full_reconciliation_query` ✅
6. "Show me her full medication reconciliation" → `meds_full_reconciliation_query` ✅

---

## Benefits

### Improved Classification Accuracy

- ✅ Simpler intent structure reduces ambiguity
- ✅ 1:1 mapping between intents and information blocks
- ✅ LLM has clearer decision boundaries
- ✅ Fewer edge cases and overlapping categories

### Enhanced Debugging Capabilities

- ✅ Every user query stored with LLM's reasoning
- ✅ Can analyze misclassifications retroactively
- ✅ Confidence scores tracked for quality monitoring
- ✅ Intent explanations provide educational insights

### Production Monitoring

- ✅ Can audit classification accuracy in real usage
- ✅ Identify queries that confuse the LLM
- ✅ Track which intents are most/least used
- ✅ Validate progressive disclosure effectiveness

---

## How to Verify Storage

### Option 1: Run Test Script

```bash
cd /Users/bruno.sena/Projects/personal/masters/smart-doc
python dev-tools/test_intent_storage.py
```

### Option 2: Query Database Directly

```bash
# SSH into production
ssh your-server

# Inside Docker container
docker exec smartdoc python3 -c "
import sqlite3
import json
conn = sqlite3.connect('/data/smartdoc.sqlite3')
cursor = conn.cursor()
cursor.execute('''
    SELECT id, content, context, meta, created_at
    FROM messages
    WHERE role = 'user' AND meta IS NOT NULL
    ORDER BY created_at DESC
    LIMIT 5
''')
for row in cursor.fetchall():
    msg_id, content, context, meta, created = row
    meta_dict = json.loads(meta) if meta else {}
    print(f'Message: {content[:50]}')
    print(f'Intent: {meta_dict.get(\"intent_id\")}')
    print(f'Confidence: {meta_dict.get(\"intent_confidence\")}')
    print(f'Explanation: {meta_dict.get(\"intent_explanation\", \"\")[:80]}')
    print('-' * 60)
"
```

### Option 3: Check Production Logs

```bash
# Look for debug logs showing stored intent
docker logs smartdoc 2>&1 | grep "Stored message with intent"
```

---

## Migration Notes

### Database Schema

**No migration needed!** The `Message.meta` field already exists as a JSON TEXT column. We're just populating it with intent data now.

### Backward Compatibility

- ✅ Existing messages without intent metadata still work
- ✅ Fallback mode (when SmartDoc engine unavailable) stores messages without intent metadata
- ✅ Legacy `/get_bot_response` endpoint unchanged (deprecated, not updated)

### Production Deployment

1. Deploy updated code
2. Restart API server
3. New queries will automatically include intent metadata
4. Old queries remain unchanged (no retroactive population)

---

## Future Enhancements

### Analytics Dashboard

- Visualize intent classification distribution
- Track confidence score trends over time
- Identify problematic queries (low confidence)
- Compare intent accuracy across different contexts

### Quality Monitoring

- Alert on low confidence classifications (< 0.7)
- Flag unusual intent patterns
- Detect when LLM consistently misclassifies certain query types
- A/B test different prompt formulations

### Educational Insights

- Analyze which intents students struggle to trigger
- Identify gaps in clinical questioning patterns
- Track progressive disclosure effectiveness
- Generate usage reports for course instructors

---

## Related Documentation

- [Session Management](../development/session-management.md)
- [Intent Classification System](../architecture/README.md)
- [Progressive Disclosure Engine](../architecture/README.md)
- [Development Guide](../development/DEVELOPMENT.md)

---

## Conclusion

This update significantly improves the SmartDoc system by:

1. **Simplifying** the intent structure for better LLM accuracy
2. **Storing** classification metadata for debugging and analysis
3. **Enabling** production monitoring and quality assurance
4. **Maintaining** backward compatibility with existing data

The medication escalation test passing with 100% accuracy validates that the simplification improved classification quality while the new storage mechanism provides visibility into LLM decision-making for ongoing system improvement.
