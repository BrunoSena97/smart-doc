#!/usr/bin/env python3
"""Test the improved medication escalation system"""

import sys
import os
sys.path.insert(0, '/Users/bruno.sena/Projects/personal/masters/smart-doc/packages/core/src')

from smartdoc_core.simulation.engine import IntentDrivenDisclosureManager

def test_improved_medication_escalation():
    try:
        # Initialize engine with correct path
        case_path = '/Users/bruno.sena/Projects/personal/masters/smart-doc/data/raw/cases/intent_driven_case.json'
        engine = IntentDrivenDisclosureManager(case_file_path=case_path)

        # Start a session
        session_id = engine.start_intent_driven_session()

        print('💊 Testing Improved Medication Escalation (3-Level System)')
        print('=' * 65)

        # Level 1: Ask about current medications (should get basic meds)
        print('\n1. Level 1 - Asking about current medications:')
        result1 = engine.process_doctor_query(session_id, 'What medications is she currently taking?', context='anamnesis')
        if result1['success'] and result1['response']['discoveries']:
            discovery = result1['response']['discoveries'][0]
            print(f'   ✅ {discovery["label"]} - {discovery["block_id"]}')
            print(f'   📝 Content: {discovery["content"][:100]}...')
        else:
            print('   ❌ No discoveries')

        # Level 2: Ask about RA medications (should get uncertainty)
        print('\n2. Level 2 - Asking about RA medications:')
        result2 = engine.process_doctor_query(session_id, 'What medications does she take for rheumatoid arthritis?', context='anamnesis')
        if result2['success'] and result2['response']['discoveries']:
            discovery2 = result2['response']['discoveries'][0]
            print(f'   ✅ {discovery2["label"]} - {discovery2["block_id"]}')
            print(f'   📝 Content: {discovery2["content"][:100]}...')
        else:
            print('   ❌ No new discoveries')

        # Level 3: Ask for full medication reconciliation (should get infliximab)
        print('\n3. Level 3 - Requesting complete medication reconciliation:')
        result3 = engine.process_doctor_query(session_id, 'I need a complete medication list from previous hospitalizations', context='anamnesis')
        if result3['success'] and result3['response']['discoveries']:
            discovery3 = result3['response']['discoveries'][0]
            print(f'   ✅ {discovery3["label"]} - {discovery3["block_id"]}')
            print(f'   📝 Content: {discovery3["content"][:100]}...')
        else:
            print('   ❌ No new discoveries')

        # Check session state
        session = engine.store.get_session(session_id)
        if session:
            print(f'\n📊 Final Session State:')
            print(f'   Total blocks revealed: {len(session.revealed_blocks)}')
            print(f'   Revealed blocks: {list(session.revealed_blocks)}')

            # Check RA medication group specifically
            ra_blocks = [block for block in session.blocks.values() if getattr(block, 'group_id', None) == 'grp_meds_ra']
            print(f'\n💊 RA Medication Group Progress:')
            for block in sorted(ra_blocks, key=lambda x: getattr(x, 'level', 999)):
                status = "✅ REVEALED" if block.is_revealed else "❌ NOT REVEALED"
                prereqs = getattr(block, 'prerequisites', []) or []
                prereq_met = all(req in session.revealed_blocks for req in prereqs) if prereqs else True
                level = getattr(block, 'level', '?')
                print(f'   Level {level}: {block.block_id} - {status}')
                if prereqs:
                    print(f'     Prerequisites: {prereqs} - {"✅ MET" if prereq_met else "❌ NOT MET"}')

        print('\n✅ Improved medication escalation test completed')

    except Exception as e:
        print(f'❌ Error during medication escalation test: {e}')
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_improved_medication_escalation()
