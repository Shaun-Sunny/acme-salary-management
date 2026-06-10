from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class EmployeeBase(BaseModel):
    emp_id: str
    full_name: str
    email: str
    department: str
    country: str
    job_title: str
    band: str
    employment_type: str
    status: str
    base_salary: float
    currency: str


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    emp_id: str | None = None
    full_name: str | None = None
    email: str | None = None
    department: str | None = None
    country: str | None = None
    job_title: str | None = None
    band: str | None = None
    employment_type: str | None = None
    status: str | None = None
    base_salary: float | None = None
    currency: str | None = None
    changed_by: str | None = None


class EmployeeResponse(EmployeeBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SalaryHistoryResponse(BaseModel):
    id: int
    employee_id: int
    changed_by: str
    previous_salary: float
    new_salary: float
    reason: str
    changed_at: datetime

    model_config = ConfigDict(from_attributes=True)
