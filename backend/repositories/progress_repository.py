import logging
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from sqlalchemy import Integer

# Using the exact existing models
from models.db_models import Attempt, ReviewSchedule, Problem

logger = logging.getLogger(__name__)

class ProgressRepository:
    """Handles data access for user attempts and spaced repetition schedules."""
    
    def __init__(self, db: Session):
        self.db = db
        # Hardcoding a user_id for now since auth isn't fully implemented
        self.current_user_id = 1 

    def store_attempt(self, problem_id: int, is_solved: bool, time_spent_minutes: int, hint_level_used: int = 0):
        """Stores a new attempt in the database."""
        attempt = Attempt(
            user_id=self.current_user_id,
            problem_id=problem_id,
            is_solved=is_solved,
            hint_level_used=hint_level_used,
            time_spent_minutes=time_spent_minutes,
            attempted_at=datetime.utcnow()
        )
        self.db.add(attempt)
        self.db.commit()
        logger.info(f"Stored attempt for problem {problem_id}")

    def update_sm2_progress(self, problem_id: int, interval_days: int, repetitions: int, ease_factor: float):
        """Upserts SM-2 metrics into the ReviewSchedule table for a specific problem."""
        schedule = self.db.query(ReviewSchedule).filter_by(
            user_id=self.current_user_id, problem_id=problem_id
        ).first()

        next_review = datetime.utcnow() + timedelta(days=interval_days)

        if schedule:
            schedule.interval_days = interval_days
            schedule.repetitions = repetitions
            schedule.ease_factor = ease_factor
            schedule.next_review_date = next_review
        else:
            schedule = ReviewSchedule(
                user_id=self.current_user_id,
                problem_id=problem_id,
                interval_days=interval_days,
                repetitions=repetitions,
                ease_factor=ease_factor,
                next_review_date=next_review
            )
            self.db.add(schedule)
        self.db.commit()

    def get_solved_count(self) -> int:
        """Computes total successfully solved problems."""
        return self.db.query(Attempt).filter_by(
            user_id=self.current_user_id, is_solved=True
        ).count()

    def get_accuracy(self) -> float:
        """Computes overall accuracy percentage."""
        total = self.db.query(Attempt).filter_by(user_id=self.current_user_id).count()
        if total == 0: 
            return 0.0
        correct = self.get_solved_count()
        return round((correct / total) * 100, 2)

    def get_mastered_topics(self) -> int:
        """Counts topics with an SM-2 interval_days > 21 days (arbitrary mastery threshold)."""
        result = self.db.query(func.count(func.distinct(Problem.topic)))\
            .join(ReviewSchedule, ReviewSchedule.problem_id == Problem.id)\
            .filter(
                ReviewSchedule.user_id == self.current_user_id,
                ReviewSchedule.interval_days > 21
            ).scalar()
        return result or 0

    def get_weak_topics(self) -> list[str]:
        """
        Computes weak topics by joining Attempt and Problem.
        Calculates the average correctness per topic and returns the lowest 3.
        """
        results = self.db.query(
            Problem.topic,
            func.avg(func.cast(Attempt.is_solved, Integer)).label('accuracy')
        ).join(Attempt, Attempt.problem_id == Problem.id)\
         .filter(Attempt.user_id == self.current_user_id)\
         .group_by(Problem.topic)\
         .order_by('accuracy')\
         .limit(3).all()
         
        return [row[0] for row in results] if results else []
    
    def get_topics_due_for_review(self) -> list[str]:
        """Finds topics where next_review_date is in the past."""
        now = datetime.utcnow()
        results = self.db.query(Problem.topic)\
            .join(ReviewSchedule, ReviewSchedule.problem_id == Problem.id)\
            .filter(
                ReviewSchedule.user_id == self.current_user_id,
                ReviewSchedule.next_review_date <= now
            ).distinct().all()
        return [r[0] for r in results] if results else []