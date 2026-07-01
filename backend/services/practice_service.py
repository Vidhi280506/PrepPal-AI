from sqlalchemy.orm import Session
import logging
from backend.schemas.practice import SubmitRequest

# TODO: Import your existing models and SM2 utils here
# from database.models import Problem, UserProgress
# from utils.sm2 import calculate_sm2

logger = logging.getLogger(__name__)

class PracticeService:
    def __init__(self, db: Session):
        self.db = db

    def get_next_problem(self):
        """Fetches the next problem based on SM-2 spacing."""
        logger.info("Fetching next optimal problem.")
        # Hook up your existing SQLite query here.
        # e.g., return self.db.query(Problem).filter(...).first()
        
        # Returning mock data so the app remains runnable immediately
        return {
            "id": 1,
            "question": "What is the time complexity of binary search?",
            "options": {"A": "O(1)", "B": "O(n)", "C": "O(log n)", "D": "O(n^2)"},
            "topic": "Algorithms",
            "difficulty": 2
        }

    def evaluate_submission(self, request: SubmitRequest):
        """Evaluates correctness and updates SM-2 parameters."""
        logger.info(f"Evaluating submission for problem_id: {request.problem_id}")
        
        # 1. Fetch problem from self.db
        # 2. Check correctness
        # 3. Call your existing SM-2 logic
        # 4. Commit to self.db

        return {
            "correct": True,
            "correct_answer": "C",
            "explanation": "Binary search halves the search space each iteration.",
            "new_sm2_interval": 3
        }