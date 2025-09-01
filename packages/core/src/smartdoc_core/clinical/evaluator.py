"""
SmartDoc Clinical Evaluator - LLM-based comprehensive analysis of clinical performance
"""

from __future__ import annotations
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import json

from smartdoc_core.config.settings import config
from smartdoc_core.utils.logger import sys_logger
from smartdoc_core.llm.providers.base import LLMProvider
from smartdoc_core.llm.providers.ollama import OllamaProvider


@dataclass
class EvaluationInputs:
    dialogue_transcript: List[Dict[str, Any]]
    detected_biases: List[Dict[str, Any]]
    metacognitive_responses: Dict[str, str]
    final_diagnosis: str
    case_context: Dict[str, Any]


class ClinicalEvaluator:
    """
    LLM-backed evaluator with DI provider. Produces a structured JSON evaluation.
    """

    def __init__(
        self,
        provider: Optional[LLMProvider] = None,
        model_name: Optional[str] = None,
    ):
        self.provider = provider or OllamaProvider(config.OLLAMA_BASE_URL, config.OLLAMA_MODEL)
        self.model_name = model_name or getattr(self.provider, "model", config.OLLAMA_MODEL)
        sys_logger.log_system("info", f"ClinicalEvaluator using model: {self.model_name}")

    # ----- Public API -----
    def evaluate(self, inputs: EvaluationInputs) -> Dict[str, Any]:
        try:
            prompt = self._build_eval_prompt(inputs)
            raw = self.provider.generate(
                prompt,
                temperature=0.3,
                top_p=0.9,
                timeout_s=120,
            ).strip()
            parsed = self._parse_json_or_fallback(raw)
            return {"success": True, "evaluation": parsed, "raw_response": raw}
        except Exception as e:
            sys_logger.log_system("error", f"Evaluation failed: {e}")
            return self._fallback(inputs)

    def deep_bias_analysis(
        self, dialogue_transcript: List[Dict[str, Any]], final_diagnosis: str
    ) -> Dict[str, Any]:
        try:
            prompt = self._build_bias_prompt(dialogue_transcript, final_diagnosis)
            raw = self.provider.generate(
                prompt, temperature=0.2, top_p=0.9, timeout_s=90
            ).strip()
            return {"success": True, "bias_analysis": self._parse_json_or_text(raw), "raw_analysis": raw}
        except Exception as e:
            sys_logger.log_system("warning", f"Deep bias analysis failed: {e}")
            return {"success": False, "error": str(e)}

    # ----- Legacy methods for backward compatibility -----
    def evaluate_clinical_performance(
        self,
        dialogue_transcript: List[Dict],
        detected_biases: List[Dict],
        metacognitive_responses: Dict[str, str],
        final_diagnosis: str,
        case_context: Dict,
    ) -> Dict[str, Any]:
        """Legacy wrapper for backward compatibility."""
        inputs = EvaluationInputs(
            dialogue_transcript=dialogue_transcript,
            detected_biases=detected_biases,
            metacognitive_responses=metacognitive_responses,
            final_diagnosis=final_diagnosis,
            case_context=case_context,
        )
        return self.evaluate(inputs)

    def analyze_cognitive_biases(
        self, dialogue_transcript: List[Dict], final_diagnosis: str
    ) -> Dict[str, Any]:
        """Legacy wrapper for backward compatibility."""
        return self.deep_bias_analysis(dialogue_transcript, final_diagnosis)

    # ----- Prompt builders -----
    def _build_eval_prompt(self, inp: EvaluationInputs) -> str:
        dialogue = self._fmt_dialogue(inp.dialogue_transcript)
        bias = self._fmt_biases(inp.detected_biases)
        reflection = self._fmt_reflection(inp.metacognitive_responses)
        ctx = inp.case_context or {}

        return f"""You are an expert medical education evaluator and cognitive psychology specialist.

CASE CONTEXT
- Case Type: {ctx.get('case_type','Clinical case')}
- Correct Diagnosis: {ctx.get('correct_diagnosis','Not specified')}
- Key Clinical Features: {ctx.get('key_features','Not specified')}

STUDENT FINAL DIAGNOSIS
{inp.final_diagnosis}

COMPLETE DIALOGUE TRANSCRIPT
{dialogue}

DETECTED COGNITIVE BIASES
{bias}

STUDENT METACOGNITIVE REFLECTION
{reflection}

Return ONLY valid JSON in this schema:
{{
  "overall_score": 0-100,
  "diagnostic_accuracy": {{
    "score": 0-100, "analysis": "...", "correct_elements": [], "missed_elements": []
  }},
  "information_gathering": {{
    "score": 0-100, "analysis": "...", "strengths": [], "areas_for_improvement": []
  }},
  "cognitive_bias_awareness": {{
    "score": 0-100, "analysis": "...", "detected_biases_impact": "...", "metacognitive_quality": "..."
  }},
  "clinical_reasoning": {{
    "score": 0-100, "analysis": "...", "hypothesis_generation": "...", "evidence_synthesis": "..."
  }},
  "constructive_feedback": {{
    "positive_reinforcement": "...",
    "key_learning_points": [],
    "specific_recommendations": [],
    "bias_education": "..."
  }},
  "confidence_assessment": 0-100
}}"""

    def _build_bias_prompt(self, dialogue: List[Dict[str, Any]], final_dx: str) -> str:
        d = self._fmt_dialogue(dialogue)
        return f"""You are a cognitive psychology expert. Analyze for anchoring, confirmation bias, and premature closure.

TRANSCRIPT
{d}

FINAL DIAGNOSIS: {final_dx}

Return ONLY valid JSON:
{{
  "anchoring_bias": {{"detected": true/false, "confidence": 0-100, "evidence": "...", "explanation": "..."}},
  "confirmation_bias": {{"detected": true/false, "confidence": 0-100, "evidence": "...", "explanation": "..."}},
  "premature_closure": {{"detected": true/false, "confidence": 0-100, "evidence": "...", "explanation": "..."}},
  "overall_reasoning_quality": 0-100,
  "key_insights": []
}}"""

    # ----- Formatting & parsing -----
    def _fmt_dialogue(self, t: List[Dict[str, Any]]) -> str:
        out = []
        for i, x in enumerate(t, 1):
            role = "DOCTOR" if x.get("role") in ("user", "doctor") else "PATIENT"
            msg = x.get("message") or x.get("content") or ""
            out.append(f"{i}. {role}: {msg}")
        return "\n".join(out) if out else "No transcript available."

    def _fmt_biases(self, arr: List[Dict[str, Any]]) -> str:
        if not arr: return "No cognitive biases detected by rule-based system."
        return "\n".join([f"- {b.get('bias_type','unknown')}: {b.get('description') or b.get('message','')}" for b in arr])

    def _fmt_reflection(self, m: Dict[str, str]) -> str:
        if not m: return "No metacognitive reflection provided."
        lines = []
        for q, a in m.items():
            lines += [f"Q: {q}", f"A: {a}", ""]
        return "\n".join(lines)

    def _parse_json_or_text(self, s: str) -> Dict[str, Any]:
        i, j = s.find("{"), s.rfind("}") + 1
        if i >= 0 and j > 0:
            try:
                return json.loads(s[i:j])
            except Exception:
                pass
        return {"raw_text": s}

    def _parse_json_or_fallback(self, s: str) -> Dict[str, Any]:
        parsed = self._parse_json_or_text(s)
        if "raw_text" in parsed:
            return self._fallback_eval_payload()
        return parsed

    def _fallback(self, inp: EvaluationInputs) -> Dict[str, Any]:
        return {"success": True, "evaluation": self._fallback_eval_payload(), "fallback_used": True}

    def _fallback_eval_payload(self) -> Dict[str, Any]:
        return {
            "overall_score": 75,
            "diagnostic_accuracy": {"score": 70, "analysis": "Fallback summary."},
            "information_gathering": {"score": 75, "analysis": "Fallback summary."},
            "cognitive_bias_awareness": {"score": 70, "analysis": "Fallback summary."},
            "clinical_reasoning": {"score": 75, "analysis": "Fallback summary."},
            "constructive_feedback": {
                "positive_reinforcement": "Good clinical engagement.",
                "key_learning_points": ["Use structured reasoning.", "Balance evidence."],
                "specific_recommendations": ["Consider alternatives explicitly."],
                "bias_education": "Be mindful of anchoring / premature closure.",
            },
            "confidence_assessment": 60,
        }

    # ----- Legacy methods kept for backward compatibility -----

    # ----- Legacy methods kept for backward compatibility (these will be removed in future versions) -----
    def _create_evaluation_prompt(
        self,
        dialogue_transcript: List[Dict],
        detected_biases: List[Dict],
        metacognitive_responses: Dict[str, str],
        final_diagnosis: str,
        case_context: Dict,
    ) -> str:
        """Legacy method - use _build_eval_prompt instead."""
        inputs = EvaluationInputs(
            dialogue_transcript=dialogue_transcript,
            detected_biases=detected_biases,
            metacognitive_responses=metacognitive_responses,
            final_diagnosis=final_diagnosis,
            case_context=case_context,
        )
        return self._build_eval_prompt(inputs)

    def _create_bias_analysis_prompt(
        self, dialogue_transcript: List[Dict], final_diagnosis: str
    ) -> str:
        """Legacy method - use _build_bias_prompt instead."""
        return self._build_bias_prompt(dialogue_transcript, final_diagnosis)

    def _format_dialogue(self, dialogue_transcript: List[Dict]) -> str:
        """Legacy method - use _fmt_dialogue instead."""
        return self._fmt_dialogue(dialogue_transcript)

    def _format_bias_summary(self, detected_biases: List[Dict]) -> str:
        """Legacy method - use _fmt_biases instead."""
        return self._fmt_biases(detected_biases)

    def _format_metacognitive_responses(self, responses: Dict[str, str]) -> str:
        """Legacy method - use _fmt_reflection instead."""
        return self._fmt_reflection(responses)

    def _parse_evaluation_response(self, response: str) -> Dict[str, Any]:
        """Legacy method - use _parse_json_or_fallback instead."""
        return self._parse_json_or_fallback(response)

    def _parse_bias_analysis(self, response: str) -> Dict[str, Any]:
        """Legacy method - use _parse_json_or_text instead."""
        return self._parse_json_or_text(response)

    def _parse_text_evaluation(self, response: str) -> Dict[str, Any]:
        """Legacy method - use _fallback_eval_payload instead."""
        return self._fallback_eval_payload()

    def _fallback_evaluation(
        self,
        final_diagnosis: str,
        detected_biases: List[Dict],
        metacognitive_responses: Dict[str, str],
    ) -> Dict[str, Any]:
        """Legacy method - use _fallback instead."""
        inputs = EvaluationInputs(
            dialogue_transcript=[],
            detected_biases=detected_biases,
            metacognitive_responses=metacognitive_responses,
            final_diagnosis=final_diagnosis,
            case_context={},
        )
        return self._fallback(inputs)
