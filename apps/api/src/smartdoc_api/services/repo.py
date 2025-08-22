from contextlib import contextmanager
from typing import Iterator
from sqlalchemy.orm import Session
from json import dumps
from ..db import get_session
from ..db.models import (
    Conversation, Message, SimulationSession,
    DiscoveryEvent, BiasWarning, DiagnosisSubmission, ReflectionResponse,
    MessageRole
)

@contextmanager
def session_scope() -> Iterator[Session]:
    s = get_session()
    try:
        yield s
        s.commit()
    except:
        s.rollback()
        raise
    finally:
        s.close()

def get_or_create_conversation_for_session(session_id: str, title: str | None = None) -> int:
    """Returns the conversation ID for the given session."""
    with session_scope() as s:
        # Find if any SimulationSession already exists
        sess = s.get(SimulationSession, session_id)
        if sess and sess.conversation_id:
            conv = s.get(Conversation, sess.conversation_id)
            if conv:
                return conv.id
        # else create conv + link session
        conv = Conversation(title=title)
        s.add(conv); s.flush(); s.refresh(conv)
        conv_id = conv.id  # Extract the ID while still in session
        if not sess:
            sess = SimulationSession(id=session_id, conversation_id=conv_id, status="active")
            s.add(sess)
        else:
            sess.conversation_id = conv_id
        return conv_id

def add_message(conversation_id: int, role: MessageRole, content: str, context: str | None = None, meta: dict | None = None):
    with session_scope() as s:
        m = Message(conversation_id=conversation_id, role=role, content=content, context=context, meta=dumps(meta) if meta else None)
        s.add(m)

def ensure_session(session_id: str, conversation_id: int | None):
    with session_scope() as s:
        sess = s.get(SimulationSession, session_id)
        if not sess:
            s.add(SimulationSession(id=session_id, conversation_id=conversation_id, status="active"))

def add_discoveries(session_id: str, events: list[dict]):
    if not events: return
    with session_scope() as s:
        for ev in events:
            s.add(DiscoveryEvent(
                session_id=session_id,
                category=ev.get("category","general"),
                label=ev.get("field",""),
                value=ev.get("value",""),
                confidence=ev.get("confidence"),
                block_id=ev.get("block_id"),
            ))

def add_biases(session_id: str, warnings: list[dict]):
    if not warnings: return
    with session_scope() as s:
        for w in warnings:
            s.add(BiasWarning(
                session_id=session_id,
                bias_type=w.get("bias_type",""),
                description=w.get("description","")
            ))

def submit_diagnosis(session_id: str, diagnosis_text: str, score_overall: int | None, score_breakdown: dict | None, feedback: str | None, reflections: dict[str,str] | None):
    with session_scope() as s:
        d = DiagnosisSubmission(
            session_id=session_id,
            diagnosis_text=diagnosis_text,
            score_overall=score_overall,
            score_breakdown=dumps(score_breakdown) if score_breakdown else None,
            feedback=feedback
        )
        s.add(d); s.flush(); s.refresh(d)
        if reflections:
            for q, a in reflections.items():
                s.add(ReflectionResponse(diagnosis_id=d.id, question=q, answer=a))
