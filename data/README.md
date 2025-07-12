# Data Directory

This directory contains all data files used by the SmartDoc system.

## Structure

```
data/
├── cases/                    # Patient case data
│   └── case01.json          # Elderly woman with heart failure case
└── mappings/                 # NLU intent mappings
    └── case01_canonical_question_mappings.json  # Intent mappings for case01
```

## Files Description

### Cases Directory (`cases/`)
Contains patient case data in JSON format. Each file represents a complete medical case with:
- Patient profile and demographics
- Medical history
- Present illness details
- Physical examination findings
- Laboratory and imaging results
- Discoverable information for educational progression

### Mappings Directory (`mappings/`)
Contains Natural Language Understanding (NLU) intent mappings in JSON format. These files define:
- Canonical questions that students might ask
- Variations of how questions can be phrased
- Actions to take when intents are recognized
- Expected dialogue states for each intent

## Adding New Data

### Adding a New Case
1. Create a new JSON file in `cases/` (e.g., `case02.json`)
2. Follow the same structure as `case01.json`
3. Update the configuration in `smartdoc/config/settings.py` if needed

### Adding New Intent Mappings
1. Create a new JSON file in `mappings/` (e.g., `case02_mappings.json`)
2. Follow the same structure as the existing mappings file
3. Update the configuration to point to the new file

## Configuration

The paths to these files are configured in `smartdoc/config/settings.py`:
- `CASE_FILE`: Points to the active case file
- `CANONICAL_MAPPINGS_FILE`: Points to the active mappings file

These can be overridden using environment variables:
- `SMARTDOC_CASE_FILE`
- `SMARTDOC_CANONICAL_MAPPINGS_FILE`
