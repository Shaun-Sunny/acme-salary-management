from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.schemas.employee import EmployeeResponse
from app.services import analytics_service


router = APIRouter(tags=["analytics"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/salary-stats")
def read_salary_stats(db: Session = Depends(get_db)):
    return analytics_service.get_salary_stats(db=db)


@router.get("/headcount")
def read_headcount(db: Session = Depends(get_db)):
    return analytics_service.get_headcount(db=db)


@router.get("/band-distribution")
def read_band_distribution(db: Session = Depends(get_db)):
    return analytics_service.get_band_distribution(db=db)


@router.get("/top-earners", response_model=list[EmployeeResponse])
def read_top_earners(
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return analytics_service.get_top_earners(db=db, limit=limit)
