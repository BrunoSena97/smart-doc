#!/usr/bin/env python3
"""Test the enhanced intent classification for medication escalation"""

import sys
import os
sys.path.insert(0, '/Users/bruno.sena/Projects/personal/masters/smart-doc/packages/core/src')

from smartdoc_core.intent.classifier import LLMIntentClassifier

def test_enhanced_intent_classification():
    try:
        classifier = LLMIntentClassifier()

        print('🧠 Testing Enhanced Intent Classification for Medication Escalation')
        print('=' * 70)

        # Test queries that should trigger different medication escalation levels
        test_queries = [
            # Level 1: Basic medication queries
            ("What medications is she currently taking?", "meds_current_known"),
            ("Current meds?", "meds_current_known"),
            ("Tell me about her medications", "meds_current_known"),

            # Level 2: RA-specific queries
            ("What medications does she take for rheumatoid arthritis?", "meds_ra_specific_initial_query"),
            ("What does she take for her arthritis?", "meds_ra_specific_initial_query"),
            ("Any arthritis medications?", "meds_ra_specific_initial_query"),
            ("RA medications?", "meds_ra_specific_initial_query"),

            # Level 3: Full reconciliation queries
            ("I need a complete medication reconciliation from previous hospitalizations", "meds_full_reconciliation_query"),
            ("Can you get her complete medication list from previous hospitalizations?", "meds_full_reconciliation_query"),
            ("Any biologics or immunosuppressive medications?", "meds_full_reconciliation_query"),
            ("What about infliximab or other biologics?", "meds_full_reconciliation_query"),
            ("Check previous medical records for RA medications", "meds_full_reconciliation_query"),
        ]

        print('\n📋 Testing Intent Classification Results:')
        print('=' * 50)

        correct_classifications = 0
        total_tests = len(test_queries)

        for query, expected_intent in test_queries:
            # Test with anamnesis context
            result = classifier.classify_intent_with_context(query, "anamnesis")
            classified_intent = result['intent_id']
            confidence = result['confidence']

            status = "✅" if classified_intent == expected_intent else "❌"
            if classified_intent == expected_intent:
                correct_classifications += 1

            print(f'{status} Query: "{query}"')
            print(f'   Expected: {expected_intent}')
            print(f'   Got: {classified_intent} (confidence: {confidence:.2f})')
            if classified_intent != expected_intent:
                print(f'   ⚠️  Classification mismatch!')
            print()

        accuracy = (correct_classifications / total_tests) * 100
        print(f'📊 Classification Accuracy: {correct_classifications}/{total_tests} ({accuracy:.1f}%)')

        # Test medication intent categories
        print(f'\n💊 Medication Intent Categories:')
        print('=' * 40)

        medication_intents = [
            'meds_current_known',
            'meds_ra_specific_initial_query',
            'meds_full_reconciliation_query',
            'meds_uncertainty',
            'meds_other_meds_initial_query'
        ]

        for intent_id in medication_intents:
            info = classifier.get_intent_info(intent_id)
            if info:
                print(f'{intent_id}:')
                print(f'  Description: {info["description"]}')
                print(f'  Examples: {len(info["examples"])} provided')
                print()

        print('✅ Enhanced intent classification test completed')

    except Exception as e:
        print(f'❌ Error during intent classification test: {e}')
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_enhanced_intent_classification()
