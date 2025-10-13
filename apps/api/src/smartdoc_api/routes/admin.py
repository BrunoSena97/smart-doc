from flask import Blueprint, request, jsonify, g, send_file
from sqlalchemy import select, update, delete, text
from datetime import datetime
from pathlib import Path
import json

from ..services.auth_service import require_auth
from ..db import get_session
from ..db.models import User, LLMProfile, AgentPrompt, AuditLog
from smartdoc_core.utils.logger import sys_logger

bp = Blueprint("admin", __name__, url_prefix="/api/v1/admin")

def admin_required(fn):
    """Decorator that requires admin role."""
    from functools import wraps

    @wraps(fn)
    @require_auth
    def wrapper(*args, **kwargs):
        # g.user is set by require_auth
        if not hasattr(g, 'user') or g.user.role != 'admin':
            return jsonify({"error": "admin access required"}), 403
        return fn(*args, **kwargs)
    return wrapper

def log_admin_action(action: str, payload: dict | None = None):
    """Log admin actions for audit trail."""
    try:
        with get_session() as s:
            log_entry = AuditLog(
                actor_user_id=g.user.id if hasattr(g, 'user') else None,
                action=action,
                payload=json.dumps(payload) if payload else None
            )
            s.add(log_entry)
            s.commit()
    except Exception:
        # Don't fail the main action if logging fails
        pass

# =============================================================================
# USERS MANAGEMENT
# =============================================================================

@bp.get("/users")
@admin_required
def list_users():
    """List all users."""
    with get_session() as s:
        users = s.execute(
            select(User).order_by(User.created_at.desc())
        ).scalars().all()

        result = []
        for user in users:
            result.append({
                "id": user.id,
                "display_name": user.display_name,
                "email": user.email,
                "age": user.age,
                "sex": user.sex,
                "medical_experience": user.medical_experience,
                "role": user.role,
                "code_label": user.code_label,
                "is_active": user.is_active,
                "usage_limit": user.usage_limit,
                "usage_count": user.usage_count,
                "created_at": user.created_at.isoformat() if user.created_at else None,
                "last_used_at": user.last_used_at.isoformat() if user.last_used_at else None
            })

    return jsonify(result)

@bp.post("/users")
@admin_required
def create_user():
    """Create a new user."""
    from ..services.auth_service import hash_code
    import secrets

    data = request.get_json(silent=True) or {}

    # Generate a random access code
    access_code = secrets.token_hex(4).upper()  # 8-character code

    try:
        with get_session() as s:
            user = User(
                display_name=data.get("display_name"),
                email=data.get("email"),
                age=data.get("age"),
                sex=data.get("sex"),
                medical_experience=data.get("medical_experience"),
                role=data.get("role", "user"),
                code_hash=hash_code(access_code),
                code_label=data.get("code_label"),
                is_active=data.get("is_active", True),
                usage_limit=data.get("usage_limit")
            )
            s.add(user)
            s.commit()

            log_admin_action("create_user", {
                "user_id": user.id,
                "display_name": user.display_name,
                "role": user.role
            })

            return jsonify({
                "ok": True,
                "user_id": user.id,
                "access_code": access_code  # Return code for initial setup
            })

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@bp.patch("/users/<int:user_id>")
@admin_required
def update_user(user_id):
    """Update a user."""
    data = request.get_json(silent=True) or {}

    try:
        with get_session() as s:
            user = s.get(User, user_id)
            if not user:
                return jsonify({"error": "user not found"}), 404

            # Update allowed fields
            updatable_fields = [
                "display_name", "email", "age", "sex", "medical_experience",
                "role", "code_label", "is_active", "usage_limit"
            ]

            updated_fields = {}
            for field in updatable_fields:
                if field in data:
                    setattr(user, field, data[field])
                    updated_fields[field] = data[field]

            if updated_fields:
                s.commit()
                log_admin_action("update_user", {
                    "user_id": user_id,
                    "updated_fields": updated_fields
                })

            return jsonify({"ok": True})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@bp.delete("/users/<int:user_id>")
@admin_required
def delete_user(user_id):
    """Delete a user."""
    try:
        with get_session() as s:
            user = s.get(User, user_id)
            if not user:
                return jsonify({"error": "user not found"}), 404

            # Don't allow deleting yourself
            if user.id == g.user.id:
                return jsonify({"error": "cannot delete yourself"}), 400

            log_admin_action("delete_user", {
                "user_id": user_id,
                "display_name": user.display_name
            })

            s.delete(user)
            s.commit()

            return jsonify({"ok": True})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

# =============================================================================
# LLM PROFILES MANAGEMENT
# =============================================================================

@bp.get("/llm-profiles")
@admin_required
def list_llm_profiles():
    """List all LLM profiles."""
    with get_session() as s:
        profiles = s.execute(
            select(LLMProfile).order_by(LLMProfile.created_at.desc())
        ).scalars().all()

        result = []
        for profile in profiles:
            result.append({
                "id": profile.id,
                "name": profile.name,
                "provider": profile.provider,
                "model": profile.model,
                "temperature": profile.temperature,
                "top_p": profile.top_p,
                "max_tokens": profile.max_tokens,
                "is_default": profile.is_default,
                "created_at": profile.created_at.isoformat() if profile.created_at else None
            })

    return jsonify(result)

@bp.post("/llm-profiles")
@admin_required
def create_llm_profile():
    """Create a new LLM profile."""
    data = request.get_json(silent=True) or {}

    try:
        with get_session() as s:
            # If this is set as default, unset others
            if data.get("is_default"):
                s.execute(
                    update(LLMProfile).values(is_default=False)
                )

            profile = LLMProfile(
                name=data["name"],
                provider=data["provider"],
                model=data["model"],
                temperature=data.get("temperature", 0.1),
                top_p=data.get("top_p", 0.9),
                max_tokens=data.get("max_tokens"),
                is_default=data.get("is_default", False)
            )
            s.add(profile)
            s.commit()

            log_admin_action("create_llm_profile", {
                "profile_id": profile.id,
                "name": profile.name,
                "provider": profile.provider,
                "model": profile.model
            })

            return jsonify({"ok": True, "profile_id": profile.id})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@bp.patch("/llm-profiles/<int:profile_id>")
@admin_required
def update_llm_profile(profile_id):
    """Update an LLM profile."""
    data = request.get_json(silent=True) or {}

    try:
        with get_session() as s:
            profile = s.get(LLMProfile, profile_id)
            if not profile:
                return jsonify({"error": "profile not found"}), 404

            # If setting as default, unset others first
            if data.get("is_default"):
                s.execute(
                    update(LLMProfile).where(LLMProfile.id != profile_id).values(is_default=False)
                )

            # Update fields
            updatable_fields = [
                "name", "provider", "model", "temperature",
                "top_p", "max_tokens", "is_default"
            ]

            updated_fields = {}
            for field in updatable_fields:
                if field in data:
                    setattr(profile, field, data[field])
                    updated_fields[field] = data[field]

            if updated_fields:
                s.commit()
                log_admin_action("update_llm_profile", {
                    "profile_id": profile_id,
                    "updated_fields": updated_fields
                })

            return jsonify({"ok": True})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@bp.delete("/llm-profiles/<int:profile_id>")
@admin_required
def delete_llm_profile(profile_id):
    """Delete an LLM profile."""
    try:
        with get_session() as s:
            profile = s.get(LLMProfile, profile_id)
            if not profile:
                return jsonify({"error": "profile not found"}), 404

            log_admin_action("delete_llm_profile", {
                "profile_id": profile_id,
                "name": profile.name
            })

            s.delete(profile)
            s.commit()

            return jsonify({"ok": True})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

# =============================================================================
# AGENT PROMPTS MANAGEMENT
# =============================================================================

@bp.get("/prompts")
@admin_required
def list_agent_prompts():
    """List all agent prompts."""
    with get_session() as s:
        # Join with profiles to get profile name
        query = text("""
        SELECT ap.*, lp.name AS profile_name
        FROM agent_prompts ap
        LEFT JOIN llm_profiles lp ON ap.profile_id = lp.id
        ORDER BY ap.created_at DESC
        """)
        result = s.execute(query)

        prompts = []
        for row in result:
            prompts.append({
                "id": row.id,
                "agent_key": row.agent_key,
                "profile_id": row.profile_id,
                "profile_name": row.profile_name,
                "prompt_text": row.prompt_text,
                "version": row.version,
                "is_active": row.is_active,
                "created_at": row.created_at
            })

    return jsonify(prompts)

@bp.post("/prompts")
@admin_required
def create_agent_prompt():
    """Create a new agent prompt."""
    data = request.get_json(silent=True) or {}

    if not data.get("agent_key") or not data.get("prompt_text"):
        return jsonify({"error": "agent_key and prompt_text required"}), 400

    try:
        with get_session() as s:
            is_active = data.get("is_active", True)

            # If creating an active prompt, deactivate all other prompts for this agent
            if is_active:
                s.execute(
                    update(AgentPrompt)
                    .where(AgentPrompt.agent_key == data["agent_key"])
                    .values(is_active=False)
                )

            prompt = AgentPrompt(
                agent_key=data["agent_key"],
                profile_id=data.get("profile_id"),
                prompt_text=data["prompt_text"],
                version=data.get("version", 1),
                is_active=is_active
            )
            s.add(prompt)
            s.commit()

            log_admin_action("create_agent_prompt", {
                "prompt_id": prompt.id,
                "agent_key": prompt.agent_key,
                "profile_id": prompt.profile_id,
                "is_active": is_active
            })

            return jsonify({"ok": True, "prompt_id": prompt.id})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@bp.patch("/prompts/<int:prompt_id>")
@admin_required
def update_agent_prompt(prompt_id):
    """Update an agent prompt."""
    data = request.get_json(silent=True) or {}

    try:
        with get_session() as s:
            prompt = s.get(AgentPrompt, prompt_id)
            if not prompt:
                return jsonify({"error": "prompt not found"}), 404

            # Update fields
            updatable_fields = [
                "agent_key", "profile_id", "prompt_text", "version", "is_active"
            ]

            updated_fields = {}
            for field in updatable_fields:
                if field in data:
                    setattr(prompt, field, data[field])
                    updated_fields[field] = data[field]

            if updated_fields:
                s.commit()
                log_admin_action("update_agent_prompt", {
                    "prompt_id": prompt_id,
                    "updated_fields": updated_fields
                })

            return jsonify({"ok": True})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@bp.delete("/prompts/<int:prompt_id>")
@admin_required
def delete_agent_prompt(prompt_id):
    """Delete an agent prompt."""
    try:
        with get_session() as s:
            prompt = s.get(AgentPrompt, prompt_id)
            if not prompt:
                return jsonify({"error": "prompt not found"}), 404

            log_admin_action("delete_agent_prompt", {
                "prompt_id": prompt_id,
                "agent_key": prompt.agent_key
            })

            s.delete(prompt)
            s.commit()

            return jsonify({"ok": True})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@bp.post("/prompts/<int:prompt_id>/toggle-status")
@admin_required
def toggle_prompt_status(prompt_id):
    """Toggle prompt active status. Ensures only one prompt per agent is active."""
    try:
        with get_session() as s:
            prompt = s.get(AgentPrompt, prompt_id)
            if not prompt:
                return jsonify({"error": "prompt not found"}), 404

            # If activating this prompt, deactivate all other prompts for the same agent
            if not prompt.is_active:
                # Deactivate all other prompts for this agent
                s.execute(
                    update(AgentPrompt)
                    .where(AgentPrompt.agent_key == prompt.agent_key)
                    .where(AgentPrompt.id != prompt_id)
                    .values(is_active=False)
                )

                # Activate this prompt
                prompt.is_active = True
                status_action = "activated"
            else:
                # Deactivate this prompt
                prompt.is_active = False
                status_action = "deactivated"

            s.commit()

            log_admin_action("toggle_prompt_status", {
                "prompt_id": prompt_id,
                "agent_key": prompt.agent_key,
                "action": status_action,
                "new_status": prompt.is_active
            })

            return jsonify({
                "ok": True,
                "new_status": prompt.is_active,
                "message": f"Prompt {status_action} successfully"
            })

    except Exception as e:
        return jsonify({"error": str(e)}), 400

# =============================================================================
# AUDIT LOGS
# =============================================================================

@bp.get("/audit-logs")
@admin_required
def list_audit_logs():
    """List recent audit logs."""
    limit = min(int(request.args.get("limit", 50)), 200)  # Max 200

    with get_session() as s:
        logs = s.execute(
            select(AuditLog, User.display_name)
            .outerjoin(User, AuditLog.actor_user_id == User.id)
            .order_by(AuditLog.created_at.desc())
            .limit(limit)
        ).all()

        result = []
        for log, actor_name in logs:
            result.append({
                "id": log.id,
                "actor_user_id": log.actor_user_id,
                "actor_name": actor_name,
                "action": log.action,
                "payload": json.loads(log.payload) if log.payload else None,
                "created_at": log.created_at.isoformat() if log.created_at else None
            })

    return jsonify(result)

# =============================================================================
# DATABASE BACKUP
# =============================================================================

@bp.get("/download-db")
@admin_required
def download_database():
    """Download the SQLite database file."""
    try:
        # Find the database file - try multiple possible locations
        possible_paths = [
            Path(__file__).resolve().parents[4] / "instance" / "smartdoc_dev.sqlite3",
            Path(__file__).resolve().parents[4] / "instance" / "smartdoc.sqlite3",
            Path("/data/smartdoc.sqlite3"),  # Docker production path
            Path("/workspace/instance/smartdoc_dev.sqlite3"),  # Docker dev path
        ]

        db_path = None
        for path in possible_paths:
            if path.exists():
                db_path = path
                break

        if db_path is None:
            sys_logger.log_system("error", "Database file not found in any expected location")
            return jsonify({"error": "Database file not found"}), 404

        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        download_name = f"smartdoc_backup_{timestamp}.sqlite3"

        sys_logger.log_system("info", f"Admin downloading database from {db_path}")
        log_admin_action("download_database", {"db_path": str(db_path)})

        return send_file(
            db_path,
            as_attachment=True,
            download_name=download_name,
            mimetype="application/x-sqlite3"
        )

    except Exception as e:
        sys_logger.log_system("error", f"Database download failed: {e}")
        return jsonify({"error": str(e)}), 500
