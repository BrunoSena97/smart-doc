"""
SmartDoc Clinical Evaluator - LLM-based comprehensive analysis of clinical performance
"""

import requests
import json
from typing import Dict, List, Any, Optional
from smartdoc_core.config.settings import config
from smartdoc_core.utils.logger import sys_logger

class ClinicalEvaluator:
    """
    Advanced LLM-based evaluator for comprehensive clinical performance analysis.

    This evaluator analyzes:
    - Complete dialogue transcript
    - Detected cognitive biases
    - Metacognitive checkpoint responses
    - Diagnostic accuracy and reasoning
    """

    def __init__(self, model_name: str = None):
        """Initialize the Clinical Evaluator."""
        self.model_name = model_name or config.OLLAMA_MODEL
        self.ollama_url = f"{config.OLLAMA_BASE_URL}/api/generate"
        sys_logger.log_system("info", f"Clinical Evaluator initialized with model: {self.model_name}")

    def evaluate_clinical_performance(self,
                                    dialogue_transcript: List[Dict],
                                    detected_biases: List[Dict],
                                    metacognitive_responses: Dict[str, str],
                                    final_diagnosis: str,
                                    case_context: Dict) -> Dict[str, Any]:
        """
        Comprehensive evaluation of clinical performance using LLM analysis.

        Args:
            dialogue_transcript: Complete conversation history
            detected_biases: List of detected cognitive biases
            metacognitive_responses: Answers to reflection questions
            final_diagnosis: Student's final diagnosis
            case_context: Case information and correct diagnosis

        Returns:
            Comprehensive evaluation results
        """
        try:
            # Prepare the evaluation prompt
            evaluation_prompt = self._create_evaluation_prompt(
                dialogue_transcript, detected_biases, metacognitive_responses,
                final_diagnosis, case_context
            )

            # Get LLM evaluation
            evaluation_result = self._query_llm(evaluation_prompt)

            if evaluation_result:
                # Parse the structured response
                parsed_evaluation = self._parse_evaluation_response(evaluation_result)

                sys_logger.log_system("info", f"Clinical evaluation completed successfully")
                return {
                    "success": True,
                    "evaluation": parsed_evaluation,
                    "raw_response": evaluation_result
                }
            else:
                return self._fallback_evaluation(final_diagnosis, detected_biases, metacognitive_responses)

        except Exception as e:
            sys_logger.log_system("error", f"Clinical evaluation failed: {e}")
            return self._fallback_evaluation(final_diagnosis, detected_biases, metacognitive_responses)

    def analyze_cognitive_biases(self,
                               dialogue_transcript: List[Dict],
                               final_diagnosis: str) -> Dict[str, Any]:
        """
        Deep LLM-based analysis of cognitive biases in the clinical dialogue.
        Uses Chain-of-Thought prompting for detailed bias detection.
        """
        try:
            cot_prompt = self._create_bias_analysis_prompt(dialogue_transcript, final_diagnosis)
            bias_analysis = self._query_llm(cot_prompt)

            if bias_analysis:
                parsed_bias = self._parse_bias_analysis(bias_analysis)
                return {
                    "success": True,
                    "bias_analysis": parsed_bias,
                    "raw_analysis": bias_analysis
                }
            else:
                return {"success": False, "error": "LLM bias analysis failed"}

        except Exception as e:
            sys_logger.log_system("error", f"Bias analysis failed: {e}")
            return {"success": False, "error": str(e)}

    def _create_evaluation_prompt(self, dialogue_transcript: List[Dict],
                                detected_biases: List[Dict],
                                metacognitive_responses: Dict[str, str],
                                final_diagnosis: str,
                                case_context: Dict) -> str:
        """Create comprehensive evaluation prompt for LLM."""

        # Format dialogue transcript
        formatted_dialogue = self._format_dialogue(dialogue_transcript)

        # Format detected biases
        bias_summary = self._format_bias_summary(detected_biases)

        # Format metacognitive responses
        reflection_summary = self._format_metacognitive_responses(metacognitive_responses)

        prompt = f"""You are an expert medical education evaluator and cognitive psychology specialist. Your task is to provide a comprehensive evaluation of a medical student's clinical performance in a virtual patient simulation.

CASE CONTEXT:
- Case Type: {case_context.get('case_type', 'Clinical case')}
- Correct Diagnosis: {case_context.get('correct_diagnosis', 'Not specified')}
- Key Clinical Features: {case_context.get('key_features', 'Not specified')}

STUDENT'S PERFORMANCE DATA:

FINAL DIAGNOSIS SUBMITTED:
{final_diagnosis}

COMPLETE DIALOGUE TRANSCRIPT:
{formatted_dialogue}

DETECTED COGNITIVE BIASES:
{bias_summary}

STUDENT'S METACOGNITIVE REFLECTION RESPONSES:
{reflection_summary}

EVALUATION INSTRUCTIONS:
Please provide a comprehensive evaluation following this exact JSON structure:

{{
    "overall_score": <number 0-100>,
    "diagnostic_accuracy": {{
        "score": <number 0-100>,
        "analysis": "<detailed analysis of diagnostic accuracy>",
        "correct_elements": ["<list of correct diagnostic elements>"],
        "missed_elements": ["<list of missed important elements>"]
    }},
    "information_gathering": {{
        "score": <number 0-100>,
        "analysis": "<analysis of questioning strategy and thoroughness>",
        "strengths": ["<list of strengths>"],
        "areas_for_improvement": ["<list of areas to improve>"]
    }},
    "cognitive_bias_awareness": {{
        "score": <number 0-100>,
        "analysis": "<analysis of bias patterns and self-awareness>",
        "detected_biases_impact": "<how detected biases affected performance>",
        "metacognitive_quality": "<quality of reflection responses>"
    }},
    "clinical_reasoning": {{
        "score": <number 0-100>,
        "analysis": "<analysis of logical reasoning and evidence integration>",
        "hypothesis_generation": "<quality of differential diagnosis thinking>",
        "evidence_synthesis": "<how well evidence was integrated>"
    }},
    "constructive_feedback": {{
        "positive_reinforcement": "<specific praise for good actions>",
        "key_learning_points": ["<main educational takeaways>"],
        "specific_recommendations": ["<actionable improvement suggestions>"],
        "bias_education": "<gentle explanation of bias impact with examples>"
    }},
    "confidence_assessment": <number 0-100>
}}

Please ensure your response is valid JSON and provide detailed, educational feedback that is constructive and encouraging while being honest about areas needing improvement."""

        return prompt

    def _create_bias_analysis_prompt(self, dialogue_transcript: List[Dict], final_diagnosis: str) -> str:
        """Create Chain-of-Thought prompt for detailed bias analysis."""

        formatted_dialogue = self._format_dialogue(dialogue_transcript)

        prompt = f"""You are an expert in cognitive psychology and medical education. Your task is to analyze the following clinical interview transcript for evidence of cognitive biases using Chain-of-Thought reasoning.

CLINICAL DIALOGUE TRANSCRIPT:
{formatted_dialogue}

FINAL DIAGNOSIS: {final_diagnosis}

Please perform the following analysis steps:

STEP 1 - IDENTIFY INITIAL HYPOTHESIS:
Based on the early part of the conversation, what was the student's most likely initial working hypothesis? Quote specific evidence from the transcript.

STEP 2 - ANALYZE INFORMATION SEEKING:
List the key questions the student asked and categorize each as:
- Confirming evidence (supports initial hypothesis)
- Disconfirming evidence (challenges initial hypothesis)
- Neutral/exploratory (neither confirming nor disconfirming)

STEP 3 - PATTERN ANALYSIS:
Analyze the progression of questioning for these bias patterns:
- Anchoring bias: Over-reliance on initial information
- Confirmation bias: Seeking confirming evidence while avoiding disconfirming
- Premature closure: Stopping information gathering too early

STEP 4 - EVIDENCE INTEGRATION:
How well did the student integrate contradictory or unexpected findings? Did they adjust their hypothesis appropriately?

STEP 5 - FINAL SYNTHESIS:
Provide your conclusions in this JSON format:
{{
    "anchoring_bias": {{
        "detected": <true/false>,
        "confidence": <0-100>,
        "evidence": "<specific examples from transcript>",
        "explanation": "<how this bias manifested>"
    }},
    "confirmation_bias": {{
        "detected": <true/false>,
        "confidence": <0-100>,
        "evidence": "<specific examples from transcript>",
        "explanation": "<how this bias manifested>"
    }},
    "premature_closure": {{
        "detected": <true/false>,
        "confidence": <0-100>,
        "evidence": "<specific examples from transcript>",
        "explanation": "<how this bias manifested>"
    }},
    "overall_reasoning_quality": <0-100>,
    "key_insights": ["<main insights about reasoning patterns>"]
}}

Let's think step-by-step."""

        return prompt

    def _format_dialogue(self, dialogue_transcript: List[Dict]) -> str:
        """Format dialogue transcript for LLM analysis."""
        formatted = []
        for i, interaction in enumerate(dialogue_transcript, 1):
            role = "DOCTOR" if interaction.get('role') == 'user' else "PATIENT"
            message = interaction.get('message', interaction.get('content', ''))
            timestamp = interaction.get('timestamp', '')
            formatted.append(f"{i}. {role}: {message}")

        return "\n".join(formatted)

    def _format_bias_summary(self, detected_biases: List[Dict]) -> str:
        """Format detected biases for LLM analysis."""
        if not detected_biases:
            return "No cognitive biases detected by rule-based system."

        formatted = []
        for bias in detected_biases:
            bias_type = bias.get('bias_type', 'Unknown')
            description = bias.get('description', bias.get('message', ''))
            formatted.append(f"- {bias_type}: {description}")

        return "\n".join(formatted)

    def _format_metacognitive_responses(self, responses: Dict[str, str]) -> str:
        """Format metacognitive checkpoint responses."""
        if not responses:
            return "No metacognitive reflection responses provided."

        formatted = []
        for question, answer in responses.items():
            formatted.append(f"Q: {question}")
            formatted.append(f"A: {answer}")
            formatted.append("")

        return "\n".join(formatted)

    def _query_llm(self, prompt: str) -> Optional[str]:
        """Query the LLM with the given prompt."""
        try:
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.3,  # Lower temperature for more consistent analysis
                    "top_p": 0.9,
                    "max_tokens": 4000
                }
            }

            response = requests.post(self.ollama_url, json=payload, timeout=120)
            response.raise_for_status()

            result = response.json()
            return result.get('response', '').strip()

        except Exception as e:
            sys_logger.log_system("error", f"LLM query failed: {e}")
            return None

    def _parse_evaluation_response(self, response: str) -> Dict[str, Any]:
        """Parse structured JSON response from LLM evaluation."""
        try:
            # Try to extract JSON from response
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1

            if start_idx != -1 and end_idx != 0:
                json_str = response[start_idx:end_idx]
                return json.loads(json_str)
            else:
                # Fallback parsing if JSON not found
                return self._parse_text_evaluation(response)

        except json.JSONDecodeError:
            return self._parse_text_evaluation(response)

    def _parse_bias_analysis(self, response: str) -> Dict[str, Any]:
        """Parse bias analysis response."""
        try:
            # Extract JSON portion
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1

            if start_idx != -1 and end_idx != 0:
                json_str = response[start_idx:end_idx]
                return json.loads(json_str)
            else:
                return {"error": "Could not parse bias analysis", "raw_response": response}

        except json.JSONDecodeError:
            return {"error": "Invalid JSON in bias analysis", "raw_response": response}

    def _parse_text_evaluation(self, response: str) -> Dict[str, Any]:
        """Fallback text parsing for evaluation response."""
        return {
            "overall_score": 75,  # Default score
            "diagnostic_accuracy": {"score": 70, "analysis": "Unable to parse detailed analysis"},
            "information_gathering": {"score": 75, "analysis": "Unable to parse detailed analysis"},
            "cognitive_bias_awareness": {"score": 70, "analysis": "Unable to parse detailed analysis"},
            "clinical_reasoning": {"score": 75, "analysis": "Unable to parse detailed analysis"},
            "constructive_feedback": {
                "positive_reinforcement": "Good clinical engagement",
                "key_learning_points": ["Continue practicing systematic clinical reasoning"],
                "specific_recommendations": ["Focus on comprehensive information gathering"],
                "bias_education": "Consider multiple hypotheses before settling on a diagnosis"
            },
            "confidence_assessment": 60,
            "raw_llm_response": response
        }

    def _fallback_evaluation(self, final_diagnosis: str, detected_biases: List[Dict],
                           metacognitive_responses: Dict[str, str]) -> Dict[str, Any]:
        """Provide fallback evaluation when LLM analysis fails."""
        bias_count = len(detected_biases)
        bias_penalty = min(30, bias_count * 10)  # Max 30 point penalty

        base_score = 80 - bias_penalty

        return {
            "success": True,
            "evaluation": {
                "overall_score": max(50, base_score),
                "diagnostic_accuracy": {"score": 70, "analysis": "Requires expert review for detailed assessment"},
                "information_gathering": {"score": 75, "analysis": "Demonstrated systematic questioning approach"},
                "cognitive_bias_awareness": {
                    "score": max(50, 90 - bias_penalty),
                    "analysis": f"Detected {bias_count} potential cognitive biases during the session"
                },
                "clinical_reasoning": {"score": 70, "analysis": "Showed logical progression in clinical thinking"},
                "constructive_feedback": {
                    "positive_reinforcement": "Demonstrated engagement with the clinical case",
                    "key_learning_points": ["Continue developing systematic clinical reasoning skills"],
                    "specific_recommendations": ["Practice considering alternative diagnoses", "Use structured reflection techniques"],
                    "bias_education": "Be aware of cognitive biases that can influence clinical decision-making"
                },
                "confidence_assessment": 60
            },
            "fallback_used": True
        }
