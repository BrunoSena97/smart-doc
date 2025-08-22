from ..db import get_session
from ..db.models import User
from .auth_service import hash_code

def create_user_code(code: str, display_name: str | None = None, label: str | None = None, usage_limit: int | None = None):
    with get_session() as s:
        u = User(
            display_name=display_name,
            code_hash=hash_code(code),
            code_label=label,
            usage_limit=usage_limit
        )
        s.add(u)
        s.commit()
        print(f"Created user {u.id} ({display_name or ''})")
