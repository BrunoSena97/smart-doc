#!/usr/bin/env python3
"""
Discovery Processing Service for SmartDoc
Deterministic discovery classifier with optional LLM fallback for enrichment.
"""

from __future__ import annotations
import json
from typing import Dict, Any, Optional
from smartdoc_core.utils.logger import sys_logger
from smartdoc_core.config.settings import config

try:
    # keep optional import so we can still use the old LLM path in "hybrid" or "llm"
    from smartdoc_core.llm.providers.ollama import OllamaProvider
    HAVE_LLM = True
except Exception:
    HAVE_LLM = False


class DiscoveryClassifier:
    """
    Deterministic discovery classifier.
    - Reads label/category from the case (block metadata or discoverySchema.blockLabels)
    - Returns the same shape your engine already expects.
    Optional "hybrid" mode will fall back to LLM if metadata is missing.
    """

    def __init__(self, *, provider=None, mode: Optional[str] = None, schema: Optional[Dict] = None):
        self.mode = (mode or getattr(config, "DISCOVERY_MODE", "deterministic")).lower()
        self.provider = provider or (OllamaProvider(config.OLLAMA_BASE_URL, config.OLLAMA_MODEL) if HAVE_LLM else None)
        self.schema = schema or {}
        sys_logger.log_system("info", f"DiscoveryClassifier mode={self.mode}")

    def process_discovery(
        self,
        *,
        block_id: str,
        block_type: str,
        clinical_content: str,
        intent_id: str,
        doctor_question: str = "",
        patient_response: str = "",
        case_labels_map: Optional[Dict[str, Dict[str, str]]] = None,
    ) -> Dict[str, Any]:
        # 1) deterministic: try case-provided metadata
        label_info = None
        if case_labels_map and block_id in case_labels_map:
            label_info = case_labels_map[block_id]
        elif "blockLabels" in self.schema and block_id in self.schema["blockLabels"]:
            label_info = self.schema["blockLabels"][block_id]

        if label_info and "label" in label_info:
            return {
                "label": label_info["label"],
                "category": label_info.get("category", self._default_category(block_type)),
                "summary": clinical_content if block_type in ("Labs","Imaging","PhysicalExam") else self._summary_from_content(clinical_content),
                "confidence": 0.95,
                "reasoning": "Deterministic mapping from case metadata",
                "original_content": clinical_content,
                "intent_context": intent_id,
            }

        # 2) hybrid/llm fallback (optional)
        if self.mode in ("hybrid", "llm") and self.provider:
            try:
                prompt = self._build_min_prompt(block_type, intent_id, doctor_question, patient_response, clinical_content)
                text = self.provider.generate(prompt, temperature=0.1, top_p=0.9, timeout_s=90).strip()
                parsed = self._parse_json(text, clinical_content, block_type, intent_id)
                parsed["reasoning"] = "LLM classification (fallback)"
                return parsed
            except Exception as e:
                sys_logger.log_system("warning", f"LLM discovery fallback failed: {e}")

        # 3) final fallback (simple rule)
        return {
            "label": self._rule_label(block_type, clinical_content, intent_id),
            "category": self._default_category(block_type),
            "summary": clinical_content,
            "confidence": 0.6,
            "reasoning": "Rule-based fallback",
            "original_content": clinical_content,
            "intent_context": intent_id,
        }

    # ------- helpers -------
    def _default_category(self, block_type: str) -> str:
        return {
            "History": "presenting_symptoms",
            "PhysicalExam": "physical_examination",
            "Labs": "diagnostic_results",
            "Imaging": "diagnostic_results",
            "Demographics": "patient_profile",
            "Medications": "current_medications",
        }.get(block_type, "clinical_assessment")

    def _summary_from_content(self, content: str) -> str:
        return content if len(content) < 300 else (content[:297] + "...")

    def _rule_label(self, block_type: str, content: str, intent_id: str) -> str:
        # very small heuristic as last resort
        if block_type == "PhysicalExam": return "General Appearance" if "appear" in content.lower() else "Vital Signs"
        if block_type == "Labs": return "Lab Results"
        if block_type == "Imaging": return "Chest X-ray" if "chest" in content.lower() else "Other Imaging"
        if "shortness" in content.lower() or "dyspnea" in content.lower(): return "Shortness of Breath"
        return "Clinical Concerns"

    def _build_min_prompt(self, block_type, intent_id, dq, pr, content) -> str:
        return f"""You must return ONLY JSON:
{{
  "label": "one concise clinical label",
  "category": "one category string",
  "summary": "1-2 sentence clinical summary",
  "confidence": 0-1
}}
Context:
- Block type: {block_type}
- Intent: {intent_id}
- Doctor: {dq}
- Patient: {pr}
- Content: {content}
"""

    def _parse_json(self, text: str, content: str, block_type: str, intent_id: str) -> Dict[str, Any]:
        i, j = text.find("{"), text.rfind("}") + 1
        if i >= 0 and j > 0:
            try:
                data = json.loads(text[i:j])
                return {
                    "label": data.get("label","Clinical Concerns"),
                    "category": data.get("category", self._default_category(block_type)),
                    "summary": data.get("summary", content),
                    "confidence": float(data.get("confidence", 0.5)),
                    "original_content": content,
                    "intent_context": intent_id,
                }
            except (json.JSONDecodeError, ValueError):
                pass
        return {
            "label": "Clinical Concerns",
            "category": self._default_category(block_type),
            "summary": content,
            "confidence": 0.6,
            "original_content": content,
            "intent_context": intent_id,
        }


# Legacy compatibility: keep LLMDiscoveryProcessor as an alias
class LLMDiscoveryProcessor(DiscoveryClassifier):
    """
    Legacy compatibility wrapper for the old LLM-based processor.
    Now delegates to DiscoveryClassifier with LLM mode enabled.
    """

    def __init__(self, provider=None, prompt_builder=None, discovery_schema: Optional[Dict[str, Dict[str, str]]] = None):
        # Convert old interface to new one
        super().__init__(
            provider=provider,
            mode="llm",  # Force LLM mode for legacy compatibility
            schema=discovery_schema or {}
        )
        sys_logger.log_system("info", "LLMDiscoveryProcessor (legacy mode) initialized")

    def process_discovery(
        self,
        intent_id: str,
        doctor_question: str,
        patient_response: str,
        clinical_content: str,
        *,
        agent: Optional[str] = None
    ) -> Dict[str, Any]:
        """Legacy method signature support."""
        return super().process_discovery(
            block_id=f"legacy_block_{intent_id}",
            block_type="History",  # Default assumption for legacy calls
            clinical_content=clinical_content,
            intent_id=intent_id,
            doctor_question=doctor_question,
            patient_response=patient_response,
        )
