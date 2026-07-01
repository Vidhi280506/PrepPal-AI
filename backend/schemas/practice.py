from pydantic import BaseModel
from typing import Optional, Dict

class ProblemResponse(BaseModel):
    id: int
    question: str
    options: Optional[Dict[str, str]] = None
    topic: str
    difficulty: str
    
    class Config:
        from_attributes = True # Allows Pydantic to read from your existing SQLAlchemy models

class SubmitRequest(BaseModel):
    problem_id: int
    user_answer: str
    time_taken_seconds: int

class SubmitResponse(BaseModel):
    correct: bool
    correct_answer: str
    explanation: str
    new_sm2_interval: int