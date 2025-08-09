"""
Simulation Engine for SmartDoc Virtual Patient System

This module orchestrates the core simulation engine that integrates AI intent classification
with progressive information disclosure, enabling natural conversation-driven clinical interviews.
"""

import json
import uuid
import requests
from typing import Dict, List, Set, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime

from smartdoc.utils.logger import sys_logger
from smartdoc.config.settings import config
from smartdoc.simulation.state_manager import ProgressiveDisclosureManager, InformationBlock
from smartdoc.ai.intent_classifier import LLMIntentClassifier
from smartdoc.ai.discovery_processor import LLMDiscoveryProcessor
from smartdoc.simulation.bias_analyzer import BiasEvaluator


@dataclass
class DiscoveryEvent:
    """Represents a discovery event triggered by an intent."""
    event_id: str
    session_id: str
    intent_id: str
    user_query: str
    discovered_blocks: List[str]
    timestamp: datetime
    trigger_type: str  # 'direct', 'indirect', 'follow_up'
    confidence: float


class IntentDrivenDisclosureManager:
    """
    Manages intent-driven progressive disclosure where natural conversation
    triggers information discovery rather than manual clicking.
    """

    def __init__(self, case_file_path: str = None):
        """Initialize the Intent-Driven Disclosure Manager."""
        self.case_file_path = case_file_path or config.CASE_FILE
        self.case_data = None
        self.progressive_manager = ProgressiveDisclosureManager(case_file_path)
        self.intent_classifier = LLMIntentClassifier()
        self.discovery_processor = LLMDiscoveryProcessor()

        # Enhanced intent-to-block mappings
        self.intent_block_mappings = {}
        self.load_enhanced_mappings()

        # Discovery tracking
        self.discovery_events: Dict[str, List[DiscoveryEvent]] = {}

        # Initialize bias analyzer with case data
        self.bias_analyzer = None
        if self.progressive_manager.case_data:
            try:
                self.bias_analyzer = BiasEvaluator(self.progressive_manager.case_data)
                sys_logger.log_system("info", "Bias analyzer initialized successfully")
            except Exception as e:
                sys_logger.log_system("warning", f"Bias analyzer initialization failed: {e}")

        sys_logger.log_system("info", "Intent-Driven Disclosure Manager initialized")

    def load_enhanced_mappings(self):
        """Load intent-to-block mappings directly from JSON case file."""
        if not self.progressive_manager.case_data:
            self.intent_block_mappings = {}
            sys_logger.log_system("warning", "No case data available - using empty mappings")
            return

        case_data = self.progressive_manager.case_data

        if 'intentBlockMappings' in case_data:
            self.intent_block_mappings = case_data['intentBlockMappings']
            sys_logger.log_system("info", f"Loaded intent mappings for {len(self.intent_block_mappings)} intents from JSON")
        else:
            # Empty mappings if not specified in case file
            self.intent_block_mappings = {}
            sys_logger.log_system("warning", "No intentBlockMappings found in case file - using empty mappings")

    def start_intent_driven_session(self, session_id: str = None) -> str:
        """Start a new intent-driven disclosure session."""
        if session_id is None:
            session_id = f"intent_session_{uuid.uuid4().hex[:8]}"

        # Start progressive disclosure session
        pd_session = self.progressive_manager.start_new_session(session_id)

        # Initialize discovery tracking
        self.discovery_events[session_id] = []

        sys_logger.log_system("info", f"Started intent-driven session: {session_id}")
        return session_id

    def process_doctor_query(self, session_id: str, user_query: str, context: str = 'anamnesis') -> Dict[str, Any]:
        """
        Process a doctor's query and trigger appropriate information discovery with context filtering.

        Args:
            session_id: The session ID
            user_query: The doctor's question or statement
            context: The clinical context ('anamnesis', 'exam', 'labs')

        Returns:
            Dictionary containing response, discovered information, and discovery notifications
        """
        if session_id not in self.discovery_events:
            # Auto-start session if not exists
            self.start_intent_driven_session(session_id)

        try:
            # 1. Classify the intent with context filtering
            intent_result = self.intent_classifier.classify_intent(user_query, context)
            intent_id = intent_result['intent_id']
            confidence = intent_result['confidence']

            sys_logger.log_system("debug", f"Query '{user_query}' in context '{context}' classified as '{intent_id}' (confidence: {confidence:.2f})")

            # 2. Discover relevant information blocks (filtered by context)
            discovery_result = self._discover_blocks_for_intent_with_context(session_id, intent_id, user_query, confidence, context)

            # 3. Generate contextual response
            response_result = self._generate_discovery_response_with_context(session_id, intent_result, discovery_result, context)

            # 4. Real-time bias detection
            bias_warning = None
            if self.bias_analyzer:
                try:
                    # Get session interactions for bias analysis
                    session_interactions = self._get_session_interactions(session_id)

                    bias_result = self.bias_analyzer.check_real_time_bias(
                        session_interactions=session_interactions,
                        current_intent=intent_id,
                        user_input=user_query,
                        vsp_response=response_result['text']
                    )

                    if bias_result.get('detected'):
                        bias_warning = {
                            'detected': True,
                            'bias_type': bias_result.get('bias_type'),
                            'message': bias_result.get('message'),
                            'confidence': bias_result.get('confidence', 0.5)
                        }
                        sys_logger.log_system("warning", f"Bias detected: {bias_result.get('bias_type')} - {bias_result.get('message')}")

                        # Log bias warning to session tracker
                        from smartdoc.simulation.session_tracker import get_current_session
                        session_logger = get_current_session()
                        session_logger.log_bias_warning(bias_warning)

                except Exception as bias_error:
                    sys_logger.log_system("warning", f"Bias detection failed: {bias_error}")

            # 5. Log the discovery event
            if discovery_result['discovered_blocks']:
                event = DiscoveryEvent(
                    event_id=f"discovery_{uuid.uuid4().hex[:8]}",
                    session_id=session_id,
                    intent_id=intent_id,
                    user_query=user_query,
                    discovered_blocks=discovery_result['discovered_blocks'],
                    timestamp=datetime.now(),
                    trigger_type=discovery_result['trigger_type'],
                    confidence=confidence
                )
                self.discovery_events[session_id].append(event)

            result = {
                'success': True,
                'intent_classification': intent_result,
                'discovery_result': discovery_result,
                'response': response_result,
                'session_stats': self._get_session_discovery_stats(session_id)
            }

            # Add bias warning if detected
            if bias_warning:
                result['bias_warning'] = bias_warning

            return result

        except Exception as e:
            sys_logger.log_system("error", f"Error processing query '{user_query}': {e}")
            return {
                'success': False,
                'error': str(e),
                'fallback_response': "I understand you're asking about the patient. Let me think about what information I can provide..."
            }

    def _discover_blocks_for_intent(self, session_id: str, intent_id: str, user_query: str, confidence: float) -> Dict[str, Any]:
        """Discover information blocks based on the classified intent."""
        session = self.progressive_manager.get_session(session_id)
        if not session:
            return {'discovered_blocks': [], 'trigger_type': 'none', 'message': 'Session not found'}

        discovered_blocks = []
        trigger_type = 'none'

        # Direct intent mapping - rely on LLM classification
        if intent_id in self.intent_block_mappings:
            mapped_blocks = self.intent_block_mappings[intent_id]
            for block_id in mapped_blocks:
                if block_id in session.blocks and not session.blocks[block_id].is_revealed:
                    # Reveal the block
                    reveal_result = self.progressive_manager.reveal_block(session_id, block_id, user_query)
                    if reveal_result.get('success'):
                        discovered_blocks.append(block_id)
                        trigger_type = 'direct'

        return {
            'discovered_blocks': discovered_blocks,
            'trigger_type': trigger_type,
            'intent_id': intent_id,
            'confidence': confidence
        }

    def _generate_discovery_response(self, session_id: str, intent_result: Dict, discovery_result: Dict) -> Dict[str, Any]:
        """Generate a response using LLM for natural conversation."""
        discovered_blocks = discovery_result['discovered_blocks']
        session = self.progressive_manager.get_session(session_id)

        discoveries = []
        clinical_data = []

        # Collect discovered information and process with LLM Discovery Processor
        for block_id in discovered_blocks:
            if block_id in session.blocks:
                block = session.blocks[block_id]

                # Use LLM Discovery Processor to categorize and label the discovery
                discovery_info = self.discovery_processor.process_discovery(
                    intent_id=intent_result['intent_id'],
                    doctor_question=intent_result.get('original_input', ''),
                    patient_response="",  # Will be generated by LLM patient response
                    clinical_content=block.content
                )

                discoveries.append({
                    'block_id': block_id,
                    'block_type': block.block_type,
                    'content': block.content,
                    'is_critical': block.is_critical,
                    'discovery_notification': f"📋 **New Information Discovered**: {discovery_info['label']}",
                    # New structured discovery data using fixed labels
                    'label': discovery_info['label'],
                    'category': discovery_info['category'],
                    'summary': discovery_info['summary'],
                    'confidence': discovery_info['confidence']
                })

                # Collect clinical data for LLM generation
                clinical_data.append({
                    'type': block.block_type,
                    'content': block.content,
                    'label': discovery_info['label'],
                    'summary': discovery_info['summary']
                })

        # Generate natural patient response using LLM
        if discoveries:
            response_text = self._generate_llm_patient_response(
                intent_result['intent_id'],
                intent_result.get('original_input', ''),
                clinical_data
            )
        else:
            # No new discoveries - use contextual fallback
            response_text = self._generate_patient_fallback_response(intent_result, session)

        return {
            'text': response_text,
            'discoveries': discoveries,
            'discovery_count': len(discoveries),
            'has_discoveries': len(discoveries) > 0
        }

    def _generate_llm_patient_response(self, intent_id: str, doctor_question: str, clinical_data: List[Dict]) -> str:
        """Generate natural patient response using LLM based on discovered clinical data."""

        # Create context about the clinical scenario
        scenario_context = """You are the English-speaking son of an elderly Spanish-speaking woman in the emergency department.
You are translating for your mother who only speaks Spanish. You are concerned but trying to be helpful.
You speak naturally to the doctor, providing information based on what you know about your mother's condition."""

        # Format the clinical data for the LLM using the structured labels
        data_points = []
        for item in clinical_data:
            label = item.get('label', item['type'])
            summary = item.get('summary', item['content'])
            data_points.append(f"- {label}: {summary}")

        clinical_info = "\n".join(data_points) if data_points else "No specific clinical data"

        # Create the prompt
        prompt = f"""{scenario_context}

The doctor just asked: "{doctor_question}"

Based ONLY on the following clinical information that has just been revealed, formulate a single, natural, conversational response as the patient's son speaking. Do not add any medical information not present in the data. Speak as a concerned family member would, not as a medical professional.

Clinical Data:
{clinical_info}

Your response as the patient's son (keep it natural and conversational):"""

        try:
            # Call the LLM to generate natural response
            response = self._call_llm_for_response(prompt)
            return response.strip('"').strip()
        except Exception as e:
            sys_logger.log_system("warning", f"LLM response generation failed: {e}")
            # Fallback to a generic response
            return "Let me tell you what I know about that."

    def _call_llm_for_response(self, prompt: str) -> str:
        """Call the LLM API for response generation."""
        payload = {
            "model": self.intent_classifier.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,  # Higher temperature for more natural responses
                "top_p": 0.9,
                "max_tokens": 150
            }
        }

        headers = {"Content-Type": "application/json"}

        response = requests.post(
            f"{self.intent_classifier.ollama_url}/api/generate",
            json=payload,
            headers=headers,
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            return result.get("response", "I'm not sure how to answer that.")
        else:
            raise Exception(f"LLM API error: {response.status_code}")

    def _create_natural_patient_response(self, response_parts: list, intent_result: Dict, discovery_result: Dict) -> str:
        """Create a natural patient response from discovered information."""

        # If we have discovered information, use it directly
        if response_parts:
            response = " ".join(response_parts)

            # Add natural transitions for multiple pieces of information
            if len(response_parts) > 1:
                return response.replace(". ", ". Also, ")

            return response

        # If no new information was discovered, we shouldn't be calling this method
        # The caller should use _generate_patient_fallback_response instead
        return "I'm not sure I have new information about that."

    def _generate_patient_fallback_response(self, intent_result: Dict, session) -> str:
        """Generate a fallback response when no new information is discovered."""
        intent_id = intent_result['intent_id']
        confidence = intent_result.get('confidence', 0)

        # Always provide contextually appropriate responses based on the specific question type
        # Even if we don't have new information blocks to reveal
        intent_specific_responses = {
            # Chief complaint and history
            'hpi_chief_complaint': "The main reason we're here is her breathing problems and how she's been feeling weak lately.",
            'hpi_onset_duration_primary': "It all started about two months ago and has been getting slowly worse since then.",
            'hpi_shortness_of_breath': "Her breathing has been getting worse over the past couple of months. It's especially bad when she tries to walk around.",
            'hpi_appetite': "She hasn't been eating as well lately. I've noticed she doesn't finish her meals like she used to.",
            'hpi_eating': "Her appetite has definitely decreased. She's been eating smaller portions and doesn't seem interested in food.",
            'hpi_weight_loss': "I've noticed her clothes are getting loose on her. She's definitely lost some weight recently.",
            'hpi_cough': "She has this dry cough that won't go away. It's worse at night and keeps her up.",
            'hpi_fever': "No, she hasn't had any fever. Her temperature has been normal.",
            'hpi_chest_pain': "No, she says she doesn't have any chest pain.",

            # Physical exam
            'exam_cardiovascular': "Would you like to examine her heart? She's sitting here if you need to listen.",
            'exam_respiratory': "You can examine her lungs if you need to. Her breathing has been the main problem.",
            'exam_vital_signs': "The nurses already took her vital signs when we arrived.",
            'exam_general_appearance': "As you can see, she looks tired and is breathing a bit fast.",

            # Medications
            'meds_current_known': "I think I told you all the medications I know about. There might be others her regular doctor prescribed.",
            'meds_ra_specific_initial_query': "I'm sorry, I don't know much about her arthritis treatments. Her rheumatologist handles that.",
            'meds_full_reconciliation_query': "Let me check if they found her records from the other hospital... Yes! They found her previous records with her complete medication list.",
            'meds_other_meds_initial_query': "I'm not sure about other medications. She sees different doctors for her various conditions.",

            # Imaging and tests
            'imaging_chest': "I think they did a chest X-ray when we got here. Did you see the results?",
            'imaging_general': "They've done some imaging tests. I think there was a chest X-ray, and maybe they mentioned other scans?",
            'labs_general': "They drew some blood when we arrived. I don't know the results yet.",

            # Profile and background
            'profile_age': "She's elderly, in her 70s. I help her because she only speaks Spanish.",
            'profile_language': "My mother only speaks Spanish, so I'm translating for her.",
            'pmh_general': "She has diabetes, high blood pressure, and arthritis. She's also quite overweight.",

            # General responses
            'clarification': "I'm not sure I understand what you're asking. Could you ask it differently?"
        }

        # First check if we have a specific contextual response for this intent
        if intent_id in intent_specific_responses:
            return intent_specific_responses[intent_id]

        # Check if information was already revealed for this intent and give acknowledging responses
        if intent_id in self.intent_block_mappings:
            mapped_blocks = self.intent_block_mappings[intent_id]
            already_revealed = [
                block_id for block_id in mapped_blocks
                if block_id in session.blocks and session.blocks[block_id].is_revealed
            ]

            if already_revealed:
                # Provide brief acknowledgment but still try to be helpful
                if intent_id == 'hpi_weight_loss':
                    return "I already mentioned her weight loss, but yes, she's definitely been losing weight over the past few weeks."
                elif intent_id == 'hpi_shortness_of_breath':
                    return "I talked about her breathing before - it's been getting worse over the past couple of months, especially with walking."
                elif intent_id.startswith('imaging_'):
                    return "I believe they've done some imaging studies. Have you had a chance to review the results?"
                elif intent_id.startswith('meds_'):
                    return "I mentioned her medications earlier. Is there something specific about her medications you'd like to know?"
                else:
                    return "I think we discussed that already, but let me know if you need me to clarify anything specific."

        # If confidence is low, acknowledge uncertainty
        if confidence < 0.5:
            return "I'm not sure I understood your question completely. Could you be more specific about what you'd like to know?"

        # Default response
        return "I'm not sure I have more information about that right now. Is there something else you'd like to know?"

    def _generate_fallback_response(self, intent_result: Dict, session) -> str:
        """Generate a fallback response when no new information is discovered."""
        intent_id = intent_result['intent_id']

        # Check if information was already revealed
        if intent_id in self.intent_block_mappings:
            mapped_blocks = self.intent_block_mappings[intent_id]
            already_revealed = [
                block_id for block_id in mapped_blocks
                if block_id in session.blocks and session.blocks[block_id].is_revealed
            ]

            if already_revealed:
                return "I've already provided that information earlier in our conversation. Is there anything specific you'd like me to clarify or expand on?"

        # Generic contextual responses based on intent
        fallback_responses = {
            'hpi_chief_complaint': "I understand you're asking about the patient's main concern. Let me review what we know so far...",
            'exam_cardiovascular': "You'd like to examine the cardiovascular system. Let me provide the relevant findings...",
            'exam_respiratory': "For the respiratory examination, here are the findings...",
            'meds_current_known': "Regarding current medications, let me tell you what I know...",
            'clarification': "I'm not sure I understood your question completely. Could you be more specific about what you'd like to know?"
        }

        return fallback_responses.get(intent_id,
            "I understand your question. Let me think about what information might be most relevant...")

    def _get_session_discovery_stats(self, session_id: str) -> Dict[str, Any]:
        """Get discovery statistics for the session."""
        session = self.progressive_manager.get_session(session_id)
        events = self.discovery_events.get(session_id, [])

        if not session:
            return {}

        total_blocks = len(session.blocks)
        revealed_blocks = len(session.revealed_blocks)
        total_discoveries = len(events)

        discovery_types = {}
        for event in events:
            discovery_types[event.trigger_type] = discovery_types.get(event.trigger_type, 0) + 1

        return {
            'total_blocks': total_blocks,
            'revealed_blocks': revealed_blocks,
            'discovery_percentage': (revealed_blocks / total_blocks * 100) if total_blocks > 0 else 0,
            'total_discovery_events': total_discoveries,
            'discovery_types': discovery_types,
            'session_duration_minutes': (datetime.now() - session.start_time).total_seconds() / 60
        }

    def get_session_discoveries(self, session_id: str) -> Dict[str, Any]:
        """Get all discoveries for a session."""
        events = self.discovery_events.get(session_id, [])
        session = self.progressive_manager.get_session(session_id)

        if not session:
            return {'success': False, 'error': 'Session not found'}

        discoveries_summary = []
        for event in events:
            discoveries_summary.append({
                'event_id': event.event_id,
                'intent_id': event.intent_id,
                'user_query': event.user_query,
                'discovered_blocks': event.discovered_blocks,
                'timestamp': event.timestamp.isoformat(),
                'trigger_type': event.trigger_type,
                'confidence': event.confidence
            })

        return {
            'success': True,
            'session_id': session_id,
            'discoveries': discoveries_summary,
            'stats': self._get_session_discovery_stats(session_id)
        }

    def get_available_information_summary(self, session_id: str) -> Dict[str, Any]:
        """Get a summary of available vs. discovered information."""
        session = self.progressive_manager.get_session(session_id)
        if not session:
            return {'success': False, 'error': 'Session not found'}

        categories = {}
        for block_id, block in session.blocks.items():
            if block.block_type not in categories:
                categories[block.block_type] = {
                    'total': 0,
                    'revealed': 0,
                    'critical_total': 0,
                    'critical_revealed': 0
                }

            categories[block.block_type]['total'] += 1
            if block.is_critical:
                categories[block.block_type]['critical_total'] += 1

            if block.is_revealed:
                categories[block.block_type]['revealed'] += 1
                if block.is_critical:
                    categories[block.block_type]['critical_revealed'] += 1

        return {
            'success': True,
            'categories': categories,
            'total_blocks': len(session.blocks),
            'total_revealed': len(session.revealed_blocks)
        }

    def _get_session_interactions(self, session_id: str) -> List[Dict[str, Any]]:
        """Get session interactions formatted for bias analysis."""
        interactions = []

        # Convert discovery events to interaction format for bias analysis
        events = self.discovery_events.get(session_id, [])

        for event in events:
            interaction = {
                'intent_id': event.intent_id,
                'user_query': event.user_query,
                'timestamp': event.timestamp.isoformat(),
                'discovered_blocks': event.discovered_blocks,
                'confidence': event.confidence,
                'trigger_type': event.trigger_type
            }
            interactions.append(interaction)

        return interactions

    def _discover_blocks_for_intent_with_context(self, session_id: str, intent_id: str, user_query: str, confidence: float, context: str) -> Dict[str, Any]:
        """Discover blocks for intent with context filtering."""
        # Filter intents based on context
        if not self._is_intent_valid_for_context(intent_id, context):
            return {
                'discovered_blocks': [],
                'new_discoveries': [],
                'context_filtered': True,
                'original_intent': intent_id
            }

        # Use existing discovery logic but with context awareness
        return self._discover_blocks_for_intent(session_id, intent_id, user_query, confidence)

    def _is_intent_valid_for_context(self, intent_id: str, context: str) -> bool:
        """Check if an intent is valid for the given context."""
        # Define context-specific intent mappings
        context_intents = {
            'anamnesis': [
                # History and medication related intents
                'hpi_chief_complaint', 'hpi_shortness_of_breath', 'hpi_cough', 'hpi_weight_loss',
                'hpi_onset_duration_primary', 'hpi_associated_symptoms_general', 'hpi_pertinent_negatives',
                'hpi_chest_pain', 'hpi_fever', 'hpi_recent_medical_care', 'pmh_general',
                'meds_current_known', 'meds_uncertainty', 'meds_ra_specific_initial_query',
                'meds_full_reconciliation_query', 'meds_other_meds_initial_query',
                'profile_age', 'profile_language', 'profile_social_context_historian', 'profile_medical_records'
            ],
            'exam': [
                # Physical examination related intents
                'exam_vital_signs', 'exam_general_appearance', 'exam_respiratory', 'exam_cardiovascular'
            ],
            'labs': [
                # Laboratory and imaging related intents
                'labs_general', 'imaging_chest', 'imaging_general'
            ]
        }

        return intent_id in context_intents.get(context, [])

    def _generate_discovery_response_with_context(self, session_id: str, intent_result: Dict[str, Any], discovery_result: Dict[str, Any], context: str) -> Dict[str, Any]:
        """Generate response with context-appropriate persona."""
        # Check if intent was filtered due to context
        if discovery_result.get('context_filtered'):
            return self._generate_context_filtered_response(intent_result['intent_id'], context)

        # Use existing response generation but with context-aware persona
        base_response = self._generate_discovery_response(session_id, intent_result, discovery_result)

        # Modify response based on context
        if context == 'anamnesis':
            # Son speaking for mother
            persona_prefix = ""  # Already handled in base response
        elif context == 'exam':
            # Direct examination findings
            if discovery_result['new_discoveries']:
                base_response['text'] = f"On examination: {base_response['text']}"
        elif context == 'labs':
            # Resident reporting results
            if discovery_result['new_discoveries']:
                base_response['text'] = f"The results show: {base_response['text']}"
            else:
                base_response['text'] = "I can order that test for you. " + base_response['text']

        return base_response

    def _generate_context_filtered_response(self, intent_id: str, context: str) -> Dict[str, Any]:
        """Generate response when intent is filtered due to context mismatch."""
        responses = {
            'anamnesis': {
                'exam': "I'm here to provide history about my mother. For physical examination findings, you'll need to examine her directly.",
                'labs': "I don't have access to laboratory results. You might want to speak with the resident about ordering tests.",
                'default': "I can help you with information about my mother's history and symptoms. What would you like to know?"
            },
            'exam': {
                'anamnesis': "This is the physical examination. For history questions, please speak with the patient's son.",
                'labs': "For laboratory or imaging results, please consult with the resident.",
                'default': "What aspect of the physical examination would you like me to perform?"
            },
            'labs': {
                'anamnesis': "For patient history, please speak with the patient's son.",
                'exam': "For physical examination, you'll need to examine the patient directly.",
                'default': "What laboratory tests or imaging studies would you like me to order or review?"
            }
        }

        # Determine the response based on context mismatch
        response_text = responses.get(context, {}).get('default', "I'm not sure how to help with that in this context.")

        return {
            'text': response_text,
            'discoveries': [],
            'context_filtered': True
        }
