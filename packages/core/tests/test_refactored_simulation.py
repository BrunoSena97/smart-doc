"""
Test suite for refactored simulation engine with dependency injection

This test validates that the state management and session logging refactor
works correctly with clean dependencies and no global state.
"""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime

from smartdoc_core.simulation.engine import IntentDrivenDisclosureManager
from smartdoc_core.simulation.disclosure_store import ProgressiveDisclosureStore
from smartdoc_core.simulation.session_logger import InMemorySessionLogger, SessionLogger


class TestRefactoredSimulationEngine:
    """Test the refactored simulation engine with dependency injection."""

    def test_engine_initialization_with_dependency_injection(self):
        """Test that engine initializes correctly with injected dependencies."""
        # Mock dependencies
        mock_provider = Mock()
        mock_intent_classifier = Mock()
        mock_discovery_processor = Mock()
        mock_store = Mock(spec=ProgressiveDisclosureStore)
        mock_store.case_data = {"caseId": "test_case"}

        def mock_logger_factory(session_id):
            return InMemorySessionLogger(session_id)

        # Initialize engine with DI
        engine = IntentDrivenDisclosureManager(
            provider=mock_provider,
            intent_classifier=mock_intent_classifier,
            discovery_processor=mock_discovery_processor,
            store=mock_store,
            session_logger_factory=mock_logger_factory
        )

        # Verify dependencies are properly injected
        assert engine.provider is mock_provider
        assert engine.intent_classifier is mock_intent_classifier
        assert engine.discovery_processor is mock_discovery_processor
        assert engine.store is mock_store
        assert engine.session_logger_factory is mock_logger_factory

    def test_session_creation_creates_logger(self):
        """Test that starting a session creates a logger instance."""
        mock_store = Mock(spec=ProgressiveDisclosureStore)
        mock_store.case_data = {"caseId": "test_case"}
        mock_store.start_new_session.return_value = Mock()

        engine = IntentDrivenDisclosureManager(store=mock_store)

        session_id = engine.start_intent_driven_session("test_session")

        # Verify session logger was created
        assert session_id in engine._session_loggers
        assert isinstance(engine._session_loggers[session_id], SessionLogger)

    def test_session_logger_independence(self):
        """Test that different sessions have independent loggers."""
        mock_store = Mock(spec=ProgressiveDisclosureStore)
        mock_store.case_data = {"caseId": "test_case"}
        mock_store.start_new_session.return_value = Mock()

        engine = IntentDrivenDisclosureManager(store=mock_store)

        session1_id = engine.start_intent_driven_session("session1")
        session2_id = engine.start_intent_driven_session("session2")

        # Verify independent loggers
        logger1 = engine._session_loggers[session1_id]
        logger2 = engine._session_loggers[session2_id]

        assert logger1 is not logger2
        assert isinstance(logger1, InMemorySessionLogger)
        assert isinstance(logger2, InMemorySessionLogger)
        assert logger1.session_id == "session1"
        assert logger2.session_id == "session2"

    def test_session_summary_retrieval(self):
        """Test that session summaries can be retrieved."""
        mock_store = Mock(spec=ProgressiveDisclosureStore)
        mock_store.case_data = {"caseId": "test_case"}
        mock_store.start_new_session.return_value = Mock()

        engine = IntentDrivenDisclosureManager(store=mock_store)

        session_id = engine.start_intent_driven_session("test_session")

        # Get session summary
        summary = engine.get_session_summary(session_id)

        # Verify summary structure
        assert "session_id" in summary
        assert "total_interactions" in summary
        assert "duration_minutes" in summary
        assert summary["session_id"] == "test_session"

    def test_no_global_state(self):
        """Test that the engine doesn't rely on global state."""
        # Create two independent engine instances
        engine1 = IntentDrivenDisclosureManager()
        engine2 = IntentDrivenDisclosureManager()

        # They should have independent state
        assert engine1.discovery_events is not engine2.discovery_events
        assert engine1._session_loggers is not engine2._session_loggers

        # Starting sessions in one shouldn't affect the other
        if engine1.store.case_data:  # Only if we have valid case data
            session1 = engine1.start_intent_driven_session("test1")
            assert session1 not in engine2._session_loggers

    def test_persistence_hooks_integration(self):
        """Test that persistence hooks are properly wired through store."""
        # Mock callbacks
        on_reveal_mock = Mock()
        on_interaction_mock = Mock()

        # Create store with hooks
        store = ProgressiveDisclosureStore(
            case_data={"caseId": "test", "informationBlocks": []},
            on_reveal=on_reveal_mock,
            on_interaction=on_interaction_mock
        )

        engine = IntentDrivenDisclosureManager(store=store)

        # Verify hooks are accessible through store
        assert store._on_reveal is on_reveal_mock
        assert store._on_interaction is on_interaction_mock


class TestInMemorySessionLogger:
    """Test the in-memory session logger implementation."""

    def test_session_logger_tracks_interactions(self):
        """Test that session logger correctly tracks interactions."""
        logger = InMemorySessionLogger("test_session")

        # Log some interactions
        logger.log_interaction(
            intent_id="test_intent",
            user_query="What are the vital signs?",
            vsp_response="The blood pressure is 140/90",
            dialogue_state="EXAM"
        )

        interactions = logger.get_interactions()
        assert len(interactions) == 1
        assert interactions[0]["intent_id"] == "test_intent"
        assert interactions[0]["dialogue_state"] == "EXAM"

    def test_session_logger_tracks_bias_warnings(self):
        """Test that session logger correctly tracks bias warnings."""
        logger = InMemorySessionLogger("test_session")

        # Log a bias warning
        logger.log_bias_warning({
            "bias_type": "anchoring",
            "message": "Consider other diagnoses",
            "confidence": 0.8
        })

        bias_summary = logger.get_bias_summary()
        assert bias_summary["total_warnings"] == 1
        assert "anchoring" in bias_summary["bias_types"]

    def test_session_logger_export(self):
        """Test that session logger can export complete data."""
        logger = InMemorySessionLogger("test_session")

        # Add some data
        logger.log_interaction(
            intent_id="test_intent",
            user_query="Test query",
            vsp_response="Test response"
        )

        exported_data = logger.export()
        assert exported_data["session_id"] == "test_session"
        assert "interactions" in exported_data
        assert len(exported_data["interactions"]) == 1


class TestProgressiveDisclosureStore:
    """Test the progressive disclosure store with hooks."""

    def test_store_fires_reveal_hooks(self):
        """Test that store fires reveal hooks when blocks are revealed."""
        on_reveal_mock = Mock()

        store = ProgressiveDisclosureStore(
            case_data={
                "caseId": "test",
                "informationBlocks": [
                    {
                        "blockId": "test_block",
                        "blockType": "History",
                        "content": "Test content",
                        "isCritical": False
                    }
                ]
            },
            on_reveal=on_reveal_mock
        )

        # Start session and reveal block
        session = store.start_new_session("test_session")
        result = store.reveal_block("test_session", "test_block", "test query")

        # Verify hook was called
        assert result["success"] is True
        on_reveal_mock.assert_called_once()
        call_args = on_reveal_mock.call_args[0][0]
        assert call_args["session_id"] == "test_session"
        assert call_args["block_id"] == "test_block"

    def test_store_fires_interaction_hooks(self):
        """Test that store fires interaction hooks."""
        on_interaction_mock = Mock()

        store = ProgressiveDisclosureStore(
            case_data={"caseId": "test", "informationBlocks": []},
            on_interaction=on_interaction_mock
        )

        # Start session and add hypothesis
        session = store.start_new_session("test_session")
        result = store.add_working_hypothesis(
            "test_session",
            "Test hypothesis",
            "Test reasoning"
        )

        # Verify hook was called
        assert result["success"] is True
        on_interaction_mock.assert_called_once()


if __name__ == "__main__":
    # Run basic tests
    test_engine = TestRefactoredSimulationEngine()
    test_logger = TestInMemorySessionLogger()
    test_store = TestProgressiveDisclosureStore()

    print("Running dependency injection tests...")
    test_engine.test_engine_initialization_with_dependency_injection()
    test_engine.test_session_creation_creates_logger()
    test_engine.test_session_logger_independence()
    test_engine.test_session_summary_retrieval()
    test_engine.test_no_global_state()
    test_engine.test_persistence_hooks_integration()

    print("Running session logger tests...")
    test_logger.test_session_logger_tracks_interactions()
    test_logger.test_session_logger_tracks_bias_warnings()
    test_logger.test_session_logger_export()

    print("Running disclosure store tests...")
    test_store.test_store_fires_reveal_hooks()
    test_store.test_store_fires_interaction_hooks()

    print("✅ All tests passed! Refactored architecture working correctly.")
