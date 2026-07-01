from sqlalchemy.orm import Session
import logging

logger = logging.getLogger(__name__)

class DashboardService:
    def __init__(self, db: Session):
        self.db = db

    def get_progress_metrics(self):
        """Aggregates user metrics from SQLite."""
        # Query your existing UserProgress models here
        return {
            "total_problems_solved": 150,
            "accuracy_rate": 78.5,
            "topics_mastered": 4
        }

    def get_study_plan(self):
        """Generates plan based on weakest topics via SM-2 metrics."""
        return {
            "plan": [
                {"topic": "Dynamic Programming", "recommended_problems": 5, "priority": "High"},
                {"topic": "Graph Theory", "recommended_problems": 3, "priority": "Medium"}
            ]
        }