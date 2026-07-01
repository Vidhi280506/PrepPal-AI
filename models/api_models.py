"""
PrepPal AI — Pydantic API Models (v2)
Request/Response contracts for all FastAPI endpoints.
"""
from __future__ import annotations
from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel, Field, field_validator


# ============================================================
# User Models
# ============================================================

class UserCreate(BaseModel):
    """Request model to create/init the user profile."""
    name: str = Field(default="Learner", min_length=1, max_length=100)
    target_role: Optional[str] = Field(default=None, max_length=100)
    target_companies: list[str] = Field(default_factory=list)
    experience_level: str = Field(default="beginner")
    daily_goal_minutes: int = Field(default=60, ge=15, le=480)

    @field_validator("experience_level")
    @classmethod
    def validate_experience(cls, v: str) -> str:
        allowed = {"beginner", "intermediate", "advanced"}
        if v not in allowed:
            raise ValueError(f"experience_level must be one of {allowed}")
        return v


class UserUpdate(BaseModel):
    """Partial update for user profile."""
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    target_role: Optional[str] = Field(default=None, max_length=100)
    target_companies: Optional[list[str]] = None
    experience_level: Optional[str] = None
    daily_goal_minutes: Optional[int] = Field(default=None, ge=15, le=480)


class UserResponse(BaseModel):
    """Response model for user data."""
    id: int
    name: str
    target_role: Optional[str]
    target_companies: list[str]
    experience_level: str
    daily_goal_minutes: int
    created_at: datetime

    model_config = {"from_attributes": True}


# ============================================================
# Problem Models
# ============================================================

class ProblemExample(BaseModel):
    input: str
    output: str
    explanation: str


class ProblemResponse(BaseModel):
    """Full problem details returned to frontend."""
    id: int
    title: str
    topic: str
    difficulty: str
    companies: list[str]
    description: str
    constraints: list[str]
    examples: list[dict[str, Any]]
    hints: list[str]           # All 3 hints (revealed progressively on frontend)
    solution: Optional[str]    # Hidden unless unlocked
    tags: list[str]
    time_complexity: Optional[str]
    space_complexity: Optional[str]

    model_config = {"from_attributes": True}


class ProblemSummary(BaseModel):
    """Lightweight problem card for lists."""
    id: int
    title: str
    topic: str
    difficulty: str
    companies: list[str]
    tags: list[str]

    model_config = {"from_attributes": True}


class ProblemFilter(BaseModel):
    """Filter parameters for problem listing."""
    topic: Optional[str] = None
    difficulty: Optional[str] = None
    company: Optional[str] = None
    tag: Optional[str] = None
    search: Optional[str] = None


# ============================================================
# Attempt Models
# ============================================================

class AttemptCreate(BaseModel):
    """Request model to record an attempt."""
    user_id: int
    problem_id: int
    is_solved: bool
    hint_level_used: int = Field(default=0, ge=0, le=3)
    time_spent_minutes: float = Field(default=0.0, ge=0)
    notes: Optional[str] = Field(default=None, max_length=2000)
    code_submitted: Optional[str] = Field(default=None, max_length=10000)
    quality_score: Optional[int] = Field(default=None, ge=0, le=5)

    @field_validator("problem_id", "user_id")
    @classmethod
    def validate_positive(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("ID must be a positive integer")
        return v


class AttemptResponse(BaseModel):
    """Response model for a recorded attempt."""
    id: int
    user_id: int
    problem_id: int
    is_solved: bool
    hint_level_used: int
    time_spent_minutes: float
    quality_score: Optional[int]
    attempted_at: datetime

    model_config = {"from_attributes": True}


# ============================================================
# Progress Models
# ============================================================

class TopicProgress(BaseModel):
    """Progress breakdown per topic."""
    topic: str
    total_problems: int
    solved: int
    attempted: int
    accuracy_rate: float          # 0.0 - 1.0
    mastery_percent: float        # 0.0 - 100.0
    avg_hints_used: float
    is_weak: bool                 # True if accuracy < 60%


class ProgressResponse(BaseModel):
    """Full progress report for a user."""
    user_id: int
    total_solved: int
    total_attempted: int
    overall_accuracy: float
    streak_days: int
    total_time_minutes: float
    topics: list[TopicProgress]
    weak_topics: list[str]
    strong_topics: list[str]
    recent_activity: list[dict[str, Any]]


# ============================================================
# Study Plan Models
# ============================================================

class StudyPlanCreate(BaseModel):
    """Request to generate a study plan."""
    user_id: int
    total_weeks: int = Field(default=4, ge=1, le=12)
    focus_topics: Optional[list[str]] = None
    target_company: Optional[str] = None


class StudyPlanResponse(BaseModel):
    """AI-generated study plan."""
    id: int
    user_id: int
    title: str
    description: Optional[str]
    plan_data: dict[str, Any]
    total_weeks: int
    is_active: bool
    progress_percent: float
    created_at: datetime

    model_config = {"from_attributes": True}


# ============================================================
# Agent Models
# ============================================================

class AgentRequest(BaseModel):
    """Request to invoke the root agent."""
    user_id: int
    message: str = Field(min_length=1, max_length=5000)
    session_id: Optional[str] = None
    context: Optional[dict[str, Any]] = None

    @field_validator("message")
    @classmethod
    def sanitize_message(cls, v: str) -> str:
        # Strip leading/trailing whitespace
        return v.strip()


class AgentResponse(BaseModel):
    """Response from the agent."""
    session_id: str
    message: str
    agent_used: str          # which agent handled this: root/coach/tracker/mock
    tool_calls: list[str]    # names of MCP tools invoked
    metadata: Optional[dict[str, Any]] = None


# ============================================================
# Mock Interview Models
# ============================================================

class MockInterviewRequest(BaseModel):
    """Start a new mock interview session."""
    user_id: int
    problem_id: Optional[int] = None      # if None, agent picks based on profile
    target_company: Optional[str] = None


class MockTurnRequest(BaseModel):
    """User's turn response during mock interview."""
    session_id: str
    user_id: int
    message: str = Field(min_length=1, max_length=5000)


class MockInterviewResponse(BaseModel):
    """Response from the mock interview agent."""
    session_id: str
    message: str
    is_complete: bool = False
    score: Optional[int] = None
    feedback: Optional[str] = None
    evaluation: Optional[dict[str, Any]] = None


# ============================================================
# Review Schedule Models
# ============================================================

class ReviewScheduleResponse(BaseModel):
    """Spaced repetition review item."""
    id: int
    problem_id: int
    problem_title: str
    problem_topic: str
    next_review_date: datetime
    interval_days: int
    ease_factor: float
    repetitions: int

    model_config = {"from_attributes": True}
