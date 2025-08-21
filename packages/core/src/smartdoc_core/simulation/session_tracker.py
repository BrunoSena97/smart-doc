"""
Session Tracker for SmartDoc Virtual Patient Simulation

This module tracks clinical simulation sessions, recording user interactions,
temporal sequences, and session state for comprehensive bias analysis and evaluation.
"""

import uuid
import json
from datetime import datetime
from typing import Dict, List, Any
from smartdoc_core.utils.logger import sys_logger


class SessionLogger:
    """Logs clinical interview sessions for evaluation and bias detection."""

    def __init__(self):
        self.session_data = {
            "session_id": str(uuid.uuid4()),
            "start_time": datetime.now().isoformat(),
            "interactions": [],
            "student_responses": [],
            "detected_biases": [],
            "bias_warnings": [],  # New: track bias warnings
            "current_state": "INTRODUCTION",
        }
        sys_logger.log_system(
            "info", f"Started new session: {self.session_data['session_id']}"
        )

    def log_interaction(
        self,
        intent_id: str,
        user_query: str,
        vsp_response: str,
        nlu_output: Dict = None,
        dialogue_state: str = None,
    ):
        """Log a single interaction between user and VSP."""
        interaction = {
            "intent_id": intent_id,
            "user_query": user_query,
            "vsp_response": vsp_response,
            "timestamp": datetime.now().isoformat(),
            "nlu_output": nlu_output or {},
            "dialogue_state": dialogue_state or "UNKNOWN",
        }

        self.session_data["interactions"].append(interaction)

        # Update current state
        if dialogue_state:
            self.session_data["current_state"] = dialogue_state

        # Check for bias after each interaction (enhanced)
        self._check_for_biases()

        sys_logger.log_system(
            "debug", f"Logged interaction: {intent_id} in state {dialogue_state}"
        )

    def get_session_data(self):
        """Get the full session data for bias analysis."""
        return self.session_data

    def get_interactions(self) -> List[Dict]:
        """Get the interactions list for bias analysis."""
        return self.session_data.get("interactions", [])

    def log_bias_warning(self, bias_event: Dict):
        """Log a bias warning event."""
        bias_warning = {
            "bias_type": bias_event.get("bias_type"),
            "message": bias_event.get("message"),
            "confidence": bias_event.get("confidence", 0.5),
            "timestamp": datetime.now().isoformat(),
        }
        self.session_data["bias_warnings"].append(bias_warning)
        sys_logger.log_system(
            "warning",
            f"BIAS WARNING: {bias_event.get('bias_type')} - {bias_event.get('message')}",
        )

    def get_bias_summary(self) -> Dict:
        """Get a summary of all bias warnings in this session."""
        warnings = self.session_data.get("bias_warnings", [])
        bias_types = {}
        for warning in warnings:
            bias_type = warning.get("bias_type", "unknown")
            bias_types[bias_type] = bias_types.get(bias_type, 0) + 1

        return {
            "total_warnings": len(warnings),
            "bias_types": bias_types,
            "warnings": warnings,
        }

    def _check_for_biases(self):
        """Simple bias detection based on interaction patterns."""
        recent_interactions = self.session_data["interactions"][
            -5:
        ]  # Last 5 interactions

        # Check for anchoring bias (focusing too much on heart failure)
        if self._detect_anchoring_bias(recent_interactions):
            self._add_bias_warning(
                "anchoring",
                "You seem to be focusing heavily on heart failure. Consider other diagnoses.",
            )

        # Check for confirmation bias
        if self._detect_confirmation_bias(recent_interactions):
            self._add_bias_warning(
                "confirmation",
                "You're seeking information that confirms heart failure. What evidence might contradict it?",
            )

        # Check for premature closure
        if self._detect_premature_closure():
            self._add_bias_warning(
                "premature_closure",
                "Consider gathering more information before reaching a conclusion.",
            )

    def _detect_anchoring_bias(self, interactions: List[Dict]) -> bool:
        """Detect if user is anchoring on cardiovascular/heart failure diagnosis."""
        # LLM intent categories that suggest cardiovascular focus
        cardio_related_intents = [
            "physical_exam_cardiovascular",
            "vital_signs",
            "lab_tests",
            "imaging",
            "ekg",
            "medications",
        ]

        # Also check for cardiovascular keywords in user queries
        cardio_keywords = [
            "heart",
            "cardiac",
            "chest",
            "cardiovascular",
            "blood pressure",
            "pulse",
            "heart rate",
            "ecg",
            "ekg",
            "echo",
            "bnp",
        ]

        cardio_count = 0
        for interaction in interactions:
            intent_id = interaction.get("intent_id", "")
            user_query = interaction.get("user_query", "").lower()

            # Check intent category
            if any(
                cardio_intent in intent_id for cardio_intent in cardio_related_intents
            ):
                cardio_count += 1
            # Check keywords in user query
            elif any(keyword in user_query for keyword in cardio_keywords):
                cardio_count += 1

        # If >60% of recent questions are cardio-related, flag as anchoring
        return len(interactions) > 0 and (cardio_count / len(interactions)) > 0.6

    def _detect_confirmation_bias(self, interactions: List[Dict]) -> bool:
        """Detect confirmation bias - seeking confirming evidence while avoiding contradictory."""
        # Tests that might confirm heart failure
        confirmatory_intents = ["lab_tests", "imaging", "ekg"]
        # More diverse assessment that might contradict
        contradictory_intents = [
            "social_history",
            "family_history",
            "past_medical_history",
        ]

        # Also check keywords
        confirmatory_keywords = ["bnp", "chest x-ray", "echo", "heart failure"]
        contradictory_keywords = ["other", "different", "alternative", "rule out"]

        confirmatory_count = 0
        contradictory_count = 0

        for interaction in interactions:
            intent_id = interaction.get("intent_id", "")
            user_query = interaction.get("user_query", "").lower()

            # Check confirmatory evidence
            if any(intent in intent_id for intent in confirmatory_intents) or any(
                keyword in user_query for keyword in confirmatory_keywords
            ):
                confirmatory_count += 1

            # Check contradictory/broader assessment
            if any(intent in intent_id for intent in contradictory_intents) or any(
                keyword in user_query for keyword in contradictory_keywords
            ):
                contradictory_count += 1

        # If asking many confirmatory questions but avoiding contradictory ones
        return confirmatory_count >= 2 and contradictory_count == 0

    def _detect_premature_closure(self) -> bool:
        """Detect if user is trying to conclude/diagnose without sufficient investigation."""
        if not self.session_data["interactions"]:
            return False

        # Only check the most recent user input for conclusion attempts
        latest_input = (
            self.session_data["interactions"][-1].get("user_query", "").lower()
        )

        # Keywords that indicate doctor is trying to conclude/diagnose
        conclusion_keywords = [
            "diagnosis",
            "diagnose",
            "conclusion",
            "conclude",
            "final",
            "treatment",
            "recommend",
            "prescription",
            "discharge",
            "follow up",
            "plan",
            "likely",
            "probably",
            "most likely",
            "appears to be",
            "seems like",
            "let's treat",
            "start treatment",
            "prescribe",
            "medication for",
            "it's",
            "this is",
            "you have",
            "patient has",
            "have heart failure",
            "start",
            "begin treatment",
            "lisinopril",
            "medication",
        ]

        # Essential assessment areas that should be covered
        essential_areas = {
            "history": ["history", "symptoms", "when", "started", "duration"],
            "physical": ["examine", "listen", "check", "feel", "look"],
            "vitals": ["blood pressure", "heart rate", "temperature", "pulse"],
            "tests": ["test", "lab", "x-ray", "ekg", "blood work"],
        }

        # Check if current input suggests conclusion attempt
        has_conclusion_attempt = any(
            keyword in latest_input for keyword in conclusion_keywords
        )

        if has_conclusion_attempt:
            # Check how many essential areas have been covered in the entire conversation
            all_inputs = [
                interaction.get("user_query", "").lower()
                for interaction in self.session_data["interactions"]
            ]

            covered_areas = 0
            for area, keywords in essential_areas.items():
                if any(
                    keyword in input_text
                    for input_text in all_inputs
                    for keyword in keywords
                ):
                    covered_areas += 1

            # If trying to conclude but haven't covered enough essential areas
            return covered_areas < 2  # Should cover at least 2 out of 4 essential areas

        return False

    def _add_bias_warning(self, bias_type: str, message: str):
        """Add a bias warning to the session."""
        # Don't duplicate recent warnings
        recent_biases = [
            b["bias_type"] for b in self.session_data["detected_biases"][-3:]
        ]
        if bias_type not in recent_biases:
            bias_warning = {
                "bias_type": bias_type,
                "message": message,
                "timestamp": datetime.now().isoformat(),
                "interaction_count": len(self.session_data["interactions"]),
            }
            self.session_data["detected_biases"].append(bias_warning)
            sys_logger.log_system("info", f"Bias detected: {bias_type} - {message}")

    def get_latest_bias_warning(self) -> Dict[str, Any]:
        """Get the most recent bias warning if any."""
        if self.session_data["detected_biases"]:
            return self.session_data["detected_biases"][-1]
        return {}

    def get_session_summary(self) -> Dict[str, Any]:
        """Get a summary of the current session."""
        return {
            "session_id": self.session_data["session_id"],
            "duration": self._calculate_duration(),
            "total_interactions": len(self.session_data["interactions"]),
            "biases_detected": len(self.session_data["detected_biases"]),
            "bias_types": list(
                set([b["bias_type"] for b in self.session_data["detected_biases"]])
            ),
            "current_state": self.session_data["current_state"],
        }

    def _calculate_duration(self) -> str:
        """Calculate session duration in minutes."""
        start = datetime.fromisoformat(self.session_data["start_time"])
        now = datetime.now()
        duration = (now - start).total_seconds() / 60
        return f"{duration:.1f} minutes"

    def get_session_duration_minutes(self) -> float:
        """Get session duration in minutes as a float."""
        start = datetime.fromisoformat(self.session_data["start_time"])
        now = datetime.now()
        duration = (now - start).total_seconds() / 60
        return round(duration, 1)

    def save_session(self, filepath: str = None):
        """Save session data to file."""
        if not filepath:
            filepath = f"logs/session_{self.session_data['session_id']}.json"

        self.session_data["end_time"] = datetime.now().isoformat()

        try:
            # Ensure logs directory exists
            import os

            os.makedirs("logs", exist_ok=True)

            with open(filepath, "w") as f:
                json.dump(self.session_data, f, indent=2)
            sys_logger.log_system("info", f"Session saved to {filepath}")
        except Exception as e:
            sys_logger.log_system("error", f"Failed to save session: {e}")


# Global session logger instance
current_session = None


def get_current_session() -> SessionLogger:
    """Get or create the current session logger."""
    global current_session
    if current_session is None:
        current_session = SessionLogger()
    return current_session


def start_new_session() -> SessionLogger:
    """Start a new session, saving the previous one if it exists."""
    global current_session
    if current_session is not None:
        current_session.save_session()
    current_session = SessionLogger()
    return current_session
