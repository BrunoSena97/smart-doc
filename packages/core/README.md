# SmartDoc Core Package

Core AI and domain logic for the SmartDoc virtual patient simulation platform.

## Overview

This package contains the fundamental AI components that power SmartDoc:
- Intent classification for clinical queries
- Discovery processing for progressive information disclosure
- Clinical evaluation and bias detection
- Simulation engines and state management

## Components

### Intent Classification (`smartdoc_core.intent`)
- LLM-based classification of doctor queries into clinical intents
- Context-aware filtering for different clinical phases
- Ollama integration for natural language understanding

### Discovery Processing (`smartdoc_core.discovery`)
- Progressive revelation of clinical information
- Intent-to-information mapping
- Dynamic content generation

### Clinical Evaluation (`smartdoc_core.clinical`)
- Cognitive bias detection and analysis
- Clinical reasoning assessment
- Educational feedback generation

### Simulation Engine (`smartdoc_core.simulation`)
- Intent-driven disclosure management
- Session state tracking
- Bias trigger monitoring
- Educational outcome measurement

## Installation

```bash
pip install -e .
```

For development:
```bash
pip install -e .[dev]
```

## Usage

```python
from smartdoc_core import IntentClassifier, DiscoveryProcessor

# Initialize components
classifier = IntentClassifier()
processor = DiscoveryProcessor()

# Classify clinical query
result = classifier.classify_intent("What's the patient's blood pressure?", context="exam")
```

## Configuration

The package uses the centralized configuration system from `smartdoc_core.config.settings`.

## Testing

```bash
pytest tests/
```
