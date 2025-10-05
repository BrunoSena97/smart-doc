# Session Management & Authentication

## Overview

SmartDoc implements enterprise-grade session management with comprehensive data persistence and automatic session restoration. This ensures seamless user experience across browser sessions and provides administrative users with non-expiring access.

## Table of Contents

- [Authentication System](#authentication-system)
- [Session Persistence](#session-persistence)
- [Session Restoration](#session-restoration)
- [Implementation Details](#implementation-details)
- [Testing Guide](#testing-guide)
- [Troubleshooting](#troubleshooting)

## Authentication System

### User Types

SmartDoc supports two types of users with different authentication behaviors:

#### Regular Users

- **Token Expiration**: 14 days
- **Usage Limits**: Configurable per user
- **Access Control**: Standard simulation access

#### Admin Users

- **Token Expiration**: Never (10-year expiration for practical purposes)
- **Usage Limits**: Unlimited
- **Access Control**: Full admin panel access + simulation access

### Admin Authentication

#### Default Admin Account

```yaml
Username: admin
Access Code: #Admin13
Role: admin
Expires: Never
Usage Limit: Unlimited
```

#### Admin Token Features

- **Non-Expiring**: Admin tokens are valid for 10 years (effectively permanent)
- **Special Flag**: Admin tokens include `"admin": true` in JWT payload
- **Response Indicator**: Login response shows `"expires_at": "never"` for admins
- **Automatic Detection**: System automatically detects admin role during token issuance

#### Implementation

```python
# In auth_service.py
def issue_token(user_id: int) -> dict:
    # Check if user is admin for non-expiring token
    with get_session() as s:
        user = s.get(User, user_id)
        is_admin = user and user.role == "admin"

    if is_admin:
        # Admin tokens never expire (10 years)
        exp = now + timedelta(days=365 * 10)
        payload = {..., "admin": True}
    else:
        # Regular user tokens expire after 14 days
        exp = now + timedelta(minutes=JWT_TTL_MIN)
```

## Session Persistence

### Data Persistence Architecture

SmartDoc automatically persists all simulation data to the database in real-time:

#### Database Tables

- **`simulation_sessions`**: Session metadata and status
- **`conversations`**: Chat conversation containers
- **`messages`**: Individual chat messages
- **`discovery_events`**: Information discoveries by category
- **`bias_warnings`**: Cognitive bias detection events

#### Persistence Hooks

The simulation engine uses dependency injection to automatically persist data:

```python
# Engine initialization with persistence hooks
engine = IntentDrivenDisclosureManager(
    on_discovery=lambda payload: add_discoveries(session_id, [payload]),
    on_message=lambda payload: add_message(conversation_id, ...)
)
```

#### What Gets Persisted

- ✅ **Session State**: ID, status, creation time, statistics
- ✅ **Chat Messages**: All user queries and system responses
- ✅ **Discoveries**: Information revealed by category (HPI, medications, exam, labs, imaging)
- ✅ **Bias Warnings**: Real-time cognitive bias detection results
- ✅ **Timestamps**: Precise timing for all events
- ✅ **Metadata**: Confidence scores, block IDs, categories

## Session Restoration

### Automatic Session Recovery

When users return to SmartDoc, the system automatically attempts to restore their previous session:

#### Detection Methods

1. **URL Parameter**: `index.html?session=SESSION_ID`
2. **LocalStorage**: Automatically saved session ID from previous visits

#### Restoration Process

```javascript
// 1. Check for existing session
const sessionId =
  urlParams.get("session") || localStorage.getItem("smartdoc_session_id");

// 2. Fetch complete session history
const sessionData = await getSessionHistory(sessionId);

// 3. Restore application state
restoreSessionState(sessionData);

// 4. Update UI to reflect restored state
updateUIAfterSessionRestore(sessionData);
```

#### Restoration Logic

```javascript
function restoreSessionState(sessionData) {
  // Restore session ID
  state.sessionId = sessionData.session_id;

  // Restore discoveries by category
  sessionData.discoveries.forEach((discovery) => {
    const category = discovery.category || "hpi";
    state.discoveredInfo[category][discovery.label] = {
      label: discovery.label,
      value: discovery.value,
      timestamp: new Date(discovery.timestamp).getTime(),
    };
    state.discoveredCount++;
  });

  // Restore bias warnings
  state.biasWarningCount = sessionData.bias_warnings.length;
}
```

### User Experience

#### Successful Restoration

- **Notification**: Green banner showing restoration summary
- **Progress Indicators**: Updated to reflect discovered information
- **Chat History**: Previous messages available (if implemented)
- **Seamless Continuation**: User can continue exactly where they left off

#### Failed Restoration

- **Graceful Degradation**: Automatically creates new session
- **No Data Loss**: Previous session data remains in database
- **User Notification**: Clear indication of new session start

## Implementation Details

### Frontend Architecture

#### State Management (`state.js`)

```javascript
export const state = {
  sessionId: null,
  discoveredInfo: {
    hpi: {}, // label -> { label, value, timestamp }
    medications: {},
    exam: {},
    labs: {},
    imaging: {},
  },
  totalAvailableInfo: 0,
  discoveredCount: 0,
  biasWarningCount: 0,
};
```

#### API Integration (`api.js`)

```javascript
// Get complete session history for restoration
export async function getSessionHistory(sessionId) {
  const url = `${V1_BASE_URL}/simulation/${sessionId}/history`;
  return request(url, { method: "GET" });
}
```

#### Session Persistence (`main.js`)

```javascript
// Automatic session restoration on page load
if (sessionId) {
  await attemptSessionRestore(sessionId);
} else {
  const newSessionId = newSession();
  localStorage.setItem("smartdoc_session_id", newSessionId);
}
```

### Backend Architecture

#### Session History Endpoint

```python
@bp.get("/simulation/<session_id>/history")
def get_session_history(session_id):
    """Get complete session history for resuming sessions."""
    # Returns: messages, discoveries, bias_warnings, session_metadata
```

#### Database Models

```python
class SimulationSession(Base):
    id: str  # Primary session identifier
    conversation_id: int
    status: str  # 'active', 'completed', 'abandoned'
    stats: str  # JSON-encoded statistics
    created_at: datetime
    ended_at: datetime

    # Relationships
    discoveries = relationship("DiscoveryEvent")
    biases = relationship("BiasWarning")
    diagnoses = relationship("DiagnosisSubmission")
```

## Testing Guide

### Admin Authentication Testing

#### Test Non-Expiring Admin Tokens

```bash
# 1. Login as admin
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"code": "#Admin13"}'

# Expected response
{
  "token": "eyJ...",
  "expires_at": "never",
  "user": {"id": 1, "name": "admin", "label": "ADMIN"}
}

# 2. Verify token works after extended period
# (Admin tokens should work indefinitely)
```

#### Test Regular User Token Expiration

```bash
# Regular users should have 14-day expiration
{
  "token": "eyJ...",
  "expires_at": "2025-10-19T15:30:00Z",
  "user": {"id": 2, "name": "student", "label": "COHORT_1"}
}
```

### Session Persistence Testing

#### Test Complete Session Lifecycle

```bash
# 1. Start new session and make discoveries
POST /api/v1/chat
{
  "message": "What medications is she taking?",
  "context": "anamnesis",
  "session_id": "session_123"
}

# 2. Verify data persistence
GET /api/v1/simulation/session_123/history

# Expected: Complete session data with discoveries

# 3. Test restoration (close browser, return)
GET /index.html?session=session_123

# Expected: Automatic restoration with notification
```

#### Test URL Session Sharing

```bash
# Share session via URL
https://smartdoc.example.com/index.html?session=session_123

# Should automatically restore shared session
```

#### Test LocalStorage Persistence

```javascript
// 1. Start session in browser
// 2. Check localStorage
localStorage.getItem("smartdoc_session_id"); // Should return session ID

// 3. Close browser, reopen
// 4. Should automatically restore session
```

### Manual Testing Scenarios

#### Scenario 1: Admin Session Persistence

1. Login to admin panel with `#Admin13`
2. Leave browser open for 24+ hours
3. **Expected**: Admin panel remains accessible
4. **Expected**: No re-authentication required

#### Scenario 2: Simulation Session Restoration

1. Start new simulation session
2. Ask 5-10 questions and discover information
3. Note discovered items in results panel
4. Close browser completely
5. Reopen browser and navigate to SmartDoc
6. **Expected**: Green notification showing restored session
7. **Expected**: All discovered information visible in results panel
8. **Expected**: Can continue simulation seamlessly

#### Scenario 3: Cross-Device Session Sharing

1. Start session on Device A
2. Copy URL with session parameter
3. Open URL on Device B
4. **Expected**: Complete session restoration on Device B
5. **Expected**: Can continue simulation on either device

## Troubleshooting

### Common Issues

#### Admin Token Expiring

```yaml
Problem: Admin session expires unexpectedly
Cause: User created with role != "admin"
Solution: Verify user role in database
Query: SELECT role FROM users WHERE code_label = 'ADMIN';
Fix: UPDATE users SET role = 'admin' WHERE code_label = 'ADMIN';
```

#### Session Not Restoring

```yaml
Problem: Session restoration fails silently
Cause: Session not found in database
Debugging:
  1. Check session exists: GET /api/v1/simulation/{session_id}/history
  2. Verify localStorage: localStorage.getItem('smartdoc_session_id')
  3. Check browser console for restoration errors
  4. Verify database contains session data
```

#### LocalStorage Issues

```yaml
Problem: Session ID not persisting
Cause: LocalStorage disabled or cleared
Solutions: 1. Enable localStorage in browser settings
  2. Check browser privacy/incognito mode
  3. Verify domain consistency (localhost vs 127.0.0.1)
  4. Clear localStorage and start fresh session
```

### Database Verification

#### Check Session Data

```sql
-- Verify session exists
SELECT * FROM simulation_sessions WHERE id = 'session_123';

-- Check discoveries for session
SELECT * FROM discovery_events WHERE session_id = 'session_123';

-- Verify messages
SELECT m.* FROM messages m
JOIN conversations c ON m.conversation_id = c.id
JOIN simulation_sessions s ON s.conversation_id = c.id
WHERE s.id = 'session_123';
```

#### Cleanup Old Sessions

```sql
-- Remove sessions older than 30 days
DELETE FROM simulation_sessions
WHERE created_at < NOW() - INTERVAL 30 DAY;
```

### Error Handling

#### Graceful Degradation

- **Invalid Session ID**: Creates new session automatically
- **Database Errors**: Falls back to in-memory session
- **Network Issues**: Retries restoration with exponential backoff
- **Corrupted Data**: Validates session data before restoration

#### Logging

- **Frontend**: Console logs for restoration process
- **Backend**: Structured logging for session operations
- **Database**: Transaction logging for data persistence

## Configuration

### Environment Variables

```yaml
# JWT Configuration
JWT_TTL_MIN: 20160 # 14 days for regular users
JWT_SECRET_KEY: "your-secret-key"

# Session Configuration
SESSION_CLEANUP_DAYS: 30 # Clean old sessions after 30 days
MAX_SESSIONS_PER_USER: 10 # Limit concurrent sessions
```

### Feature Flags

```python
# In settings.py
ENABLE_SESSION_RESTORATION = True
ENABLE_ADMIN_NEVER_EXPIRE = True
ENABLE_URL_SESSION_SHARING = True
ENABLE_CROSS_DEVICE_SESSIONS = True
```

This comprehensive session management system ensures that SmartDoc provides a robust, enterprise-grade user experience with seamless continuity across sessions and devices.
