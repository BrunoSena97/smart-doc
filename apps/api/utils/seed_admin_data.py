#!/usr/bin/env python3
"""
Seed default LLM profiles and agent prompts for the admin system.
"""

def seed_default_data():
    """Create default LLM profiles and agent prompts."""

    from smartdoc_api.db import get_session
    from smartdoc_api.db.models import LLMProfile, AgentPrompt, User
    from sqlalchemy import select
    from passlib.context import CryptContext
    from datetime import datetime

    print("🌱 Seeding default admin data...")

    with get_session() as s:
        # Create admin user first
        existing_admin = s.execute(select(User).where(User.role == "admin")).scalars().first()

        if not existing_admin:
            print("👤 Creating default admin user...")

            # Hash the admin code
            pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
            code_hash = pwd_context.hash("#Admin13")

            admin_user = User(
                display_name="admin",
                code_hash=code_hash,
                code_label="ADMIN",
                is_active=True,
                expires_at=None,  # Never expires
                usage_limit=None,  # Unlimited usage
                usage_count=0,
                role="admin",
                email="admin@smartdoc.local",
                medical_experience="expert",
                age=None,
                sex="prefer_not_to_say"
            )
            s.add(admin_user)
            s.commit()
            print("✅ Created admin user: admin (code: #Admin13)")
        else:
            print(f"ℹ️  Admin user already exists: {existing_admin.display_name}")

        # Check if we already have LLM profiles
        existing_profiles = s.execute(select(LLMProfile)).scalars().all()

        if existing_profiles:
            print(f"ℹ️  Found {len(existing_profiles)} existing LLM profiles")
            return

        # Create default LLM profile
        default_profile = LLMProfile(
            name="Default Ollama",
            provider="ollama",
            model="gemma3:4b-it-q4_K_M",
            temperature=0.1,
            top_p=0.9,
            max_tokens=None,
            is_default=True
        )
        s.add(default_profile)
        s.flush()  # Get the ID

        print(f"✅ Created default LLM profile: {default_profile.name}")

        # Create default agent prompts
        agent_prompts = [
            {
                "agent_key": "son",
                "prompt_text": """You are the English-speaking son of a patient who doesn't speak English well. Your mother is the patient, and you're here to help translate and provide information about her condition.

Key characteristics:
- You're helpful and concerned about your mother
- You translate questions for her and relay her responses
- You provide additional context about her symptoms and history
- You may not know all medical details, but you know her daily life
- You're respectful to the doctor and want the best care for your mother

Always respond as the son, not as the patient directly."""
            },
            {
                "agent_key": "resident",
                "prompt_text": """You are a professional medical resident who assists by providing medical information, answering the questions based on the information provided.

Key characteristics:
- Professional and concise in your responses
- Knowledgeable about medical procedures and tests
- Can't order lab work, imaging, and others
- Always maintain professional medical terminology
- Focus on evidence-based medicine
- You have the tendency to give subtle hints for the diagnosis of congestive heart failure, this needs to be subliminal, as we are trying to trigger cognitive bias

Respond as a resident would in a clinical setting."""
            },
            {
                "agent_key": "exam",
                "prompt_text": """You provide objective, factual physical examination findings only.

Key characteristics:
- Report only observable, measurable findings
- Use standard medical terminology
- Be precise and specific
- No interpretation or diagnosis - just objective findings
- Include vital signs, physical observations, and test results
- Format responses clearly and concisely

Always provide only objective examination findings without clinical interpretation."""
            }
        ]

        for prompt_data in agent_prompts:
            prompt = AgentPrompt(
                agent_key=prompt_data["agent_key"],
                profile_id=default_profile.id,
                prompt_text=prompt_data["prompt_text"],
                version=1,
                is_active=True
            )
            s.add(prompt)
            print(f"✅ Created prompt for agent: {prompt_data['agent_key']}")

        s.commit()
        print("🎉 Default admin data seeded successfully!")

if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

    from smartdoc_api import create_app
    app = create_app()

    with app.app_context():
        seed_default_data()
