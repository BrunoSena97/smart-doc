# SmartDoc Deployment Guide

## 🎯 **Traefik Integration Setup**

SmartDoc is now configured for deployment behind **Traefik** reverse proxy on `https://mestrados.logimade.com`.

### 📋 **Deployment Checklist**

1. **Copy to deployment machine**:

   ```bash
   cd /workspace
   git clone https://github.com/BrunoSena97/smart-doc.git
   cd smart-doc/deployments
   ```

2. **Deploy the application**:

   ```bash
   make deploy
   # OR manually:
   docker compose up --build -d
   ```

3. **Verify deployment**:
   ```bash
   ./health-check.sh
   # OR comprehensive tests:
   make test-deployment
   ```

### 🏗️ **Architecture Overview**

```
Internet → Traefik (HTTPS) → Nginx (Port 8000) → Flask API (Internal)
           ↓
       mestrados.logimade.com
```

- **External Access**: `https://mestrados.logimade.com` (handled by Traefik)
- **Internal Architecture**: Nginx serves static files + proxies `/api/*` to Flask
- **Single Port**: Only port 8000 exposed (Traefik requirement)
- **Database**: SQLite persisted in `/data/smartdoc.sqlite3` volume

### ⚙️ **Configuration Files**

| File                    | Purpose                                            |
| ----------------------- | -------------------------------------------------- |
| `compose.yaml`          | Single-port Docker Compose for Traefik integration |
| `docker/web.nginx.conf` | Nginx config listening on port 8000                |
| `docker/api.Dockerfile` | Production-ready Flask API with Gunicorn           |
| `health-check.sh`       | Quick deployment verification                      |
| `test_deployment.py`    | Comprehensive testing script                       |

### 🔧 **Key Features**

- ✅ **Traefik Compatible**: Single port 8000 exposure
- ✅ **HTTPS Ready**: Traefik handles SSL termination
- ✅ **Production Grade**: Gunicorn WSGI server with health checks
- ✅ **Persistent Database**: SQLite volume at `/data/smartdoc.sqlite3`
- ✅ **Automatic Migrations**: Alembic runs on container startup
- ✅ **Admin Interface**: Full admin panel at `/admin.html`
- ✅ **API Proxy**: All `/api/*` calls routed through Nginx

### 🏥 **Health Monitoring**

```bash
# Quick health check
./health-check.sh

# Comprehensive testing
make test-deployment

# View logs
docker compose logs -f api
docker compose logs -f web

# Container status
docker compose ps
```

### 🐞 **Troubleshooting**

1. **Check container status**: `docker compose ps`
2. **View logs**: `docker compose logs api web`
3. **Test internal API**: `docker compose exec api curl http://localhost:8000/healthz`
4. **Database access**: `docker compose exec api sqlite3 /data/smartdoc.sqlite3 ".tables"`
5. **Restart services**: `docker compose restart`

### 📊 **Expected URLs**

- **Public**: `https://mestrados.logimade.com` → Main application
- **Admin**: `https://mestrados.logimade.com/admin.html` → Admin interface
- **API**: `https://mestrados.logimade.com/api/v1/health` → API health check

### 🔒 **Security Notes**

- Flask API is **internal only** (not directly accessible)
- All traffic flows through Nginx proxy
- Security headers configured in Nginx
- Non-root container user
- CORS properly configured for production
