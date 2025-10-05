# SmartDoc Tests

This directory contains all test files for the SmartDoc project, organized by type and purpose.

## Directory Structure

### `integration/`

Contains comprehensive integration tests that test the full system behavior:

- `test_medication_escalation_flow.py` - Tests complete medication progressive disclosure
- `test_imaging_escalation_flow.py` - Tests complete imaging progressive disclosure
- `test_labs_specific_intents.py` - Tests complete lab value disclosure

### `frontend/`

Contains test scripts designed for frontend demonstration and validation:

- `test_correct_diagnosis_path.py` - Demonstrates ideal clinical workflow
- `test_biased_diagnosis_path.py` - Demonstrates diagnostic errors and cognitive biases

## Running Tests

### Using Makefile (Recommended)

```bash
# Run all integration tests
make test-integration

# Run frontend demonstration scripts
make test-frontend

# Run specific test file
make test-file FILE=tests/integration/test_medication_escalation_flow.py
make test-file FILE=tests/frontend/test_correct_diagnosis_path.py

# Run complete test suite (unit + integration)
make test
```

### Direct Execution (Advanced)

```bash
# Integration tests (run from core package environment)
cd packages/core && poetry run python ../../tests/integration/test_medication_escalation_flow.py

# Frontend tests (run from core package environment)
cd packages/core && poetry run python ../../tests/frontend/test_correct_diagnosis_path.py
```

## Test Organization

- **Unit Tests**: Located in `packages/*/tests/` directories
- **Integration Tests**: Located in `tests/integration/`
- **Frontend Tests**: Located in `tests/frontend/`
- **Development Tools**: Located in `dev-tools/`

## Notes

- All tests use the main case file: `data/raw/cases/intent_driven_case.json`
- Integration tests verify the complete progressive disclosure system
- Frontend tests are designed for demonstration and educational purposes
- Each test directory contains focused, well-documented test scripts
