from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.employee import Employee, SalaryHistory
from app.schemas.employee import EmployeeCreate, EmployeeUpdate


def get_employees(
    db: Session,
    skip: int = 0,
    limit: int = 50,
    search: str | None = None,
    department: str | None = None,
    country: str | None = None,
    band: str | None = None,
    status: str | None = None,
) -> list[Employee]:
    query = db.query(Employee)
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (Employee.full_name.ilike(search_term)) |
            (Employee.email.ilike(search_term))
        )
    
    if department:
        query = query.filter(Employee.department == department)
    if country:
        query = query.filter(Employee.country == country)
    if band:
        query = query.filter(Employee.band == band)
    if status:
        query = query.filter(Employee.status == status)
    
    return query.offset(skip).limit(limit).all()


def get_employee(db: Session, employee_id: int) -> Employee | None:
    return db.query(Employee).filter(Employee.id == employee_id).first()


def create_employee(db: Session, data: EmployeeCreate) -> Employee:
    existing = db.query(Employee).filter(Employee.emp_id == data.emp_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="emp_id already exists")
    
    employee = Employee(**data.model_dump())
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee


def update_employee(db: Session, employee_id: int, data: EmployeeUpdate) -> Employee:
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    update_data = data.model_dump(exclude_unset=True)
    changed_by = update_data.pop("changed_by", "HR Manager")
    
    if "base_salary" in update_data and update_data["base_salary"] is not None:
        if update_data["base_salary"] != employee.base_salary:
            history = SalaryHistory(
                employee_id=employee.id,
                changed_by=changed_by,
                previous_salary=employee.base_salary,
                new_salary=update_data["base_salary"],
                reason="Salary adjustment",
            )
            db.add(history)
    
    for key, value in update_data.items():
        if value is not None:
            setattr(employee, key, value)
    
    db.commit()
    db.refresh(employee)
    return employee


def deactivate_employee(db: Session, employee_id: int) -> Employee:
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    employee.status = "inactive"
    db.commit()
    db.refresh(employee)
    return employee


def get_salary_history(db: Session, employee_id: int) -> list[SalaryHistory]:
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    return (
        db.query(SalaryHistory)
        .filter(SalaryHistory.employee_id == employee_id)
        .order_by(SalaryHistory.changed_at.desc())
        .all()
    )
