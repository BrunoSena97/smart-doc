#!/usr/bin/env python3
"""
Test pertinent negatives accumulation flow end-to-end.

Tests that pertinent negative questions accumulate responses rather than overwriting them.
This ensures that asking "Any fever?" followed by "Any chest pain?" shows both negatives.
"""

import asyncio
import json
from pathlib import Path
from typing import Dict, Any, Optional

# Add packages to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "packages" / "core" / "src"))
sys.path.insert(0, str(Path(__file__).parent.parent / "packages" / "shared" / "src"))

try:
    from smartdoc_core.intent.classifier import LLMIntentClassifier
    from smartdoc_core.simulation.engine import IntentDrivenDisclosureManager
    from smartdoc_core.simulation.disclosure_store import ProgressiveDisclosureStore
    from smartdoc_core.llm.providers.ollama import OllamaProvider
except ImportError as e:
    print(f"Import error: {e}")
    print("Please ensure the packages are properly installed.")
    sys.exit(1)


class TestPertinentNegativesAccumulation:
    """Test the complete pertinent negatives accumulation flow."""

    def __init__(self):
        self.case_file = Path(__file__).parent.parent.parent / "data" / "raw" / "cases" / "intent_driven_case.json"
        self.engine: Optional[IntentDrivenDisclosureManager] = None
        self.session_id: Optional[str] = None

    def setup(self):
        """Set up the test environment."""
        print("🔧 Setting up pertinent negatives accumulation test...")
        
        # Verify case file exists
        if not self.case_file.exists():
            raise FileNotFoundError(f"Case file not found: {self.case_file}")
        
        # Initialize engine with full path to case file
        self.engine = IntentDrivenDisclosureManager(case_file_path=str(self.case_file))
        self.session_id = self.engine.start_intent_driven_session()
        
        print(f"✅ Test setup complete. Session ID: {self.session_id}")

    def test_sequential_pertinent_negatives(self):
        """Test that asking sequential pertinent negative questions accumulates responses."""
        print("\n🧪 Testing sequential pertinent negatives accumulation...")
        
        if not self.engine or not self.session_id:
            raise RuntimeError("Test not properly set up. Call setup() first.")
        
        # First, ask about fever
        print("\n1️⃣ Asking: 'Any fever?'")
        response1 = self.engine.process_doctor_query(self.session_id, "Any fever?", "anamnesis")
        response1_data = response1.get('response', {})
        text1 = response1_data.get('text', '') if isinstance(response1_data, dict) else str(response1_data)
        print(f"Response 1: {text1}")
        
        # Then ask about chest pain
        print("\n2️⃣ Asking: 'Any chest pain?'")
        response2 = self.engine.process_doctor_query(self.session_id, "Any chest pain?", "anamnesis")
        response2_data = response2.get('response', {})
        text2 = response2_data.get('text', '') if isinstance(response2_data, dict) else str(response2_data)
        print(f"Response 2: {text2}")
        
        # Check discoveries for accumulation
        discoveries2 = response2_data.get('discoveries', []) if isinstance(response2_data, dict) else []
        print(f"Discoveries in response 2: {len(discoveries2)} items")
        for i, disc in enumerate(discoveries2):
            print(f"  Discovery {i+1}: {disc.get('label', 'No label')} - {disc.get('content', 'No content')[:100]}...")
        
        # Check if the second response includes both negatives
        fever_mentioned = "fever" in text2.lower() or "fevers" in text2.lower()
        chest_pain_mentioned = "chest pain" in text2.lower() or "chest" in text2.lower()
        
        print(f"\n📊 Analysis:")
        print(f"   Fever mentioned in response 2: {fever_mentioned}")
        print(f"   Chest pain mentioned in response 2: {chest_pain_mentioned}")
        
        # Test result
        accumulation_working = fever_mentioned and chest_pain_mentioned
        
        if accumulation_working:
            print("✅ SUCCESS: Pertinent negatives are accumulating correctly!")
        elif chest_pain_mentioned and not fever_mentioned:
            print("❌ ISSUE: Only the latest pertinent negative is shown (overwriting behavior)")
        else:
            print("❓ UNCLEAR: Unexpected response pattern")
        
        return {
            'accumulation_working': accumulation_working,
            'fever_in_response2': fever_mentioned,
            'chest_pain_in_response2': chest_pain_mentioned,
            'response1': text1,
            'response2': text2
        }

    def test_general_pertinent_negatives_query(self):
        """Test asking general pertinent negatives after specific ones."""
        print("\n🔍 Testing general pertinent negatives query...")
        
        if not self.engine or not self.session_id:
            raise RuntimeError("Test not properly set up. Call setup() first.")
        
        # Ask general pertinent negatives
        print("\n3️⃣ Asking: 'What about pertinent negatives?'")
        response3 = self.engine.process_doctor_query(self.session_id, "What about pertinent negatives?", "anamnesis")
        response3_data = response3.get('response', {})
        text3 = response3_data.get('text', '') if isinstance(response3_data, dict) else str(response3_data)
        print(f"Response 3: {text3}")
        
        # Check discoveries for accumulation
        discoveries3 = response3_data.get('discoveries', []) if isinstance(response3_data, dict) else []
        print(f"Discoveries in response 3: {len(discoveries3)} items")
        for i, disc in enumerate(discoveries3):
            print(f"  Discovery {i+1}: {disc.get('label', 'No label')} - {disc.get('content', 'No content')[:150]}...")
        
        # Should trigger group escalation and reveal additional negatives
        chills_mentioned = "chill" in text3.lower()
        
        print(f"   Chills mentioned in response 3: {chills_mentioned}")
        
        return {
            'chills_revealed': chills_mentioned,
            'response3': text3
        }

    def test_complete_flow(self):
        """Test the complete flow of pertinent negatives accumulation."""
        print("\n🔄 Running complete pertinent negatives accumulation test...")
        
        try:
            # Setup
            self.setup()
            
            # Test sequential queries
            sequential_result = self.test_sequential_pertinent_negatives()
            
            # Test general query
            general_result = self.test_general_pertinent_negatives_query()
            
            # Overall assessment
            success = sequential_result['accumulation_working']
            
            print(f"\n🎯 FINAL RESULT: {'PASS' if success else 'FAIL'}")
            
            if not success:
                print("❌ The pertinent negatives are not accumulating properly.")
                print("   Each new question overwrites the previous response instead of adding to it.")
            
            return {
                'test_passed': success,
                'sequential_test': sequential_result,
                'general_test': general_result
            }
            
        except Exception as e:
            print(f"❌ Test failed with error: {e}")
            import traceback
            traceback.print_exc()
            return {'test_passed': False, 'error': str(e)}


def test_pertinent_negatives_accumulation():
    """Main test function for pytest compatibility."""
    tester = TestPertinentNegativesAccumulation()
    result = tester.test_complete_flow()
    
    # Assert for pytest
    assert result['test_passed'], "Pertinent negatives accumulation test failed"
    
    return result


if __name__ == "__main__":
    # Run the test directly
    tester = TestPertinentNegativesAccumulation()
    result = tester.test_complete_flow()
    
    if result['test_passed']:
        print("🎉 All tests passed!")
        sys.exit(0)
    else:
        print("💥 Tests failed!")
        sys.exit(1)