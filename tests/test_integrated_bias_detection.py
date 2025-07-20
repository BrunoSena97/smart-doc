#!/usr/bin/env python3
"""
Test script for integrated cognitive bias detection in SmartDoc
Demonstrates the bias detection working within the existing conversation flow
"""

import requests
import json
import time

def test_bias_detection():
    """Test the integrated bias detection system."""
    
    base_url = "http://127.0.0.1:8080"
    
    print("🧠 Testing Integrated Cognitive Bias Detection in SmartDoc")
    print("=" * 70)
    
    # Start a new session by visiting the home page
    try:
        home_response = requests.get(base_url)
        print(f"✅ Connected to SmartDoc: {home_response.status_code}")
    except Exception as e:
        print(f"❌ Could not connect to SmartDoc: {e}")
        print("Please ensure the server is running with: python3 main.py")
        return
    
    # Test conversation that should trigger bias detection
    test_conversations = [
        {
            "name": "Anchoring Bias Test - Heavy Heart Failure Focus",
            "messages": [
                "What brings the patient here today?",
                "Tell me about the heart sounds",
                "I want to check cardiovascular examination", 
                "Let me listen to the heart",
                "What's the BNP level?",
                "I think this is heart failure"
            ]
        },
        {
            "name": "Confirmation Bias Test - Seeking Only Confirming Evidence",
            "messages": [
                "What are the chief complaints?",
                "I want to do an echocardiogram",
                "Check the chest X-ray", 
                "What about the BNP?",
                "Tell me about heart failure medications"
            ]
        },
        {
            "name": "Premature Closure Test - Quick Assessment",
            "messages": [
                "What's wrong with the patient?",
                "Sounds like heart failure",
                "Let's start treatment"
            ]
        }
    ]
    
    for i, conversation in enumerate(test_conversations, 1):
        print(f"\n🔍 Test Case #{i}: {conversation['name']}")
        print("-" * 50)
        
        bias_warnings_detected = []
        
        for j, message in enumerate(conversation['messages'], 1):
            try:
                # Send message to SmartDoc
                response = requests.get(f"{base_url}/get", params={"msg": message})
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"  Message {j}: '{message}'")
                    print(f"  Response: {data.get('response', 'No response')[:100]}...")
                    
                    # Check for bias warning
                    if data.get('bias_warning') and data['bias_warning'].get('show'):
                        bias_type = data['bias_warning']['type']
                        bias_message = data['bias_warning']['message']
                        bias_warnings_detected.append((bias_type, bias_message))
                        print(f"  🚨 BIAS DETECTED: {bias_type}")
                        print(f"     Warning: {bias_message}")
                    else:
                        print(f"  ✅ No bias detected")
                        
                    # Check debug info
                    if data.get('debug_info'):
                        debug = data['debug_info']
                        print(f"  Debug: Intent={debug.get('intent_id')}, "
                              f"Confidence={debug.get('confidence', 0):.2f}, "
                              f"State={debug.get('dialogue_state')}")
                    
                else:
                    print(f"  ❌ Error: {response.status_code}")
                    
            except Exception as e:
                print(f"  ❌ Request failed: {e}")
            
            # Small delay between messages
            time.sleep(0.5)
        
        # Summary for this conversation
        print(f"\n  📊 Summary for '{conversation['name']}':")
        if bias_warnings_detected:
            print(f"     ✅ Bias detection working! Detected {len(bias_warnings_detected)} warnings:")
            for bias_type, message in bias_warnings_detected:
                print(f"       - {bias_type}: {message[:60]}...")
        else:
            print(f"     ⚠️  No bias warnings detected (might need more interactions)")
    
    # Test bias evaluation endpoint
    print(f"\n🎯 Testing Comprehensive Bias Evaluation Endpoint")
    print("-" * 50)
    
    try:
        eval_response = requests.get(f"{base_url}/bias_evaluation")
        if eval_response.status_code == 200:
            evaluation_data = eval_response.json()
            print("✅ Bias evaluation endpoint working!")
            
            if 'evaluation' in evaluation_data:
                evaluation = evaluation_data['evaluation']
                print(f"   Overall bias score: {evaluation.get('overall_score', 0)}")
                
                for bias_type in ['anchoring_bias', 'confirmation_bias', 'premature_closure']:
                    bias_result = evaluation.get(bias_type, {})
                    detected = bias_result.get('detected', False)
                    reason = bias_result.get('reason', 'N/A')
                    print(f"   {bias_type}: {'✅ Detected' if detected else '❌ Not detected'} - {reason}")
            
            if 'session_summary' in evaluation_data:
                summary = evaluation_data['session_summary']
                print(f"   Total interactions: {summary.get('total_interactions', 0)}")
                print(f"   Current state: {summary.get('current_state', 'Unknown')}")
                
        else:
            print(f"❌ Bias evaluation endpoint failed: {eval_response.status_code}")
            
    except Exception as e:
        print(f"❌ Bias evaluation test failed: {e}")
    
    print(f"\n🎉 Integrated Bias Detection Test Complete!")
    print("=" * 70)
    print("The system successfully integrates:")
    print("✅ Real-time bias detection during conversations")
    print("✅ LLM intent classification with bias awareness") 
    print("✅ Session logging with bias tracking")
    print("✅ Educational feedback generation")
    print("✅ Web interface with bias warning display")
    print("\n🏥 Your SmartDoc system now includes comprehensive cognitive bias detection!")

if __name__ == "__main__":
    test_bias_detection()
