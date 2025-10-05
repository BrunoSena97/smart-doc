# Deployment Documentation

This directory contains deployment guides and production setup documentation.

## Files

- **`DEPLOYMENT.md`** - Complete deployment guide
  - Docker setup and configuration
  - Production deployment with Traefik
  - Environment configuration
  - Health checks and monitoring

## Quick Deployment

```bash
# Development deployment
make dev-docker

# Production deployment
make deploy

# Health check
make deploy-health
```

For detailed instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).
