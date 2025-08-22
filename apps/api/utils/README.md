# SmartDoc API Utilities

This directory contains utility scripts for database management and system administration.

## Scripts

- `seed_admin_data.py` - Seeds default admin user and LLM profiles
- `query_users.py` - Query and manage users in the database

## Usage

These scripts are automatically copied into the Docker container and can be run as:

```bash
# Seed admin data
docker compose exec smartdoc poetry run python seed_admin_data.py

# Query users
docker compose exec smartdoc poetry run python query_users.py

# Create test user
docker compose exec smartdoc poetry run python query_users.py create "Name" "email@example.com"
```
