"""
SmartDoc Clinical Evaluator - LLM-based comprehensive analysis of clinical performance
Enhanced with structured validation, rubric-based scoring, and research reliability features.
"""

from __future__ import annotations
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import json
import re
from datetime import datetime
from pydantic import ValidationError

from smartdoc_core.config.settings import config
from smartdoc_core.utils.logger import sys_logger
from smartdoc_core.llm.providers.base import LLMProvider
from smartdoc_core.llm.providers.ollama import OllamaProvider
from smartdoc_core.clinical.evaluation_schemas import (
    ClinicalEvaluation, BiasAnalysis, ReliabilityMetrics, ResearchEvaluationOutput
)


@dataclass
class EvaluationInputs:
    dialogue_transcript: List[Dict[str, Any]]
    detected_biases: List[Dict[str, Any]]
    metacognitive_responses: Dict[str, str]
    final_diagnosis: str
    case_context: Dict[str, Any]


class ClinicalEvaluator:
    """
    Research-grade LLM evaluator with structured validation, rubric-based scoring,
    and reliability tracking for clinical simulation assessment.
    """

    def __init__(
        self,
        provider: Optional[LLMProvider] = None,
        model_name: Optional[str] = None,
        enable_validation: bool = True,
        enable_reliability_tracking: bool = True,
        temperature: float = 0.1,  # Lower temperature for more consistent scoring
    ):
        self.provider = provider or OllamaProvider(config.OLLAMA_BASE_URL, config.OLLAMA_MODEL)
        self.model_name = model_name or getattr(self.provider, "model", config.OLLAMA_MODEL)
        self.enable_validation = enable_validation
        self.enable_reliability_tracking = enable_reliability_tracking
        self.temperature = temperature

        # JSON parsing sentinels for robust extraction
        self.json_start = "<<<JSON_START>>>"
        self.json_end = "<<<JSON_END>>>"

        sys_logger.log_system("info", f"ClinicalEvaluator initialized: model={self.model_name}, validation={enable_validation}, reliability={enable_reliability_tracking}")

    # ----- Public API -----
    def evaluate(self, inputs: EvaluationInputs) -> Dict[str, Any]:
        """Enhanced evaluation with structured validation and reliability tracking."""
        try:
            # Build rubric-based prompt with JSON constraints
            prompt = self._build_rubric_prompt(inputs)

            # Generate with research-appropriate parameters
            raw_response = self.provider.generate(
                prompt,
                temperature=self.temperature,  # Lower temperature for consistency
                top_p=0.9,
                timeout_s=150,  # More time for complex evaluation
            ).strip()

            # Extract and validate JSON with robust parsing
            evaluation_json, extraction_success = self._extract_json_robust(raw_response)

            if self.enable_validation and extraction_success:
                # Validate against Pydantic schema
                try:
                    validated_evaluation = ClinicalEvaluation(**evaluation_json)
                    evaluation_dict = validated_evaluation.dict()
                    validation_errors = []
                except ValidationError as ve:
                    sys_logger.log_system("warning", f"Validation failed, using repair: {ve}")
                    # Attempt repair with targeted prompt
                    evaluation_dict, validation_errors = self._repair_evaluation(raw_response, evaluation_json, ve)
            else:
                evaluation_dict = evaluation_json if extraction_success else self._fallback_eval_payload()
                validation_errors = [] if extraction_success else ["JSON extraction failed"]

            # Build response with reliability metrics
            response = {
                "success": True,
                "evaluation": evaluation_dict,
                "raw_response": raw_response,
                "extraction_success": extraction_success,
                "validation_errors": validation_errors
            }

            if self.enable_reliability_tracking:
                response["reliability_metrics"] = self._build_reliability_metrics()

            return response

        except Exception as e:
            sys_logger.log_system("error", f"Evaluation failed: {e}")
            return self._fallback(inputs)

    def deep_bias_analysis(
        self, dialogue_transcript: List[Dict[str, Any]], final_diagnosis: str
    ) -> Dict[str, Any]:
        """Enhanced bias analysis with structured validation and evidence linking."""
        try:
            prompt = self._build_evidence_based_bias_prompt(dialogue_transcript, final_diagnosis)
            raw_response = self.provider.generate(
                prompt, temperature=0.1, top_p=0.9, timeout_s=120  # Even lower temp for bias detection
            ).strip()

            # Extract and validate JSON
            bias_json, extraction_success = self._extract_json_robust(raw_response)

            if self.enable_validation and extraction_success:
                try:
                    validated_bias = BiasAnalysis(**bias_json)
                    bias_dict = validated_bias.dict()
                    validation_errors = []
                except ValidationError as ve:
                    sys_logger.log_system("warning", f"Bias validation failed: {ve}")
                    bias_dict = bias_json
                    validation_errors = [str(ve)]
            else:
                bias_dict = bias_json if extraction_success else {"error": "JSON extraction failed"}
                validation_errors = [] if extraction_success else ["JSON extraction failed"]

            return {
                "success": extraction_success,
                "bias_analysis": bias_dict,
                "raw_analysis": raw_response,
                "validation_errors": validation_errors
            }

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

    # ----- Robust JSON Processing -----
    def _extract_json_robust(self, response: str) -> Tuple[Dict[str, Any], bool]:
        """Extract JSON with multiple fallback strategies for maximum reliability."""

        # Strategy 1: Look for sentinel markers first
        start_idx = response.find(self.json_start)
        end_idx = response.rfind(self.json_end)

        if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
            json_content = response[start_idx + len(self.json_start):end_idx].strip()
            try:
                return json.loads(json_content), True
            except json.JSONDecodeError as e:
                sys_logger.log_system("warning", f"Sentinel JSON parsing failed: {e}")

        # Strategy 2: Find first complete JSON object
        brace_start = response.find("{")
        if brace_start != -1:
            brace_count = 0
            for i, char in enumerate(response[brace_start:], brace_start):
                if char == "{":
                    brace_count += 1
                elif char == "}":
                    brace_count -= 1
                    if brace_count == 0:
                        try:
                            json_content = response[brace_start:i+1]
                            return json.loads(json_content), True
                        except json.JSONDecodeError:
                            continue

        # Strategy 3: Extract with regex patterns
        json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
        matches = re.findall(json_pattern, response, re.DOTALL)

        for match in matches:
            try:
                return json.loads(match), True
            except json.JSONDecodeError:
                continue

        # Strategy 4: Last resort - try to parse the entire response
        try:
            return json.loads(response), True
        except json.JSONDecodeError:
            pass

        sys_logger.log_system("error", "All JSON extraction strategies failed")
        return {}, False

    def _repair_evaluation(self, raw_response: str, invalid_json: Dict[str, Any],
                          validation_error: ValidationError) -> Tuple[Dict[str, Any], List[str]]:
        """Attempt to repair invalid evaluation using targeted prompt."""
        repair_prompt = f"""The following JSON evaluation has validation errors. Please fix it to match the required schema:

ORIGINAL JSON:
{json.dumps(invalid_json, indent=2)}

VALIDATION ERRORS:
{str(validation_error)}

Return ONLY the corrected JSON between {self.json_start} and {self.json_end}:"""

        try:
            repair_response = self.provider.generate(
                repair_prompt, temperature=0.1, top_p=0.8, timeout_s=60
            ).strip()

            repaired_json, success = self._extract_json_robust(repair_response)
            if success:
                try:
                    validated = ClinicalEvaluation(**repaired_json)
                    return validated.dict(), []
                except ValidationError as ve:
                    return repaired_json, [f"Repair validation failed: {ve}"]

        except Exception as e:
            sys_logger.log_system("warning", f"Evaluation repair failed: {e}")

        # Final fallback
        return self._fallback_eval_payload(), ["Validation failed, using fallback"]

    def _build_reliability_metrics(self) -> Dict[str, Any]:
        """Build reliability metrics for research validation."""
        return {
            "model_temperature": self.temperature,
            "model_name": self.model_name,
            "evaluation_timestamp": datetime.now().isoformat(),
            "validation_enabled": self.enable_validation,
            "extraction_method": "multi_strategy_robust"
        }

    # ----- Prompt builders -----
    def _build_rubric_prompt(self, inp: EvaluationInputs) -> str:
        """Build comprehensive rubric-based evaluation prompt with evidence linking."""
        dialogue = self._fmt_dialogue(inp.dialogue_transcript)
        bias = self._fmt_biases(inp.detected_biases)
        reflection = self._fmt_reflection(inp.metacognitive_responses)
        ctx = inp.case_context or {}

        return f"""You are an expert medical education evaluator using a strict, rubric-based scoring system for research assessment.

CRITICAL INSTRUCTIONS:
- Always return ONLY valid JSON between {self.json_start} and {self.json_end}
- Use the FULL 0–100 range with strict standards
- Provide evidence linking to transcript turns and information blocks
- Be consistent and objective - this is for research data collection

CASE CONTEXT:
- Case Type: {ctx.get('case_type', 'Clinical simulation case')}
- Correct Diagnosis: {ctx.get('correct_diagnosis', 'Not specified')}
- Critical Features: {ctx.get('key_features', 'Not specified')}
- Available Information Blocks: {ctx.get('total_blocks', 'Not specified')}

STUDENT PERFORMANCE DATA:

FINAL DIAGNOSIS:
{inp.final_diagnosis}

COMPLETE DIALOGUE TRANSCRIPT:
{dialogue}

RULE-BASED BIAS DETECTION:
{bias}

METACOGNITIVE REFLECTION:
{reflection}

RUBRIC WITH WEIGHTS:

1. DIAGNOSTIC ACCURACY (30% weight):
   • 0-20: Incorrect & potentially unsafe diagnosis
   • 21-49: Incorrect but shows some clinical reasoning
   • 50-79: Partially correct differential with gaps
   • 80-95: Correct diagnosis with solid justification
   • 96-100: Exemplary diagnosis with comprehensive reasoning

   REQUIREMENTS:
   - Reference specific transcript turns and information blockIds in correct_elements/missed_elements
   - Consider accuracy relative to available information gathered

2. INFORMATION GATHERING (25% weight):
   • Systematic exploration across history/physical/labs/imaging
   • Discovery of critical findings and appropriate depth
   • Breadth vs. focused investigation balance

   REQUIREMENTS:
   - Reference discovered critical blockIds in analysis
   - Evaluate efficiency and comprehensiveness

3. COGNITIVE BIAS AWARENESS (25% weight):
   • Recognition of bias patterns in behavior or reflections
   • Evidence of self-correction or reconsideration
   • Quality of metacognitive responses (not just completion)

   REQUIREMENTS:
   - Assess reflection quality: generic answers = low scores
   - Link to detected bias patterns from rule-based system

4. CLINICAL REASONING (20% weight):
   • Hypothesis generation and revision process
   • Evidence synthesis and coherence
   • Logical flow from data to conclusions

   REQUIREMENTS:
   - Reference specific reasoning steps in transcript
   - Evaluate hypothesis evolution over time

SCORING STANDARDS:
- Use strict criteria: average performance should score 55–70
- Exceptional work: 85+ requires multiple exemplary elements
- Poor work: <40 for unsafe/illogical reasoning
- Each dimension requires 1-3 sentence analysis with evidence
- Constructive feedback must include 2-4 specific, actionable recommendations

OUTPUT REQUIREMENTS:
Return ONLY valid JSON complying with this exact schema:

{self.json_start}
{{
  "overall_score": 0-100,
  "diagnostic_accuracy": {{
    "score": 0-100,
    "analysis": "Evidence-based analysis with transcript/block references",
    "correct_elements": ["list of correct diagnostic elements"],
    "missed_elements": ["list of missed critical elements"]
  }},
  "information_gathering": {{
    "score": 0-100,
    "analysis": "Analysis referencing information blocks discovered",
    "strengths": ["specific strengths in information gathering"],
    "areas_for_improvement": ["specific areas needing improvement"]
  }},
  "cognitive_bias_awareness": {{
    "score": 0-100,
    "analysis": "Analysis of bias recognition and metacognitive quality",
    "detected_biases_impact": "Impact assessment of detected biases",
    "metacognitive_quality": "Quality assessment of reflection responses"
  }},
  "clinical_reasoning": {{
    "score": 0-100,
    "analysis": "Analysis of reasoning process with evidence",
    "hypothesis_generation": "Assessment of hypothesis development",
    "evidence_synthesis": "Assessment of evidence integration"
  }},
  "constructive_feedback": {{
    "positive_reinforcement": "Specific positive elements observed",
    "key_learning_points": ["2-4 key educational points"],
    "specific_recommendations": ["2-4 actionable improvement suggestions"],
    "bias_education": "Educational message about cognitive biases"
  }},
  "confidence_assessment": 0-100
}}
{self.json_end}"""

    def _build_evidence_based_bias_prompt(self, dialogue: List[Dict[str, Any]], final_dx: str) -> str:
        """Build evidence-based bias analysis prompt with transcript linking."""
        d = self._fmt_dialogue(dialogue)
        return f"""You are a cognitive psychology expert analyzing clinical reasoning patterns for research.

ANALYSIS REQUIREMENTS:
- Ground all findings in specific transcript evidence
- Reference transcript turn numbers and specific phrases
- Provide detailed explanations for each bias detection
- Use conservative confidence thresholds

DIALOGUE TRANSCRIPT (numbered for reference):
{d}

FINAL DIAGNOSIS: {final_dx}

BIAS DETECTION CRITERIA:

1. ANCHORING BIAS:
   - Early hypothesis formation followed by persistence
   - Insufficient revision despite contradictory evidence
   - Evidence: cite specific transcript turns showing fixation

2. CONFIRMATION BIAS:
   - Selective information seeking that supports hypothesis
   - Avoiding or dismissing contradictory evidence
   - Evidence: cite patterns in information requests

3. PREMATURE CLOSURE:
   - Rushing to diagnosis with insufficient information
   - Missing critical diagnostic steps or information
   - Evidence: cite gaps in information gathering

Return ONLY valid JSON between {self.json_start} and {self.json_end}:

{self.json_start}
{{
  "anchoring_bias": {{
    "detected": true/false,
    "confidence": 0-100,
    "evidence": "Specific transcript references and turns",
    "explanation": "Detailed explanation of observed pattern"
  }},
  "confirmation_bias": {{
    "detected": true/false,
    "confidence": 0-100,
    "evidence": "Specific examples from transcript",
    "explanation": "Detailed explanation of selective seeking pattern"
  }},
  "premature_closure": {{
    "detected": true/false,
    "confidence": 0-100,
    "evidence": "Evidence of rushed reasoning or missing steps",
    "explanation": "Detailed explanation of premature conclusion pattern"
  }},
  "overall_reasoning_quality": 0-100,
  "key_insights": ["Key insights about reasoning patterns"]
}}
{self.json_end}"""

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
        """Legacy method - use _build_rubric_prompt instead."""
        inputs = EvaluationInputs(
            dialogue_transcript=dialogue_transcript,
            detected_biases=detected_biases,
            metacognitive_responses=metacognitive_responses,
            final_diagnosis=final_diagnosis,
            case_context=case_context,
        )
        return self._build_rubric_prompt(inputs)

    def _create_bias_analysis_prompt(
        self, dialogue_transcript: List[Dict], final_diagnosis: str
    ) -> str:
        """Legacy method - use _build_evidence_based_bias_prompt instead."""
        return self._build_evidence_based_bias_prompt(dialogue_transcript, final_diagnosis)

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
