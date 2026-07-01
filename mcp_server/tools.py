import json
import logging
from typing import Optional
from pydantic import BaseModel, ValidationError

# Importing from the existing backend structure
from database.connection import SessionLocal
from backend.repositories.problem_repository import ProblemRepository
from backend.repositories.progress_repository import ProgressRepository
from models.db_models import Problem

logger = logging.getLogger(__name__)

# --- Input Validation Schemas ---

class GetProblemArgs(BaseModel):
    topic: Optional[str] = None
    difficulty: Optional[str] = None 

class SubmitAttemptArgs(BaseModel):
    problem_id: int
    solved: bool
    time_spent_minutes: int

# --- Tool Handlers ---

def execute_get_problem(arguments: dict) -> str:
    """Fetches a problem, optionally filtered by topic and difficulty."""
    try:
        args = GetProblemArgs(**arguments)
    except ValidationError as e:
        logger.warning(f"Validation error in get_problem: {e.errors()}")
        return json.dumps({"error": "Invalid arguments", "details": e.errors()})

    db = SessionLocal()
    try:
        repo = ProblemRepository(db)
        problem: Optional[Problem] = repo.get_random(topic=args.topic)
        
        if not problem:
            return json.dumps({"message": "No problems found matching criteria."})

        return json.dumps({
            "id": problem.id,
            "title": problem.title,
            "topic": problem.topic,
            "difficulty": problem.difficulty,
            "question": problem.description
        })
    except Exception as e:
        logger.error(f"Error in execute_get_problem: {e}")
        return json.dumps({"error": "Internal database error."})
    finally:
        db.close()

def execute_submit_attempt(arguments: dict) -> str:
    """Stores an attempt using the ProgressRepository."""
    try:
        args = SubmitAttemptArgs(**arguments)
    except ValidationError as e:
        return json.dumps({"error": "Invalid arguments", "details": e.errors()})

    db = SessionLocal()
    try:
        repo = ProgressRepository(db)
        repo.store_attempt(
            problem_id=args.problem_id,
            is_solved=args.solved,
            time_spent_minutes=args.time_spent_minutes
        )
        return json.dumps({"status": "success", "message": f"Attempt stored for problem {args.problem_id}."})
    except Exception as e:
        logger.error(f"Error in execute_submit_attempt: {e}")
        return json.dumps({"error": "Failed to store attempt."})
    finally:
        db.close()

def execute_get_progress(arguments: dict) -> str:
    """Returns dashboard metrics using the ProgressRepository."""
    db = SessionLocal()
    try:
        repo = ProgressRepository(db)
        metrics = {
            "total_solved": repo.get_solved_count(),
            "accuracy_percentage": repo.get_accuracy(),
            "mastered_topics": repo.get_mastered_topics(),
            "weak_topics": repo.get_weak_topics()
        }
        return json.dumps({"progress": metrics})
    except Exception as e:
        logger.error(f"Error in execute_get_progress: {e}")
        return json.dumps({"error": "Failed to retrieve progress."})
    finally:
        db.close()

def execute_get_review_queue(arguments: dict) -> str:
    """Finds topics due for spaced repetition and retrieves a problem for each."""
    db = SessionLocal()
    try:
        prog_repo = ProgressRepository(db)
        prob_repo = ProblemRepository(db)
        
        due_topics = prog_repo.get_topics_due_for_review()
        if not due_topics:
            return json.dumps({"message": "No reviews due right now. Great job!"})
        
        queue = []
        for topic in due_topics:
            prob = prob_repo.get_random(topic=topic)
            if prob:
                queue.append({
                    "topic": topic,
                    "problem_id": prob.id,
                    "problem_title": prob.title
                })
                
        return json.dumps({"due_reviews": queue})
    except Exception as e:
        logger.error(f"Error in execute_get_review_queue: {e}")
        return json.dumps({"error": "Failed to retrieve review queue."})
    finally:
        db.close()

# --- Schema Definitions for MCP ---

def get_problem_schema() -> dict:
    return {
        "type": "object",
        "properties": {
            "topic": {"type": "string", "description": "Optional topic filter (e.g., 'Dynamic Programming')"},
            "difficulty": {"type": "string", "description": "Optional difficulty filter"}
        }
    }

def submit_attempt_schema() -> dict:
    return {
        "type": "object",
        "properties": {
            "problem_id": {"type": "integer"},
            "solved": {"type": "boolean"},
            "time_spent_minutes": {"type": "integer"}
        },
        "required": ["problem_id", "solved", "time_spent_minutes"]
    }