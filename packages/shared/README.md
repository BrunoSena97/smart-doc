# SmartDoc Shared Package

Shared schemas, types, and client libraries used across SmartDoc applications.

## Overview

This package contains common components shared between the SmartDoc API and core packages:
- Pydantic schemas for data validation
- Type definitions
- Client libraries
- Common utilities

## Installation

```bash
pip install -e .
```

## Usage

```python
from smartdoc_shared.schemas import PatientInfo
from smartdoc_shared.clients import OllamaClient
```
