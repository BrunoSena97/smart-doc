# SmartDoc

> Advanced AI-Powered Clinical Simulation Platform for Medical Education

[![Python](https://img.shields.io/badge/Python-3.13%2B-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.1.1-green.svg)](https://flask.palletsprojects.com)
[![LLM](https://img.shields.io/badge/LLM-Ollama-orange.svg)](https://ollama.ai)
[![Architecture](https://img.shields.io/badge/Architecture-Monorepo-blue.svg)](https://monorepo.tools)

SmartDoc is a comprehensive master's thesis project featuring advanced AI systems for medical education with professional monorepo architecture, including LLM-powered discovery, cognitive bias detection, and metacognitive assessment.

## 🚀 Quick Start

```bash
# Set up development environment
make setup

# Start development servers
make api    # API server
make web    # Frontend server

# Run tests
make test   # All tests
make test-integration  # Integration tests
```

## 📚 Documentation

**Complete documentation is available in the [`docs/`](docs/) directory:**

- **[📖 Main Documentation](docs/README.MD)** - Comprehensive project overview and features
- **[🚀 Development Guide](docs/development/DEVELOPMENT.md)** - Setup and development instructions
- **[🏗️ Architecture](docs/architecture/)** - System architecture and diagrams
- **[🐳 Deployment](docs/deployment/DEPLOYMENT.md)** - Production deployment guide
- **[📋 Project Updates](docs/project/CLEANUP_SUMMARY.md)** - Recent structural improvements

**Quick Links:**

- [Documentation Index](docs/INDEX.md) - Navigation guide for all documentation
- [Test Organization](tests/README.md) - Testing structure and commands
- [Development Tools](dev-tools/README.md) - Debug and development utilities

## 🏗️ Project Structure

```
SmartDoc/
├── apps/                    # Applications
│   ├── api/                # Flask API backend
│   └── web/                # Static frontend
├── packages/               # Core packages
│   ├── core/              # SmartDoc core engine
│   └── shared/            # Shared utilities
├── tests/                 # Organized test suite
│   ├── integration/       # System tests
│   └── frontend/         # Demo scripts
├── dev-tools/             # Development utilities
├── docs/                  # Documentation
│   ├── architecture/      # System design
│   ├── development/       # Dev guides
│   ├── deployment/        # Deployment guides
│   └── project/          # Project status
├── configs/               # Configuration files
└── deployments/          # Docker deployment
```

## ✨ Key Features

- **🧠 LLM-Powered Progressive Disclosure** - Context-aware information revelation
- **🎯 Intent Classification** - Advanced query understanding
- **⚖️ Cognitive Bias Detection** - Real-time bias identification
- **📊 Metacognitive Assessment** - Learning evaluation
- **🏥 Clinical Simulation** - Realistic patient interactions
- **🔄 Escalation System** - Dynamic information complexity

## 🧪 Testing

SmartDoc includes comprehensive testing with proper Poetry environment handling:

```bash
# Test by category
make test-core          # Core package tests
make test-api-unit      # API package tests
make test-integration   # Integration tests
make test-frontend      # Demo scripts

# Test specific files
make test-file FILE=tests/integration/test_medication_escalation_flow.py
```

## 🛠️ Development

For complete development setup instructions, see [Development Guide](docs/development/DEVELOPMENT.md).

### Prerequisites

- Python 3.13+
- Poetry
- Ollama with `gemma3:4b-it-q4_K_M` model

### Quick Setup

```bash
# Install dependencies
make setup

# Start development
make api-dev    # Development API server
make web        # Static frontend server
```

## 🚀 Deployment

For production deployment instructions, see [Deployment Guide](docs/deployment/DEPLOYMENT.md).

```bash
# Development deployment
make dev-docker

# Production deployment
make deploy
```

## 📄 License

Academic use license. See project documentation for details.

## 🤝 Contributing

This is a master's thesis project. For contribution guidelines and project structure details, see the [documentation](docs/).

---

**For complete documentation, visit [`docs/`](docs/) directory.**
