# Development Documentation

This directory contains development guides and setup instructions for SmartDoc.

## Files

- **`DEVELOPMENT.md`** - Comprehensive development setup guide

  - Environment setup with Poetry
  - Local vs Docker development
  - Testing and debugging
  - Code formatting and linting

- **`session-management.md`** - Complete session management documentation

  - Admin authentication with never-expiring tokens
  - Comprehensive session persistence and restoration
  - Implementation details and testing guides
  - Troubleshooting common issues

- **`session-management-quick-reference.md`** - Quick reference for developers
  - Admin credentials and setup
  - Session restoration commands
  - Database queries and cleanup
  - Implementation checklists

## Quick Start

For complete development setup instructions, see [DEVELOPMENT.md](DEVELOPMENT.md).

```bash
# Quick setup
make setup
make api  # Start development server
make web  # Start frontend server
```

## Admin Access

Default admin credentials for development:

```
Access Code: #Admin13
Features: Never-expiring token, unlimited usage
```

For complete session management details, see [session-management.md](session-management.md).
