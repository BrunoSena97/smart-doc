#!/usr/bin/env bash
# Remote Database Backup via SSH
# Backs up SmartDoc database from remote server to local machine

set -e

# Configuration
REMOTE_HOST="${1:-}"
REMOTE_USER="${2:-}"
CONTAINER_NAME="smartdoc"
DB_PATH="/data/smartdoc.sqlite3"
LOCAL_BACKUP_DIR="./backups/remote"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="smartdoc_remote_${TIMESTAMP}.sqlite3"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Usage information
usage() {
    echo "Usage: $0 <remote_host> [remote_user]"
    echo ""
    echo "Examples:"
    echo "  $0 192.168.1.100 ubuntu"
    echo "  $0 myserver.com"
    echo "  $0 user@myserver.com"
    echo ""
    echo "Environment variables:"
    echo "  SSH_KEY: Path to SSH private key (optional)"
    exit 1
}

# Check arguments
if [ -z "${REMOTE_HOST}" ]; then
    usage
fi

# Parse user@host format
if [[ "${REMOTE_HOST}" == *@* ]]; then
    REMOTE_USER="${REMOTE_HOST%%@*}"
    REMOTE_HOST="${REMOTE_HOST#*@}"
fi

# Build SSH connection string
if [ -n "${REMOTE_USER}" ]; then
    SSH_TARGET="${REMOTE_USER}@${REMOTE_HOST}"
else
    SSH_TARGET="${REMOTE_HOST}"
fi

# SSH key option
SSH_KEY_OPT=""
if [ -n "${SSH_KEY}" ]; then
    SSH_KEY_OPT="-i ${SSH_KEY}"
fi

echo -e "${GREEN}=== SmartDoc Remote Database Backup ===${NC}"
echo -e "Remote: ${SSH_TARGET}"
echo ""

# Create backup directory
mkdir -p "${LOCAL_BACKUP_DIR}"

# Check SSH connectivity
echo -e "${YELLOW}→ Testing SSH connection...${NC}"
if ! ssh ${SSH_KEY_OPT} -o ConnectTimeout=10 "${SSH_TARGET}" "echo 'SSH connection successful'" > /dev/null 2>&1; then
    echo -e "${RED}✗ Failed to connect to ${SSH_TARGET}${NC}"
    echo "Please check:"
    echo "  - SSH credentials"
    echo "  - Network connectivity"
    echo "  - Firewall settings"
    exit 1
fi
echo -e "${GREEN}✓ SSH connection successful${NC}"

# Check if Docker is available on remote
echo -e "${YELLOW}→ Checking remote Docker installation...${NC}"
if ! ssh ${SSH_KEY_OPT} "${SSH_TARGET}" "command -v docker > /dev/null 2>&1"; then
    echo -e "${RED}✗ Docker not found on remote host${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Docker found${NC}"

# Check if container is running
echo -e "${YELLOW}→ Checking if container '${CONTAINER_NAME}' is running...${NC}"
if ! ssh ${SSH_KEY_OPT} "${SSH_TARGET}" "docker ps --format '{{.Names}}' | grep -q '^${CONTAINER_NAME}$'"; then
    echo -e "${RED}✗ Container '${CONTAINER_NAME}' is not running${NC}"
    echo "Available containers:"
    ssh ${SSH_KEY_OPT} "${SSH_TARGET}" "docker ps --format 'table {{.Names}}\t{{.Status}}'"
    exit 1
fi
echo -e "${GREEN}✓ Container is running${NC}"

# Create temporary backup on remote
REMOTE_TMP="/tmp/${BACKUP_FILE}"
echo ""
echo -e "${YELLOW}→ Creating backup on remote server...${NC}"
ssh ${SSH_KEY_OPT} "${SSH_TARGET}" "docker cp ${CONTAINER_NAME}:${DB_PATH} ${REMOTE_TMP}"
echo -e "${GREEN}✓ Remote backup created${NC}"

# Download backup from remote
echo -e "${YELLOW}→ Downloading backup to local machine...${NC}"
scp ${SSH_KEY_OPT} "${SSH_TARGET}:${REMOTE_TMP}" "${LOCAL_BACKUP_DIR}/${BACKUP_FILE}"
echo -e "${GREEN}✓ Download complete${NC}"

# Clean up remote temporary file
echo -e "${YELLOW}→ Cleaning up remote temporary file...${NC}"
ssh ${SSH_KEY_OPT} "${SSH_TARGET}" "rm -f ${REMOTE_TMP}"
echo -e "${GREEN}✓ Remote cleanup complete${NC}"

# Verify local backup
if [ -f "${LOCAL_BACKUP_DIR}/${BACKUP_FILE}" ]; then
    FILE_SIZE=$(du -h "${LOCAL_BACKUP_DIR}/${BACKUP_FILE}" | cut -f1)
    echo ""
    echo -e "${GREEN}✓ Backup successful!${NC}"
    echo -e "  File: ${LOCAL_BACKUP_DIR}/${BACKUP_FILE}"
    echo -e "  Size: ${FILE_SIZE}"

    # Verify database integrity
    echo ""
    echo -e "${YELLOW}→ Verifying database integrity...${NC}"
    if command -v sqlite3 > /dev/null 2>&1; then
        if sqlite3 "${LOCAL_BACKUP_DIR}/${BACKUP_FILE}" "PRAGMA integrity_check;" | grep -q "ok"; then
            echo -e "${GREEN}✓ Database integrity check passed${NC}"
        else
            echo -e "${RED}⚠ Database integrity check failed${NC}"
            exit 1
        fi

        # Show database stats
        echo ""
        echo -e "${YELLOW}→ Database statistics:${NC}"
        sqlite3 "${LOCAL_BACKUP_DIR}/${BACKUP_FILE}" "
            SELECT 'Users: ' || COUNT(*) FROM users
            UNION ALL
            SELECT 'Conversations: ' || COUNT(*) FROM conversations
            UNION ALL
            SELECT 'Messages: ' || COUNT(*) FROM messages
            UNION ALL
            SELECT 'Evaluations: ' || COUNT(*) FROM evaluations;
        " 2>/dev/null || echo "  (Tables may not exist yet)"
    else
        echo -e "${YELLOW}⚠ sqlite3 not installed locally, skipping integrity check${NC}"
        echo "  Install with: brew install sqlite3"
    fi

    # Create latest symlink
    ln -sf "${BACKUP_FILE}" "${LOCAL_BACKUP_DIR}/latest.sqlite3"
    echo ""
    echo -e "${GREEN}✓ Latest backup symlink created: ${LOCAL_BACKUP_DIR}/latest.sqlite3${NC}"

else
    echo -e "${RED}✗ Backup failed${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}=== Remote Backup Complete ===${NC}"
