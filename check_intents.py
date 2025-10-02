#!/usr/bin/env python3
"""Check intent mapping consistency between case file and classifier"""

import json
import sys
import os
sys.path.insert(0, '/Users/bruno.sena/Projects/personal/masters/smart-doc/packages/core/src')

from smartdoc_core.intent.classifier import LLMIntentClassifier

def check_intent_consistency():
    # Load case file
    case_path = '/Users/bruno.sena/Projects/personal/masters/smart-doc/data/raw/cases/intent_driven_case.json'
    with open(case_path, 'r') as f:
        case_data = json.load(f)

    # Get case file intents
    case_intents = set(case_data.get('intentBlockMappings', {}).keys())

    # Get classifier intents
    classifier = LLMIntentClassifier()
    classifier_intents = set(classifier.intent_categories.keys())

    # Get context-specific intents from classifier
    anamnesis_intents = classifier._valid_intents_for_context('anamnesis')
    exam_intents = classifier._valid_intents_for_context('exam')
    labs_intents = classifier._valid_intents_for_context('labs')

    print("🔍 Intent Consistency Check")
    print("=" * 50)

    print(f"\n📋 Case File Intents ({len(case_intents)}):")
    for intent in sorted(case_intents):
        print(f"  • {intent}")

    print(f"\n🤖 Classifier Intents ({len(classifier_intents)}):")
    for intent in sorted(classifier_intents):
        print(f"  • {intent}")

    print(f"\n📝 Anamnesis Context Intents ({len(anamnesis_intents)}):")
    for intent in sorted(anamnesis_intents):
        print(f"  • {intent}")

    # Check for mismatches
    case_only = case_intents - classifier_intents
    classifier_only = classifier_intents - case_intents

    print(f"\n❌ Intents in Case File but NOT in Classifier ({len(case_only)}):")
    for intent in sorted(case_only):
        print(f"  • {intent}")

    print(f"\n⚠️  Intents in Classifier but NOT in Case File ({len(classifier_only)}):")
    for intent in sorted(classifier_only):
        print(f"  • {intent}")

    # Check if case intents are available in context
    anamnesis_missing = case_intents - anamnesis_intents - exam_intents - labs_intents
    print(f"\n🚫 Case Intents NOT available in ANY context ({len(anamnesis_missing)}):")
    for intent in sorted(anamnesis_missing):
        print(f"  • {intent}")

    print(f"\n✅ Summary:")
    print(f"  - Case file defines {len(case_intents)} intents")
    print(f"  - Classifier supports {len(classifier_intents)} intents")
    print(f"  - Anamnesis context allows {len(anamnesis_intents)} intents")
    print(f"  - {len(case_only)} intents missing from classifier")
    print(f"  - {len(anamnesis_missing)} case intents not available in any context")

if __name__ == "__main__":
    check_intent_consistency()