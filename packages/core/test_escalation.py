#!/usr/bin/env python3
"""Test the escalation system"""

import sys
import os
sys.path.insert(0, '/Users/bruno.sena/Projects/personal/masters/smart-doc/packages/core/src')

from smartdoc_core.simulation.engine import IntentDrivenDisclosureManager

def test_escalation():
    # Initialize engine with correct path
    case_path = '/Users/bruno.sena/Projects/personal/masters/smart-doc/data/raw/cases/intent_driven_case.json'
    engine = IntentDrivenDisclosureManager(case_file_path=case_path)

    # Start a session
    session_id = engine.start_intent_driven_session()

    print('🔍 Testing Escalation System')
    print('=' * 60)

    # Test 1: Anamnesis (history-taking) escalation
    print('\n1. Testing anamnesis escalation (pertinent negatives):')
    result1 = engine.process_doctor_query(session_id, 'Does she have any chest pain?', context='anamnesis')
    if result1['success'] and result1['response']['discoveries']:
        discovery = result1['response']['discoveries'][0]
        print(f'  First negative: {discovery["label"]} - {discovery["block_id"]}')

        # Ask for more negatives
        result2 = engine.process_doctor_query(session_id, 'Any fever or chills?', context='anamnesis')
        if result2['success'] and result2['response']['discoveries']:
            discovery2 = result2['response']['discoveries'][0]
            print(f'  Second negative: {discovery2["label"]} - {discovery2["block_id"]}')
        else:
            print('  Second negative: No new discoveries')
    else:
        print('  First negative: No discoveries')

    # Test 2: Labs escalation
    print('\n2. Testing labs escalation:')
    result3 = engine.process_doctor_query(session_id, 'What are her lab results?', context='labs')
    if result3['success'] and result3['response']['discoveries']:
        discovery = result3['response']['discoveries'][0]
        print(f'  First labs: {discovery["label"]} - {discovery["block_id"]}')

        # Ask again for more labs
        result4 = engine.process_doctor_query(session_id, 'Any other lab results?', context='labs')
        if result4['success'] and result4['response']['discoveries']:
            discovery2 = result4['response']['discoveries'][0]
            print(f'  Second labs: {discovery2["label"]} - {discovery2["block_id"]}')
        else:
            print('  Second labs: No new discoveries')
    else:
        print('  First labs: No discoveries')

    # Test 3: Imaging escalation
    print('\n3. Testing imaging escalation (CXR):')
    result5 = engine.process_doctor_query(session_id, 'I need a chest X-ray', context='labs')  # Use labs context for imaging requests
    if result5['success'] and result5['response']['discoveries']:
        discovery = result5['response']['discoveries'][0]
        print(f'  First imaging: {discovery["label"]} - {discovery["block_id"]}')

        # Ask again for formal interpretation
        result6 = engine.process_doctor_query(session_id, 'Can you get the formal chest X-ray interpretation?', context='labs')
        if result6['success'] and result6['response']['discoveries']:
            discovery2 = result6['response']['discoveries'][0]
            print(f'  Second imaging: {discovery2["label"]} - {discovery2["block_id"]}')
        else:
            print('  Second imaging: No new discoveries')
    else:
        print('  First imaging: No discoveries')

    # Test 4: Medication escalation
    print('\n4. Testing medication escalation (RA medications):')
    result7 = engine.process_doctor_query(session_id, 'What medications does she take for arthritis?', context='anamnesis')
    if result7['success'] and result7['response']['discoveries']:
        discovery = result7['response']['discoveries'][0]
        print(f'  First med query: {discovery["label"]} - {discovery["block_id"]}')

        # Ask for full medication reconciliation
        result8 = engine.process_doctor_query(session_id, 'Can we do a full medication reconciliation?', context='anamnesis')
        if result8['success'] and result8['response']['discoveries']:
            discovery2 = result8['response']['discoveries'][0]
            print(f'  Full reconciliation: {discovery2["label"]} - {discovery2["block_id"]}')
        else:
            print('  Full reconciliation: No new discoveries')
    else:
        print('  First med query: No discoveries')

if __name__ == "__main__":
    test_escalation()
