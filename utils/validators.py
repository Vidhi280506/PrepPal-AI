"""
PrepPal AI — Input Validators
Sanitization and validation helpers used across services and API layers.
"""
import re
from typing import Optional
from utils.exceptions import ValidationError

# Allowed DSA topics
VALID_TOPICS = {
    "Arrays", "Strings", "Linked Lists", "Trees", "Graphs",
    "Dynamic Programming", "Backtracking", "Heaps",
    "Binary Search", "Sliding Window",
}

# Allowed difficulty levels
VALID_DIFFICULTIES = {"Easy", "Medium", "Hard"}

# Allowed experience levels
VALID_EXPERIENCE_LEVELS = {"beginner", "intermediate", "advanced"}

# Max lengths
MAX_NAME_LEN = 100
MAX_MESSAGE_LEN = 5000
MAX_CODE_LEN = 10_000
MAX_NOTES_LEN = 2_000


def validate_topic(topic: str) -> str:
    """Validate and return a normalized DSA topic name."""
    stripped = topic.strip()
    if stripped not in VALID_TOPICS:
        raise ValidationError(
            f"Invalid topic '{stripped}'. Must be one of: {sorted(VALID_TOPICS)}",
            field="topic"
        )
    return stripped


def validate_difficulty(difficulty: str) -> str:
    """Validate and return a normalized difficulty level."""
    stripped = difficulty.strip().capitalize()
    if stripped not in VALID_DIFFICULTIES:
        raise ValidationError(
            f"Invalid difficulty '{difficulty}'. Must be: Easy, Medium, or Hard",
            field="difficulty"
        )
    return stripped


def sanitize_text(text: str, max_len: int = MAX_MESSAGE_LEN, field: str = "text") -> str:
    """
    Sanitize free-text input:
    - Strip whitespace
    - Remove null bytes
    - Enforce max length
    """
    if not isinstance(text, str):
        raise ValidationError(f"{field} must be a string", field=field)
    cleaned = text.strip().replace("\x00", "")
    if len(cleaned) == 0:
        raise ValidationError(f"{field} cannot be empty", field=field)
    if len(cleaned) > max_len:
        raise ValidationError(
            f"{field} exceeds maximum length of {max_len} characters",
            field=field
        )
    return cleaned


def validate_positive_int(value: int, field: str = "id") -> int:
    """Validate that an integer is positive."""
    if not isinstance(value, int) or value <= 0:
        raise ValidationError(f"{field} must be a positive integer, got {value}", field=field)
    return value


def validate_user_name(name: str) -> str:
    """Validate a user display name."""
    cleaned = sanitize_text(name, max_len=MAX_NAME_LEN, field="name")
    # Only allow letters, spaces, hyphens, apostrophes
    if not re.match(r"^[\w\s'\-\.]+$", cleaned):
        raise ValidationError(
            "Name contains invalid characters. Use letters, spaces, hyphens, or apostrophes.",
            field="name"
        )
    return cleaned


def validate_hint_level(level: int) -> int:
    """Validate hint level is 0-3."""
    if not isinstance(level, int) or level < 0 or level > 3:
        raise ValidationError("hint_level must be 0, 1, 2, or 3", field="hint_level")
    return level


def validate_quality_score(score: Optional[int]) -> Optional[int]:
    """Validate quality score is None or 0-5."""
    if score is None:
        return None
    if not isinstance(score, int) or score < 0 or score > 5:
        raise ValidationError("quality_score must be 0-5 or null", field="quality_score")
    return score
