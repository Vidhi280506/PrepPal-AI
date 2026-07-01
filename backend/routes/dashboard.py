from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.connection import get_db # Use your existing DB dependency

from backend.repositories.progress_repository import ProgressRepository
from backend.services.dashboard_service import DashboardService
from backend.schemas.dashboard import ProgressResponse, StudyPlanResponse

router = APIRouter()

def get_dashboard_service(db: Session = Depends(get_db)) -> DashboardService:
    progress_repo = ProgressRepository(db)
    return DashboardService(progress_repo)

@router.get("/progress", response_model=ProgressResponse)
def get_user_progress(service: DashboardService = Depends(get_dashboard_service)):
    return service.get_progress_metrics()

@router.get("/study-plan", response_model=StudyPlanResponse)
def get_study_plan(service: DashboardService = Depends(get_dashboard_service)):
    return service.get_study_plan()