#!/usr/bin/env python3
"""
Simple test to debug specific lab intent issue.
"""

import asyncio
from pathlib import Path
import sys

# Add the packages/core/src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "packages" / "core" / "src"))

from smartdoc_core.intent.classifier import LLMIntentClassifier
from smartdoc_core.simulation.engine import IntentDrivenDisclosureManager
from smartdoc_core.llm.providers.ollama import OllamaProvider


async def debug_lab_intent():
    """Debug why specific lab intents aren't working."""

    case_file = Path(__file__).parent.parent / "data" / "raw" / "cases" / "intent_driven_case.json"

    # Initialize engine
    engine = IntentDrivenDisclosureManager(case_file_path=str(case_file))

    # Initialize classifier
    llm_provider = OllamaProvider(
        base_url="http://localhost:11434",
        model="gemma3:4b-it-q4_K_M"
    )
    classifier = LLMIntentClassifier(provider=llm_provider)

    # Start a session
    session_id = "debug_session"
    engine.start_intent_driven_session(session_id)

    # Test a specific BNP query
    query = "What's the BNP level?"
    print(f"Testing query: '{query}'")

    # 1. Test classification
    print("\n1. Testing Classification:")
    try:
        result = classifier.classify_intent(query, "labs")
        print(f"   Intent: {result.get('intent_id')}")
        print(f"   Confidence: {result.get('confidence', 0.0):.2f}")
    except Exception as e:
        print(f"   Classification error: {e}")

    # 2. Test discovery
    print("\n2. Testing Discovery:")
    try:
        result = engine.process_doctor_query(session_id, query, context="labs")
        discovery_result = result.get("discovery_result", {})
        discovered_blocks = discovery_result.get("discovered_blocks", [])

        print(f"   Discovery result keys: {list(discovery_result.keys())}")
        print(f"   Discovered blocks: {discovered_blocks}")
        print(f"   Intent ID from engine: {discovery_result.get('intent_id')}")
        print(f"   Trigger type: {discovery_result.get('trigger_type')}")

    except Exception as e:
        print(f"   Discovery error: {e}")


if __name__ == "__main__":
    asyncio.run(debug_lab_intent())
