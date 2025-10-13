#!/usr/bin/env python3
"""
Test script to verify intent classification metadata is being stored in the database.
This validates that intent_id, confidence, and explanation are properly persisted.
"""

import sys
from pathlib import Path

# Add project paths
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "apps" / "api" / "src"))

def test_intent_storage():
    """Test that intent metadata is stored in message meta field."""

    print("🧪 Testing Intent Classification Storage")
    print("=" * 70)

    try:
        from smartdoc_api.db.models import Base, Message
        from sqlalchemy import create_engine, desc
        from sqlalchemy.orm import sessionmaker
        import json

        # Connect to development database
        db_path = project_root / "apps" / "api" / "instance" / "smartdoc_dev.sqlite3"
        if not db_path.exists():
            print(f"❌ Database not found at: {db_path}")
            return

        engine = create_engine(f"sqlite:///{db_path}")
        Session = sessionmaker(bind=engine)
        session = Session()

        print(f"✅ Connected to database: {db_path}\n")

        # Get the most recent user messages with metadata
        print("📋 Recent User Messages with Intent Metadata:")
        print("-" * 70)

        messages = session.query(Message)\
            .filter(Message.role == "user")\
            .filter(Message.meta.isnot(None))\
            .order_by(desc(Message.created_at))\
            .limit(10)\
            .all()

        if not messages:
            print("⚠️  No user messages found with metadata.")
            print("   This is expected if you haven't sent any queries yet after the update.\n")
            print("💡 To test:")
            print("   1. Start the API server: make api")
            print("   2. Send a query through the UI or API")
            print("   3. Run this script again")
            session.close()
            return

        count_with_intent = 0
        for msg in messages:
            try:
                meta = json.loads(msg.meta) if msg.meta else {}
                intent_id = meta.get("intent_id")
                intent_confidence = meta.get("intent_confidence")
                intent_explanation = meta.get("intent_explanation")

                if intent_id:
                    count_with_intent += 1
                    print(f"\n✅ Message ID: {msg.id}")
                    print(f"   Content: {msg.content[:60]}...")
                    print(f"   Context: {msg.context}")
                    print(f"   Intent ID: {intent_id}")
                    print(f"   Confidence: {intent_confidence:.2f}" if intent_confidence else "   Confidence: N/A")
                    print(f"   Explanation: {intent_explanation[:80]}..." if intent_explanation else "   Explanation: N/A")
                    print(f"   Created: {msg.created_at}")
                else:
                    print(f"\n⚠️  Message ID: {msg.id} has metadata but no intent_id")
                    print(f"   Content: {msg.content[:60]}...")
                    print(f"   Meta keys: {list(meta.keys())}")

            except json.JSONDecodeError as e:
                print(f"\n❌ Message ID: {msg.id} has invalid JSON metadata")
                print(f"   Error: {e}")

        print("\n" + "=" * 70)
        print(f"📊 Summary:")
        print(f"   Total messages checked: {len(messages)}")
        print(f"   Messages with intent data: {count_with_intent}")

        if count_with_intent > 0:
            print(f"\n🎉 SUCCESS! Intent classification metadata is being stored correctly!")
        else:
            print(f"\n⚠️  No messages found with intent classification data.")
            print(f"   This suggests the feature needs testing with new queries.")

        session.close()

    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Make sure you're in the correct environment and dependencies are installed.")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_intent_storage()
