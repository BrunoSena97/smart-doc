#!/usr/bin/env python3
"""
NLU Variation Generator for SmartDoc

This script helps generate natural language variations for canonical questions
to improve NLU coverage and make conversations more natural.
"""

import json
import re
from typing import List, Dict, Any

class NLUVariationGenerator:
    """Generates natural language variations for medical interview questions."""

    def __init__(self):
        self.question_transformations = {
            # Question word substitutions
            "what": ["tell me", "can you describe", "I need to know", "please explain"],
            "how": ["in what way", "tell me about how", "describe how"],
            "when": ["at what time", "tell me when", "what time"],
            "where": ["in what location", "at what place"],
            "why": ["for what reason", "what's the cause", "what made"],
            "who": ["which person", "what person", "tell me who"],

            # Medical terms and their informal equivalents
            "patient": ["she", "her", "your mother", "the woman", "this lady"],
            "medications": ["meds", "pills", "drugs", "medicines", "prescriptions"],
            "chief complaint": ["main problem", "primary issue", "main concern", "what's wrong"],
            "symptoms": ["problems", "issues", "complaints", "what's bothering her"],
            "examination": ["exam", "checkup", "physical", "looking at her"],
            "history": ["background", "past", "previous", "before"],

            # Question starters
            "what is": ["what's", "tell me", "can you describe", "I want to know"],
            "what are": ["what're", "tell me about", "list", "describe"],
            "tell me": ["what is", "describe", "explain", "can you tell me"],
            "does she": ["is she", "has she", "does the patient"],
            "is there": ["are there", "does she have", "has she had"],
        }

        self.informal_patterns = [
            # More casual ways to ask
            "So, {question}?",
            "Can you tell me {question}?",
            "I need to know {question}.",
            "What about {question}?",
            "How about {question}?",
            "{question}, right?",
            "Could you explain {question}?",
            "I'm wondering about {question}.",
        ]

        self.medical_context_starters = [
            "From a medical standpoint,",
            "Clinically speaking,",
            "For the medical record,",
            "Regarding her condition,",
            "In terms of her health,",
            "Medically,",
        ]

    def generate_variations(self, canonical_question: str, existing_variations: List[str] = None) -> List[str]:
        """Generate multiple variations of a canonical question."""
        if existing_variations is None:
            existing_variations = []

        variations = set(existing_variations)  # Use set to avoid duplicates
        base_question = canonical_question.lower()

        # 1. Simple word substitutions
        for original, replacements in self.question_transformations.items():
            if original in base_question:
                for replacement in replacements:
                    new_variation = base_question.replace(original, replacement)
                    variations.add(self._capitalize_first(new_variation))

        # 2. Apply informal patterns
        question_core = self._extract_question_core(canonical_question)
        for pattern in self.informal_patterns:
            variation = pattern.format(question=question_core.lower())
            variations.add(self._capitalize_first(variation))

        # 3. Add medical context
        for starter in self.medical_context_starters:
            variation = f"{starter} {canonical_question.lower()}"
            variations.add(self._capitalize_first(variation))

        # 4. Create shortened versions
        shortened = self._create_shortened_versions(canonical_question)
        variations.update(shortened)

        # Remove the original canonical question and existing variations
        variations.discard(canonical_question)
        for existing in existing_variations:
            variations.discard(existing)

        return sorted(list(variations))

    def _extract_question_core(self, question: str) -> str:
        """Extract the core part of a question (remove question words)."""
        # Remove common question starters
        question = re.sub(r'^(what is|what are|tell me|how|when|where|why|who is)\s+', '', question.lower())
        # Remove question marks and trailing punctuation
        question = re.sub(r'[?!.]+$', '', question)
        return question.strip()

    def _create_shortened_versions(self, question: str) -> List[str]:
        """Create shortened, more direct versions of questions."""
        shortened = []

        # Remove articles and prepositions for very short versions
        short_version = re.sub(r'\b(the|a|an|of|for|in|on|at|by|with)\b', '', question.lower())
        short_version = re.sub(r'\s+', ' ', short_version).strip()  # Clean up spaces
        if short_version and short_version != question.lower():
            shortened.append(self._capitalize_first(short_version))

        # Create keyword-only versions
        keywords = self._extract_keywords(question)
        if len(keywords) >= 2:
            keyword_question = " ".join(keywords) + "?"
            shortened.append(self._capitalize_first(keyword_question))

        return shortened

    def _extract_keywords(self, question: str) -> List[str]:
        """Extract key medical/important words from a question."""
        # Common medical keywords to prioritize
        medical_keywords = {
            'patient', 'medication', 'symptoms', 'history', 'examination',
            'age', 'complaint', 'treatment', 'diagnosis', 'pain', 'breathing',
            'heart', 'lung', 'blood', 'pressure', 'test', 'result'
        }

        # Remove common stop words
        stop_words = {
            'what', 'is', 'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on',
            'at', 'to', 'for', 'of', 'with', 'by', 'does', 'has', 'have',
            'are', 'was', 'were', 'been', 'be', 'being'
        }

        words = re.findall(r'\b\w+\b', question.lower())
        keywords = []

        for word in words:
            if word in medical_keywords or (word not in stop_words and len(word) > 3):
                keywords.append(word)

        return keywords[:4]  # Limit to 4 keywords

    def _capitalize_first(self, text: str) -> str:
        """Capitalize the first letter of a string."""
        if not text:
            return text
        return text[0].upper() + text[1:]

def enhance_mapping_file(file_path: str, output_path: str = None):
    """Enhance an existing mapping file with more variations."""
    generator = NLUVariationGenerator()

    with open(file_path, 'r') as f:
        data = json.load(f)

    total_added = 0

    for mapping in data['canonical_question_mappings']:
        canonical = mapping['canonical_question']
        existing = mapping.get('variations', [])

        print(f"\nProcessing: {canonical}")
        print(f"Existing variations: {len(existing)}")

        new_variations = generator.generate_variations(canonical, existing)

        # Add the new variations
        if 'variations' not in mapping:
            mapping['variations'] = []
        mapping['variations'].extend(new_variations[:15])  # Limit to prevent explosion
        total_added += len(new_variations[:15])

        print(f"Added: {len(new_variations[:15])} new variations")
        print(f"Total variations now: {len(mapping['variations'])}")

    # Save the enhanced file
    if output_path is None:
        output_path = file_path.replace('.json', '_enhanced.json')

    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"\n✅ Enhancement complete!")
    print(f"📊 Total variations added: {total_added}")
    print(f"💾 Enhanced file saved to: {output_path}")

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python nlu_variation_generator.py <mapping_file.json> [output_file.json]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    enhance_mapping_file(input_file, output_file)
