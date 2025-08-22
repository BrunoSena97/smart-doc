# State Management & Session Logging Refactor Documentation

## Overview

This document describes the comprehensive refactor of SmartDoc's state management and session logging components to eliminate global state, implement dependency injection, and provide clean interfaces for database persistence.

## Architecture Changes

### Before: Monolithic + Global State

- `state_manager.py` handled both state management and file I/O
- `session_tracker.py` used global `current_session` singleton
- Hard dependencies on file system and configuration
- Difficult to test, no dependency injection

### After: Clean DI + Modular Design

- **`disclosure_store.py`**: Pure state management with optional persistence hooks
- **`session_logger.py`**: Abstract interface + in-memory implementation
- **`types.py`**: Centralized data structures
- **`engine.py`**: Dependency injection throughout

## Key Components

### 1. Centralized Types (`simulation/types.py`)

```python
@dataclass
class InformationBlock:
    block_id: str
    block_type: str
    content: str
    is_critical: bool
    is_revealed: bool = False
    revealed_at: Optional[datetime] = None
    revealed_by_query: Optional[str] = None

@dataclass
class ProgressiveDisclosureSession:
    session_id: str
    case_id: str
    start_time: datetime
    blocks: Dict[str, InformationBlock] = field(default_factory=dict)
    revealed_blocks: Set[str] = field(default_factory=set)
    # ... additional fields
```

**Benefits:**

- Single source of truth for data structures
- Eliminates circular imports
- Clean separation between logic and data

### 2. Session Logger Interface (`simulation/session_logger.py`)

```python
class SessionLogger(ABC):
    @abstractmethod
    def log_interaction(self, *, intent_id: str, user_query: str,
                       vsp_response: str, nlu_output: Optional[Dict] = None,
                       dialogue_state: Optional[str] = None) -> None: ...

    @abstractmethod
    def log_bias_warning(self, bias_event: Dict[str, Any]) -> None: ...

    @abstractmethod
    def get_interactions(self) -> List[Dict[str, Any]]: ...

    @abstractmethod
    def export(self) -> Dict[str, Any]: ...

class InMemorySessionLogger(SessionLogger):
    """Default implementation - no globals, injectable"""
    def __init__(self, session_id: str): ...
```

**Benefits:**

- No global state - each session gets its own logger
- Easy to test with mocks
- Pluggable implementations (memory, database, file)
- Clean interface for different storage backends

### 3. Progressive Disclosure Store (`simulation/disclosure_store.py`)

```python
class ProgressiveDisclosureStore:
    def __init__(
        self,
        case_file_path: Optional[str] = None,
        case_data: Optional[Dict] = None,
        on_reveal: Optional[Callable] = None,        # DB persistence hook
        on_interaction: Optional[Callable] = None   # DB persistence hook
    ):
```

**Benefits:**

- Pure in-memory state management
- Optional persistence via callbacks (no DB coupling)
- Case data can be injected or loaded from file
- Hooks fire automatically on state changes

### 4. Engine with Full Dependency Injection (`simulation/engine.py`)

```python
class IntentDrivenDisclosureManager:
    def __init__(
        self,
        case_file_path: Optional[str] = None,
        provider=None,                              # LLM provider
        intent_classifier=None,                     # Intent classifier
        discovery_processor=None,                   # Discovery processor
        responders: Optional[Dict[str, Any]] = None, # Context responders
        session_logger_factory=None,                # Logger factory
        store: Optional[ProgressiveDisclosureStore] = None, # State store
        on_discovery: Optional[Callable] = None,    # DB hooks
        on_message: Optional[Callable] = None
    ):
```

**Benefits:**

- Full dependency injection - everything is configurable
- No hardcoded providers or classifiers
- Per-session loggers created via factory
- Optional persistence hooks for database integration
- Easy testing with mocks

## Usage Examples

### Basic Usage (Default Components)

```python
# Uses default providers, in-memory logging
engine = IntentDrivenDisclosureManager()
session_id = engine.start_intent_driven_session()
```

### Advanced Usage (Custom Components)

```python
# Custom provider and components
custom_provider = CustomLLMProvider()
custom_store = ProgressiveDisclosureStore(
    case_data=loaded_case,
    on_reveal=save_to_database,
    on_interaction=log_to_database
)

def db_logger_factory(session_id):
    return DatabaseSessionLogger(session_id, db_connection)

engine = IntentDrivenDisclosureManager(
    provider=custom_provider,
    store=custom_store,
    session_logger_factory=db_logger_factory
)
```

### Testing (Easy Mocking)

```python
mock_provider = Mock()
mock_store = Mock(spec=ProgressiveDisclosureStore)
mock_logger_factory = Mock(return_value=Mock(spec=SessionLogger))

engine = IntentDrivenDisclosureManager(
    provider=mock_provider,
    store=mock_store,
    session_logger_factory=mock_logger_factory
)

# Test with full control over dependencies
```

## Database Integration Strategy

### Current Architecture (Preparation)

- **Hooks**: Store and engine accept `on_reveal`, `on_interaction` callbacks
- **Interfaces**: `SessionLogger` abstract base enables DB implementations
- **No Coupling**: Core logic doesn't import SQLAlchemy or database code

### Future Implementation (API Layer)

```python
# In your Flask app
def save_discovery_to_db(payload):
    # Save to SQLite/Postgres
    session = db.session
    discovery = DiscoveryEvent(**payload)
    session.add(discovery)
    session.commit()

def create_db_logger(session_id):
    return DatabaseSessionLogger(session_id, db.session)

# Wire up the engine with DB persistence
engine = IntentDrivenDisclosureManager(
    store=ProgressiveDisclosureStore(
        case_file_path=case_path,
        on_reveal=save_discovery_to_db,
        on_interaction=save_interaction_to_db
    ),
    session_logger_factory=create_db_logger
)
```

## Migration Guide

### Import Changes

```python
# OLD
from smartdoc_core.simulation.state_manager import ProgressiveDisclosureManager
from smartdoc_core.simulation.session_tracker import get_current_session

# NEW
from smartdoc_core.simulation.disclosure_store import ProgressiveDisclosureStore
from smartdoc_core.simulation.session_logger import SessionLogger, InMemorySessionLogger
from smartdoc_core.simulation.types import InformationBlock, ProgressiveDisclosureSession
```

### API Changes

```python
# OLD - Global session access
session_logger = get_current_session()
session_logger.log_interaction(...)

# NEW - Injected session logger
logger = engine._session_loggers[session_id]
logger.log_interaction(...)

# OR - Via engine method
summary = engine.get_session_summary(session_id)
```

### Backwards Compatibility

- All public API methods remain the same
- Constructor signatures extended (old params still work)
- Default behavior unchanged for existing code

## Testing Strategy

### Unit Tests

- Each component tested in isolation
- Mock all dependencies
- Verify interfaces and contracts

### Integration Tests

- Test engine with real components
- Verify session lifecycle
- Test persistence hooks

### Example Test

```python
def test_dependency_injection():
    mock_provider = Mock()
    mock_store = Mock(spec=ProgressiveDisclosureStore)

    engine = IntentDrivenDisclosureManager(
        provider=mock_provider,
        store=mock_store
    )

    assert engine.provider is mock_provider
    assert engine.store is mock_store
```

## Performance Impact

### Memory

- **Reduced**: No global state reduces memory leaks
- **Controlled**: Each session has isolated state
- **Configurable**: Can swap in lightweight loggers for production

### CPU

- **Minimal**: Same core algorithms
- **Improved**: Better caching via dependency injection
- **Scalable**: Multiple concurrent sessions without conflicts

## Future Enhancements

### Admin UI Ready

- **Provider Selection**: Choose different LLM models per context
- **Prompt Configuration**: Swap prompt builders via admin interface
- **Analytics**: Rich session data via database loggers
- **A/B Testing**: Easy to swap components for experiments

### Database Implementations

```python
class DatabaseSessionLogger(SessionLogger):
    def __init__(self, session_id: str, db_session):
        self.session_id = session_id
        self.db = db_session

    def log_interaction(self, **kwargs):
        interaction = InteractionModel(**kwargs)
        self.db.add(interaction)
        self.db.commit()
```

### Multi-tenant Support

```python
# Different configurations per tenant
tenant_config = get_tenant_config(tenant_id)
engine = IntentDrivenDisclosureManager(
    provider=tenant_config.llm_provider,
    responders=tenant_config.responders,
    session_logger_factory=tenant_config.logger_factory
)
```

## Summary

This refactor achieves the main goals:

✅ **No Globals**: All state is explicitly managed and passed
✅ **DI-Friendly**: Everything can be injected and configured
✅ **DB Hooks**: Clean persistence without coupling
✅ **Crisp Responsibilities**: Each component has one clear job
✅ **Easy Testing**: Full mock support and isolated testing
✅ **Admin Ready**: Pluggable components for UI configuration

The architecture is now ready for database integration, multi-tenancy, and advanced admin features while maintaining clean separation of concerns.
