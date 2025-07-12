# SmartDoc: Hybrid AI System for Virtual Standardized Patient Interactions

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.0%2B-green.svg)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/License-Academic-orange.svg)](LICENSE)

> A dissertation project combining rule-based dialogue management with Large Language Model based natural language generation for medical education.

## 🎯 Project Overview

SmartDoc is an innovative hybrid AI system designed to create realistic virtual standardized patient interactions for medical education. The system combines the reliability of rule-based dialogue management with the natural language capabilities of modern Large Language Models (LLMs).

### Key Features
- **Hybrid Architecture**: Rule-based dialogue flow with LLM-powered responses
- **Medical Education Focus**: Specifically designed for clinical interview training
- **Multi-language Support**: Handles language barriers in patient interactions
- **Bias Detection**: Built-in research capabilities for educational bias analysis
- **Real-time Web Interface**: User-friendly Flask-based web application

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     SmartDoc System                        │
├─────────────────────────────────────────────────────────────┤
│  Student Input → NLU → Dialogue Manager → Knowledge Base   │
│                   ↓                                         │
│  Web Interface ← NLG ← Response Generation ← Information    │
│                   ↓                                         │
│              System Logger (Research Data)                 │
└─────────────────────────────────────────────────────────────┘
```

### Technical Components
- **NLU Service**: SBERT (all-MiniLM-L6-v2) for intent recognition
- **Dialogue Manager**: Finite State Machine with 13 clinical interview states
- **Knowledge Base**: JSON-structured patient case data
- **NLG Service**: Ollama + Gemma 3 4B for natural response generation
- **Logging System**: Dual conversation/system logging for research analysis

## 📁 Project Structure

```
smart-doc/
├── 📄 main.py                    # Application entry point
├── 📄 requirements.txt           # Python dependencies
├── 📄 README.md                  # This file
├── 📂 data/                      # Organized data directory
│   ├── 📂 cases/                 # Patient case files
│   │   └── 📄 case01.json       # Elderly woman with heart failure
│   └── 📂 mappings/              # NLU intent mappings
│       └── 📄 case01_canonical_question_mappings.json
├── 📂 smartdoc/                  # Main Python package
│   ├── 📂 config/                # Configuration management
│   │   └── 📄 settings.py       # Centralized configuration
│   ├── 📂 core/                  # Core dialogue components
│   │   ├── 📄 dialogue_manager.py  # Main dialogue logic
│   │   ├── 📄 state_machine.py     # FSM states and transitions
│   │   └── 📄 intents.py           # Intent loading and processing
│   ├── 📂 services/              # AI and external services
│   │   ├── 📄 nlu.py            # Natural Language Understanding
│   │   ├── 📄 nlg.py            # Natural Language Generation
│   │   └── 📄 knowledge_manager.py  # Knowledge base operations
│   ├── 📂 utils/                 # Utility functions
│   │   ├── 📄 logger.py         # Comprehensive logging system
│   │   └── 📄 exceptions.py     # Custom exception hierarchy
│   └── 📂 web/                   # Web interface
│       └── 📄 app.py            # Flask application
├── 📂 static/                    # CSS and static assets
│   └── 📄 style.css
├── 📂 templates/                 # HTML templates
│   ├── 📄 index.html
│   └── 📄 error.html
└── 📂 docs/                      # Comprehensive documentation
    ├── 📄 technical-architecture.md
    ├── 📄 dissertation-structure.md
    └── 📄 methodology.md
```

## 🚀 Getting Started

### Prerequisites
- **Python**: 3.8 or higher
- **Ollama**: For LLM inference
- **Git**: For version control

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/BrunoSena97/smart-doc.git
   cd smart-doc
   ```

2. **Create virtual environment**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Ollama with Gemma model**
   ```bash
   # Install Ollama (see https://ollama.ai)
   ollama serve
   ollama pull gemma3:4b-it-q4_K_M
   ```

5. **Configure environment (optional)**
   ```bash
   cp .env.example .env
   # Edit .env file with your preferences
   ```

### Running the Application

```bash
python main.py
```

The web interface will be available at `http://localhost:5000`

## ⚙️ Configuration

SmartDoc uses a centralized configuration system with environment variable support:

| Variable | Default | Description |
|----------|---------|-------------|
| `SMARTDOC_FLASK_HOST` | `127.0.0.1` | Flask server host |
| `SMARTDOC_FLASK_PORT` | `5000` | Flask server port |
| `SMARTDOC_CASE_FILE` | `data/cases/case01.json` | Patient case data file |
| `SMARTDOC_CANONICAL_MAPPINGS_FILE` | `data/mappings/case01_canonical_question_mappings.json` | NLU mappings |
| `SMARTDOC_OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama server URL |
| `SMARTDOC_SBERT_MODEL` | `all-MiniLM-L6-v2` | SBERT model for NLU |
| `SMARTDOC_LOG_LEVEL` | `INFO` | System logging level |

## 🧪 Usage Example

1. **Start the application**
   ```bash
   python main.py
   ```

2. **Open browser** to `http://localhost:5000`

3. **Begin clinical interview**
   - Ask about patient history: *"What is the patient's chief complaint?"*
   - Explore symptoms: *"Tell me about the onset of shortness of breath"*
   - Review medications: *"What medications is she currently taking?"*
   - Request exam findings: *"What were the vital signs?"*

4. **System responds** as patient's son providing realistic medical information

## 🔬 Research Features

### Conversation Logging
- **Dual Logging**: Separate conversation and system logs
- **Research Data**: Detailed interaction tracking for bias analysis
- **Performance Metrics**: Response times, intent recognition accuracy

### Bias Detection Framework
- **Built-in Analytics**: Conversation pattern analysis
- **Educational Metrics**: Learning outcome tracking
- **Diagnostic Reasoning**: Critical thinking assessment

## 🏥 Medical Case: Elderly Woman with Heart Failure

The system includes a comprehensive medical case featuring:
- **Patient Profile**: Elderly, Spanish-speaking woman
- **Presentation**: Shortness of breath and cough
- **Complexity**: Multiple comorbidities (diabetes, hypertension, RA)
- **Learning Objectives**: Diagnostic reasoning, cultural sensitivity
- **Discoverable Information**: Critical details revealed through proper questioning

## 📚 Documentation

Comprehensive documentation is available in the `docs/` directory:
- **Technical Architecture**: System design and components
- **Dissertation Structure**: Academic framework and methodology
- **Literature Review**: Research background and related work
- **Project Timeline**: Development phases and milestones

## 🔧 Development

### Adding New Cases
1. Create new case file in `data/cases/`
2. Create corresponding mappings in `data/mappings/`
3. Update configuration to point to new files

### Extending Functionality
- **New Intents**: Add to canonical question mappings
- **New States**: Extend the finite state machine
- **New Services**: Add to `smartdoc/services/`

### Testing
```bash
# Test configuration loading
python -c "from smartdoc.config.settings import config; print('✅ Config loaded')"

# Test knowledge base
python -c "from smartdoc.services.knowledge_manager import KnowledgeBaseManager; kb = KnowledgeBaseManager(); print(f'✅ Case loaded: {kb.get_case_title()}')"

# Test NLU
python -c "from smartdoc.core.intents import canonical_question_mappings; print(f'✅ Loaded {len(canonical_question_mappings)} intents')"
```

## 📊 Performance

- **Response Time**: Target <2 seconds for user interactions
- **Accuracy**: 70%+ similarity threshold for intent matching
- **Scalability**: Stateless design supports horizontal scaling
- **Resource Usage**: Optimized for standard development hardware

## 🤝 Contributing

This is a dissertation project. For academic collaboration or questions:
- Review the technical documentation in `docs/`
- Check the methodology and research framework
- Contact the author for research collaboration

## 📄 License

This project is part of a Master's dissertation in Software Engineering. All rights reserved for academic purposes.

## 👨‍💻 Author

**Bruno Sena**
Master's in Software Engineering
*Hybrid AI Systems for Medical Education*

## 🙏 Acknowledgments

- **SBERT**: Sentence transformers for semantic understanding
- **Ollama**: Local LLM inference platform
- **Flask**: Web framework for user interface
- **Medical Education Community**: For use case validation

---

*This project represents a novel approach to medical education technology, combining the reliability of rule-based systems with the naturalness of modern language models.*
