from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# TODO: Import your existing DB dependency
# from database.connection import get_db 

from backend.services.practice_service import PracticeService
from backend.schemas.practice import ProblemResponse, SubmitRequest, SubmitResponse

router = APIRouter()

# Mock get_db until you link your existing one to keep it runnable
def get_db():
    yield None 

def get_practice_service(db: Session = Depends(get_db)) -> PracticeService:
    return PracticeService(db)

@router.get("/problem", response_model=ProblemResponse)
def get_practice_problem(service: PracticeService = Depends(get_practice_service)):
    problem = service.get_next_problem()
    if not problem:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No problems found.")
    return problem

@router.post("/submit", response_model=SubmitResponse)
def submit_practice_problem(request: SubmitRequest, service: PracticeService = Depends(get_practice_service)):
    try:
        return service.evaluate_submission(request)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))