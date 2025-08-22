"""
SmartDoc API Application Package

A Flask-based REST API for the SmartDoc virtual patient simulation system.
Provides endpoints for clinical simulation, chat interactions, and performance evaluation.
"""

import os
import yaml
from flask import Flask
from flask_cors import CORS
from .db import init_app as db_init

__version__ = "0.1.0"


def _load_config():
    """Load configuration from YAML files based on environment."""
    env = os.getenv("SMARTDOC_ENV", "dev")
    # Navigate to repo root more reliably
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
    config_path = os.path.join(root, "configs", f"{env}.yaml")

    try:
        with open(config_path, "r") as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        print(f"Warning: Config file {config_path} not found, using defaults")
        return {}


def create_app() -> Flask:
    """
    Application factory for SmartDoc API.

    Returns:
        Flask: Configured Flask application instance
    """
    # Set instance path to be outside src/ directory
    # Navigate from src/smartdoc_api to apps/api/instance
    instance_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        "instance"
    )

    app = Flask(__name__, instance_path=instance_path)

    # Enable CORS for frontend communication
    CORS(
        app,
        resources={
            r"/api/*": {"origins": ["http://localhost:3000"]},
            r"/*": {
                "origins": ["http://localhost:3000"]
            },  # For legacy routes during migration
        },
    )

    # Load configuration from YAML
    cfg = _load_config()

    # Database configuration - support environment override
    db_config = cfg.get("database", {})
    if "SMARTDOC_DB_URL" in os.environ:
        db_config["url"] = os.environ["SMARTDOC_DB_URL"]

    app.config["DATABASE"] = db_config
    app.config["SECRET_KEY"] = "smartdoc-dev-key-change-in-production"

    # Initialize database
    db_init(app)

    # Register blueprints
    from .routes import bp as api_v1
    from .routes.auth import bp as auth_bp
    from .routes.admin import bp as admin_bp

    app.register_blueprint(api_v1, url_prefix="/api/v1")
    app.register_blueprint(auth_bp, url_prefix="/api/v1")
    app.register_blueprint(admin_bp)  # Already has /api/v1/admin prefix

    # Legacy routes (for backward compatibility during migration)
    from .routes.legacy import bp as legacy_bp

    app.register_blueprint(legacy_bp)

    # Health check endpoints
    @app.get("/health")
    def health():
        return {"status": "ok", "service": "smartdoc-api", "version": __version__}

    @app.get("/healthz")
    def healthz():
        """Kubernetes-style health check endpoint."""
        return {"ok": True}

    return app


# Application instance for WSGI servers (Gunicorn, etc.)
app = create_app()
