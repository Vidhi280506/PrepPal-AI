"""
PrepPal AI — Database ORM Models
SQLAlchemy 2.0 declarative models mapping to SQLite tables.
"""
from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Float, Boolean,
    Text, DateTime, ForeignKey, JSON
)
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    """Base class for all ORM models."""
    pass


class User(Base):
    """Single user profile (single-user local session mode)."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, default="Learner")
    target_role = Column(String(100), nullable=True)
    target_companies = Column(JSON, nullable=True, default=list)  # list of strings
    experience_level = Column(String(50), default="beginner")    # beginner/intermediate/advanced
    daily_goal_minutes = Column(Integer, default=60)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    attempts = relationship("Attempt", back_populates="user", cascade="all, delete-orphan")
    study_plans = relationship("StudyPlan", back_populates="user", cascade="all, delete-orphan")
    review_schedules = relationship("ReviewSchedule", back_populates="user", cascade="all, delete-orphan")
    sessions = relationship("InterviewSession", back_populates="user", cascade="all, delete-orphan")


class Topic(Base):
    """DSA topic registry."""
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    order_index = Column(Integer, default=0)  # recommended learning order

    # Relationships
    problems = relationship("Problem", back_populates="topic_rel")


class Problem(Base):
    """DSA problem with full metadata."""
    __tablename__ = "problems"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    topic = Column(String(100), nullable=False, index=True)
    difficulty = Column(String(20), nullable=False, index=True)  # Easy/Medium/Hard
    companies = Column(JSON, default=list)       # ["Google", "Amazon", ...]
    description = Column(Text, nullable=False)
    constraints = Column(JSON, default=list)     # list of constraint strings
    examples = Column(JSON, default=list)        # list of {input, output, explanation}
    hints = Column(JSON, default=list)           # 3-tier progressive hints
    solution = Column(Text, nullable=False)      # full Python solution
    tags = Column(JSON, default=list)            # algorithm tags
    time_complexity = Column(String(50), nullable=True)
    space_complexity = Column(String(50), nullable=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=True)

    # Relationships
    topic_rel = relationship("Topic", back_populates="problems")
    attempts = relationship("Attempt", back_populates="problem", cascade="all, delete-orphan")
    review_schedules = relationship("ReviewSchedule", back_populates="problem", cascade="all, delete-orphan")


class Attempt(Base):
    """Records each attempt a user makes on a problem."""
    __tablename__ = "attempts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    problem_id = Column(Integer, ForeignKey("problems.id"), nullable=False, index=True)
    is_solved = Column(Boolean, default=False)
    hint_level_used = Column(Integer, default=0)   # 0=no hint, 1/2/3=progressive hints
    time_spent_minutes = Column(Float, default=0)
    notes = Column(Text, nullable=True)             # user's approach notes
    code_submitted = Column(Text, nullable=True)    # user's submitted code
    quality_score = Column(Integer, nullable=True)  # 0-5 self-rating
    attempted_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="attempts")
    problem = relationship("Problem", back_populates="attempts")


class StudyPlan(Base):
    """AI-generated personalized study plan."""
    __tablename__ = "study_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    plan_data = Column(JSON, nullable=False)  # {week: [{day, topic, problem_ids, goal}]}
    total_weeks = Column(Integer, default=4)
    is_active = Column(Boolean, default=True)
    progress_percent = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="study_plans")


class ReviewSchedule(Base):
    """Spaced repetition review schedule (SM-2 algorithm)."""
    __tablename__ = "review_schedules"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    problem_id = Column(Integer, ForeignKey("problems.id"), nullable=False, index=True)
    next_review_date = Column(DateTime, nullable=False)
    interval_days = Column(Integer, default=1)      # current SM-2 interval
    ease_factor = Column(Float, default=2.5)        # SM-2 ease factor
    repetitions = Column(Integer, default=0)        # number of successful reviews
    last_reviewed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="review_schedules")
    problem = relationship("Problem", back_populates="review_schedules")


class InterviewSession(Base):
    """Mock interview session with transcript."""
    __tablename__ = "interview_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    problem_id = Column(Integer, ForeignKey("problems.id"), nullable=True)
    status = Column(String(20), default="active")   # active/completed/abandoned
    transcript = Column(JSON, default=list)          # [{role, content, timestamp}]
    score = Column(Integer, nullable=True)           # 0-100
    feedback = Column(Text, nullable=True)           # AI evaluator feedback
    evaluation = Column(JSON, nullable=True)         # {correctness, clarity, complexity, communication}
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    # Relationships
    user = relationship("User", back_populates="sessions")
