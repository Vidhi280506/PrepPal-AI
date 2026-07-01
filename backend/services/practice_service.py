import logging

from backend.schemas.practice import SubmitRequest
from backend.repositories.problem_repository import ProblemRepository
from backend.repositories.progress_repository import ProgressRepository
from utils.sm2 import calculate_next_review, attempt_to_quality

logger = logging.getLogger(__name__)


class PracticeService:

    def __init__(
        self,
        problem_repo: ProblemRepository,
        progress_repo: ProgressRepository,
    ):
        self.problem_repo = problem_repo
        self.progress_repo = progress_repo

    def recommend_problem(self) -> dict:
        """Recommend a DSA problem."""

        due_topics = self.progress_repo.get_topics_due_for_review()

        if due_topics:
            target_topic = due_topics[0]
            reason = f"It's time to review {target_topic}."
        else:
            weak_topics = self.progress_repo.get_weak_topics()
            target_topic = weak_topics[0] if weak_topics else None
            reason = (
                f"Let's strengthen {target_topic}."
                if target_topic
                else "Here's a new challenge."
            )

        problem = self.problem_repo.get_random(topic=target_topic)

        if problem is None:
            return None

        estimated_time = {
            "Easy": 15,
            "Medium": 30,
            "Hard": 45,
        }.get(problem.difficulty, 30)

        return {
            "id": problem.id,
            "question": problem.description,
            "topic": problem.topic,
            "difficulty": problem.difficulty,
            "recommendation_reason": reason,
            "estimated_time_minutes": estimated_time,
            "hint": f"Think about standard approaches to {problem.topic}.",
        }

    def evaluate_submission(self, request: SubmitRequest) -> dict:
        """Evaluate a user's submission."""

        problem = self.problem_repo.get_by_id(request.problem_id)

        if problem is None:
            raise ValueError("Problem not found.")

        correct_answer = getattr(problem, "solution", "")

        is_solved = (
            str(request.user_answer).strip().lower()
            == str(correct_answer).strip().lower()
        )

        quality = attempt_to_quality(
            is_solved=is_solved,
            hint_level=0,
            attempts=1,
        )

        previous_interval = 1
        previous_repetitions = 0
        previous_ease_factor = 2.5

        (
            new_interval,
            new_ease_factor,
            new_repetitions,
            next_review_date,
        ) = calculate_next_review(
            ease_factor=previous_ease_factor,
            interval_days=previous_interval,
            repetitions=previous_repetitions,
            quality=quality,
        )

        self.progress_repo.store_attempt(
            problem_id=problem.id,
            is_solved=is_solved,
            time_spent_minutes=request.time_taken_seconds / 60,
            hint_level_used=0,
        )

        self.progress_repo.update_sm2_progress(
            problem_id=problem.id,
            interval_days=new_interval,
            repetitions=new_repetitions,
            ease_factor=new_ease_factor,
        )

        return {
            "correct": is_solved,
            "correct_answer": correct_answer,
            "explanation": getattr(problem, "solution", ""),
            "new_sm2_interval": new_interval,
        }