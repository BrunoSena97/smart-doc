#!/usr/bin/env python3
"""
Create an admin user with the code 'admin1234'.
"""

def create_admin_user():
    """Create admin user with code 'admin1234'."""
    
    from smartdoc_api.services.auth_service import hash_code
    from smartdoc_api.db import get_session
    from smartdoc_api.db.models import User
    from sqlalchemy import select
    
    ADMIN_CODE = "admin1234"
    
    print("🔧 Creating admin user...")
    
    # Check if admin already exists
    with get_session() as s:
        existing = s.execute(
            select(User).where(User.display_name == "Admin")
        ).scalar_one_or_none()
        
        if existing:
            print(f"ℹ️  Admin user already exists (ID: {existing.id})")
            print(f"   Updating with new code: {ADMIN_CODE}")
            
            # Update existing admin with new code
            existing.code_hash = hash_code(ADMIN_CODE)
            s.commit()
            
            print("✅ Admin user updated successfully!")
        else:
            # Create new admin user
            admin_user = User(
                display_name="Admin",
                code_hash=hash_code(ADMIN_CODE),
                code_label="admin",
                is_active=True,
                usage_limit=None  # unlimited usage
            )
            s.add(admin_user)
            s.commit()
            
            print(f"✅ Admin user created successfully! (ID: {admin_user.id})")
    
    print(f"\n📝 Admin Login Credentials:")
    print(f"   Code: {ADMIN_CODE}")
    print(f"   Display name: Admin")
    print(f"   Label: admin")
    
    print(f"\n🔐 Test login with:")
    print(f"curl -X POST http://localhost:8000/api/v1/auth/login \\")
    print(f"  -H 'Content-Type: application/json' \\")
    print(f"  -d '{{\"code\": \"{ADMIN_CODE}\"}}'")
    
    return ADMIN_CODE

if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
    
    from smartdoc_api import create_app
    app = create_app()
    
    with app.app_context():
        create_admin_user()
