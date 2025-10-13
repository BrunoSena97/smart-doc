# Database Backup & Recovery Guide

## Overview

SmartDoc uses SQLite for data persistence, stored in a Docker volume. This guide covers multiple methods for backing up and restoring your database.

## Database Location

- **Inside Container**: `/data/smartdoc.sqlite3`
- **Docker Volume**: `smartdoc_data`
- **Tables**: users, conversations, messages, evaluations, simulations

---

## ⭐ Method 1: Admin Panel Download (Easiest - Recommended)

**Use when**: You need to download the database from a deployed instance via the web interface.

**Best for**: Remote deployments with restricted SSH access.

### Steps:

1. Navigate to the admin panel: `https://your-domain.com/admin.html`
2. Login with your admin credentials
3. Click the **"📥 Download Database Backup"** button in the "Database Backup" section
4. The database will download automatically with a timestamp in the filename: `smartdoc_backup_YYYYMMDD_HHMMSS.sqlite3`

### Benefits:
- ✅ Works through firewalls and restricted SSH
- ✅ No command-line knowledge needed
- ✅ Automatic timestamped filenames
- ✅ Secure (requires admin authentication)
- ✅ Works from any browser

---

## Method 2: Local Backup (Direct Docker Access)

**Use when**: You have direct Docker access on the deployment machine.

### Automated Script

```bash
# Make script executable
chmod +x scripts/backup_database.sh

# Run backup
./scripts/backup_database.sh
```

**Output**: `./backups/smartdoc_backup_YYYYMMDD_HHMMSS.sqlite3`

### Manual Commands

```bash
# Create backup directory
mkdir -p backups

# Copy database from container
docker cp smartdoc:/data/smartdoc.sqlite3 backups/smartdoc_backup_$(date +%Y%m%d_%H%M%S).sqlite3

# Verify integrity
sqlite3 backups/latest.sqlite3 "PRAGMA integrity_check;"
```

---

## Method 2: Remote Backup via SSH

**Use when**: You only have SSH access to the deployment machine.

### Automated Script

```bash
# Make script executable
chmod +x scripts/backup_remote_database.sh

# Run remote backup
./scripts/backup_remote_database.sh user@yourserver.com

# Or with SSH key
SSH_KEY=~/.ssh/id_rsa ./scripts/backup_remote_database.sh user@yourserver.com
```

**Output**: `./backups/remote/smartdoc_remote_YYYYMMDD_HHMMSS.sqlite3`

### Manual SSH Commands

```bash
# Single command to download database
ssh user@yourserver.com "docker cp smartdoc:/data/smartdoc.sqlite3 /tmp/backup.sqlite3" && \
scp user@yourserver.com:/tmp/backup.sqlite3 ./backups/ && \
ssh user@yourserver.com "rm /tmp/backup.sqlite3"
```

---

## Method 3: One-Liner SSH Backup

**Use when**: You want a quick, single-command backup.

```bash
# Direct streaming backup (fastest)
ssh user@yourserver.com "docker exec smartdoc cat /data/smartdoc.sqlite3" > backups/smartdoc_$(date +%Y%m%d_%H%M%S).sqlite3
```

---

## Method 4: Docker Volume Export

**Use when**: You want to backup the entire Docker volume.

```bash
# On remote server via SSH
ssh user@yourserver.com "docker run --rm -v smartdoc_data:/data -v \$(pwd):/backup alpine tar czf /backup/smartdoc_volume_backup.tar.gz -C /data ."

# Download the archive
scp user@yourserver.com:~/smartdoc_volume_backup.tar.gz ./backups/
```

---

## Database Inspection

### View Database Schema

```bash
sqlite3 backups/latest.sqlite3 ".schema"
```

### Query Data

```bash
# Count records
sqlite3 backups/latest.sqlite3 "
SELECT 'Users: ' || COUNT(*) FROM users
UNION ALL
SELECT 'Conversations: ' || COUNT(*) FROM conversations
UNION ALL
SELECT 'Messages: ' || COUNT(*) FROM messages
UNION ALL
SELECT 'Evaluations: ' || COUNT(*) FROM evaluations;
"

# List users
sqlite3 backups/latest.sqlite3 "SELECT id, username, email, role FROM users;"

# Recent conversations
sqlite3 backups/latest.sqlite3 "SELECT id, user_id, case_id, created_at FROM conversations ORDER BY created_at DESC LIMIT 10;"
```

### Export to CSV

```bash
# Export users table
sqlite3 -header -csv backups/latest.sqlite3 "SELECT * FROM users;" > users.csv

# Export conversations
sqlite3 -header -csv backups/latest.sqlite3 "SELECT * FROM conversations;" > conversations.csv

# Export messages
sqlite3 -header -csv backups/latest.sqlite3 "SELECT * FROM messages;" > messages.csv
```

### Export to JSON

```bash
# Create Python script for JSON export
cat > export_db.py << 'EOF'
import sqlite3
import json
from pathlib import Path

db_path = Path("backups/latest.sqlite3")
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row

data = {}
for table in ['users', 'conversations', 'messages', 'evaluations']:
    cursor = conn.execute(f"SELECT * FROM {table}")
    data[table] = [dict(row) for row in cursor.fetchall()]

with open('database_export.json', 'w') as f:
    json.dump(data, f, indent=2, default=str)

print(f"Exported to database_export.json")
EOF

python export_db.py
```

---

## Database Recovery

### Method 1: Restore to Running Container

```bash
# Copy backup into running container
docker cp backups/smartdoc_backup_20241012_120000.sqlite3 smartdoc:/data/smartdoc.sqlite3

# Restart container to reload database
docker compose -f deployments/docker-compose.yml restart smartdoc
```

### Method 2: Restore to Docker Volume

```bash
# Stop container
docker compose -f deployments/docker-compose.yml down

# Copy database to volume using temporary container
docker run --rm -v smartdoc_data:/data -v $(pwd)/backups:/backup alpine \
  cp /backup/smartdoc_backup_20241012_120000.sqlite3 /data/smartdoc.sqlite3

# Start container
docker compose -f deployments/docker-compose.yml up -d
```

### Method 3: Fresh Deployment with Backup

```bash
# Clean existing deployment
docker compose -f deployments/docker-compose.yml down -v

# Deploy fresh
docker compose -f deployments/docker-compose.yml up -d

# Wait for initialization
sleep 10

# Restore backup
docker cp backups/smartdoc_backup_20241012_120000.sqlite3 smartdoc:/data/smartdoc.sqlite3

# Restart
docker compose -f deployments/docker-compose.yml restart smartdoc
```

---

## Automated Backup Schedule

### Using Cron (Recommended)

```bash
# Add to crontab on deployment server
crontab -e

# Add this line (daily backup at 2 AM)
0 2 * * * docker cp smartdoc:/data/smartdoc.sqlite3 /backups/smartdoc_$(date +\%Y\%m\%d).sqlite3

# Or weekly backup (Sunday at 2 AM)
0 2 * * 0 docker cp smartdoc:/data/smartdoc.sqlite3 /backups/smartdoc_$(date +\%Y\%m\%d).sqlite3
```

### Backup Rotation Script

```bash
# Create backup with automatic old file cleanup
cat > /usr/local/bin/smartdoc-backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/backups/smartdoc"
mkdir -p "$BACKUP_DIR"

# Create backup
docker cp smartdoc:/data/smartdoc.sqlite3 "$BACKUP_DIR/smartdoc_$(date +%Y%m%d_%H%M%S).sqlite3"

# Keep only last 30 days
find "$BACKUP_DIR" -name "smartdoc_*.sqlite3" -mtime +30 -delete

# Verify latest backup
sqlite3 "$BACKUP_DIR/smartdoc_latest.sqlite3" "PRAGMA integrity_check;"
EOF

chmod +x /usr/local/bin/smartdoc-backup.sh

# Add to cron
echo "0 2 * * * /usr/local/bin/smartdoc-backup.sh" | crontab -
```

---

## Troubleshooting

### Database Locked

```bash
# Check if container is running
docker ps | grep smartdoc

# Stop container before backup
docker compose -f deployments/docker-compose.yml stop smartdoc

# Create backup
docker cp smartdoc:/data/smartdoc.sqlite3 backups/

# Restart
docker compose -f deployments/docker-compose.yml start smartdoc
```

### Corrupted Database

```bash
# Check integrity
sqlite3 backups/latest.sqlite3 "PRAGMA integrity_check;"

# Attempt recovery
sqlite3 backups/corrupted.sqlite3 ".recover" | sqlite3 backups/recovered.sqlite3
```

### Large Database Size

```bash
# Vacuum to reduce size
sqlite3 backups/latest.sqlite3 "VACUUM;"

# Compress backup
gzip backups/smartdoc_backup_20241012_120000.sqlite3
```

---

## Best Practices

1. **Regular Backups**: Schedule daily automated backups
2. **Test Restores**: Periodically verify backup integrity and test restore process
3. **Off-site Storage**: Store backups remotely (S3, Dropbox, etc.)
4. **Retention Policy**: Keep 30 daily + 12 monthly + yearly backups
5. **Pre-update Backup**: Always backup before system updates
6. **Monitor Size**: Track database growth and plan for scaling

---

## Quick Reference

| Task          | Command                                                                            |
| ------------- | ---------------------------------------------------------------------------------- |
| Local backup  | `./scripts/backup_database.sh`                                                     |
| Remote backup | `./scripts/backup_remote_database.sh user@host`                                    |
| One-liner SSH | `ssh user@host "docker exec smartdoc cat /data/smartdoc.sqlite3" > backup.sqlite3` |
| Restore       | `docker cp backup.sqlite3 smartdoc:/data/smartdoc.sqlite3`                         |
| Verify        | `sqlite3 backup.sqlite3 "PRAGMA integrity_check;"`                                 |
| Query stats   | `sqlite3 backup.sqlite3 "SELECT COUNT(*) FROM users;"`                             |

---

## Security Notes

- **Sensitive Data**: Database contains user credentials and session data
- **Encryption**: Consider encrypting backups at rest
- **Access Control**: Restrict backup file permissions (chmod 600)
- **Secure Transfer**: Use SSH/SCP for remote transfers
- **Password Protection**: Consider SQLCipher for encrypted SQLite databases
