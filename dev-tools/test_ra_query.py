#!/usr/bin/env python3
"""
Test the specific "What does she take for RA?" query.
"""

import asyncio
import sys
from pathlib import Path

# Add packages to path
sys.path.insert(0, str(Path(__file__).parent.parent / "packages" / "core" / "src"))

from smartdoc_core.intent.classifier import LLMIntentClassifier
from smartdoc_core.llm.providers.ollama import OllamaProvider


async def test_ra_query():
    """Test the specific RA query that was failing."""

    # Initialize classifier
    llm_provider = OllamaProvider(
        base_url="http://localhost:11434",
        model="llama3.1:8b"
    )
    classifier = LLMIntentClassifier(provider=llm_provider)

    # Test the problematic query
    query = "What does she take for RA?"
    context = "anamnesis"

    print(f"Testing query: '{query}'")
    print(f"Context: {context}")
    print("-" * 50)

    try:
        result = classifier.classify_intent(query, context)

        intent_id = result.get("intent_id")
        confidence = result.get("confidence", 0.0)
        explanation = result.get("explanation", "No explanation")

        print(f"Result: {intent_id}")
        print(f"Confidence: {confidence:.2f}")
        print(f"Explanation: {explanation}")

        if intent_id == "meds_ra_specific_initial_query":
            print("✅ SUCCESS: Correctly classified as RA medication query!")
        else:
            print(f"❌ FAILURE: Expected 'meds_ra_specific_initial_query', got '{intent_id}'")

    except Exception as e:
        print(f"❌ ERROR: {e}")


if __name__ == "__main__":
    asyncio.run(test_ra_query())
