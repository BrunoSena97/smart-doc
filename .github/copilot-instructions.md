---
applyTo: "**"
---

# SmartDoc – Copilot Instructions

## Project Overview

SmartDoc is an AI-powered clinical simulation platform built as a professional monorepo featuring:

- **Flask API** (apps/api) – REST endpoints with v1/v2 versioning and legacy compatibility
- **Vanilla Web UI** (apps/web/public) – Static HTML/CSS/JS (ES modules, no build step) for medical education
- **Core AI Engine** (packages/core) – LLM-powered progressive disclosure, intent classification, and clinical evaluation
- **Shared Libraries** (packages/shared) – Cross-cutting schemas, clients, and utilities
- **Comprehensive Testing** (tests/) – Integration tests, frontend demos, and development tools
- **Professional Documentation** (docs/) – Organized by architecture, development, deployment, and project status

## Key Simplifications Made

**EVALUATION SYSTEM** - We removed the complex research coordinator and simplified to:

- **Single LLM Evaluator** - `ClinicalEvaluator` with quality checks and strict scoring
- **Main Endpoint** - `/api/v1/diagnosis/reflection` for diagnosis submission with metacognitive reflection
- **Quality Detection** - Automatic detection of poor responses (nonsense answers, spelling errors) with appropriate low scores
- **Simplified Schema** - Three core areas: information_gathering, diagnostic_accuracy, cognitive_bias_awareness

The evaluation now correctly handles poor quality responses by giving very low scores (5-20/100) instead of being overly generous.

## Tech Stack & Architecture (MUST follow)

### **Backend**

- **Python 3.13+** managed with **Poetry** (`pyproject.toml` + `poetry.lock`) per package
- **Flask** with app factory pattern (`create_app`) and **blueprints**:
  - Modern API at `/api/v1/` and `/api/v2/` from `apps/api/src/smartdoc_api/routes/`
  - **Legacy endpoints** at root (no prefix) from `routes/legacy.py` for backward compatibility
- **Ollama LLM Integration** with `gemma3:4b-it-q4_K_M` model for intent classification and clinical reasoning
- **SQLite/PostgreSQL** with Alembic migrations for persistent data
- **Pydantic** for request/response validation and data schemas

### **Frontend**

- **Pure static** served via `python -m http.server` (no webpack/Vite/React)
- **ES modules** architecture under `apps/web/public/js/**`
- **Relative paths** for all assets `./assets/...`
- **Modular UI components** in `js/ui/` with centralized state management

### **Core AI Engine**

- **Progressive Disclosure System** – Intent-driven information revelation with escalation levels
- **LLM Intent Classification** – 30+ clinical intents with context-aware processing
- **Cognitive Bias Detection** – Real-time identification of anchoring, confirmation bias, premature closure
- **Clinical Evaluation** – Metacognitive assessment with structured JSON output
- **Simulation Engine** – Session management with bias analysis and critical finding tracking

## Monorepo Structure

```
SmartDoc/
├── apps/
│   ├── api/src/smartdoc_api/          # Flask API application
│   │   ├── __init__.py                # create_app + CORS + blueprints
│   │   ├── main.py                    # dev entrypoint
│   │   ├── routes/                    # API route modules (thin controllers)
│   │   │   ├── __init__.py           # v1 blueprint registration
│   │   │   ├── chat.py               # Chat/simulation endpoints
│   │   │   ├── diagnosis.py          # Diagnostic endpoints
│   │   │   ├── evaluation.py         # Clinical evaluation endpoints
│   │   │   ├── simulation.py         # Simulation management
│   │   │   └── legacy.py             # Legacy compatibility
│   │   └── services/                  # Business logic orchestration
│   └── web/public/                   # Static frontend
│       ├── index.html, admin.html    # Main interfaces
│       ├── js/                       # ES modules
│       │   ├── config.js, api.js     # Configuration and API layer
│       │   ├── state.js, main.js     # State management and app init
│       │   └── ui/                   # UI components (chat, results, tabs)
│       ├── styles/main.css           # Styling
│       └── assets/                   # Images and static assets
├── packages/
│   ├── core/src/smartdoc_core/       # Core AI engine
│   │   ├── clinical/                 # Clinical evaluation and bias detection
│   │   ├── discovery/                # Progressive disclosure engine
│   │   ├── intent/                   # LLM intent classification
│   │   ├── llm/                      # LLM provider abstractions
│   │   ├── simulation/               # Session management and simulation
│   │   └── utils/                    # Core utilities and logging
│   └── shared/src/smartdoc_shared/   # Shared libraries
│       ├── schemas/                  # Pydantic models
│       └── clients/                  # External service clients
├── tests/                            # Organized test suite
│   ├── integration/                  # End-to-end system tests
│   │   ├── test_medication_escalation_flow.py
│   │   ├── test_imaging_escalation_flow.py
│   │   └── test_labs_specific_intents.py
│   └── frontend/                     # Educational demo scripts
│       ├── test_correct_diagnosis_path.py
│       └── test_biased_diagnosis_path.py
├── dev-tools/                        # Development utilities
│   ├── debug_lab_intent.py          # Intent classification debugging
│   ├── check_intents.py              # Intent mapping validation
│   └── manual_testing_scenarios.py   # API testing scenarios
├── docs/                             # Professional documentation
│   ├── architecture/                # System design and diagrams
│   ├── development/                  # Development guides
│   ├── deployment/                   # Production deployment
│   └── project/                      # Project status and updates
├── configs/{default,dev,prod}.yaml   # Environment configurations
└── data/raw/cases/                   # Clinical case definitions
```

## Dependencies & Development Commands

### **Setup & Installation**

```bash
# Complete environment setup
make setup                    # Sets up all Poetry environments

# Individual package installation
cd packages/core && poetry install
cd apps/api && poetry install
```

### **Development Servers**

```bash
# API servers (choose one)
make api                      # Standard Flask server
make api-dev                  # Development server with mock data
make api-flask                # Flask CLI with debug mode
make api-gunicorn             # Production-like Gunicorn server

# Frontend server
make web                      # Static file server on port 3000

# Health checks
make health-check             # API health verification
```

### **Testing (NEW Comprehensive System)**

```bash
# Complete test suite
make test                     # All tests (core + API + integration)

# By category
make test-core                # Core package unit tests
make test-api-unit            # API package unit tests
make test-integration         # Integration tests (medication, imaging, labs)
make test-frontend            # Frontend demo scripts (correct vs biased diagnosis)
make test-dev                 # Development tools validation

# Specific test files
make test-file FILE=tests/integration/test_medication_escalation_flow.py
make test-file FILE=tests/frontend/test_correct_diagnosis_path.py
make test-file FILE=dev-tools/check_intents.py
```

### **Code Quality**

```bash
make format                   # Format code with Black
make lint                     # Lint with Ruff
make type-check               # Type checking with MyPy
make check                    # All quality checks + tests
```

## Core AI System Understanding

### **Progressive Disclosure Engine**

- **Information Blocks** organized by `groupId`, `level`, and `prerequisites`
- **Intent-driven revelation** based on LLM classification of clinical queries
- **Escalation levels** for medications (3 levels), imaging (2 levels), labs (individual)
- **Critical findings** tracking for diagnostic completeness assessment

### **Intent Classification System**

- **30+ clinical intents** covering anamnesis, examination, labs, imaging, medications
- **Context-aware processing** (anamnesis, exam, labs contexts)
- **LLM-powered classification** with fallback keyword matching
- **Enhanced accuracy** with comprehensive examples and improved categories

### **Cognitive Bias Detection**

- **Anchoring bias** – persistence in initial hypotheses despite contradictory evidence
- **Confirmation bias** – seeking only supporting evidence, ignoring refuting information
- **Premature closure** – stopping investigation too early before adequate information gathering
- **Real-time detection** with session analysis and metacognitive feedback

### **Clinical Evaluation (Simplified)**

- **Single Evaluator** – `ClinicalEvaluator` class handles all evaluation logic
- **Quality Detection** – Automatic detection of poor responses with appropriate low scoring
- **Three Core Areas** – Information gathering, diagnostic accuracy, cognitive bias awareness
- **Strict Scoring** – Most students score 20-60, excellent students 70-90, perfect 90+
- **Main API Endpoint** – `/api/v1/diagnosis/reflection` for diagnosis + reflection evaluation

## Coding Standards & Best Practices

### **Backend Development**

- Keep **routes thin** – business logic belongs in `packages/core` or `services/`
- Use **Pydantic models** for all request/response shapes in `packages/shared/schemas`
- Implement **path-agnostic file access** using `Path(__file__).resolve().parents[...]`
- Follow **async/await patterns** for LLM operations and external API calls
- Use **structured logging** with context and correlation IDs

### **Frontend Development**

- **One responsibility per module** – no inline `<script>` in HTML files
- **ES modules only** – no global jQuery or framework dependencies
- **Centralized API layer** – all backend calls through `js/api.js`
- **State management** in `js/state.js` with event-driven updates
- **Absolute API URLs** from `js/config.js` configuration

### **AI System Development**

- **Context-aware prompts** with specific examples for each clinical domain
- **Fallback strategies** for LLM failures (keyword matching, default responses)
- **Session state management** with proper cleanup and error handling
- **Bias detection thresholds** tuned for educational value vs accuracy
- **Progressive disclosure prerequisites** properly validated before revelation

## File Organization & Naming

### **Python**

- Packages: `snake_case` (smartdoc_core, smartdoc_shared)
- Modules: `snake_case.py` (intent_classifier.py, bias_analyzer.py)
- Classes: `CamelCase` (IntentDrivenDisclosureManager, ClinicalEvaluator)
- Functions/variables: `snake_case`

### **Frontend**

- Directories: lowercase (ui, assets)
- Files: `kebab-case.js` (except main.js)
- Components: descriptive names (chat.js, results.js, patient-info.js)

### **Tests**

- Mirror source structure with `test_` prefix
- Integration tests: `test_[domain]_escalation_flow.py`
- Frontend demos: `test_[type]_diagnosis_path.py`
- Development tools: descriptive names for debugging

### **Documentation**

- Organized by category in `docs/` subdirectories
- README.md in each directory explaining purpose
- PlantUML diagrams for architecture documentation

## When Adding NEW API Endpoints (CRITICAL)

1. **Create/extend route module** in `apps/api/src/smartdoc_api/routes/`
2. **Register on v1/v2 blueprint** with proper versioning (`from . import bp`)
3. **Validate input** with Pydantic models from `packages/shared/schemas`
4. **Orchestrate logic** via `services/` that call `packages/core` functions
5. **Return structured JSON** – never HTML from `/api/v1/*` or `/api/v2/*`
6. **Add comprehensive test** in `apps/api/tests/` covering success/error cases
7. **Update frontend API layer** in `apps/web/public/js/api.js` if consumed by UI
8. **Maintain legacy compatibility** – ensure existing `/get_bot_response` and `/chat` still work
9. **Document in appropriate docs/** folder if behavior changes

## When Adding NEW Frontend Features

1. **Create UI component** in `apps/web/public/js/ui/<feature>.js`
2. **Update state management** in `js/state.js` for new data/events
3. **Add API integration** in `js/api.js` with proper error handling
4. **Wire component** from `js/main.js` with proper initialization
5. **Add assets** to `apps/web/public/assets/` with relative path references
6. **Maintain ES module architecture** – no global variables or inline scripts
7. **Test across different clinical scenarios** for educational effectiveness

## When Working with AI Systems

### **Intent Classification**

- **Add new intents** to both case file and classifier with comprehensive examples
- **Test classification accuracy** using `dev-tools/check_intents.py`
- **Maintain context-specific intent availability** (anamnesis vs exam vs labs)
- **Validate fallback keyword matching** for critical clinical terms

### **Progressive Disclosure**

- **Design escalation patterns** based on clinical workflow and educational value
- **Set appropriate prerequisites** to ensure logical information revelation
- **Test complete disclosure flows** using integration tests
- **Balance educational pacing** with realistic clinical information access

### **Bias Detection**

- **Tune detection thresholds** for educational effectiveness without false positives
- **Implement bias-specific logic** for anchoring, confirmation, and premature closure
- **Provide educational feedback** that explains bias mechanisms and prevention
- **Track session patterns** to identify bias development over time

## Critical Don'ts

- **NO bundlers or frameworks** (webpack, Vite, React) – maintain static architecture
- **NO breaking legacy endpoints** – `/get_bot_response` and `/chat` must always work
- **NO direct core imports** in frontend – `packages/core` is server-side only
- **NO test files outside designated areas** – use `tests/`, `packages/*/tests/`, `dev-tools/`
- **NO documentation outside docs/** – maintain organized documentation structure
- **NO hardcoded paths** – use relative paths and Path objects for cross-platform compatibility
- **NO global state pollution** – maintain modular ES module architecture
- **NO LLM calls without fallback** – always implement graceful degradation strategies

## Definition of Done (Comprehensive PR Checklist)

### **Code Quality**

- [ ] All endpoints registered on appropriate `/api/v1/` or `/api/v2/` blueprint
- [ ] Comprehensive tests added in appropriate test directories
- [ ] Passes `make check` (format, lint, type-check, and all tests)
- [ ] No broken legacy endpoints (`/get_bot_response`, `/chat` still functional)
- [ ] Frontend uses `js/api.js` exclusively for backend communication

### **AI System Integration**

- [ ] Intent classification tested and validated for new clinical scenarios
- [ ] Progressive disclosure flows tested end-to-end with integration tests
- [ ] Bias detection properly calibrated and educationally effective
- [ ] LLM prompts tested with fallback strategies for failure cases

### **Documentation & Organization**

- [ ] Documentation updated in appropriate `docs/` subdirectory
- [ ] Configuration changes reflected in environment files
- [ ] Test organization maintained (integration vs frontend vs dev-tools)
- [ ] Relative paths used throughout for cross-platform compatibility

### **Educational Effectiveness**

- [ ] Clinical scenarios provide realistic medical education value
- [ ] Bias demonstration clear and pedagogically sound
- [ ] Information revelation follows logical clinical workflow
- [ ] Metacognitive feedback constructive and specific

---

**SmartDoc represents the cutting edge of AI-powered medical education. Maintain the high standards of code quality, educational effectiveness, and professional architecture that make this system exceptional.**
