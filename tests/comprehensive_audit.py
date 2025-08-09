#!/usr/bin/env python3
"""
Comprehensive audit script to check conformity between all components
"""

import json
from smartdoc.ai.intent_classifier import LLMIntentClassifier
from smartdoc.ai.discovery_processor import LLMDiscoveryProcessor
from smartdoc.simulation.engine import IntentDrivenDisclosureManager

def audit_system_conformity():
    """Comprehensive audit of system conformity."""
    
    print("🔍 COMPREHENSIVE SYSTEM CONFORMITY AUDIT")
    print("=" * 60)
    
    # Load case JSON
    with open('data/cases/intent_driven_case.json', 'r') as f:
        case_data = json.load(f)
    
    # Initialize components
    intent_classifier = LLMIntentClassifier()
    discovery_processor = LLMDiscoveryProcessor()
    
    # Extract all unique intents from case JSON
    all_case_intents = set()
    for block in case_data['informationBlocks']:
        for intent in block['intentTriggers']:
            all_case_intents.add(intent)
    
    # Get intents from intentBlockMappings
    mapping_intents = set(case_data['intentBlockMappings'].keys())
    
    print(f"📋 INTENT ANALYSIS")
    print(f"  - Case blocks contain: {len(all_case_intents)} unique intents")
    print(f"  - Intent mappings contain: {len(mapping_intents)} intents")
    
    # Check for inconsistencies between blocks and mappings
    missing_from_mappings = all_case_intents - mapping_intents
    extra_in_mappings = mapping_intents - all_case_intents
    
    if missing_from_mappings:
        print(f"  ⚠️ Intents in blocks but missing from mappings:")
        for intent in sorted(missing_from_mappings):
            print(f"    - {intent}")
    
    if extra_in_mappings:
        print(f"  ⚠️ Intents in mappings but not used in blocks:")
        for intent in sorted(extra_in_mappings):
            print(f"    - {intent}")
    
    if not missing_from_mappings and not extra_in_mappings:
        print(f"  ✅ Perfect consistency between blocks and mappings!")
    
    # Check Intent Classifier coverage
    print(f"\n🧠 INTENT CLASSIFIER ANALYSIS")
    classifier_intents = set(intent_classifier.intent_categories.keys())
    print(f"  - Intent Classifier defines: {len(classifier_intents)} intents")
    
    missing_from_classifier = all_case_intents - classifier_intents
    extra_in_classifier = classifier_intents - all_case_intents
    
    if missing_from_classifier:
        print(f"  ❌ Case intents missing from Intent Classifier:")
        for intent in sorted(missing_from_classifier):
            print(f"    - {intent}")
    else:
        print(f"  ✅ All case intents are defined in Intent Classifier")
    
    if extra_in_classifier:
        print(f"  ℹ️ Extra intents in Intent Classifier (not used in case):")
        for intent in sorted(extra_in_classifier):
            print(f"    - {intent}")
    
    # Check Discovery Processor mapping coverage
    print(f"\n🏷️ DISCOVERY PROCESSOR ANALYSIS")
    processor_mapped_intents = set()
    
    # Get all intents that have explicit mappings in the discovery processor
    for intent in all_case_intents:
        label = discovery_processor._find_fallback_label(intent, "")
        if label != "Clinical Concerns":  # "Clinical Concerns" is the default fallback
            processor_mapped_intents.add(intent)
    
    unmapped_in_processor = all_case_intents - processor_mapped_intents
    
    print(f"  - Discovery Processor maps: {len(processor_mapped_intents)}/{len(all_case_intents)} case intents")
    
    if unmapped_in_processor:
        print(f"  ❌ Case intents using fallback mapping:")
        for intent in sorted(unmapped_in_processor):
            label = discovery_processor._find_fallback_label(intent, "")
            print(f"    - {intent} → {label}")
    else:
        print(f"  ✅ All case intents have specific mappings")
    
    # Check Engine integration
    print(f"\n⚙️ ENGINE INTEGRATION ANALYSIS")
    try:
        # Try to initialize the engine
        engine = IntentDrivenDisclosureManager('data/cases/intent_driven_case.json')
        
        # Check if intent block mappings loaded correctly
        engine_mappings = set(engine.intent_block_mappings.keys())
        print(f"  - Engine loaded: {len(engine_mappings)} intent mappings")
        
        if engine_mappings == mapping_intents:
            print(f"  ✅ Engine mappings match case JSON perfectly")
        else:
            missing_in_engine = mapping_intents - engine_mappings
            extra_in_engine = engine_mappings - mapping_intents
            
            if missing_in_engine:
                print(f"  ❌ Mappings missing in engine:")
                for intent in sorted(missing_in_engine):
                    print(f"    - {intent}")
            
            if extra_in_engine:
                print(f"  ⚠️ Extra mappings in engine:")
                for intent in sorted(extra_in_engine):
                    print(f"    - {intent}")
        
        print(f"  ✅ Engine initialization successful")
        
    except Exception as e:
        print(f"  ❌ Engine initialization failed: {e}")
    
    # Block validation
    print(f"\n📦 BLOCK VALIDATION")
    block_ids = set()
    for block in case_data['informationBlocks']:
        block_ids.add(block['blockId'])
    
    # Check if all blocks referenced in mappings exist
    referenced_blocks = set()
    for intent, blocks in case_data['intentBlockMappings'].items():
        for block_id in blocks:
            referenced_blocks.add(block_id)
    
    missing_blocks = referenced_blocks - block_ids
    unreferenced_blocks = block_ids - referenced_blocks
    
    print(f"  - Total blocks defined: {len(block_ids)}")
    print(f"  - Blocks referenced in mappings: {len(referenced_blocks)}")
    
    if missing_blocks:
        print(f"  ❌ Referenced blocks that don't exist:")
        for block_id in sorted(missing_blocks):
            print(f"    - {block_id}")
    
    if unreferenced_blocks:
        print(f"  ⚠️ Blocks that are never referenced:")
        for block_id in sorted(unreferenced_blocks):
            print(f"    - {block_id}")
    
    if not missing_blocks and not unreferenced_blocks:
        print(f"  ✅ Perfect block consistency!")
    
    # Summary
    print(f"\n📊 SUMMARY")
    total_issues = 0
    
    if missing_from_mappings or extra_in_mappings:
        total_issues += 1
        print(f"  ❌ Block-Mapping inconsistencies found")
    else:
        print(f"  ✅ Block-Mapping consistency: PERFECT")
    
    if missing_from_classifier:
        total_issues += 1
        print(f"  ❌ Intent Classifier missing definitions")
    else:
        print(f"  ✅ Intent Classifier coverage: COMPLETE")
    
    if unmapped_in_processor:
        total_issues += 1
        print(f"  ❌ Discovery Processor using fallbacks")
    else:
        print(f"  ✅ Discovery Processor mapping: COMPLETE")
    
    if missing_blocks:
        total_issues += 1
        print(f"  ❌ Missing block references found")
    else:
        print(f"  ✅ Block references: VALID")
    
    print(f"\n🎯 FINAL RESULT: {total_issues} issues found")
    if total_issues == 0:
        print(f"🎉 SYSTEM IS FULLY CONFORMANT! 🎉")
    else:
        print(f"⚠️ System needs attention on {total_issues} areas")
    
    return total_issues == 0

if __name__ == "__main__":
    audit_system_conformity()
