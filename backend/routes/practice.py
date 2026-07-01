from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.connection import get_db # Use your existing DB dependency

from backend.repositories.problem_repository import ProblemRepository
from backend.repositories.progress_repository import ProgressRepository
from backend.services.practice_service import PracticeService
from backend.schemas.practice import ProblemResponse, SubmitRequest, SubmitResponse

router = APIRouter()

# Dependency Injection setup
def get_practice_service(db: Session = Depends(get_db)) -> PracticeService:
    problem_repo = ProblemRepository(db) # <-- Now requires db session
    progress_repo = ProgressRepository(db)
    return PracticeService(problem_repo, progress_repo)

@router.get("/problem") # Note: You may need to update the response_model in schemas to accept new fields
def get_practice_problem(service: PracticeService = Depends(get_practice_service)):
    problem = service.recommend_problem()
    if not problem:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No problems found in dataset.")
    return problem

@router.post("/submit", response_model=SubmitResponse)
def submit_practice_problem(request: SubmitRequest, service: PracticeService = Depends(get_practice_service)):
    try:
        return service.evaluate_submission(request)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))