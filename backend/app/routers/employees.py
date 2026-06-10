from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.schemas.employee import EmployeeCreate, EmployeeUpdate, EmployeeResponse, SalaryHistoryResponse
from app.services import employee_service


router = APIRouter(tags=["employees"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[EmployeeResponse])
def list_employees(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=1000),
    search: str | None = None,
    department: str | None = None,
    country: str | None = None,
    band: str | None = None,
    status: str | None = None,
    db: Session = Depends(get_db),
):
    employees = employee_service.get_employees(
        db=db,
        skip=skip,
        limit=limit,
        search=search,
        department=department,
        country=country,
        band=band,
        status=status,
    )
    return employees


@router.get("/{employee_id}", response_model=EmployeeResponse)
def read_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = employee_service.get_employee(db=db, employee_id=employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@router.post("/", response_model=EmployeeResponse, status_code=201)
def create_employee(data: EmployeeCreate, db: Session = Depends(get_db)):
    return employee_service.create_employee(db=db, data=data)


@router.put("/{employee_id}", response_model=EmployeeResponse)
def update_employee(
    employee_id: int,
    data: EmployeeUpdate,
    db: Session = Depends(get_db),
):
    return employee_service.update_employee(db=db, employee_id=employee_id, data=data)


@router.delete("/{employee_id}", response_model=EmployeeResponse)
def deactivate_employee(employee_id: int, db: Session = Depends(get_db)):
    return employee_service.deactivate_employee(db=db, employee_id=employee_id)


@router.get("/{employee_id}/salary-history", response_model=list[SalaryHistoryResponse])
def read_salary_history(employee_id: int, db: Session = Depends(get_db)):
    return employee_service.get_salary_history(db=db, employee_id=employee_id)
