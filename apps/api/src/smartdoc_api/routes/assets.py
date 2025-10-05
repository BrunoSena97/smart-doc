"""
Assets serving endpoints for the SmartDoc API v1.
"""

import os
from flask import send_from_directory, current_app
from pathlib import Path
from . import bp


@bp.route("/assets/<path:filename>")
def serve_asset(filename):
    """
    Serve static assets like images from the web frontend.
    
    Args:
        filename: The asset filename to serve
        
    Returns:
        The requested asset file with appropriate headers
    """
    # Check if we're running in Docker (mounted volume) or development
    docker_assets_dir = Path("/app/web/assets")
    
    if docker_assets_dir.exists():
        # Running in Docker container
        assets_dir = docker_assets_dir
        current_app.logger.info(f"Using Docker assets directory: {assets_dir}")
    else:
        # Running in development mode
        routes_dir = Path(__file__).parent
        project_root = routes_dir.parent.parent.parent.parent.parent
        assets_dir = project_root / "apps" / "web" / "public" / "assets"
        current_app.logger.info(f"Using development assets directory: {assets_dir}")
    
    current_app.logger.info(f"Assets directory exists: {assets_dir.exists()}")
    
    # Verify the assets directory exists
    if not assets_dir.exists():
        current_app.logger.error(f"Assets directory not found: {assets_dir}")
        return {"error": f"Assets directory not configured: {assets_dir}"}, 500
    
    try:
        response = send_from_directory(str(assets_dir), filename)
        # Add CORS headers for cross-origin requests
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Cache-Control'] = 'public, max-age=3600'  # Cache for 1 hour
        return response
    except FileNotFoundError:
        return {"error": f"Asset not found: {filename}"}, 404
