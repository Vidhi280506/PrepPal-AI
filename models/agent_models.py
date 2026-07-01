"""
PrepPal AI — Agent Communication Models
Pydantic models for inter-agent payloads and MCP tool contracts.
"""
from __future__ import annotations
from typing import Any, Optional
from pydantic import BaseModel, Field


class AgentContext(BaseModel):
    """Context passed between agents during orchestration."""
    user_id: int
    session_id: str
    user_name: str = "Learner"
    experience_level: str = "beginner"
    target_role: Optional[str] = None
    target_companies: list[str] = Field(default_factory=list)
    current_topic: Optional[str] = None
    current_problem_id: Optional[int] = None


class CoachRequest(BaseModel):
    """Request sent to the Coach Agent."""
    context: AgentContext
    user_message: str
    hint_level: int = Field(default=0, ge=0, le=3)
    problem_id: Optional[int] = None


class CoachResponse(BaseModel):
    """Response from the Coach Agent."""
    message: str
    hint_level_revealed: int = 0
    should_reveal_solution: bool = False
    suggested_problem_id: Optional[int] = None
    encouragement: Optional[str] = None


class TrackerRequest(BaseModel):
    """Request sent to the Tracker Agent."""
    context: AgentContext
    action: str   # "get_progress" | "recommend_topic" | "schedule_review" | "get_plan"


class TrackerResponse(BaseModel):
    """Response from the Tracker Agent."""
    message: str
    weak_topics: list[str] = Field(default_factory=list)
    recommended_topic: Optional[str] = None
    due_reviews: list[dict[str, Any]] = Field(default_factory=list)
    stats_summary: Optional[dict[str, Any]] = None


class MockInterviewTurn(BaseModel):
    """A single turn in the mock interview conversation."""
    role: str   # "interviewer" | "candidate"
    content: str
    timestamp: str


class MCPToolInput(BaseModel):
    """Base input model for MCP tool calls."""
    user_id: int


class GetProblemInput(MCPToolInput):
    problem_id: Optional[int] = None
    topic: Optional[str] = None
    difficulty: Optional[str] = None


class SubmitAttemptInput(MCPToolInput):
    problem_id: int
    is_solved: bool
    hint_level_used: int = 0
    time_spent_minutes: float = 0.0
    notes: Optional[str] = None


class GetProgressInput(MCPToolInput):
    pass


class RecommendTopicInput(MCPToolInput):
    pass


class GenerateStudyPlanInput(MCPToolInput):
    total_weeks: int = 4
    focus_topics: Optional[list[str]] = None
    target_company: Optional[str] = None


class GetStatisticsInput(MCPToolInput):
    pass
