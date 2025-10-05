# Development Tools

This directory contains development and debugging utilities for SmartDoc.

## Tools Available

### Debugging Scripts

- `debug_lab_intent.py` - Debug lab intent classification issues
- `check_intents.py` - Verify intent classification mappings
- `test_enhanced_intents.py` - Test enhanced intent classification features
- `test_ra_query.py` - Debug specific RA medication queries

### Testing Utilities

- `manual_testing_scenarios.py` - Manual API testing scenarios for evaluation system

## Usage

These tools are intended for:

- **Development debugging** - Troubleshooting specific issues
- **Intent classification testing** - Verifying LLM classification accuracy
- **Manual testing** - API endpoint validation
- **System validation** - Checking specific functionality

## Running Development Tools

```bash
# Run intent debugging
cd dev-tools
python debug_lab_intent.py
python check_intents.py

# Test enhanced features
python test_enhanced_intents.py
python test_ra_query.py

# Manual API testing
python manual_testing_scenarios.py
```

## Notes

- These tools are for development use only
- They may contain hardcoded paths or test data
- Not intended for production use
- Use for debugging and validation during development
