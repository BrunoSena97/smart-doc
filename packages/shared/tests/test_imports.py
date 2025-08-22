#!/usr/bin/env python3
"""
Simple import test for SmartDoc packages
"""

import sys
import os

# Add package paths
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(project_root, 'packages', 'core', 'src'))

print("🔍 Testing SmartDoc package imports...")

# Test 1: Basic utils
try:
    from smartdoc_core.utils.logger import sys_logger
    print("✅ Utils logger import successful!")
except Exception as e:
    print(f"❌ Utils logger import failed: {e}")

# Test 2: Config
try:
    from smartdoc_core.config.settings import config
    print("✅ Config import successful!")
except Exception as e:
    print(f"❌ Config import failed: {e}")

# Test 3: Intent classifier
try:
    from smartdoc_core.intent.classifier import LLMIntentClassifier
    print("✅ Intent classifier import successful!")
except Exception as e:
    print(f"❌ Intent classifier import failed: {e}")

# Test 4: Discovery processor
try:
    from smartdoc_core.discovery.processor import LLMDiscoveryProcessor
    print("✅ Discovery processor import successful!")
except Exception as e:
    print(f"❌ Discovery processor import failed: {e}")

# Test 5: Clinical evaluator
try:
    from smartdoc_core.clinical.evaluator import ClinicalEvaluator
    print("✅ Clinical evaluator import successful!")
except Exception as e:
    print(f"❌ Clinical evaluator import failed: {e}")

# Test 6: Simulation components (one by one)
try:
    from smartdoc_core.simulation.bias_analyzer import BiasEvaluator
    print("✅ Bias evaluator import successful!")
except Exception as e:
    print(f"❌ Bias evaluator import failed: {e}")

try:
    from smartdoc_core.simulation.session_logger import SessionLogger
    print("✅ Session logger import successful!")
except Exception as e:
    print(f"❌ Session logger import failed: {e}")

try:
    from smartdoc_core.simulation.disclosure_store import ProgressiveDisclosureStore
    print("✅ Disclosure store import successful!")
except Exception as e:
    print(f"❌ Disclosure store import failed: {e}")

try:
    from smartdoc_core.simulation.engine import IntentDrivenDisclosureManager
    print("✅ Simulation engine import successful!")
except Exception as e:
    print(f"❌ Simulation engine import failed: {e}")

print("\n🎯 Testing module-level imports...")

# Test module imports
try:
    from smartdoc_core.intent import LLMIntentClassifier
    print("✅ Intent module import successful!")
except Exception as e:
    print(f"❌ Intent module import failed: {e}")

try:
    from smartdoc_core.discovery import DiscoveryProcessor
    print("✅ Discovery module import successful!")
except Exception as e:
    print(f"❌ Discovery module import failed: {e}")

try:
    from smartdoc_core.simulation import SessionLogger, BiasEvaluator
    print("✅ Simulation module import successful!")
except Exception as e:
    print(f"❌ Simulation module import failed: {e}")

print("\n🏁 Import testing complete!")
