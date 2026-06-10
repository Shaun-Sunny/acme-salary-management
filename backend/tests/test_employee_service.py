from datetime import datetime, timedelta, timezone

import pytest
from fastapi import HTTPException

from app.models.employee import SalaryHistory
from app.schemas.employee import EmployeeCreate, EmployeeUpdate
from app.services.employee_service import (
    create_employee,
    deactivate_employee,
    get_employee,
    get_salary_history,
    update_employee,
)


def test_create_employee_success(db):
    employee = create_employee(
        db=db,
        data=EmployeeCreate(
            emp_id="EMP00002",
            full_name="Bob Jones",
            email="bob@acme.com",
            department="Sales",
            country="United States",
            job_title="Sales Manager",
            band="L4",
            employment_type="full-time",
            status="active",
            base_salary=110000.0,
            currency="USD",
        ),
    )

    assert employee.emp_id == "EMP00002"
    assert employee.base_salary == 110000.0


def test_create_employee_duplicate_emp_id(db, sample_employee):
    with pytest.raises(HTTPException) as exc_info:
        create_employee(
            db=db,
            data=EmployeeCreate(
                emp_id=sample_employee.emp_id,
                full_name="Duplicate Employee",
                email="duplicate@acme.com",
                department="Engineering",
                country="United States",
                job_title="Engineer",
                band="L3",
                employment_type="full-time",
                status="active",
                base_salary=90000.0,
                currency="USD",
            ),
        )

    assert exc_info.value.status_code == 400


def test_get_employee_found(db, sample_employee):
    employee = get_employee(db=db, employee_id=sample_employee.id)

    assert employee is not None
    assert employee.full_name == "Alice Smith"


def test_get_employee_not_found(db):
    assert get_employee(db=db, employee_id=99999) is None


def test_update_employee_salary_creates_history(db, sample_employee):
    updated_employee = update_employee(
        db=db,
        employee_id=sample_employee.id,
        data=EmployeeUpdate(base_salary=100000.0, changed_by="promotion"),
    )

    history_records = db.query(SalaryHistory).filter(SalaryHistory.employee_id == sample_employee.id).all()

    assert updated_employee.base_salary == 100000.0
    assert len(history_records) == 1
    assert history_records[0].previous_salary == 90000.0
    assert history_records[0].new_salary == 100000.0


def test_update_employee_non_salary_field_no_history(db, sample_employee):
    updated_employee = update_employee(
        db=db,
        employee_id=sample_employee.id,
        data=EmployeeUpdate(job_title="Senior Engineer"),
    )

    history_records = db.query(SalaryHistory).filter(SalaryHistory.employee_id == sample_employee.id).all()

    assert updated_employee.job_title == "Senior Engineer"
    assert history_records == []


def test_deactivate_employee(db, sample_employee):
    updated_employee = deactivate_employee(db=db, employee_id=sample_employee.id)

    assert updated_employee.status == "inactive"


def test_deactivate_employee_not_found(db):
    with pytest.raises(HTTPException) as exc_info:
        deactivate_employee(db=db, employee_id=99999)

    assert exc_info.value.status_code == 404


def test_get_salary_history_ordered(db, sample_employee):
    older = SalaryHistory(
        employee_id=sample_employee.id,
        changed_by="HR Manager",
        previous_salary=80000.0,
        new_salary=90000.0,
        reason="Adjustment",
        changed_at=datetime.now(timezone.utc) - timedelta(days=1),
    )
    newer = SalaryHistory(
        employee_id=sample_employee.id,
        changed_by="HR Manager",
        previous_salary=90000.0,
        new_salary=100000.0,
        reason="Promotion",
        changed_at=datetime.now(timezone.utc),
    )
    db.add_all([older, newer])
    db.commit()

    history_records = get_salary_history(db=db, employee_id=sample_employee.id)

    assert len(history_records) == 2
    assert history_records[0].changed_at >= history_records[1].changed_at
