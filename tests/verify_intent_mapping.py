#!/usr/bin/env python3
"""
Verification script to check intent-to-label mapping consistency
"""

import sys
import os
import json

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from smartdoc.ai.discovery_processor import LLMDiscoveryProcessor

def verify_intent_label_consistency():
    """Verify that all intents in the case JSON have corresponding labels."""

    print("🔍 Verifying Intent-to-Label Mapping Consistency")
    print("=" * 55)

    # Load case JSON
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    case_file_path = os.path.join(project_root, 'data', 'cases', 'intent_driven_case.json')
    
    with open(case_file_path, 'r') as f:
        case_data = json.load(f)

    # Initialize discovery processor
    processor = LLMDiscoveryProcessor()

    # Extract all unique intents from case JSON
    all_intents = set()
    for block in case_data['informationBlocks']:
        for intent in block['intentTriggers']:
            all_intents.add(intent)

    print(f"📋 Found {len(all_intents)} unique intents in case JSON:")
    for intent in sorted(all_intents):
        print(f"  - {intent}")

    print(f"\n🏷️ Checking label mappings...")

    # Check mapping coverage
    mapped_intents = set()
    unmapped_intents = set()

    for intent in all_intents:
        label = processor._find_fallback_label(intent, "")
        if label != "Clinical Concerns":  # "Clinical Concerns" is the default fallback
            mapped_intents.add(intent)
            print(f"  ✅ {intent} → {label}")
        else:
            unmapped_intents.add(intent)
            print(f"  ❌ {intent} → {label} (fallback)")

    print(f"\n📊 Summary:")
    print(f"  - Total intents: {len(all_intents)}")
    print(f"  - Mapped intents: {len(mapped_intents)}")
    print(f"  - Unmapped intents: {len(unmapped_intents)}")
    print(f"  - Coverage: {len(mapped_intents)/len(all_intents)*100:.1f}%")

    if unmapped_intents:
        print(f"\n⚠️ Unmapped intents that need attention:")
        for intent in sorted(unmapped_intents):
            print(f"  - {intent}")
    else:
        print(f"\n🎉 All intents are properly mapped!")

    return len(unmapped_intents) == 0

if __name__ == "__main__":
    verify_intent_label_consistency()
