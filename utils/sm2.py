"""
PrepPal AI — SM-2 Spaced Repetition Algorithm
Pure Python implementation of the SuperMemo 2 (SM-2) algorithm.

Reference: https://www.supermemo.com/en/archives1990-2015/english/ol/sm2
"""
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Tuple


# SM-2 quality grades (0-5 scale)
QUALITY_BLACKOUT = 0      # complete blackout, wrong response
QUALITY_INCORRECT = 1     # incorrect, correct was easy to recall
QUALITY_INCORRECT_EASY = 2  # incorrect, but correct felt easy
QUALITY_CORRECT_HARD = 3  # correct with significant difficulty
QUALITY_CORRECT = 4       # correct with some hesitation
QUALITY_PERFECT = 5       # perfect immediate recall

MIN_EASE_FACTOR = 1.3
DEFAULT_EASE_FACTOR = 2.5


@dataclass
class SM2State:
    """State for the SM-2 algorithm for a single item."""
    interval_days: int = 1
    ease_factor: float = DEFAULT_EASE_FACTOR
    repetitions: int = 0
    next_review: datetime = None

    def __post_init__(self):
        if self.next_review is None:
            self.next_review = datetime.utcnow() + timedelta(days=self.interval_days)


def calculate_next_review(
    ease_factor: float,
    interval_days: int,
    repetitions: int,
    quality: int
) -> Tuple[int, float, int, datetime]:
    """
    Apply the SM-2 algorithm to compute the next review state.

    Args:
        ease_factor: Current ease factor (>= 1.3).
        interval_days: Current interval in days.
        repetitions: Number of successful repetitions so far.
        quality: Quality of response (0-5 scale).

    Returns:
        Tuple of (new_interval_days, new_ease_factor, new_repetitions, next_review_date).
    """
    if quality < 0 or quality > 5:
        raise ValueError(f"Quality must be 0-5, got {quality}")

    if quality >= 3:
        # Correct response — advance the interval
        if repetitions == 0:
            new_interval = 1
        elif repetitions == 1:
            new_interval = 6
        else:
            new_interval = round(interval_days * ease_factor)
        new_repetitions = repetitions + 1
    else:
        # Incorrect response — reset to beginning
        new_interval = 1
        new_repetitions = 0

    # Update ease factor using SM-2 formula
    new_ease_factor = ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    new_ease_factor = max(MIN_EASE_FACTOR, new_ease_factor)

    next_review = datetime.utcnow() + timedelta(days=new_interval)

    return new_interval, new_ease_factor, new_repetitions, next_review


def attempt_to_quality(is_solved: bool, hint_level: int, attempts: int) -> int:
    """
    Convert attempt outcome to SM-2 quality score.

    Args:
        is_solved: Whether the problem was solved.
        hint_level: Hint level used (0=none, 1/2/3=progressive).
        attempts: Number of attempts made.

    Returns:
        Quality score (0-5).
    """
    if not is_solved:
        return QUALITY_BLACKOUT if attempts >= 3 else QUALITY_INCORRECT

    if hint_level == 0:
        # Solved without hints
        return QUALITY_PERFECT if attempts == 1 else QUALITY_CORRECT
    elif hint_level == 1:
        return QUALITY_CORRECT
    elif hint_level == 2:
        return QUALITY_CORRECT_HARD
    else:
        # Used all 3 hints
        return QUALITY_INCORRECT_EASY


def get_mastery_level(repetitions: int, ease_factor: float) -> str:
    """
    Determine mastery level string from SM-2 state.

    Returns: 'new' | 'learning' | 'reviewing' | 'mastered'
    """
    if repetitions == 0:
        return "new"
    elif repetitions <= 2:
        return "learning"
    elif ease_factor < 2.0:
        return "reviewing"
    else:
        return "mastered"
