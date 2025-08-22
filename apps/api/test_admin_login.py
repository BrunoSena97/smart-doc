#!/usr/bin/env python3
"""
Test the admin login with code 'admin1234'.
"""

def test_admin_login():
    """Test admin login functionality."""
    
    from smartdoc_api.services.auth_service import verify_code
    from smartdoc_api.db import get_session
    from smartdoc_api.db.models import User
    from sqlalchemy import select
    
    ADMIN_CODE = "admin1234"
    
    print("🔍 Testing admin login...")
    
    with get_session() as s:
        admin = s.execute(
            select(User).where(User.display_name == "Admin")
        ).scalar_one_or_none()
        
        if not admin:
            print("❌ Admin user not found")
            return False
            
        print(f"👤 Found admin user (ID: {admin.id})")
        print(f"   Display name: {admin.display_name}")
        print(f"   Label: {admin.code_label}")
        print(f"   Active: {admin.is_active}")
        
        # Test the code
        if verify_code(ADMIN_CODE, admin.code_hash):
            print(f"✅ Login code '{ADMIN_CODE}' works correctly!")
            return True
        else:
            print(f"❌ Login code '{ADMIN_CODE}' failed verification")
            return False

if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
    
    from smartdoc_api import create_app
    app = create_app()
    
    with app.app_context():
        test_admin_login()
