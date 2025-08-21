#!/usr/bin/env python3
"""
Test script to verify the new package structure is working
"""

import sys
sys.path.insert(0, './packages/core/src')

try:
    from smartdoc_core.intent.classifier import LLMIntentClassifier
    print("✅ Intent classifier import successful!")
except ImportError as e:
    print(f"❌ Intent classifier import failed: {e}")

try:
    from smartdoc_core.utils.logger import sys_logger
    print("✅ Logger import successful!")
except ImportError as e:
    print(f"❌ Logger import failed: {e}")

try:
    from smartdoc_core.config.settings import config
    print("✅ Config import successful!")
except ImportError as e:
    print(f"❌ Config import failed: {e}")

try:
    from smartdoc_core.simulation.engine import IntentDrivenDisclosureManager
    print("✅ Simulation engine import successful!")
except ImportError as e:
    print(f"❌ Simulation engine import failed: {e}")

print("🎉 New package structure test complete!")
