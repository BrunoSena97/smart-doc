"""
SmartDoc API Application Package

A Flask-based REST API for the SmartDoc virtual patient simulation system.
Provides endpoints for clinical simulation, chat interactions, and performance evaluation.
"""

from flask import Flask
from flask_cors import CORS

__version__ = "0.1.0"


def create_app() -> Flask:
    """
    Application factory for SmartDoc API.

    Returns:
        Flask: Configured Flask application instance
    """
    app = Flask(__name__)

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

    # Load configuration
    app.config["SECRET_KEY"] = "smartdoc-dev-key-change-in-production"

    # Register blueprints
    from .routes import bp as api_v1

    app.register_blueprint(api_v1, url_prefix="/api/v1")

    # Legacy routes (for backward compatibility during migration)
    from .routes.legacy import bp as legacy_bp

    app.register_blueprint(legacy_bp)

    # Health check endpoint
    @app.get("/health")
    def health():
        return {"status": "ok", "service": "smartdoc-api", "version": __version__}

    return app
