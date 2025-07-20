#!/usr/bin/env python3
"""
Advanced NLU Enhancement Strategies for SmartDoc

This script provides additional strategies to improve NLU flexibility beyond simple variations.
"""

import json
from typing import List, Dict, Any, Tuple
import re

class AdvancedNLUEnhancer:
    """Advanced strategies for improving NLU performance and flexibility."""
    
    def __init__(self):
        # Semantic groupings for better intent matching
        self.semantic_groups = {
            "age_related": ["old", "age", "elderly", "young", "years", "born", "birthday"],
            "medication_related": ["medication", "pills", "drugs", "medicine", "prescription", "taking", "on"],
            "symptom_related": ["symptoms", "complaint", "problem", "issue", "pain", "hurt", "feel", "experiencing"],
            "history_related": ["history", "past", "before", "previous", "background", "earlier"],
            "examination_related": ["exam", "examination", "physical", "check", "look", "findings"],
            "test_related": ["test", "lab", "blood", "result", "finding", "report"],
            "treatment_related": ["treatment", "therapy", "care", "management", "intervention"]
        }
        
        # Context-aware question patterns
        self.conversational_patterns = [
            # Follow-up patterns
            "And {question}?",
            "Also, {question}?",
            "What about {question}?",
            "Additionally, {question}?",
            
            # Clarification patterns
            "Just to clarify, {question}?",
            "To be sure, {question}?",
            "For clarification, {question}?",
            
            # Uncertainty patterns
            "I'm not sure about {question}",
            "Could you help me understand {question}?",
            "I need clarification on {question}",
            
            # Direct patterns
            "Simply put, {question}?",
            "In short, {question}?",
            "Basically, {question}?",
        ]

    def create_semantic_fallback_mappings(self, original_mappings: List[Dict]) -> List[Dict]:
        """Create fallback mappings based on semantic similarity."""
        fallback_mappings = []
        
        # Create broader semantic intent categories
        semantic_intents = {
            "general_age_inquiry": {
                "keywords": ["age", "old", "elderly", "young", "years"],
                "fallback_to": "profile_age",
                "confidence_threshold": 0.6
            },
            "general_medication_inquiry": {
                "keywords": ["medication", "pills", "drugs", "medicine", "taking"],
                "fallback_to": "meds_current_known",
                "confidence_threshold": 0.6
            },
            "general_symptom_inquiry": {
                "keywords": ["symptoms", "complaint", "problem", "wrong", "bothering"],
                "fallback_to": "hpi_chief_complaint",
                "confidence_threshold": 0.6
            },
            "general_history_inquiry": {
                "keywords": ["history", "past", "before", "background"],
                "fallback_to": "pmh_general",
                "confidence_threshold": 0.6
            }
        }
        
        for semantic_id, config in semantic_intents.items():
            fallback_mapping = {
                "id": f"semantic_{semantic_id}",
                "canonical_question": f"General inquiry about {semantic_id.replace('_', ' ')}",
                "variations": self._generate_semantic_variations(config["keywords"]),
                "action_type": "semantic_fallback",
                "target_details": {
                    "primary_intent": config["fallback_to"],
                    "confidence_threshold": config["confidence_threshold"],
                    "semantic_keywords": config["keywords"]
                },
                "expected_dialogue_state": ["ANY"]
            }
            fallback_mappings.append(fallback_mapping)
        
        return fallback_mappings

    def _generate_semantic_variations(self, keywords: List[str]) -> List[str]:
        """Generate variations based on semantic keywords."""
        variations = []
        
        # Simple keyword-based questions
        for keyword in keywords:
            variations.extend([
                f"Tell me about {keyword}",
                f"What about {keyword}?",
                f"Regarding {keyword}",
                f"About {keyword}",
                f"Concerning {keyword}",
                f"{keyword.capitalize()}?",
                f"Info on {keyword}",
                f"Details about {keyword}"
            ])
        
        # Combination patterns
        if len(keywords) >= 2:
            for i in range(len(keywords)-1):
                variations.append(f"{keywords[i]} and {keywords[i+1]}")
                variations.append(f"{keywords[i]} or {keywords[i+1]}")
        
        return variations[:20]  # Limit to prevent explosion

    def create_conversation_flow_mappings(self) -> List[Dict]:
        """Create mappings for natural conversation flow."""
        flow_mappings = [
            {
                "id": "conversation_starter",
                "canonical_question": "Let's begin the interview",
                "variations": [
                    "Let's start", "Shall we begin?", "Let's go", "Start interview",
                    "Begin", "Ready to start", "Let's do this", "Start now",
                    "Okay, let's begin", "Ready when you are", "Let's proceed"
                ],
                "action_type": "conversation_flow",
                "target_details": {"flow_type": "initiate", "next_suggested_state": "INTRODUCTION"},
                "expected_dialogue_state": ["ANY"]
            },
            {
                "id": "conversation_continue",
                "canonical_question": "Continue with more questions",
                "variations": [
                    "What else?", "More questions", "Continue", "Next", "Go on",
                    "What's next?", "Keep going", "More info", "Tell me more",
                    "Anything else?", "What about other things?", "More details"
                ],
                "action_type": "conversation_flow",
                "target_details": {"flow_type": "continue"},
                "expected_dialogue_state": ["ANY"]
            },
            {
                "id": "conversation_clarification",
                "canonical_question": "Can you clarify or repeat that?",
                "variations": [
                    "What?", "Come again?", "Pardon?", "Repeat that", "Say that again",
                    "I didn't catch that", "Could you repeat?", "One more time",
                    "Sorry, what?", "Can you say that again?", "Didn't understand"
                ],
                "action_type": "conversation_flow",
                "target_details": {"flow_type": "clarification"},
                "expected_dialogue_state": ["ANY"]
            }
        ]
        
        return flow_mappings

    def create_typo_tolerant_variations(self, original_mappings: List[Dict]) -> Dict[str, List[str]]:
        """Create variations that handle common typos and misspellings."""
        typo_patterns = {
            # Common medical term misspellings
            "medication": ["medicaton", "mediation", "medicaiton", "medciation"],
            "patient": ["patien", "pateint", "patinet"],
            "symptoms": ["symtoms", "symptms", "synptoms"],
            "examination": ["examinaton", "examiation", "examintion"],
            "history": ["histroy", "histry", "histoy"],
            "complaint": ["complain", "compliant", "compaint"],
            "treatment": ["treatmen", "treament", "tretment"],
        }
        
        typo_variations = {}
        
        for mapping in original_mappings:
            mapping_id = mapping["id"]
            variations_with_typos = []
            
            # Add typos to existing variations
            all_variations = [mapping["canonical_question"]] + mapping.get("variations", [])
            
            for variation in all_variations:
                for correct_word, typos in typo_patterns.items():
                    if correct_word in variation.lower():
                        for typo in typos:
                            typo_variation = variation.lower().replace(correct_word, typo)
                            variations_with_typos.append(typo_variation.capitalize())
            
            if variations_with_typos:
                typo_variations[mapping_id] = variations_with_typos[:10]  # Limit typos
        
        return typo_variations

def enhance_with_advanced_strategies(input_file: str, output_file: str):
    """Apply advanced NLU enhancement strategies."""
    enhancer = AdvancedNLUEnhancer()
    
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    original_mappings = data['canonical_question_mappings']
    
    print("🚀 Applying Advanced NLU Enhancement Strategies...")
    
    # 1. Add semantic fallback mappings
    print("📊 Creating semantic fallback mappings...")
    semantic_mappings = enhancer.create_semantic_fallback_mappings(original_mappings)
    
    # 2. Add conversation flow mappings
    print("💬 Creating conversation flow mappings...")
    flow_mappings = enhancer.create_conversation_flow_mappings()
    
    # 3. Create typo-tolerant variations
    print("🔤 Adding typo-tolerant variations...")
    typo_variations = enhancer.create_typo_tolerant_variations(original_mappings)
    
    # Apply typo variations to existing mappings
    for mapping in original_mappings:
        mapping_id = mapping["id"]
        if mapping_id in typo_variations:
            if "variations" not in mapping:
                mapping["variations"] = []
            mapping["variations"].extend(typo_variations[mapping_id])
    
    # Combine all mappings
    enhanced_mappings = original_mappings + semantic_mappings + flow_mappings
    
    # Create enhanced data structure
    enhanced_data = {
        "canonical_question_mappings": enhanced_mappings,
        "enhancement_metadata": {
            "original_mappings_count": len(original_mappings),
            "semantic_mappings_added": len(semantic_mappings),
            "flow_mappings_added": len(flow_mappings),
            "typo_variations_added": sum(len(v) for v in typo_variations.values()),
            "total_mappings": len(enhanced_mappings)
        }
    }
    
    # Save enhanced file
    with open(output_file, 'w') as f:
        json.dump(enhanced_data, f, indent=2)
    
    metadata = enhanced_data["enhancement_metadata"]
    print(f"\n✅ Advanced Enhancement Complete!")
    print(f"📈 Original mappings: {metadata['original_mappings_count']}")
    print(f"🎯 Semantic fallbacks added: {metadata['semantic_mappings_added']}")
    print(f"💭 Flow mappings added: {metadata['flow_mappings_added']}")
    print(f"🔤 Typo variations added: {metadata['typo_variations_added']}")
    print(f"📊 Total mappings: {metadata['total_mappings']}")
    print(f"💾 Saved to: {output_file}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 3:
        print("Usage: python advanced_nlu_enhancer.py <input_file.json> <output_file.json>")
        sys.exit(1)
    
    enhance_with_advanced_strategies(sys.argv[1], sys.argv[2])
