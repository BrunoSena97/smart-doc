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

    # Test 1: Imaging escalation
    print('\n1. Testing imaging escalation (CXR):')
    result1 = engine.process_doctor_query(session_id, 'I need a chest X-ray')
    if result1['success'] and result1['response']['discoveries']:
        discovery = result1['response']['discoveries'][0]
        print(f'  First ask: {discovery["label"]} - {discovery["block_id"]}')

        # Ask again for chest imaging
        result2 = engine.process_doctor_query(session_id, 'Can you get the formal chest X-ray interpretation?')
        if result2['success'] and result2['response']['discoveries']:
            discovery2 = result2['response']['discoveries'][0]
            print(f'  Second ask: {discovery2["label"]} - {discovery2["block_id"]}')
        else:
            print('  Second ask: No new discoveries')
    else:
        print('  First ask: No discoveries')

    # Test 2: Labs escalation
    print('\n2. Testing labs escalation:')
    result3 = engine.process_doctor_query(session_id, 'What are her lab results?')
    if result3['success'] and result3['response']['discoveries']:
        discovery = result3['response']['discoveries'][0]
        print(f'  First labs: {discovery["label"]} - {discovery["block_id"]}')

        # Ask again for more labs
        result4 = engine.process_doctor_query(session_id, 'Any other lab results?')
        if result4['success'] and result4['response']['discoveries']:
            discovery2 = result4['response']['discoveries'][0]
            print(f'  Second labs: {discovery2["label"]} - {discovery2["block_id"]}')
        else:
            print('  Second labs: No new discoveries')
    else:
        print('  First labs: No discoveries')

if __name__ == "__main__":
    test_escalation()
