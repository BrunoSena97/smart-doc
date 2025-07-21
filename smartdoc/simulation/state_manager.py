"""
Simulation State Manager for SmartDoc Virtual Patient System

This module manages the state of clinical simulation sessions, including progressive
disclosure of information blocks, session tracking, and providing the foundation
for cognitive bias detection through temporal information sequencing.
"""

import json
import time
from typing import Dict, List, Set, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime

from smartdoc.utils.logger import sys_logger
from smartdoc.config.settings import config

@dataclass
class InformationBlock:
    """Represents a single discoverable information block."""
    block_id: str
    block_type: str  # History, PhysicalExam, Labs, Imaging
    content: str
    is_critical: bool
    is_revealed: bool = False
    revealed_at: Optional[datetime] = None
    revealed_by_query: Optional[str] = None

@dataclass
class StudentInteraction:
    """Tracks a student's interaction with the progressive disclosure system."""
    timestamp: datetime
    action: str  # 'reveal_block', 'submit_hypothesis', 'request_category'
    block_id: Optional[str] = None
    category: Optional[str] = None
    hypothesis: Optional[str] = None
    reasoning: Optional[str] = None

@dataclass
class ProgressiveDisclosureSession:
    """Manages a single progressive disclosure session."""
    session_id: str
    case_id: str
    start_time: datetime
    blocks: Dict[str, InformationBlock] = field(default_factory=dict)
    revealed_blocks: Set[str] = field(default_factory=set)
    interactions: List[StudentInteraction] = field(default_factory=list)
    working_hypotheses: List[Dict[str, str]] = field(default_factory=list)
    final_diagnosis: Optional[str] = None
    session_complete: bool = False

class ProgressiveDisclosureManager:
    """
    Manages progressive disclosure of clinical information for virtual patient simulations.

    This class implements the progressive disclosure methodology described in the dissertation,
    where information is revealed gradually to simulate realistic clinical information gathering
    and enable proper cognitive bias detection.
    """

    def __init__(self, case_file_path: str = None):
        """
        Initialize the Progressive Disclosure Manager.

        Args:
            case_file_path: Path to the JSON case file. If None, uses config default.
        """
        self.case_file_path = case_file_path or config.CASE_FILE
        self.case_data = None
        self.active_sessions: Dict[str, ProgressiveDisclosureSession] = {}
        self.load_case_data()

    def load_case_data(self) -> bool:
        """Load case data from JSON file."""
        try:
            with open(self.case_file_path, 'r', encoding='utf-8') as f:
                self.case_data = json.load(f)

            sys_logger.log_system("info", f"Progressive Disclosure: Loaded case {self.case_data.get('caseId')}")
            return True

        except Exception as e:
            sys_logger.log_system("error", f"Progressive Disclosure: Failed to load case data: {e}")
            return False

    def start_new_session(self, session_id: str) -> ProgressiveDisclosureSession:
        """
        Start a new progressive disclosure session.

        Args:
            session_id: Unique identifier for the session

        Returns:
            ProgressiveDisclosureSession: The new session object
        """
        if not self.case_data:
            raise ValueError("Case data not loaded")

        # Create information blocks from case data
        blocks = {}
        for block_data in self.case_data.get('informationBlocks', []):
            block = InformationBlock(
                block_id=block_data['blockId'],
                block_type=block_data['blockType'],
                content=block_data['content'],
                is_critical=block_data.get('isCritical', False)
            )
            blocks[block.block_id] = block

        session = ProgressiveDisclosureSession(
            session_id=session_id,
            case_id=self.case_data['caseId'],
            start_time=datetime.now(),
            blocks=blocks
        )

        self.active_sessions[session_id] = session
        sys_logger.log_system("info", f"Progressive Disclosure: Started session {session_id}")

        return session

    def get_session(self, session_id: str) -> Optional[ProgressiveDisclosureSession]:
        """Get an active session by ID."""
        return self.active_sessions.get(session_id)

    def get_available_categories(self, session_id: str) -> List[Dict[str, Any]]:
        """
        Get available information categories for progressive disclosure.

        Returns information about what types of information are available,
        without revealing the actual content.
        """
        session = self.get_session(session_id)
        if not session:
            return []

        categories = {}
        for block in session.blocks.values():
            if block.block_type not in categories:
                categories[block.block_type] = {
                    'type': block.block_type,
                    'available_count': 0,
                    'revealed_count': 0,
                    'description': self._get_category_description(block.block_type)
                }

            categories[block.block_type]['available_count'] += 1
            if block.is_revealed:
                categories[block.block_type]['revealed_count'] += 1

        return list(categories.values())

    def get_blocks_by_category(self, session_id: str, category: str, include_unrevealed: bool = True) -> List[Dict[str, Any]]:
        """
        Get information blocks by category.

        Args:
            session_id: The session ID
            category: The category to filter by
            include_unrevealed: Whether to include unrevealed blocks (with limited info)

        Returns:
            List of blocks with appropriate information based on revelation status
        """
        session = self.get_session(session_id)
        if not session:
            return []

        blocks = []
        for block in session.blocks.values():
            if block.block_type == category:
                if block.is_revealed:
                    blocks.append({
                        'blockId': block.block_id,
                        'blockType': block.block_type,
                        'content': block.content,
                        'isCritical': block.is_critical,
                        'isRevealed': True,
                        'revealedAt': block.revealed_at.isoformat() if block.revealed_at else None,
                        'revealedByQuery': block.revealed_by_query
                    })
                elif include_unrevealed:
                    blocks.append({
                        'blockId': block.block_id,
                        'blockType': block.block_type,
                        'content': self._get_block_teaser(block),
                        'isCritical': block.is_critical,
                        'isRevealed': False,
                        'canReveal': True
                    })

        return blocks

    def reveal_block(self, session_id: str, block_id: str, query: str = None) -> Dict[str, Any]:
        """
        Reveal a specific information block.

        Args:
            session_id: The session ID
            block_id: The block to reveal
            query: Optional - the student's query that triggered this revelation

        Returns:
            Dictionary with revelation result and block content
        """
        session = self.get_session(session_id)
        if not session:
            return {'success': False, 'error': 'Session not found'}

        block = session.blocks.get(block_id)
        if not block:
            return {'success': False, 'error': 'Block not found'}

        if block.is_revealed:
            return {
                'success': True,
                'already_revealed': True,
                'block': {
                    'blockId': block.block_id,
                    'blockType': block.block_type,
                    'content': block.content,
                    'isCritical': block.is_critical,
                    'revealedAt': block.revealed_at.isoformat()
                }
            }

        # Reveal the block
        block.is_revealed = True
        block.revealed_at = datetime.now()
        block.revealed_by_query = query
        session.revealed_blocks.add(block_id)

        # Log the interaction
        interaction = StudentInteraction(
            timestamp=datetime.now(),
            action='reveal_block',
            block_id=block_id
        )
        session.interactions.append(interaction)

        # Check for bias triggers
        bias_analysis = self._analyze_bias_potential(session, block_id)

        sys_logger.log_system("info",
            f"Progressive Disclosure: Block '{block_id}' revealed in session {session_id}")

        return {
            'success': True,
            'block': {
                'blockId': block.block_id,
                'blockType': block.block_type,
                'content': block.content,
                'isCritical': block.is_critical,
                'revealedAt': block.revealed_at.isoformat()
            },
            'biasAnalysis': bias_analysis,
            'sessionStats': self._get_session_stats(session)
        }

    def add_working_hypothesis(self, session_id: str, hypothesis: str, reasoning: str = "") -> Dict[str, Any]:
        """Add a working hypothesis to the session."""
        session = self.get_session(session_id)
        if not session:
            return {'success': False, 'error': 'Session not found'}

        hypothesis_entry = {
            'hypothesis': hypothesis,
            'reasoning': reasoning,
            'timestamp': datetime.now().isoformat(),
            'revealed_blocks_count': len(session.revealed_blocks)
        }

        session.working_hypotheses.append(hypothesis_entry)

        # Log the interaction
        interaction = StudentInteraction(
            timestamp=datetime.now(),
            action='submit_hypothesis',
            hypothesis=hypothesis,
            reasoning=reasoning
        )
        session.interactions.append(interaction)

        sys_logger.log_system("info",
            f"Progressive Disclosure: Hypothesis added in session {session_id}: {hypothesis}")

        return {'success': True, 'hypothesis': hypothesis_entry}

    def submit_final_diagnosis(self, session_id: str, diagnosis: str, reasoning: str = "") -> Dict[str, Any]:
        """Submit the final diagnosis and complete the session."""
        session = self.get_session(session_id)
        if not session:
            return {'success': False, 'error': 'Session not found'}

        session.final_diagnosis = diagnosis
        session.session_complete = True

        # Generate comprehensive bias analysis
        bias_analysis = self._generate_comprehensive_bias_analysis(session)

        # Calculate performance metrics
        performance = self._calculate_performance_metrics(session)

        sys_logger.log_system("info",
            f"Progressive Disclosure: Session {session_id} completed with diagnosis: {diagnosis}")

        return {
            'success': True,
            'diagnosis': diagnosis,
            'biasAnalysis': bias_analysis,
            'performance': performance,
            'sessionComplete': True
        }

    def get_initial_presentation(self) -> Dict[str, Any]:
        """Get the initial presentation information that's immediately available."""
        if not self.case_data:
            return {}

        return {
            'caseTitle': self.case_data.get('caseTitle', ''),
            'learningObjectives': self.case_data.get('learningObjectives', []),
            'initialPresentation': self.case_data.get('initialPresentation', {})
        }

    def _get_category_description(self, category: str) -> str:
        """Get description for information categories."""
        descriptions = {
            'History': 'Patient history, background, and reported symptoms',
            'PhysicalExam': 'Physical examination findings and vital signs',
            'Labs': 'Laboratory test results and blood work',
            'Imaging': 'Radiology and imaging study results'
        }
        return descriptions.get(category, 'Clinical information')

    def _get_block_teaser(self, block: InformationBlock) -> str:
        """Generate a teaser description for unrevealed blocks."""
        teasers = {
            'History': 'Additional patient history available',
            'PhysicalExam': 'Physical examination finding available',
            'Labs': 'Laboratory result available',
            'Imaging': 'Imaging study result available'
        }
        return teasers.get(block.block_type, 'Clinical information available')

    def _analyze_bias_potential(self, session: ProgressiveDisclosureSession, revealed_block_id: str) -> Dict[str, Any]:
        """Analyze potential bias implications of revealing this block."""
        if not self.case_data or 'biasTriggers' not in self.case_data:
            return {}

        bias_triggers = self.case_data['biasTriggers']
        analysis = {'potential_biases': []}

        # Check for anchoring bias
        if 'anchoring' in bias_triggers:
            anchor_info = bias_triggers['anchoring'].get('anchorInfoId')
            contradictory_info = bias_triggers['anchoring'].get('contradictoryInfoId')

            if revealed_block_id == anchor_info:
                analysis['potential_biases'].append({
                    'type': 'anchoring',
                    'description': 'This information could serve as an anchor - be careful not to overweight it',
                    'block_role': 'anchor'
                })
            elif revealed_block_id == contradictory_info and anchor_info in session.revealed_blocks:
                analysis['potential_biases'].append({
                    'type': 'anchoring',
                    'description': 'This information contradicts earlier findings - consider revising your assessment',
                    'block_role': 'contradictory'
                })

        # Check for confirmation bias
        if 'confirmation' in bias_triggers:
            supporting_blocks = bias_triggers['confirmation'].get('supportingInfoIds', [])
            refuting_blocks = bias_triggers['confirmation'].get('refutingInfoIds', [])

            if revealed_block_id in supporting_blocks:
                analysis['potential_biases'].append({
                    'type': 'confirmation',
                    'description': 'This finding supports the initial hypothesis - ensure you\'re not missing contradictory evidence',
                    'block_role': 'supporting'
                })
            elif revealed_block_id in refuting_blocks:
                analysis['potential_biases'].append({
                    'type': 'confirmation',
                    'description': 'This finding challenges the initial hypothesis - consider alternative diagnoses',
                    'block_role': 'refuting'
                })

        return analysis

    def _generate_comprehensive_bias_analysis(self, session: ProgressiveDisclosureSession) -> Dict[str, Any]:
        """Generate comprehensive bias analysis for the completed session."""
        if not self.case_data or 'biasTriggers' not in self.case_data:
            return {}

        bias_triggers = self.case_data['biasTriggers']
        ground_truth = self.case_data.get('groundTruth', {})

        analysis = {
            'anchoring_bias': {},
            'confirmation_bias': {},
            'information_gathering': {},
            'critical_findings': {}
        }

        # Analyze anchoring bias
        if 'anchoring' in bias_triggers:
            anchor_block = bias_triggers['anchoring'].get('anchorInfoId')
            contradictory_block = bias_triggers['anchoring'].get('contradictoryInfoId')

            anchor_revealed = anchor_block in session.revealed_blocks
            contradictory_revealed = contradictory_block in session.revealed_blocks

            analysis['anchoring_bias'] = {
                'anchor_encountered': anchor_revealed,
                'contradictory_evidence_found': contradictory_revealed,
                'potential_anchor_effect': anchor_revealed and not contradictory_revealed
            }

        # Analyze confirmation bias
        if 'confirmation' in bias_triggers:
            supporting_blocks = set(bias_triggers['confirmation'].get('supportingInfoIds', []))
            refuting_blocks = set(bias_triggers['confirmation'].get('refutingInfoIds', []))

            supporting_revealed = supporting_blocks & session.revealed_blocks
            refuting_revealed = refuting_blocks & session.revealed_blocks

            analysis['confirmation_bias'] = {
                'supporting_evidence_ratio': len(supporting_revealed) / len(supporting_blocks) if supporting_blocks else 0,
                'refuting_evidence_ratio': len(refuting_revealed) / len(refuting_blocks) if refuting_blocks else 0,
                'evidence_balance': len(supporting_revealed) - len(refuting_revealed)
            }

        # Analyze information gathering patterns
        critical_blocks = set(ground_truth.get('criticalFindingIds', []))
        critical_revealed = critical_blocks & session.revealed_blocks

        analysis['critical_findings'] = {
            'total_critical_blocks': len(critical_blocks),
            'critical_blocks_found': len(critical_revealed),
            'critical_completion_rate': len(critical_revealed) / len(critical_blocks) if critical_blocks else 0,
            'missed_critical_blocks': list(critical_blocks - critical_revealed)
        }

        return analysis

    def _calculate_performance_metrics(self, session: ProgressiveDisclosureSession) -> Dict[str, Any]:
        """Calculate performance metrics for the session."""
        if not self.case_data:
            return {}

        ground_truth = self.case_data.get('groundTruth', {})
        correct_diagnosis = ground_truth.get('finalDiagnosis', '')

        # Calculate diagnosis accuracy
        diagnosis_correct = False
        if session.final_diagnosis and correct_diagnosis:
            # Simple text matching - could be enhanced with semantic similarity
            diagnosis_correct = correct_diagnosis.lower() in session.final_diagnosis.lower()

        # Calculate information gathering efficiency
        total_blocks = len(session.blocks)
        revealed_blocks = len(session.revealed_blocks)
        critical_blocks = set(ground_truth.get('criticalFindingIds', []))
        critical_revealed = len(critical_blocks & session.revealed_blocks)

        session_duration = (datetime.now() - session.start_time).total_seconds() / 60  # minutes

        return {
            'diagnosis_accuracy': diagnosis_correct,
            'information_efficiency': revealed_blocks / total_blocks if total_blocks > 0 else 0,
            'critical_finding_rate': critical_revealed / len(critical_blocks) if critical_blocks else 0,
            'session_duration_minutes': round(session_duration, 2),
            'total_interactions': len(session.interactions),
            'working_hypotheses_count': len(session.working_hypotheses)
        }

    def _get_session_stats(self, session: ProgressiveDisclosureSession) -> Dict[str, Any]:
        """Get current session statistics."""
        total_blocks = len(session.blocks)
        revealed_blocks = len(session.revealed_blocks)

        return {
            'total_blocks': total_blocks,
            'revealed_blocks': revealed_blocks,
            'completion_percentage': (revealed_blocks / total_blocks * 100) if total_blocks > 0 else 0,
            'working_hypotheses': len(session.working_hypotheses),
            'session_duration_minutes': (datetime.now() - session.start_time).total_seconds() / 60
        }
