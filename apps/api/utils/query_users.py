#!/usr/bin/env python3
"""
Query utility to fetch and display users from the SmartDoc database.
"""

def fetch_users():
    """Fetch and display all users from the database."""
    
    from smartdoc_api.db import get_session
    from smartdoc_api.db.models import User
    from sqlalchemy import select
    
    print("👥 Fetching users from database...")
    
    try:
        with get_session() as s:
            # Query all users
            users = s.execute(select(User).order_by(User.created_at.desc())).scalars().all()
            
            if not users:
                print("📭 No users found in the database")
                return
            
            print(f"📊 Found {len(users)} user(s):")
            print("-" * 80)
            
            for user in users:
                print(f"ID: {user.id}")
                print(f"Display Name: {user.display_name}")
                print(f"Email: {user.email or 'N/A'}")
                print(f"Role: {user.role}")
                print(f"Active: {'✅' if user.is_active else '❌'}")
                print(f"Code Label: {user.code_label}")
                print(f"Medical Experience: {user.medical_experience or 'N/A'}")
                print(f"Age: {user.age or 'N/A'}")
                print(f"Sex: {user.sex or 'N/A'}")
                print(f"Usage: {user.usage_count}/{user.usage_limit or '∞'}")
                print(f"Created: {user.created_at}")
                print(f"Last Used: {user.last_used_at or 'Never'}")
                print(f"Expires: {user.expires_at or 'Never'}")
                print("-" * 80)
                
    except Exception as e:
        print(f"❌ Error fetching users: {e}")

def create_test_user(display_name="Test User", email="test@example.com"):
    """Create a test user for development purposes."""
    
    from smartdoc_api.db import get_session
    from smartdoc_api.db.models import User
    from passlib.context import CryptContext
    import secrets
    import string
    from datetime import datetime, timedelta
    
    print(f"👤 Creating test user: {display_name}")
    
    try:
        with get_session() as s:
            # Generate a random access code
            code = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(8))
            
            # Hash the code
            pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
            code_hash = pwd_context.hash(code)
            
            # Create user
            user = User(
                display_name=display_name,
                email=email,
                code_hash=code_hash,
                code_label=f"TEST_{code}",
                is_active=True,
                expires_at=datetime.utcnow() + timedelta(days=30),
                usage_limit=100,
                usage_count=0,
                role="student",
                medical_experience="student",
                age=25,
                sex="prefer_not_to_say"
            )
            
            s.add(user)
            s.commit()
            
            print(f"✅ Created test user successfully!")
            print(f"🔑 Access Code: {code}")
            print(f"📧 Email: {email}")
            print(f"🏷️  Code Label: {user.code_label}")
            
    except Exception as e:
        print(f"❌ Error creating test user: {e}")

def main():
    """Main function with options."""
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "create":
            name = sys.argv[2] if len(sys.argv) > 2 else "Test User"
            email = sys.argv[3] if len(sys.argv) > 3 else "test@example.com"
            create_test_user(name, email)
        elif command == "list":
            fetch_users()
        else:
            print("Usage:")
            print("  python query_users.py list              # List all users")
            print("  python query_users.py create [name] [email]  # Create test user")
    else:
        # Default: list users
        fetch_users()

if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
    
    from smartdoc_api import create_app
    app = create_app()
    
    with app.app_context():
        main()
