from datetime import datetime
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey, Float, Enum, Boolean
import enum

Base = declarative_base()

def utcnow(): return datetime.utcnow()

class MessageRole(str, enum.Enum):
    user = "user"
    assistant = "assistant"
    system = "system"

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    display_name: Mapped[str | None] = mapped_column(String(120))
    # Store ONLY hash of the access code
    code_hash: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    code_label: Mapped[str | None] = mapped_column(String(120))  # e.g., cohort or tag
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime)
    usage_limit: Mapped[int | None] = mapped_column(Integer)     # None = unlimited
    usage_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)
    last_used_at: Mapped[datetime | None] = mapped_column(DateTime)
    # Admin-related fields
    email: Mapped[str | None] = mapped_column(String(255), index=True)
    age: Mapped[int | None] = mapped_column(Integer)
    sex: Mapped[str | None] = mapped_column(String(20))
    medical_experience: Mapped[str | None] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(20), default="user", nullable=False)  # 'admin' | 'user'

class AuthSession(Base):
    __tablename__ = "auth_sessions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    jti: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)   # JWT ID for revocation
    issued_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)
    revoked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    user = relationship("User")

class Conversation(Base):
    __tablename__ = "conversations"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str | None] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, onupdate=utcnow, nullable=False)
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")
    sessions = relationship("SimulationSession", back_populates="conversation", cascade="all, delete-orphan")

class Message(Base):
    __tablename__ = "messages"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    conversation_id: Mapped[int] = mapped_column(ForeignKey("conversations.id"), index=True, nullable=False)
    role: Mapped[MessageRole] = mapped_column(Enum(MessageRole), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    context: Mapped[str | None] = mapped_column(String(64))
    meta: Mapped[str | None] = mapped_column(Text)  # JSON-encoded string
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)
    conversation = relationship("Conversation", back_populates="messages")

class SimulationSession(Base):
    __tablename__ = "simulation_sessions"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)  # use your session_id
    conversation_id: Mapped[int | None] = mapped_column(ForeignKey("conversations.id"))
    status: Mapped[str] = mapped_column(String(16), default="active", nullable=False)
    stats: Mapped[str | None] = mapped_column(Text)  # JSON-encoded string
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)
    ended_at: Mapped[datetime | None] = mapped_column(DateTime)
    conversation = relationship("Conversation", back_populates="sessions")
    discoveries = relationship("DiscoveryEvent", back_populates="session", cascade="all, delete-orphan")
    biases = relationship("BiasWarning", back_populates="session", cascade="all, delete-orphan")
    diagnoses = relationship("DiagnosisSubmission", back_populates="session", cascade="all, delete-orphan")

class DiscoveryEvent(Base):
    __tablename__ = "discovery_events"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    session_id: Mapped[str] = mapped_column(ForeignKey("simulation_sessions.id"), index=True, nullable=False)
    category: Mapped[str] = mapped_column(String(64), nullable=False)
    label: Mapped[str] = mapped_column(String(255), nullable=False)
    value: Mapped[str] = mapped_column(Text, nullable=False)
    confidence: Mapped[float | None] = mapped_column(Float)
    block_id: Mapped[str | None] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)
    session = relationship("SimulationSession", back_populates="discoveries")

class BiasWarning(Base):
    __tablename__ = "bias_warnings"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    session_id: Mapped[str] = mapped_column(ForeignKey("simulation_sessions.id"), index=True, nullable=False)
    bias_type: Mapped[str] = mapped_column(String(64), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)
    session = relationship("SimulationSession", back_populates="biases")

class DiagnosisSubmission(Base):
    __tablename__ = "diagnosis_submissions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    session_id: Mapped[str] = mapped_column(ForeignKey("simulation_sessions.id"), index=True, nullable=False)
    diagnosis_text: Mapped[str] = mapped_column(Text, nullable=False)
    score_overall: Mapped[int | None] = mapped_column(Integer)
    score_breakdown: Mapped[str | None] = mapped_column(Text)  # JSON-encoded string
    feedback: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)
    session = relationship("SimulationSession", back_populates="diagnoses")
    reflections = relationship("ReflectionResponse", back_populates="diagnosis", cascade="all, delete-orphan")

class ReflectionResponse(Base):
    __tablename__ = "reflection_responses"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    diagnosis_id: Mapped[int] = mapped_column(ForeignKey("diagnosis_submissions.id"), index=True, nullable=False)
    question: Mapped[str] = mapped_column(Text, nullable=False)
    answer: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)
    diagnosis = relationship("DiagnosisSubmission", back_populates="reflections")

class LLMProfile(Base):
    __tablename__ = "llm_profiles"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    provider: Mapped[str] = mapped_column(String(64), nullable=False)  # 'ollama', 'openai', etc.
    model: Mapped[str] = mapped_column(String(255), nullable=False)
    temperature: Mapped[float] = mapped_column(Float, default=0.1, nullable=False)
    top_p: Mapped[float] = mapped_column(Float, default=0.9, nullable=False)
    max_tokens: Mapped[int | None] = mapped_column(Integer)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)
    # Relationship to agent prompts
    prompts = relationship("AgentPrompt", back_populates="profile", cascade="all, delete-orphan")

class AgentPrompt(Base):
    __tablename__ = "agent_prompts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    agent_key: Mapped[str] = mapped_column(String(64), nullable=False)  # 'son', 'resident', 'exam'
    profile_id: Mapped[int | None] = mapped_column(ForeignKey("llm_profiles.id"), index=True)
    prompt_text: Mapped[str] = mapped_column(Text, nullable=False)
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)
    # Relationship
    profile = relationship("LLMProfile", back_populates="prompts")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    actor_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), index=True)
    action: Mapped[str] = mapped_column(String(128), nullable=False)
    payload: Mapped[str | None] = mapped_column(Text)  # JSON string
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)
    # Relationship
    actor = relationship("User")
