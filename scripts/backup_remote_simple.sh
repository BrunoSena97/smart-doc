#!/usr/bin/env bash
# Simple Remote Database Backup for SSH Password Authentication
# Usage: ./scripts/backup_remote_simple.sh user@yourserver.com

set -e

# Configuration
REMOTE_HOST="${1}"
CONTAINER_NAME="smartdoc"
DB_PATH="/data/smartdoc.sqlite3"
BACKUP_DIR="./backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="smartdoc_${TIMESTAMP}.sqlite3"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Usage
if [ -z "${REMOTE_HOST}" ]; then
    echo "Usage: $0 <user@hostname>"
    echo ""
    echo "Examples:"
    echo "  $0 ubuntu@192.168.1.100"
    echo "  $0 admin@myserver.com"
    echo ""
    echo "Note: This script works with SSH password authentication."
    echo "      You'll be prompted for your password 3 times:"
    echo "      1. To create backup on server"
    echo "      2. To download backup"
    echo "      3. To clean up temporary file"
    exit 1
fi

echo -e "${GREEN}=== SmartDoc Simple Remote Backup ===${NC}"
echo -e "Target: ${REMOTE_HOST}"
echo ""

# Create backup directory
mkdir -p "${BACKUP_DIR}"

# Step 1: Create backup on remote server
echo -e "${YELLOW}→ Step 1/3: Creating backup on remote server...${NC}"
echo "   (You'll be prompted for your SSH password)"
ssh "${REMOTE_HOST}" "docker exec ${CONTAINER_NAME} cat ${DB_PATH} > /tmp/${BACKUP_FILE}"
echo -e "${GREEN}✓ Remote backup created${NC}"
echo ""

# Step 2: Download backup
echo -e "${YELLOW}→ Step 2/3: Downloading backup...${NC}"
echo "   (You'll be prompted for your SSH password again)"
scp "${REMOTE_HOST}:/tmp/${BACKUP_FILE}" "${BACKUP_DIR}/${BACKUP_FILE}"
echo -e "${GREEN}✓ Download complete${NC}"
echo ""

# Step 3: Clean up remote file
echo -e "${YELLOW}→ Step 3/3: Cleaning up remote server...${NC}"
echo "   (You'll be prompted for your SSH password one last time)"
ssh "${REMOTE_HOST}" "rm -f /tmp/${BACKUP_FILE}"
echo -e "${GREEN}✓ Cleanup complete${NC}"
echo ""

# Verify
if [ -f "${BACKUP_DIR}/${BACKUP_FILE}" ]; then
    FILE_SIZE=$(du -h "${BACKUP_DIR}/${BACKUP_FILE}" | cut -f1)
    echo -e "${GREEN}✓✓✓ Backup successful! ✓✓✓${NC}"
    echo ""
    echo "  Location: ${BACKUP_DIR}/${BACKUP_FILE}"
    echo "  Size: ${FILE_SIZE}"

    # Verify integrity if sqlite3 is available
    if command -v sqlite3 > /dev/null 2>&1; then
        echo ""
        echo -e "${YELLOW}→ Verifying database integrity...${NC}"
        if sqlite3 "${BACKUP_DIR}/${BACKUP_FILE}" "PRAGMA integrity_check;" | grep -q "ok"; then
            echo -e "${GREEN}✓ Database is valid and intact${NC}"

            # Show stats
            echo ""
            echo -e "${YELLOW}→ Database contents:${NC}"
            sqlite3 "${BACKUP_DIR}/${BACKUP_FILE}" "
                SELECT 'Users: ' || COUNT(*) FROM users
                UNION ALL
                SELECT 'Conversations: ' || COUNT(*) FROM conversations
                UNION ALL
                SELECT 'Messages: ' || COUNT(*) FROM messages
                UNION ALL
                SELECT 'Evaluations: ' || COUNT(*) FROM evaluations;
            " 2>/dev/null || echo "  (Database tables may not exist yet)"
        else
            echo -e "${RED}⚠ Warning: Database integrity check failed${NC}"
        fi
    fi
else
    echo -e "${RED}✗ Backup failed${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}=== Backup Complete ===${NC}"
echo ""
echo "Next steps:"
echo "  • View backup: ls -lh ${BACKUP_DIR}/${BACKUP_FILE}"
echo "  • Query data: sqlite3 ${BACKUP_DIR}/${BACKUP_FILE} 'SELECT * FROM users;'"
echo "  • Restore: docker cp ${BACKUP_DIR}/${BACKUP_FILE} smartdoc:/data/smartdoc.sqlite3"
