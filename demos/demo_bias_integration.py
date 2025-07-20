#!/usr/bin/env python3
"""
Simplified Demo: Cognitive Bias Detection Integration with SmartDoc
This version works without requiring Ollama and demonstrates the bias detection algorithms.
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Any

# Import our bias detection components
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from smartdoc.utils.bias_evaluator import BiasEvaluator
from smartdoc.utils.session_logger import SessionLogger

def load_case_data():
    """Load the Mull diagnostic error case."""
    case_file = "data/cases/mull_diagnostic_error.json"
    with open(case_file, 'r') as f:
        return json.load(f)

def simulate_conversation_with_bias_detection():
    """Simulate a conversation that triggers various cognitive biases."""
    
    print("🧠 SmartDoc Cognitive Bias Detection Demo")
    print("=" * 60)
    print("This demo shows how bias detection is integrated into your existing SmartDoc system.")
    print()
    
    # Load case data
    case_data = load_case_data()
    print(f"📋 Case: {case_data['caseTitle']}")
    print(f"🎯 Learning Objectives:")
    for obj in case_data['learningObjectives']:
        print(f"   • {obj}")
    print()
    
    # Initialize bias evaluator and session logger
    bias_evaluator = BiasEvaluator(case_data)
    session_logger = SessionLogger()
    
    print("🗣️  Simulated Clinical Conversation with Real-time Bias Detection")
    print("-" * 60)
    
    # Define conversation scenarios that trigger biases
    conversation_scenarios = [
        {
            "name": "Anchoring Bias Scenario",
            "description": "Student focuses heavily on heart failure from the beginning",
            "interactions": [
                {"user": "What brings the patient here today?", "intent": "hpi_chief_complaint"},
                {"user": "Tell me about the heart failure symptoms", "intent": "exam_cardiovascular"},
                {"user": "I want to check the heart sounds", "intent": "exam_cardiovascular"},
                {"user": "What's the BNP level?", "intent": "lab_tests"},
                {"user": "Let me listen to the heart again", "intent": "exam_cardiovascular"},
                {"user": "This looks like heart failure exacerbation", "intent": "assessment"}
            ]
        },
        {
            "name": "Confirmation Bias Scenario", 
            "description": "Student seeks evidence that confirms heart failure hypothesis",
            "interactions": [
                {"user": "What are the symptoms?", "intent": "hpi_chief_complaint"},
                {"user": "Show me the chest X-ray", "intent": "img_prelim_cxr"},
                {"user": "What's the BNP?", "intent": "lab_bnp"},
                {"user": "Check cardiovascular exam", "intent": "exam_cardiovascular"},
                {"user": "Any signs of fluid overload?", "intent": "exam_cardiovascular"},
                {"user": "This confirms heart failure", "intent": "assessment"}
            ]
        },
        {
            "name": "Premature Closure Scenario",
            "description": "Student reaches conclusion with minimal information gathering",
            "interactions": [
                {"user": "What's wrong with this patient?", "intent": "hpi_chief_complaint"},
                {"user": "Sounds like heart failure", "intent": "assessment"},
                {"user": "Let's start diuretics", "intent": "treatment"}
            ]
        }
    ]
    
    for scenario_num, scenario in enumerate(conversation_scenarios, 1):
        print(f"\n🎭 Scenario {scenario_num}: {scenario['name']}")
        print(f"   {scenario['description']}")
        print("   " + "-" * 50)
        
        # Simulate the conversation
        scenario_interactions = []
        bias_warnings = []
        
        for interaction_num, interaction in enumerate(scenario['interactions'], 1):
            user_input = interaction['user']
            intent_id = interaction['intent']
            
            # Simulate system response
            vsp_response = f"[System response to: {user_input}]"
            
            # Log the interaction
            session_logger.log_interaction(
                intent_id=intent_id,
                user_query=user_input,
                vsp_response=vsp_response,
                dialogue_state="SIMULATED"
            )
            
            scenario_interactions.append({
                "user_query": user_input,
                "intent_id": intent_id,
                "vsp_response": vsp_response,
                "timestamp": datetime.now().isoformat()
            })
            
            # Perform real-time bias detection
            session_interactions = session_logger.get_session_data()["interactions"]
            bias_check = bias_evaluator.check_real_time_bias(
                session_interactions,
                intent_id,
                user_input,
                vsp_response
            )
            
            print(f"   {interaction_num}. User: \"{user_input}\"")
            print(f"      Intent: {intent_id}")
            
            if bias_check.get("detected"):
                bias_type = bias_check["bias_type"]
                message = bias_check["message"]
                confidence = bias_check.get("confidence", 0)
                
                session_logger._add_bias_warning(bias_type, message)
                bias_warnings.append((bias_type, message, confidence))
                
                print(f"      🚨 BIAS DETECTED: {bias_type.upper()}")
                print(f"      Warning: {message}")
                print(f"      Confidence: {confidence:.1%}")
            else:
                print(f"      ✅ No bias detected")
            
            time.sleep(0.2)  # Small delay for readability
        
        # Scenario summary
        print(f"\n   📊 Scenario Summary:")
        print(f"      Total interactions: {len(scenario_interactions)}")
        print(f"      Bias warnings triggered: {len(bias_warnings)}")
        
        if bias_warnings:
            print(f"      🎯 Successfully detected biases:")
            for bias_type, message, confidence in bias_warnings:
                print(f"        • {bias_type}: {confidence:.1%} confidence")
        else:
            print(f"      ⚠️  No bias patterns detected in this scenario")
        
        print()
    
    # Comprehensive evaluation
    print("🎯 Comprehensive Session Evaluation")
    print("-" * 60)
    
    # Get all session data
    session_data = session_logger.get_session_data()
    all_interactions = session_data["interactions"]
    
    # Simulate progressive disclosure data
    revealed_blocks = {"hist_pmh", "pe_vitals", "img_prelim_cxr", "lab_bnp"}  # Simulated
    hypotheses = [{"diagnosis": "Heart failure exacerbation", "timestamp": datetime.now().isoformat()}]
    final_diagnosis = "Heart failure exacerbation"
    
    # Run comprehensive evaluation
    evaluation = bias_evaluator.evaluate_session(
        all_interactions,
        revealed_blocks,
        hypotheses,
        final_diagnosis
    )
    
    print(f"📈 Overall Bias Score: {evaluation['overall_score']}/3")
    print()
    
    bias_types = ['anchoring_bias', 'confirmation_bias', 'premature_closure']
    for bias_type in bias_types:
        result = evaluation.get(bias_type, {})
        detected = result.get('detected', False)
        reason = result.get('reason', 'N/A')
        confidence = result.get('confidence', 0)
        
        status = "✅ DETECTED" if detected else "❌ Not detected"
        print(f"{bias_type.replace('_', ' ').title()}: {status}")
        print(f"   Reason: {reason}")
        if detected:
            print(f"   Confidence: {confidence:.1%}")
        print()
    
    # Generate educational feedback
    feedback = bias_evaluator.generate_feedback_report(evaluation)
    
    print("📚 Educational Feedback")
    print("-" * 60)
    print(feedback)
    print()
    
    print("\n🎉 Demo Complete!")
    print("=" * 60)
    print("✅ Integration Achievements:")
    print("   • Real-time bias detection during conversations")
    print("   • Rule-based algorithms from research (Table 1)")
    print("   • Session logging with bias tracking")
    print("   • Educational feedback generation")
    print("   • Comprehensive post-session evaluation")
    print()
    print("🏥 Your SmartDoc system now includes:")
    print("   1. LLM Intent Classification (via Ollama)")
    print("   2. Dialogue State Management")
    print("   3. Knowledge Base Integration")
    print("   4. 🧠 COGNITIVE BIAS DETECTION (NEW!)")
    print("   5. Real-time Educational Feedback")
    print()
    print("🌐 Access your enhanced system at: http://127.0.0.1:8080")

if __name__ == "__main__":
    try:
        simulate_conversation_with_bias_detection()
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        print("Make sure you're in the smart-doc directory and case files are available.")
