from flask import Blueprint, request, jsonify
from sqlalchemy import select, update
from datetime import datetime
from ..services.auth_service import hash_code, verify_code, issue_token, require_auth
from ..db import get_session
from ..db.models import User, AuthSession

bp = Blueprint("auth", __name__)

@bp.post("/auth/login")
def login_with_code():
    data = request.get_json(silent=True) or {}
    code = (data.get("code") or "").strip()
    if not code:
        return jsonify({"error": "code is required"}), 400

    with get_session() as s:
        users = s.execute(select(User).where(User.is_active == True)).scalars().all()
        # linear scan is fine at small scale; otherwise store a code_id and pass it
        # here we just try all (or add an index table mapping code_prefix->user)
        matched = None
        for u in users:
            if verify_code(code, u.code_hash):
                matched = u
                break

        if not matched:
            return jsonify({"error": "invalid code"}), 401

        # usage limiting
        if matched.usage_limit is not None and matched.usage_count >= matched.usage_limit:
            return jsonify({"error": "code usage limit reached"}), 403

        matched.usage_count += 1
        matched.last_used_at = datetime.utcnow()
        s.commit()

        token_info = issue_token(matched.id)
        return jsonify({
            "token": token_info["token"],
            "expires_at": token_info["expires_at"],
            "user": {"id": matched.id, "name": matched.display_name, "label": matched.code_label}
        })

@bp.post("/auth/logout")
@require_auth
def logout():
    from flask import g
    jti = request.headers.get("X-JTI")  # optional; or parse from token payload again
    # Simpler: revoke all sessions for this token's jti
    with get_session() as s:
        s.execute(update(AuthSession).where(AuthSession.jti == jti).values(revoked=True))
        s.commit()
    return jsonify({"status": "ok"})

@bp.get("/auth/me")
@require_auth
def me():
    from flask import g
    u = g.user
    return jsonify({"id": u.id, "name": u.display_name, "label": u.code_label})
