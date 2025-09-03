#!/usr/bin/env python3
"""Test medication escalation specifically"""

import sys
sys.path.insert(0, '/Users/bruno.sena/Projects/personal/masters/smart-doc/packages/core/src')

from smartdoc_core.simulation.engine import IntentDrivenDisclosureManager

def test_med_escalation():
    case_path = '/Users/bruno.sena/Projects/personal/masters/smart-doc/data/raw/cases/intent_driven_case.json'
    engine = IntentDrivenDisclosureManager(case_file_path=case_path)
    session_id = engine.start_intent_driven_session()

    print('🔍 Testing Medication Escalation in Detail')
    print('=' * 60)

    # Step 1: Ask about RA medications (should trigger uncertainty)
    result1 = engine.process_doctor_query(session_id, 'What medications does she take for her rheumatoid arthritis?', context='anamnesis')
    if result1['success'] and result1['response']['discoveries']:
        discovery = result1['response']['discoveries'][0]
        print(f'Step 1 - RA medications: {discovery["label"]} - {discovery["block_id"]}')
    else:
        print('Step 1: No discoveries')

    # Step 2: Explicitly request full medication reconciliation
    result2 = engine.process_doctor_query(session_id, 'I need a complete medication reconciliation with all previous records', context='anamnesis')
    if result2['success'] and result2['response']['discoveries']:
        discovery2 = result2['response']['discoveries'][0]
        print(f'Step 2 - Full reconciliation: {discovery2["label"]} - {discovery2["block_id"]}')
    else:
        print('Step 2: No new discoveries')

    # Step 3: Show session state
    session = engine.store.get_session(session_id)
    print(f'\nRevealed blocks: {list(session.revealed_blocks)}')

if __name__ == "__main__":
    test_med_escalation()
