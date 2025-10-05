# Session Management Quick Reference

## Admin Access

### Default Admin Credentials

```
Access Code: #Admin13
Features: Never-expiring token, unlimited usage, full admin panel access
```

### Creating Additional Admin Users

```bash
# Via Admin Panel UI
POST /api/v1/admin/users
{
  "display_name": "Super Admin",
  "role": "admin",
  "code_label": "ADMIN_2",
  "is_active": true,
  "usage_limit": null
}

# Returns: {"access_code": "AB12CD34"}
```

## Session Restoration

### URL Session Sharing

```
Format: index.html?session=SESSION_ID
Example: index.html?session=intent_session_a1b2c3d4
```

### Programmatic Session Access

```javascript
// Check if session exists
const sessionId = localStorage.getItem("smartdoc_session_id");

// Get session history
const history = await getSessionHistory(sessionId);

// Restore session state
restoreSessionState(history);
```

### API Endpoints

```bash
# Get session history
GET /api/v1/simulation/{session_id}/history

# Response includes:
# - messages: All chat interactions
# - discoveries: Information revealed by category
# - bias_warnings: Cognitive bias detections
# - stats: Session statistics
```

## Database Queries

### Session Data

```sql
-- Find active sessions
SELECT * FROM simulation_sessions WHERE status = 'active';

-- Get session discoveries
SELECT * FROM discovery_events WHERE session_id = 'session_id';

-- Check admin users
SELECT * FROM users WHERE role = 'admin';
```

### Cleanup Operations

```sql
-- Remove old sessions (30+ days)
DELETE FROM simulation_sessions
WHERE created_at < NOW() - INTERVAL 30 DAY
AND status != 'active';

-- Revoke expired tokens
UPDATE auth_sessions SET revoked = true
WHERE issued_at < NOW() - INTERVAL 14 DAY
AND user_id NOT IN (SELECT id FROM users WHERE role = 'admin');
```

## Troubleshooting Commands

### Check Session Restoration

```bash
# Test session endpoint
curl -H "Authorization: Bearer TOKEN" \
  http://localhost:8000/api/v1/simulation/SESSION_ID/history

# Verify localStorage in browser console
localStorage.getItem('smartdoc_session_id')

# Check browser network tab for restoration calls
```

### Admin Token Verification

```bash
# Decode JWT token (without verification)
echo "TOKEN" | cut -d. -f2 | base64 -d | jq

# Should show: {"admin": true} for admin tokens
```

### Database Health Check

```sql
-- Count active sessions
SELECT COUNT(*) FROM simulation_sessions WHERE status = 'active';

-- Check discovery events per session
SELECT session_id, COUNT(*) as discoveries
FROM discovery_events
GROUP BY session_id
ORDER BY discoveries DESC;

-- Verify admin users
SELECT display_name, role, expires_at, is_active
FROM users
WHERE role = 'admin';
```

## Implementation Checklist

### For New Deployments

- [ ] Verify admin user exists (`#Admin13`)
- [ ] Test admin token never expires
- [ ] Confirm session persistence works
- [ ] Test session restoration from URL
- [ ] Verify localStorage persistence
- [ ] Check database table creation
- [ ] Test cross-browser compatibility

### For Existing Deployments

- [ ] Run database migrations
- [ ] Update admin users with `expires_at = NULL`
- [ ] Clear old auth sessions if needed
- [ ] Test backward compatibility
- [ ] Verify existing sessions restore correctly
