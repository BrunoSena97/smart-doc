#!/usr/bin/env python3
"""
Test Admin Settings Functionality

Quick test to verify the admin settings implementation works correctly.
"""

import os
import sys

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def test_config_methods():
    """Test the new configuration methods."""
    from smartdoc.config.settings import SmartDocConfig
    
    print("Testing SmartDocConfig methods...")
    
    # Create a test config
    test_config = SmartDocConfig()
    
    # Test get_ollama_settings
    current_settings = test_config.get_ollama_settings()
    print(f"✅ get_ollama_settings(): {current_settings}")
    
    # Test update_ollama_settings with valid data
    try:
        test_config.update_ollama_settings(
            base_url="http://localhost:11434",
            model="test-model",
            max_tokens=512,
            temperature=0.5
        )
        print("✅ update_ollama_settings() with valid data: Success")
    except Exception as e:
        print(f"❌ update_ollama_settings() failed: {e}")
    
    # Test update_ollama_settings with invalid data
    try:
        test_config.update_ollama_settings(
            base_url="",
            model="test-model",
            max_tokens=512,
            temperature=0.5
        )
        print("❌ update_ollama_settings() should have failed with empty URL")
    except ValueError:
        print("✅ update_ollama_settings() correctly rejected invalid data")
    
    print("Configuration methods test complete!\n")

def test_template_exists():
    """Test that the admin template exists."""
    template_path = os.path.join(project_root, "templates", "admin_settings.html")
    if os.path.exists(template_path):
        print("✅ Admin settings template exists")
        
        # Check if template has required elements
        with open(template_path, 'r') as f:
            content = f.read()
            
        required_elements = [
            "admin/settings", 
            "ollama_base_url",
            "ollama_model",
            "nlg_max_tokens",
            "nlg_temperature",
            "test-connection",
            "load-models"
        ]
        
        for element in required_elements:
            if element in content:
                print(f"✅ Template contains: {element}")
            else:
                print(f"❌ Template missing: {element}")
    else:
        print("❌ Admin settings template not found")
    
    print("Template test complete!\n")

def test_app_imports():
    """Test that the app can import necessary modules."""
    try:
        from smartdoc.web.app import app
        print("✅ Flask app imports successfully")
        
        # Check if admin routes are registered
        routes = [rule.rule for rule in app.url_map.iter_rules()]
        admin_routes = [route for route in routes if '/admin' in route]
        
        expected_routes = [
            '/admin/settings',
            '/admin/test-connection', 
            '/admin/list-models'
        ]
        
        for route in expected_routes:
            if route in admin_routes:
                print(f"✅ Route registered: {route}")
            else:
                print(f"❌ Route missing: {route}")
                
    except Exception as e:
        print(f"❌ App import failed: {e}")
    
    print("App import test complete!\n")

def main():
    """Run all tests."""
    print("="*60)
    print(" SmartDoc Admin Settings - Quick Test")
    print("="*60)
    
    test_config_methods()
    test_template_exists() 
    test_app_imports()
    
    print("="*60)
    print(" Test Summary")
    print("="*60)
    print("If all tests passed (✅), the admin settings functionality")
    print("has been successfully implemented and should work correctly.")
    print("\nTo use the admin interface:")
    print("1. Start SmartDoc: python main.py")
    print("2. Visit: http://localhost:8080/admin/settings")
    print("3. Configure Ollama settings as needed")
    print("\nFor detailed documentation, see: docs/ADMIN_SETTINGS.md")

if __name__ == "__main__":
    main()
