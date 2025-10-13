#!/usr/bin/env bash
# SmartDoc Database Backup Script
# Extracts SQLite database from Docker container to local machine

set -e

# Configuration
CONTAINER_NAME="smartdoc"
DB_PATH="/data/smartdoc.sqlite3"
BACKUP_DIR="./backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="smartdoc_backup_${TIMESTAMP}.sqlite3"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== SmartDoc Database Backup ===${NC}"
echo ""

# Create backup directory if it doesn't exist
mkdir -p "${BACKUP_DIR}"

# Check if container is running
if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo -e "${RED}Error: Container '${CONTAINER_NAME}' is not running${NC}"
    echo "Available containers:"
    docker ps --format "table {{.Names}}\t{{.Status}}"
    exit 1
fi

echo -e "${YELLOW}→ Backing up database from container '${CONTAINER_NAME}'...${NC}"

# Copy database from container to local backup directory
docker cp "${CONTAINER_NAME}:${DB_PATH}" "${BACKUP_DIR}/${BACKUP_FILE}"

# Check if backup was successful
if [ -f "${BACKUP_DIR}/${BACKUP_FILE}" ]; then
    FILE_SIZE=$(du -h "${BACKUP_DIR}/${BACKUP_FILE}" | cut -f1)
    echo -e "${GREEN}✓ Backup successful!${NC}"
    echo -e "  File: ${BACKUP_DIR}/${BACKUP_FILE}"
    echo -e "  Size: ${FILE_SIZE}"

    # Verify database integrity
    echo ""
    echo -e "${YELLOW}→ Verifying database integrity...${NC}"
    if sqlite3 "${BACKUP_DIR}/${BACKUP_FILE}" "PRAGMA integrity_check;" | grep -q "ok"; then
        echo -e "${GREEN}✓ Database integrity check passed${NC}"
    else
        echo -e "${RED}⚠ Database integrity check failed${NC}"
        exit 1
    fi

    # Show database stats
    echo ""
    echo -e "${YELLOW}→ Database statistics:${NC}"
    sqlite3 "${BACKUP_DIR}/${BACKUP_FILE}" "
        SELECT 'Users: ' || COUNT(*) FROM users
        UNION ALL
        SELECT 'Conversations: ' || COUNT(*) FROM conversations
        UNION ALL
        SELECT 'Messages: ' || COUNT(*) FROM messages
        UNION ALL
        SELECT 'Evaluations: ' || COUNT(*) FROM evaluations;
    "

    # Create latest symlink
    ln -sf "${BACKUP_FILE}" "${BACKUP_DIR}/latest.sqlite3"
    echo ""
    echo -e "${GREEN}✓ Latest backup symlink created: ${BACKUP_DIR}/latest.sqlite3${NC}"

else
    echo -e "${RED}✗ Backup failed${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}=== Backup Complete ===${NC}"
