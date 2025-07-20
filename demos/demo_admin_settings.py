#!/usr/bin/env python3
"""
Demo: SmartDoc Admin Settings Integration

This demo shows how the new admin settings functionality integrates with SmartDoc,
allowing real-time configuration updates without requiring application restarts.

Features demonstrated:
1. Web-based configuration management
2. Real-time Ollama model switching
3. Connection testing and validation
4. Dynamic service reinitialization

Usage: python demo_admin_settings.py
"""

import os
import sys
import time
import requests
import json
from urllib.parse import urljoin

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from smartdoc.config.settings import config
from smartdoc.utils.logger import sys_logger

class AdminSettingsDemo:
    def __init__(self, base_url="http://localhost:8080"):
        self.base_url = base_url
        self.admin_url = urljoin(base_url, "/admin/settings")
        self.test_url = urljoin(base_url, "/admin/test-connection")
        self.models_url = urljoin(base_url, "/admin/list-models")
        
    def print_header(self, title):
        """Print a formatted header."""
        print(f"\n{'='*60}")
        print(f" {title}")
        print(f"{'='*60}")
    
    def print_step(self, step, description):
        """Print a formatted step."""
        print(f"\n{step}. {description}")
        print("-" * 50)
    
    def check_smartdoc_running(self):
        """Check if SmartDoc is running."""
        try:
            response = requests.get(self.base_url, timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def check_ollama_running(self):
        """Check if Ollama is running."""
        try:
            response = requests.head(config.OLLAMA_BASE_URL, timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def test_admin_connection(self, ollama_url, model_name):
        """Test connection to Ollama with specific settings."""
        try:
            payload = {
                "ollama_base_url": ollama_url,
                "ollama_model": model_name
            }
            response = requests.post(self.test_url, 
                                   json=payload, 
                                   headers={"Content-Type": "application/json"},
                                   timeout=30)
            return response.json()
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def list_available_models(self, ollama_url):
        """List available models from Ollama."""
        try:
            payload = {"ollama_base_url": ollama_url}
            response = requests.post(self.models_url,
                                   json=payload,
                                   headers={"Content-Type": "application/json"},
                                   timeout=15)
            return response.json()
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def run_demo(self):
        """Run the admin settings demonstration."""
        self.print_header("SmartDoc Admin Settings Demo")
        
        print("This demo showcases the new admin settings functionality for SmartDoc.")
        print("The admin interface allows real-time configuration of Ollama models")
        print("without requiring application restarts.")
        
        # Step 1: Check prerequisites
        self.print_step(1, "Checking Prerequisites")
        
        smartdoc_running = self.check_smartdoc_running()
        ollama_running = self.check_ollama_running()
        
        print(f"SmartDoc Status: {'✅ Running' if smartdoc_running else '❌ Not Running'}")
        print(f"Ollama Status: {'✅ Running' if ollama_running else '❌ Not Running'}")
        
        if not smartdoc_running:
            print("\n⚠️  SmartDoc is not running!")
            print("Please start SmartDoc first:")
            print("   python main.py")
            return
        
        if not ollama_running:
            print("\n⚠️  Ollama is not running!")
            print("Please start Ollama first:")
            print("   ollama serve")
            return
        
        # Step 2: Show current configuration
        self.print_step(2, "Current Configuration")
        print(f"Base URL: {config.OLLAMA_BASE_URL}")
        print(f"Model: {config.OLLAMA_MODEL}")
        print(f"Max Tokens: {config.NLG_MAX_TOKENS}")
        print(f"Temperature: {config.NLG_TEMPERATURE}")
        
        # Step 3: List available models
        self.print_step(3, "Available Models")
        print("Fetching available models from Ollama...")
        
        models_result = self.list_available_models(config.OLLAMA_BASE_URL)
        if models_result.get("success"):
            models = models_result.get("models", [])
            if models:
                print(f"Found {len(models)} available models:")
                for i, model in enumerate(models[:5], 1):  # Show first 5
                    print(f"  {i}. {model['name']} ({model['size']})")
                if len(models) > 5:
                    print(f"  ... and {len(models) - 5} more")
            else:
                print("No models found.")
        else:
            print(f"❌ Failed to fetch models: {models_result.get('error')}")
        
        # Step 4: Test current configuration
        self.print_step(4, "Testing Current Configuration")
        print("Testing connection with current settings...")
        
        test_result = self.test_admin_connection(config.OLLAMA_BASE_URL, config.OLLAMA_MODEL)
        if test_result.get("success"):
            print("✅ Connection test successful!")
            print(f"   Message: {test_result.get('message')}")
        else:
            print(f"❌ Connection test failed: {test_result.get('error')}")
        
        # Step 5: Demo configuration changes
        self.print_step(5, "Admin Interface Access")
        print(f"🌐 Admin Settings URL: {self.admin_url}")
        print("\nThrough the admin interface, you can:")
        print("  • Change Ollama model in real-time")
        print("  • Adjust response parameters (temperature, max tokens)")
        print("  • Test connections before applying changes")
        print("  • Browse and select from available models")
        print("  • Monitor system status")
        
        # Step 6: API endpoints
        self.print_step(6, "Available API Endpoints")
        print("The admin functionality exposes these endpoints:")
        print(f"  GET  {self.admin_url} - Admin settings page")
        print(f"  POST {self.admin_url} - Update configuration")
        print(f"  POST {self.test_url} - Test connection")
        print(f"  POST {self.models_url} - List available models")
        
        # Step 7: Example usage
        self.print_step(7, "Example Configuration Update")
        print("Example: Switching to a different model via admin interface:")
        print("1. Open admin settings in your browser")
        print("2. Click 'Load Models' to see available options")
        print("3. Select a different model (e.g., llama3.2:3b)")
        print("4. Click 'Test Connection' to verify it works")
        print("5. Click 'Save Settings' to apply changes")
        print("6. The NLG service automatically reinitializes")
        print("7. Continue using SmartDoc with the new model")
        
        # Step 8: Benefits
        self.print_step(8, "Benefits of Admin Settings")
        print("✅ No application restart required")
        print("✅ Real-time configuration testing")
        print("✅ User-friendly web interface")
        print("✅ Automatic service reinitialization")
        print("✅ Configuration validation")
        print("✅ Error handling and feedback")
        
        print("\n" + "="*60)
        print(" Demo Complete!")
        print("="*60)
        print(f"Visit {self.admin_url} to try the admin interface yourself!")

if __name__ == "__main__":
    demo = AdminSettingsDemo()
    demo.run_demo()
