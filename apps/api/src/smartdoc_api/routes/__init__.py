"""
API Routes Package

Organized Flask blueprints for the SmartDoc API.
"""

from flask import Blueprint

# Create the main API v1 blueprint
bp = Blueprint("api_v1", __name__)

# Import route handlers to register them with the blueprint
from .chat import *  # noqa
from .simulation import *  # noqa
from .diagnosis import *  # noqa

__all__ = ["bp"]
