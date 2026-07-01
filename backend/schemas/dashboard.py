from pydantic import BaseModel
from typing import List

class ProgressResponse(BaseModel):
    total_problems_solved: int
    accuracy_rate: float
    topics_mastered: int

class StudyPlanItem(BaseModel):
    topic: str
    recommended_problems: int
    priority: str

class StudyPlanResponse(BaseModel):
    plan: List[StudyPlanItem]