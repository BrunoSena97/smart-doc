# SmartDoc Project Restructure Summary

## New Professional Project Structure

The SmartDoc project has been reorganized into a clean, modular structure that clearly separates responsibilities and follows professional software development practices.

### Directory Structure

```
smartdoc_project/
│
├── data/                    # Case files and simulation data
│   └── cases/
│       └── *.json
│
├── logs/                    # System logging
│   └── smartdoc.log
│
├── smartdoc/                # Main application package
│   │
│   ├── ai/                  # AI and NLU components
│   │   ├── __init__.py
│   │   └── intent_classifier.py    # LLM-based intent classification
│   │
│   ├── simulation/          # Core simulation engine
│   │   ├── __init__.py
│   │   ├── engine.py                # Main simulation orchestrator
│   │   ├── state_manager.py         # Session state management
│   │   ├── bias_analyzer.py         # Cognitive bias detection
│   │   └── session_tracker.py       # Session tracking and logging
│   │
│   ├── web/                 # Web presentation layer
│   │   ├── __init__.py
│   │   ├── app.py               # Flask application
│   │   ├── static/              # CSS, JS, images
│   │   └── templates/           # HTML templates
│   │
│   ├── utils/               # True utilities only
│   │   ├── __init__.py
│   │   ├── exceptions.py        # Custom exceptions
│   │   └── logger.py            # System logging utility
│   │
│   └── config/              # Configuration management
│       ├── __init__.py
│       └── settings.py
│
└── venv/                    # Virtual environment
```

## Module Responsibilities

### `smartdoc.ai`
- **Purpose**: Natural Language Understanding and AI components
- **Components**:
  - `intent_classifier.py`: LLM-powered clinical intent classification

### `smartdoc.simulation`
- **Purpose**: Core virtual patient simulation logic
- **Components**:
  - `engine.py`: Main simulation orchestrator (formerly `intent_driven_disclosure.py`)
  - `state_manager.py`: Session state and progressive disclosure (formerly `progressive_disclosure.py`)
  - `bias_analyzer.py`: Cognitive bias detection algorithms (formerly `bias_evaluator.py`)
  - `session_tracker.py`: Session tracking and analysis (formerly `session_logger.py`)

### `smartdoc.web`
- **Purpose**: Web interface and user interaction
- **Components**:
  - `app.py`: Flask web application
  - `static/`: Frontend assets
  - `templates/`: HTML templates

### `smartdoc.utils`
- **Purpose**: Project-wide utilities
- **Components**:
  - `logger.py`: System logging
  - `exceptions.py`: Custom exception classes

### `smartdoc.config`
- **Purpose**: Configuration management
- **Components**:
  - `settings.py`: Application settings and environment variables

## Migration Summary

| Old Location | New Location | Rationale |
|-------------|-------------|-----------|
| `services/llm_intent_classifier.py` | `ai/intent_classifier.py` | AI components separated from simulation logic |
| `services/intent_driven_disclosure.py` | `simulation/engine.py` | Core orchestrator belongs in simulation |
| `services/progressive_disclosure.py` | `simulation/state_manager.py` | State management is core simulation functionality |
| `utils/bias_evaluator.py` | `simulation/bias_analyzer.py` | Bias detection is domain logic, not utility |
| `utils/session_logger.py` | `simulation/session_tracker.py` | Session tracking is simulation functionality |
| `/static/` | `web/static/` | Frontend assets belong with web interface |
| `/templates/` | `web/templates/` | Templates belong with web interface |

## Benefits of New Structure

1. **Clear Separation of Concerns**: Each module has a well-defined responsibility
2. **Professional Organization**: Structure follows industry best practices
3. **Dissertation Quality**: Easy to explain and document the architecture
4. **Maintainability**: Related components are grouped together
5. **Scalability**: Easy to add new features within appropriate modules
6. **Import Clarity**: Import paths clearly indicate component relationships

## Import Examples

```python
# AI components
from smartdoc.ai.intent_classifier import LLMIntentClassifier

# Simulation components
from smartdoc.simulation.engine import IntentDrivenDisclosureManager
from smartdoc.simulation.state_manager import ProgressiveDisclosureManager
from smartdoc.simulation.bias_analyzer import BiasEvaluator
from smartdoc.simulation.session_tracker import get_current_session

# Web components
from smartdoc.web.app import app

# Utilities
from smartdoc.utils.logger import sys_logger
from smartdoc.utils.exceptions import SmartDocError

# Configuration
from smartdoc.config.settings import config
```

This structure is now ready for dissertation documentation and professional presentation.
