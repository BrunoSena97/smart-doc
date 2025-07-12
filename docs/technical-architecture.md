# Technical Architecture Documentation

## System Overview

SmartDoc is a hybrid AI system that combines rule-based dialogue management with Large Language Model (LLM) based natural language generation to create realistic virtual standardized patient interactions.

## Architecture Components

### 1. Natural Language Understanding (NLU) Service
- **Technology**: Sentence-BERT (all-MiniLM-L6-v2)
- **Purpose**: Intent recognition and entity extraction from student queries
- **Input**: Free-text student questions
- **Output**: Structured intent with confidence scores

### 2. Knowledge Base Manager
- **Technology**: JSON-based structured data
- **Purpose**: Store and retrieve patient case information
- **Features**: Nested data access, discoverable information mechanism
- **Extensibility**: Easy addition of new clinical cases

### 3. Dialogue Manager
- **Technology**: Finite State Machine
- **Purpose**: Control conversation flow and state transitions
- **States**: 13 clinical interview phases (Introduction → Closing)
- **Logic**: Rule-based state transitions with context awareness

### 4. Natural Language Generation (NLG) Service
- **Technology**: Ollama + Gemma 3 4B model
- **Purpose**: Generate natural, contextual responses as patient's son
- **Features**: Persona consistency, fallback responses, retry mechanisms
- **Prompt Engineering**: Tailored prompts for medical context

### 5. System Logger
- **Technology**: Custom logging framework
- **Purpose**: Capture interaction data for research analysis
- **Data**: Conversation logs, system logs, performance metrics
- **Analysis**: Support for bias detection and learning analytics

### 6. Web Interface
- **Technology**: Flask web framework
- **Purpose**: User-friendly interface for students
- **Features**: Real-time chat, error handling, health monitoring
- **Accessibility**: Responsive design, error recovery

## Project Structure

SmartDoc follows a professional Python package structure:

```
smart-doc/
├── main.py                    # Main entry point
├── requirements.txt           # Python dependencies
├── data/                     # Data files (NEW: Organized data directory)
│   ├── cases/
│   │   └── case01.json       # Patient case data
│   └── mappings/
│       └── case01_canonical_question_mappings.json  # NLU intent mappings
├── smartdoc/                 # Main package
│   ├── config/               # Configuration management
│   │   └── settings.py       # Centralized configuration
│   ├── core/                 # Core dialogue components
│   │   ├── dialogue_manager.py  # Main dialogue logic
│   │   ├── state_machine.py     # FSM states and transitions
│   │   └── intents.py           # Intent mappings and data
│   ├── services/             # AI and external services
│   │   ├── nlu.py            # Natural Language Understanding
│   │   ├── nlg.py            # Natural Language Generation
│   │   └── knowledge_manager.py  # Knowledge base management
│   ├── utils/                # Utility functions
│   │   ├── logger.py         # Logging system
│   │   └── exceptions.py     # Custom exceptions
│   └── web/                  # Web interface
│       └── app.py            # Flask application
├── static/                   # CSS and static files
├── templates/                # HTML templates
└── docs/                     # Documentation
```

## Data Flow

```
Student Input → NLU Service → Dialogue Manager → Knowledge Base Manager
                                     ↓
Web Interface ← NLG Service ← Response Generation ← Retrieved Information
                                     ↓
                              System Logger (for research)
```

## Key Design Decisions

### Hybrid Architecture
- **Rationale**: Combine reliability of rule-based systems with flexibility of LLMs
- **Benefits**: Predictable behavior with natural language capabilities
- **Trade-offs**: Increased complexity for better educational outcomes

### SBERT for Intent Recognition
- **Rationale**: Better semantic understanding than keyword matching
- **Benefits**: Handles paraphrasing and varied question formats
- **Performance**: 70% similarity threshold for intent matching

### Finite State Machine for Dialogue
- **Rationale**: Structured clinical interview flow
- **Benefits**: Ensures coverage of all clinical areas
- **Flexibility**: Allows state transitions based on student queries

### JSON Knowledge Base
- **Rationale**: Structured, readable, and easily extensible
- **Benefits**: Clear data organization, version control friendly
- **Scalability**: Simple addition of new cases and information

## Configuration Management

Centralized configuration system using environment variables and defaults:
- Model parameters (SBERT model, similarity thresholds)
- LLM settings (Ollama model, temperature, token limits)
- System settings (retry policies, fallback options)
- Deployment settings (ports, hosts, debug modes)

## Error Handling Strategy

Multi-level error handling approach:
1. **Component Level**: Each service handles its own errors
2. **System Level**: Graceful degradation when services fail
3. **User Level**: Informative error messages and recovery options
4. **Fallback Systems**: Continue operation when possible

## Performance Considerations

- **Response Time**: Target <2 seconds for user interactions
- **Scalability**: Stateless design for horizontal scaling
- **Resource Usage**: Optimized for standard development hardware
- **Caching**: Embeddings cached for better NLU performance

## Security and Privacy

- **Data Protection**: No persistent storage of student conversations
- **Access Control**: Health check endpoints for monitoring
- **Input Validation**: Sanitization of all user inputs
- **Error Disclosure**: Minimal error information in production

## Extensibility Features

- **New Cases**: Simple JSON addition for new clinical scenarios
- **New Models**: Configurable model selection for NLU and NLG
- **New Intents**: Easy expansion of canonical question mappings
- **New States**: Extensible FSM for different interview types

## Monitoring and Analytics

- **Health Checks**: System component status monitoring
- **Performance Metrics**: Response times, error rates, usage patterns
- **Research Data**: Detailed conversation logs for bias analysis
- **Debug Information**: Configurable debug output for development

## Deployment Architecture

- **Development**: Local deployment with Ollama
- **Production**: Containerized deployment option
- **Configuration**: Environment-based configuration management
- **Monitoring**: Health endpoints and logging integration
