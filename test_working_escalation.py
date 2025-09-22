#!/usr/bin/env python3
"""Test the escalation system"""

import sys
import os
sys.path.insert(0, '/Users/bruno.sena/Projects/personal/masters/smart-doc/packages/core/src')

from smartdoc_core.simulation.engine import IntentDrivenDisclosureManager

def test_escalation():
    try:
        # Initialize engine with correct path
        case_path = '/Users/bruno.sena/Projects/personal/masters/smart-doc/data/raw/cases/intent_driven_case.json'
        engine = IntentDrivenDisclosureManager(case_file_path=case_path)

        # Start a session
        session_id = engine.start_intent_driven_session()

        print('🔍 Testing Escalation System (Progressive Disclosure)')
        print('=' * 60)

        # Test 1: Labs escalation - asking repeatedly should trigger different levels
        print('\n1. Testing labs escalation (multiple levels):')

        # First request - should get level 1
        result1 = engine.process_doctor_query(session_id, 'What are her lab results?', context='labs')
        if result1['success'] and result1['response']['discoveries']:
            discovery = result1['response']['discoveries'][0]
            print(f'  Level 1 labs: {discovery["label"]} - {discovery["block_id"]}')
        else:
            print('  Level 1 labs: No discoveries')

        # Second request - should get level 2
        result2 = engine.process_doctor_query(session_id, 'Any other lab values?', context='labs')
        if result2['success'] and result2['response']['discoveries']:
            discovery2 = result2['response']['discoveries'][0]
            print(f'  Level 2 labs: {discovery2["label"]} - {discovery2["block_id"]}')
        else:
            print('  Level 2 labs: No new discoveries')

        # Third request - should get level 3
        result3 = engine.process_doctor_query(session_id, 'Show me more lab results', context='labs')
        if result3['success'] and result3['response']['discoveries']:
            discovery3 = result3['response']['discoveries'][0]
            print(f'  Level 3 labs: {discovery3["label"]} - {discovery3["block_id"]}')
        else:
            print('  Level 3 labs: No new discoveries')

        # Test 2: Imaging escalation
        print('\n2. Testing imaging escalation (CXR preliminary → formal):')

        # Ask for chest X-ray first time
        result4 = engine.process_doctor_query(session_id, 'I need a chest X-ray', context='labs')
        if result4['success'] and result4['response']['discoveries']:
            discovery4 = result4['response']['discoveries'][0]
            print(f'  CXR Level 1: {discovery4["label"]} - {discovery4["block_id"]}')
        else:
            print('  CXR Level 1: No discoveries')

        # Ask for formal interpretation
        result5 = engine.process_doctor_query(session_id, 'Get me the formal radiology reading', context='labs')
        if result5['success'] and result5['response']['discoveries']:
            discovery5 = result5['response']['discoveries'][0]
            print(f'  CXR Level 2: {discovery5["label"]} - {discovery5["block_id"]}')
        else:
            print('  CXR Level 2: No new discoveries')

        # Test 3: Medication escalation (RA medications)
        print('\n3. Testing medication escalation (RA→Infliximab):')

        # Ask about RA medications first (should trigger uncertainty)
        result6 = engine.process_doctor_query(session_id, 'What medications does she take for rheumatoid arthritis?', context='anamnesis')
        if result6['success'] and result6['response']['discoveries']:
            discovery6 = result6['response']['discoveries'][0]
            print(f'  RA Med Level 1: {discovery6["label"]} - {discovery6["block_id"]}')
        else:
            print('  RA Med Level 1: No discoveries')

        # Ask for full medication reconciliation (should escalate to infliximab)
        result7 = engine.process_doctor_query(session_id, 'Can you get her complete medication list from previous hospitalizations?', context='anamnesis')
        if result7['success'] and result7['response']['discoveries']:
            discovery7 = result7['response']['discoveries'][0]
            print(f'  RA Med Level 2: {discovery7["label"]} - {discovery7["block_id"]}')
        else:
            print('  RA Med Level 2: No new discoveries')

        print('\n✅ Escalation test completed')

    except Exception as e:
        print(f'❌ Error during escalation test: {e}')
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_escalation()
