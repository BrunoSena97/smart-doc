"""
Cognitive Bias Analyzer for SmartDoc Virtual Patient Simulation

This module implements rule-based cognitive bias detection algorithms for clinical
reasoning assessment, providing real-time and session-level bias analysis.
"""

from typing import Dict, List, Any
from datetime import datetime
import json


class BiasEvaluator:
    """
    Enhanced rule-based bias detection with case-adaptive logic, persistence checks,
    and minimum sample sizes for improved reliability and research validity.
    """

    def __init__(self, case_data: Dict[str, Any]):
        self.case_data = case_data
        self.bias_triggers = case_data.get("biasTriggers", {})

        # Calculate case-adaptive thresholds
        self.total_blocks = len(case_data.get("informationBlocks", []))
        self.critical_findings = set(case_data.get("groundTruth", {}).get("criticalFindingIds", []))

        # Adaptive thresholds based on case complexity
        self.min_actions_threshold = max(3, round(0.2 * self.total_blocks))
        self.min_critical_threshold = 0.5  # At least 50% of critical findings
        self.min_sample_size = 3  # Minimum evidence sample for bias detection

        # Intent taxonomy for robust pattern detection
        self.cardio_intents = ["exam_cardiovascular", "lab_tests_cardiac", "vital_signs", "imaging_cardiac"]
        self.broad_intents = ["pmh_general", "social_history", "family_history", "exam_general_appearance", "review_of_systems"]
        self.assessment_intents = ["assessment", "treatment", "diagnosis", "differential"]
        self.info_gathering_intents = ["hpi_", "pmh_", "exam_", "lab_", "history", "imaging_"]

        print(f"BiasEvaluator initialized: {self.total_blocks} blocks, {len(self.critical_findings)} critical findings")
        print(f"Adaptive thresholds: min_actions={self.min_actions_threshold}, min_critical={self.min_critical_threshold}")

    def evaluate_session(
        self,
        session_log: List[Dict],
        revealed_blocks: set,
        hypotheses: List[Dict],
        final_diagnosis: str,
    ) -> Dict[str, Any]:
        """
        Evaluate a complete session for cognitive biases using rule-based heuristics.

        Args:
            session_log: List of user actions with timestamps
            revealed_blocks: Set of block IDs that were revealed
            hypotheses: List of working hypotheses added by student
            final_diagnosis: Final diagnosis submitted

        Returns:
            Dictionary with bias analysis results
        """

        results = {
            "anchoring_bias": self._detect_anchoring_bias(
                session_log, hypotheses, final_diagnosis
            ),
            "confirmation_bias": self._detect_confirmation_bias(revealed_blocks),
            "premature_closure": self._detect_premature_closure(
                revealed_blocks, session_log
            ),
            "overall_score": 0,
            "detailed_analysis": {},
        }

        # Calculate overall bias score
        bias_count = sum(
            [
                1
                for bias in results.values()
                if isinstance(bias, dict) and bias.get("detected", False)
            ]
        )
        results["overall_score"] = bias_count

        return results

    def check_real_time_bias(
        self,
        session_interactions: List[Dict],
        current_intent: str,
        user_input: str,
        vsp_response: str,
    ) -> Dict[str, Any]:
        """
        Real-time bias detection during the conversation flow.
        Integrates with the main SmartDoc dialogue system.

        Args:
            session_interactions: All interactions in current session
            current_intent: The intent just classified
            user_input: User's current input
            vsp_response: System's response

        Returns:
            Dictionary with bias detection results for immediate feedback
        """

        # Skip if too few interactions for meaningful analysis
        if len(session_interactions) < 3:
            return {
                "detected": False,
                "reason": "Insufficient interactions for bias detection",
            }

        # Check for different bias types in real-time
        anchoring_result = self._real_time_anchoring_check(
            session_interactions, current_intent, user_input
        )
        if anchoring_result["detected"]:
            return anchoring_result

        confirmation_result = self._real_time_confirmation_check(
            session_interactions, current_intent
        )
        if confirmation_result["detected"]:
            return confirmation_result

        premature_result = self._real_time_premature_closure_check(
            session_interactions, current_intent
        )
        if premature_result["detected"]:
            return premature_result

        return {
            "detected": False,
            "reason": "No biases detected in current interaction",
        }

    def _real_time_anchoring_check(
        self, interactions: List[Dict], current_intent: str, user_input: str
    ) -> Dict[str, Any]:
        """Real-time anchoring bias detection."""
        if not self.bias_triggers.get("anchoring"):
            return {"detected": False, "reason": "No anchoring triggers configured"}

        # Look for cardiovascular/heart failure focus pattern
        recent_interactions = interactions[-5:]  # Last 5 interactions
        cardio_keywords = [
            "heart",
            "cardiac",
            "chest",
            "cardiovascular",
            "failure",
            "bnp",
            "echo",
        ]
        cardio_intents = ["exam_cardiovascular", "lab_tests", "vital_signs"]

        cardio_count = 0
        for interaction in recent_interactions:
            intent_id = interaction.get("intent_id", "")
            query = interaction.get("user_query", "").lower()

            if any(keyword in query for keyword in cardio_keywords):
                cardio_count += 1
            if any(cardio_intent in intent_id for cardio_intent in cardio_intents):
                cardio_count += 1

        # If >70% recent focus on cardiovascular, flag anchoring
        if (
            len(recent_interactions) > 0
            and (cardio_count / len(recent_interactions)) > 0.7
        ):
            return {
                "detected": True,
                "bias_type": "anchoring",
                "message": "⚠️ You seem focused on heart failure. Consider other diagnoses that could cause dyspnea.",
                "confidence": 0.8,
                "details": f"Cardiovascular focus in {cardio_count}/{len(recent_interactions)} recent interactions",
            }

        return {"detected": False}

    def _real_time_confirmation_check(
        self, interactions: List[Dict], current_intent: str
    ) -> Dict[str, Any]:
        """Real-time confirmation bias detection."""
        if not self.bias_triggers.get("confirmation"):
            return {
                "detected": False,
                "reason": "No confirmation bias triggers configured",
            }

        # Count confirmatory vs. refuting evidence gathering
        confirmatory_intents = ["lab_tests", "exam_cardiovascular", "vital_signs"]
        broader_intents = [
            "pmh_general",
            "social_history",
            "family_history",
            "exam_general_appearance",
        ]

        recent_interactions = interactions[-7:]  # Larger window for confirmation bias

        confirmatory_count = sum(
            1
            for i in recent_interactions
            if any(intent in i.get("intent_id", "") for intent in confirmatory_intents)
        )
        broader_count = sum(
            1
            for i in recent_interactions
            if any(intent in i.get("intent_id", "") for intent in broader_intents)
        )

        # Flag if heavily skewed toward confirmatory evidence
        if confirmatory_count >= 3 and broader_count == 0:
            return {
                "detected": True,
                "bias_type": "confirmation",
                "message": "⚠️ Consider exploring other aspects: social history, PMH, or alternative diagnoses.",
                "confidence": 0.7,
                "details": f"Confirmatory: {confirmatory_count}, Broader: {broader_count}",
            }

        return {"detected": False}

    def _real_time_premature_closure_check(
        self, interactions: List[Dict], current_intent: str
    ) -> Dict[str, Any]:
        """Real-time premature closure detection."""

        # Check if student is trying to reach conclusions too early
        assessment_intents = ["assessment", "treatment", "diagnosis"]
        info_gathering_intents = ["hpi_", "pmh_", "exam_", "lab_", "history"]

        # Count recent information gathering vs assessment attempts
        recent_interactions = interactions[-10:]

        assessment_count = sum(
            1
            for i in recent_interactions
            if any(intent in i.get("intent_id", "") for intent in assessment_intents)
        )

        info_count = sum(
            1
            for i in recent_interactions
            if any(
                intent in i.get("intent_id", "") for intent in info_gathering_intents
            )
        )

        # Flag if trying to assess with minimal information gathering
        if assessment_count > 0 and info_count < 5:
            return {
                "detected": True,
                "bias_type": "premature_closure",
                "message": "⚠️ Consider gathering more information before reaching conclusions.",
                "confidence": 0.6,
                "details": f"Assessment attempts: {assessment_count}, Info gathering: {info_count}",
            }

        return {"detected": False}

    def _detect_anchoring_bias(
        self, session_log: List[Dict], hypotheses: List[Dict], final_diagnosis: str
    ) -> Dict[str, Any]:
        """
        Enhanced Anchoring Bias Detection with Persistence Analysis

        Detects anchoring by checking:
        1. Initial hypothesis formation
        2. Contradictory evidence revelation
        3. Persistence after contradiction (key enhancement)
        4. Final diagnosis alignment with anchor
        """

        if not hypotheses or not self.bias_triggers.get("anchoring"):
            return {
                "detected": False,
                "reason": "No hypotheses or anchoring triggers defined",
            }

        # Get the initial hypothesis and timestamp
        initial_hypothesis = hypotheses[0]["diagnosis"].lower().strip()
        initial_timestamp = hypotheses[0].get("timestamp")

        # Check if initial hypothesis matches the anchor from case metadata
        anchor_info = self.bias_triggers["anchoring"].get("anchorDescription", "").lower()
        anchor_keywords = ["heart failure", "cardiac", "chf"]  # More flexible matching

        if not any(keyword in initial_hypothesis for keyword in anchor_keywords):
            return {
                "detected": False,
                "reason": "Initial hypothesis doesn't match expected anchor patterns",
            }

        # Find when contradictory evidence was revealed
        contradictory_block_id = self.bias_triggers["anchoring"].get("contradictoryInfoId")
        contradictory_timestamp = None

        for action in session_log:
            if (
                action.get("action_type") == "view_info"
                and action.get("details", {}).get("blockId") == contradictory_block_id
            ):
                contradictory_timestamp = action.get("timestamp")
                break

        if not contradictory_timestamp:
            return {"detected": False, "reason": "Contradictory evidence not revealed"}

        # ENHANCED: Check persistence after contradiction
        persistence_score = self._check_anchoring_persistence(
            session_log, contradictory_timestamp, anchor_keywords
        )

        # Check if final diagnosis still matches anchor
        final_matches_initial = any(keyword in final_diagnosis.lower() for keyword in anchor_keywords)

        if final_matches_initial and persistence_score > 0.5:
            confidence = min(0.9, 0.6 + persistence_score * 0.3)  # Scale confidence with persistence
            return {
                "detected": True,
                "reason": "Strong anchoring detected: initial hypothesis persisted despite contradictory evidence",
                "initial_hypothesis": initial_hypothesis,
                "contradictory_evidence": contradictory_block_id,
                "final_diagnosis": final_diagnosis,
                "persistence_score": persistence_score,
                "confidence": confidence,
            }
        elif final_matches_initial:
            return {
                "detected": True,
                "reason": "Moderate anchoring detected: final diagnosis matches initial anchor",
                "initial_hypothesis": initial_hypothesis,
                "final_diagnosis": final_diagnosis,
                "confidence": 0.6,
            }

        return {
            "detected": False,
            "reason": "Final diagnosis differs from initial anchor or insufficient persistence",
        }

    def _check_anchoring_persistence(self, session_log: List[Dict], contra_timestamp: str, anchor_keywords: List[str]) -> float:
        """Check if student persisted with anchor-related activities after contradictory evidence."""
        # Get actions after contradictory evidence
        post_contra_actions = [
            action for action in session_log
            if action.get("timestamp", "") > contra_timestamp
        ]

        if len(post_contra_actions) < 2:
            return 0.0  # Insufficient data

        # Count anchor-focused vs. broader exploration
        anchor_focus_count = 0
        for action in post_contra_actions:
            intent_id = action.get("intent_id", "")
            query = action.get("user_query", "").lower()

            # Check for continued cardio focus
            if any(cardio_intent in intent_id for cardio_intent in self.cardio_intents):
                anchor_focus_count += 1
            elif any(keyword in query for keyword in anchor_keywords):
                anchor_focus_count += 1

        persistence_ratio = anchor_focus_count / len(post_contra_actions)
        return persistence_ratio

    def _detect_confirmation_bias(self, revealed_blocks: set) -> Dict[str, Any]:
        """
        Algorithm 2: Confirmation Bias Detection

        Implementation from Table 1:
        1. Student adds an incorrect hypothesis (add_hypothesis)
        2. Student's subsequent view_info actions disproportionately access supporting evidence
           while neglecting refuting evidence
        """

        if not self.bias_triggers.get("confirmation"):
            return {
                "detected": False,
                "reason": "No confirmation bias triggers defined",
            }

        confirmation_data = self.bias_triggers["confirmation"]
        supporting_blocks = set(confirmation_data.get("supportingInfoIds", []))
        refuting_blocks = set(confirmation_data.get("refutingInfoIds", []))

        if not supporting_blocks or not refuting_blocks:
            return {"detected": False, "reason": "Insufficient bias trigger data"}

        # Calculate what was actually revealed
        revealed_supporting = supporting_blocks.intersection(revealed_blocks)
        revealed_refuting = refuting_blocks.intersection(revealed_blocks)

        # Apply the heuristic: disproportionate focus on supporting evidence
        total_supporting = len(supporting_blocks)
        total_refuting = len(refuting_blocks)

        support_ratio = (
            len(revealed_supporting) / total_supporting if total_supporting > 0 else 0
        )
        refute_ratio = (
            len(revealed_refuting) / total_refuting if total_refuting > 0 else 0
        )

        # Bias detected if: high support ratio AND low refute ratio
        if support_ratio >= 0.5 and refute_ratio < 0.3:
            return {
                "detected": True,
                "reason": "Disproportionate focus on confirming evidence while avoiding contradictory evidence",
                "supporting_revealed": list(revealed_supporting),
                "refuting_revealed": list(revealed_refuting),
                "support_ratio": round(support_ratio, 2),
                "refute_ratio": round(refute_ratio, 2),
                "confidence": 0.8,
            }

        return {
            "detected": False,
            "reason": f"Balanced information gathering (support: {support_ratio:.1%}, refute: {refute_ratio:.1%})",
        }

    def _detect_premature_closure(
        self, revealed_blocks: set, session_log: List[Dict]
    ) -> Dict[str, Any]:
        """
        Algorithm 3: Premature Closure Detection

        Implementation from Table 1:
        1. Student adds a hypothesis (add_hypothesis)
        2. Student submits final diagnosis with few intervening view_info events
        3. The submitted diagnosis is incorrect or differential is incomplete
        """

        # Check if critical findings were revealed
        critical_findings = set(
            self.case_data.get("groundTruth", {}).get("criticalFindingIds", [])
        )
        if not critical_findings:
            return {"detected": False, "reason": "No critical findings defined in case"}

        revealed_critical = critical_findings.intersection(revealed_blocks)
        critical_ratio = len(revealed_critical) / len(critical_findings)

        # Count information gathering actions
        info_gathering_actions = [
            action for action in session_log if action.get("action_type") == "view_info"
        ]

        # Detect premature closure based on:
        # 1. Low critical findings discovery rate
        # 2. Few information gathering actions
        min_critical_threshold = 0.5  # Should find at least 50% of critical findings
        min_actions_threshold = (
            3  # Should perform at least 3 information gathering actions
        )

        if (
            critical_ratio < min_critical_threshold
            and len(info_gathering_actions) < min_actions_threshold
        ):
            return {
                "detected": True,
                "reason": "Insufficient information gathering before reaching conclusion",
                "critical_findings_found": len(revealed_critical),
                "critical_findings_total": len(critical_findings),
                "critical_ratio": round(critical_ratio, 2),
                "info_actions_count": len(info_gathering_actions),
                "confidence": 0.9,
            }

        # Mild premature closure if only one threshold is violated
        if critical_ratio < min_critical_threshold:
            return {
                "detected": True,
                "reason": "Missed critical findings suggesting incomplete investigation",
                "critical_findings_found": len(revealed_critical),
                "critical_findings_total": len(critical_findings),
                "critical_ratio": round(critical_ratio, 2),
                "confidence": 0.6,
            }

        if len(info_gathering_actions) < min_actions_threshold:
            return {
                "detected": True,
                "reason": "Very limited information gathering before conclusion",
                "info_actions_count": len(info_gathering_actions),
                "confidence": 0.7,
            }

        return {
            "detected": False,
            "reason": f"Adequate investigation (critical: {critical_ratio:.1%}, actions: {len(info_gathering_actions)})",
        }

    def generate_feedback_report(self, evaluation_results: Dict[str, Any]) -> str:
        """
        Generate educational feedback based on bias detection results.
        """

        feedback_sections = []

        # Overall assessment
        bias_count = evaluation_results["overall_score"]
        if bias_count == 0:
            feedback_sections.append(
                "🎉 Excellent! No significant cognitive biases detected in your clinical reasoning."
            )
        elif bias_count == 1:
            feedback_sections.append(
                "⚠️ One cognitive bias pattern was detected. Review the analysis below to improve your clinical reasoning."
            )
        else:
            feedback_sections.append(
                f"🚨 Multiple cognitive bias patterns detected ({bias_count}). This suggests significant room for improvement in clinical reasoning."
            )

        # Specific feedback for each bias
        if evaluation_results["anchoring_bias"]["detected"]:
            feedback_sections.append(
                self._generate_anchoring_feedback(evaluation_results["anchoring_bias"])
            )

        if evaluation_results["confirmation_bias"]["detected"]:
            feedback_sections.append(
                self._generate_confirmation_feedback(
                    evaluation_results["confirmation_bias"]
                )
            )

        if evaluation_results["premature_closure"]["detected"]:
            feedback_sections.append(
                self._generate_closure_feedback(evaluation_results["premature_closure"])
            )

        return "\n\n".join(feedback_sections)

    def _generate_anchoring_feedback(self, result: Dict) -> str:
        return f"""
        🔗 **Anchoring Bias Detected**

        You initially focused on "{result['initial_hypothesis']}" and maintained this diagnosis even after revealing contradictory evidence ({result['contradictory_evidence']}).

        **Improvement Strategy:**
        - When new information contradicts your initial hypothesis, actively reconsider your differential diagnosis
        - Ask yourself: "What else could explain these findings?"
        - Consider the likelihood of alternative diagnoses given the new evidence
        """

    def _generate_confirmation_feedback(self, result: Dict) -> str:
        return f"""
        ✅ **Confirmation Bias Detected**

        You revealed {len(result['supporting_revealed'])} pieces of supporting evidence but only {len(result['refuting_revealed'])} pieces of contradictory evidence (support ratio: {result['support_ratio']:.1%}, refute ratio: {result['refute_ratio']:.1%}).

        **Improvement Strategy:**
        - Actively seek information that could disprove your working diagnosis
        - Ask: "What findings would make me reconsider this diagnosis?"
        - Consider: "What red flags am I missing?"
        """

    def _generate_closure_feedback(self, result: Dict) -> str:
        critical_ratio = result.get("critical_ratio", 0)
        actions_count = result.get("info_actions_count", 0)

        return f"""
        🏁 **Premature Closure Detected**

        You found only {critical_ratio:.1%} of critical findings and performed {actions_count} information-gathering actions before reaching your conclusion.

        **Improvement Strategy:**
        - Gather more information before finalizing your diagnosis
        - Ensure you've performed a systematic review of history, physical exam, and appropriate tests
        - Consider: "What important information might I be missing?"
        """


def create_bias_evaluation_demo():
    """
    Create a demonstration of the bias evaluation system.
    This shows how the rule-based algorithms work with sample data.
    """

    # Sample case data (simplified version of your mull_diagnostic_error.json)
    case_data = {
        "biasTriggers": {
            "anchoring": {
                "anchorDescription": "heart failure exacerbation anchored by preliminary chest x-ray",
                "contradictoryInfoId": "critical_echo",
            },
            "confirmation": {
                "incorrectHypothesis": "Heart failure exacerbation",
                "supportingInfoIds": ["pe_resp", "lab_bnp", "img_prelim_cxr"],
                "refutingInfoIds": [
                    "hist_weight_loss",
                    "pe_cardiac_neg",
                    "critical_formal_cxr",
                    "critical_infliximab",
                    "critical_echo",
                ],
            },
        },
        "groundTruth": {
            "finalDiagnosis": "Miliary tuberculosis",
            "criticalFindingIds": [
                "hist_weight_loss",
                "pe_cardiac_neg",
                "critical_formal_cxr",
                "critical_infliximab",
                "critical_echo",
                "critical_ct_chest",
            ],
        },
    }

    # Sample session with bias patterns
    biased_session = {
        "session_log": [
            {
                "action_type": "add_hypothesis",
                "details": {"diagnosis": "Heart failure exacerbation"},
                "timestamp": "2025-07-20T10:00:00",
            },
            {
                "action_type": "view_info",
                "details": {"blockId": "pe_resp"},
                "timestamp": "2025-07-20T10:01:00",
            },
            {
                "action_type": "view_info",
                "details": {"blockId": "lab_bnp"},
                "timestamp": "2025-07-20T10:02:00",
            },
            {
                "action_type": "view_info",
                "details": {"blockId": "critical_echo"},
                "timestamp": "2025-07-20T10:03:00",
            },
            {
                "action_type": "submit_final_diagnosis",
                "details": {"diagnosis": "Heart failure exacerbation"},
                "timestamp": "2025-07-20T10:04:00",
            },
        ],
        "revealed_blocks": {"pe_resp", "lab_bnp", "critical_echo"},
        "hypotheses": [
            {
                "diagnosis": "Heart failure exacerbation",
                "timestamp": "2025-07-20T10:00:00",
            }
        ],
        "final_diagnosis": "Heart failure exacerbation",
    }

    # Run bias evaluation
    evaluator = BiasEvaluator(case_data)
    results = evaluator.evaluate_session(
        biased_session["session_log"],
        biased_session["revealed_blocks"],
        biased_session["hypotheses"],
        biased_session["final_diagnosis"],
    )

    return results, evaluator.generate_feedback_report(results)


if __name__ == "__main__":
    # Demonstration
    results, feedback = create_bias_evaluation_demo()
    print("=== BIAS EVALUATION RESULTS ===")
    print(json.dumps(results, indent=2))
    print("\n=== EDUCATIONAL FEEDBACK ===")
    print(feedback)
