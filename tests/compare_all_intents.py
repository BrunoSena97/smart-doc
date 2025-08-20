#!/usr/bin/env python3
"""
Comprehensive test to compare all available intents vs. used intents
"""

import sys
import os
import json

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from smartdoc.ai.intent_classifier import LLMIntentClassifier

def compare_all_intents():
    """Compare all defined intents with those used in the case JSON."""
    
    print("🔍 Comparing All Available Intents vs. Used Intents")
    print("=" * 60)
    
    # Initialize intent classifier to get all defined intents
    classifier = LLMIntentClassifier()
    all_defined_intents = set(classifier.intent_categories.keys())
    
    print(f"📋 Intent Classifier defines {len(all_defined_intents)} intents:")
    for intent in sorted(all_defined_intents):
        print(f"  - {intent}")
    
    # Load case JSON to get used intents
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    case_file_path = os.path.join(project_root, 'data', 'cases', 'intent_driven_case.json')
    
    with open(case_file_path, 'r') as f:
        case_data = json.load(f)
    
    # Extract all unique intents from case JSON
    used_intents = set()
    for block in case_data['informationBlocks']:
        for intent in block['intentTriggers']:
            used_intents.add(intent)
    
    print(f"\n📋 Case JSON uses {len(used_intents)} intents:")
    for intent in sorted(used_intents):
        print(f"  - {intent}")
    
    # Find unused intents
    unused_intents = all_defined_intents - used_intents
    print(f"\n❌ Unused intents ({len(unused_intents)} intents):")
    if unused_intents:
        for intent in sorted(unused_intents):
            category = classifier.intent_categories[intent].get('category', 'unknown')
            description = classifier.intent_categories[intent].get('description', 'No description')
            print(f"  - {intent} ({category}): {description}")
    else:
        print("  None - all intents are used!")
    
    # Find undefined intents (should be none if everything is correct)
    undefined_intents = used_intents - all_defined_intents
    if undefined_intents:
        print(f"\n⚠️  Undefined intents used in case ({len(undefined_intents)} intents):")
        for intent in sorted(undefined_intents):
            print(f"  - {intent}")
    
    # Summary
    print(f"\n📊 Summary:")
    print(f"  - Total defined intents: {len(all_defined_intents)}")
    print(f"  - Used intents: {len(used_intents)}")
    print(f"  - Unused intents: {len(unused_intents)}")
    print(f"  - Undefined intents: {len(undefined_intents)}")
    print(f"  - Usage percentage: {len(used_intents)/len(all_defined_intents)*100:.1f}%")
    
    # Suggest potential additions
    if unused_intents:
        print(f"\n💡 Potential case enhancements:")
        clinical_unused = [intent for intent in unused_intents 
                          if any(category in classifier.intent_categories[intent].get('category', '') 
                                for category in ['history_present_illness', 'medications', 'physical_exam', 'diagnostics'])]
        
        if clinical_unused:
            print("  Consider adding these clinically relevant intents:")
            for intent in sorted(clinical_unused)[:5]:  # Show top 5
                description = classifier.intent_categories[intent].get('description', 'No description')
                print(f"    - {intent}: {description}")
    
    return len(unused_intents) == 0

if __name__ == "__main__":
    compare_all_intents()
