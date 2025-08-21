# SmartDoc API

Flask-based web service that exposes the SmartDoc virtual patient simulation platform.

## Overview

This application provides:
- REST API endpoints for clinical simulation
- Server-rendered web interface (optional)
- Session management and tracking
- Integration with SmartDoc Core components

## Features

- 🌐 **Web Interface**: Interactive clinical simulation UI
- 🔌 **REST API**: Programmatic access to simulation features
- 📊 **Session Management**: Comprehensive session tracking
- 🎯 **Real-time Discovery**: Progressive information revelation
- 🧠 **Bias Detection**: Live cognitive bias feedback

## Installation

```bash
pip install -e .
```

## Running the Application

### Development
```bash
export SMARTDOC_CONFIG=configs/dev.yaml
python -m smartdoc_api.main
```

### Using Scripts
```bash
# From project root
./scripts/run_api.sh
```

## API Endpoints

### Simulation
- `GET /` - Main simulation interface
- `POST /api/query` - Process doctor queries
- `GET /api/session/{id}` - Get session details

### Status
- `GET /health` - Health check
- `GET /api/status` - API status

## Configuration

The API uses YAML configuration files from the `configs/` directory:
- Environment variable `SMARTDOC_CONFIG` specifies config file
- Defaults to `configs/dev.yaml` in development

## Architecture

```
smartdoc_api/
├── main.py          # Flask application entry point
├── routes/          # API route handlers
├── templates/       # Jinja2 templates
└── static/          # Static assets (CSS, JS, images)
```

## Development

```bash
# Install in development mode
pip install -e .[dev]

# Run tests
pytest tests/

# Format code
black src/ tests/
```
