from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# TODO: Import your existing DB dependency
# from database.connection import get_db 

from backend.services.dashboard_service import DashboardService
from backend.schemas.dashboard import ProgressResponse, StudyPlanResponse

router = APIRouter()

# Mock get_db
def get_db():
    yield None

def get_dashboard_service(db: Session = Depends(get_db)) -> DashboardService:
    return DashboardService(db)

@router.get("/progress", response_model=ProgressResponse)
def get_user_progress(service: DashboardService = Depends(get_dashboard_service)):
    return service.get_progress_metrics()

@router.get("/study-plan", response_model=StudyPlanResponse)
def get_study_plan(service: DashboardService = Depends(get_dashboard_service)):
    return service.get_study_plan()