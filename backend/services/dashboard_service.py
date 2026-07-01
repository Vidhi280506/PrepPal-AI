import logging
from backend.repositories.progress_repository import ProgressRepository

logger = logging.getLogger(__name__)

class DashboardService:
    def __init__(self, progress_repo: ProgressRepository):
        self.progress_repo = progress_repo

    def get_progress_metrics(self) -> dict:
        """Aggregates real user metrics from SQLite via Attempt and ReviewSchedule models."""
        return {
            "total_problems_solved": self.progress_repo.get_solved_count(),
            "accuracy_rate": self.progress_repo.get_accuracy(),
            "topics_mastered": self.progress_repo.get_mastered_topics()
        }

    def get_study_plan(self) -> dict:
        """Generates a study plan based on weak topics and due reviews."""
        weak_topics = self.progress_repo.get_weak_topics()
        due_topics = self.progress_repo.get_topics_due_for_review()
        
        plan = []
        
        for topic in due_topics:
            plan.append({"topic": topic, "recommended_problems": 3, "priority": "High (Due for Review)"})
            
        for topic in weak_topics:
            if topic not in due_topics:
                plan.append({"topic": topic, "recommended_problems": 5, "priority": "Medium (Needs Improvement)"})

        if not plan:
            plan.append({"topic": "Data Structures", "recommended_problems": 5, "priority": "Baseline Assessment"})

        return {"plan": plan}