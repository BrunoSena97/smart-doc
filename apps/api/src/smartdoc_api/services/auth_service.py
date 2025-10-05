from datetime import datetime, timedelta, timezone
import jwt
import uuid
from passlib.hash import bcrypt
from flask import current_app, request, g
from sqlalchemy import select, update
from ..db import get_session
from ..db.models import User, AuthSession

JWT_ALG = "HS256"
JWT_TTL_MIN = 60 * 24 * 14  # 14 days

def hash_code(code: str) -> str:
    return bcrypt.hash(code)

def verify_code(code: str, code_hash: str) -> bool:
    return bcrypt.verify(code, code_hash)

def issue_token(user_id: int) -> dict:
    now = datetime.now(timezone.utc)

    # Check if user is admin for non-expiring token
    with get_session() as s:
        user = s.get(User, user_id)
        is_admin = user and user.role == "admin"

    if is_admin:
        # Admin tokens never expire (set expiration far in the future)
        exp = now + timedelta(days=365 * 10)  # 10 years
        jti = uuid.uuid4().hex
        payload = {"sub": str(user_id), "iat": int(now.timestamp()), "exp": int(exp.timestamp()), "jti": jti, "admin": True}
    else:
        # Regular user tokens expire after 14 days
        exp = now + timedelta(minutes=JWT_TTL_MIN)
        jti = uuid.uuid4().hex
        payload = {"sub": str(user_id), "iat": int(now.timestamp()), "exp": int(exp.timestamp()), "jti": jti}

    token = jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm=JWT_ALG)

    # persist session for optional revoke
    with get_session() as s:
        s.add(AuthSession(user_id=user_id, jti=jti))
        s.commit()

    return {"token": token, "expires_at": exp.isoformat() if not is_admin else "never"}

def decode_token(token: str) -> dict:
    return jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=[JWT_ALG])

def get_bearer_token() -> str | None:
    auth = request.headers.get("Authorization", "")
    if auth.lower().startswith("bearer "):
        return auth.split(" ", 1)[1].strip()
    return None

def require_auth(fn):
    from functools import wraps
    @wraps(fn)
    def wrapper(*args, **kwargs):
        token = get_bearer_token()
        if not token:
            return {"error": "missing bearer token"}, 401
        try:
            payload = decode_token(token)
        except Exception:
            return {"error": "invalid or expired token"}, 401

        jti = payload.get("jti")
        uid = int(payload.get("sub", 0))
        with get_session() as s:
            # check revoked
            sess = s.execute(select(AuthSession).where(AuthSession.jti == jti)).scalar_one_or_none()
            if not sess or sess.revoked:
                return {"error": "session revoked"}, 401
            user = s.get(User, uid)
            if not user or not user.is_active:
                return {"error": "user inactive"}, 403
            # optional: expiry check beyond JWT (e.g., user.expires_at)
            if user.expires_at and user.expires_at < datetime.utcnow():
                return {"error": "access expired"}, 403
            g.user = user
        return fn(*args, **kwargs)
    return wrapper
