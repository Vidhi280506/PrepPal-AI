import logging
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from sqlalchemy import func

# Using your existing models
from models.db_models import Problem

logger = logging.getLogger(__name__)

class ProblemRepository:
    """Handles data access for the Problem entity using SQLite."""
    
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, problem_id: int) -> Optional[Problem]:
        """Searches for a problem by its database ID."""
        return self.db.query(Problem).filter(Problem.id == problem_id).first()

    def filter_by_topic(self, topic: str) -> List[Problem]:
        """Filters problems by topic string."""
        return self.db.query(Problem).filter(Problem.topic == topic).all()

    def filter_by_difficulty(self, difficulty: str) -> List[Problem]:
        """Filters problems by difficulty level."""
        return self.db.query(Problem).filter(Problem.difficulty == difficulty).all()

    def get_random(self, topic: Optional[str] = None) -> Optional[Problem]:
        """Selects a random problem, optionally filtered by topic."""

        query = self.db.query(Problem)

        if topic:
            topic = topic.strip().lower()

            # Handle common singular/plural variations
            topic_aliases = {
              "array": "arrays",
              "arrays": "arrays",
              "graph": "graphs",
              "graphs": "graphs",
              "tree": "trees",
              "trees": "trees",
              "heap": "heaps",
              "heaps": "heaps",
              "string": "strings",
              "strings": "strings",
              "linked list": "linked lists",
              "linked lists": "linked lists",
              "dp": "dynamic programming",
              "dynamic programming": "dynamic programming",
              "binary search": "binary search",
              "backtracking": "backtracking",
              "sliding window": "sliding window",
            }

        normalized_topic = topic_aliases.get(topic, topic)

        query = query.filter(
            func.lower(Problem.topic) == normalized_topic
        )

        return query.order_by(func.random()).first()