#!/usr/bin/env python3
"""Test medication escalation specifically"""

import sys
import os
sys.path.insert(0, '/Users/bruno.sena/Projects/personal/masters/smart-doc/packages/core/src')

from smartdoc_core.simulation.engine import IntentDrivenDisclosureManager

def test_medication_escalation():
    try:
        # Initialize engine with correct path
        case_path = '/Users/bruno.sena/Projects/personal/masters/smart-doc/data/raw/cases/intent_driven_case.json'
        engine = IntentDrivenDisclosureManager(case_file_path=case_path)

        # Start a session
        session_id = engine.start_intent_driven_session()

        print('🏥 Testing Medication Escalation in Detail')
        print('=' * 60)

        # Step 1: Ask about RA medications (should trigger uncertainty)
        print('\n1. Asking about RA medications (should get uncertainty):')
        result1 = engine.process_doctor_query(session_id, 'What medications does she take for her rheumatoid arthritis?', context='anamnesis')
        if result1['success'] and result1['response']['discoveries']:
            discovery = result1['response']['discoveries'][0]
            print(f'   Result: {discovery["label"]} - {discovery["block_id"]}')
            print(f'   Content: {discovery["content"][:100]}...')
        else:
            print('   No discoveries')

        # Step 2: Explicitly request full medication reconciliation
        print('\n2. Requesting full medication reconciliation (should get infliximab):')
        result2 = engine.process_doctor_query(session_id, 'I need a complete medication reconciliation from all sources', context='anamnesis')
        if result2['success'] and result2['response']['discoveries']:
            discovery2 = result2['response']['discoveries'][0]
            print(f'   Result: {discovery2["label"]} - {discovery2["block_id"]}')
            print(f'   Content: {discovery2["content"][:100]}...')
        else:
            print('   No new discoveries')

        # Step 3: Try different phrasing for medication reconciliation
        print('\n3. Alternative phrasing for medication reconciliation:')
        result3 = engine.process_doctor_query(session_id, 'Can you get her complete medication list from previous hospitalizations?', context='anamnesis')
        if result3['success'] and result3['response']['discoveries']:
            discovery3 = result3['response']['discoveries'][0]
            print(f'   Result: {discovery3["label"]} - {discovery3["block_id"]}')
            print(f'   Content: {discovery3["content"][:100]}...')
        else:
            print('   No new discoveries')

        # Check session state
        session = engine.store.get_session(session_id)
        if session:
            print(f'\n📊 Session State:')
            print(f'   Total blocks revealed: {len(session.revealed_blocks)}')
            print(f'   Revealed blocks: {list(session.revealed_blocks)}')

            # Check which RA med blocks exist
            ra_blocks = [block for block in session.blocks.values() if getattr(block, 'group_id', None) == 'grp_meds_ra']
            print(f'\n💊 RA Medication Blocks Available:')
            for block in ra_blocks:
                status = "✅ REVEALED" if block.is_revealed else "❌ NOT REVEALED"
                prereqs = getattr(block, 'prerequisites', []) or []
                prereq_met = all(req in session.revealed_blocks for req in prereqs) if prereqs else True
                print(f'   {block.block_id} (Level {getattr(block, "level", "?")}): {status}')
                if prereqs:
                    print(f'     Prerequisites: {prereqs} - {"✅ MET" if prereq_met else "❌ NOT MET"}')
        else:
            print('\n❌ No session found')

        print('\n✅ Medication escalation test completed')

    except Exception as e:
        print(f'❌ Error during medication escalation test: {e}')
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_medication_escalation()
