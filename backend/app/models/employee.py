from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    emp_id: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    department: Mapped[str] = mapped_column(String, nullable=False)
    country: Mapped[str] = mapped_column(String, nullable=False)
    job_title: Mapped[str] = mapped_column(String, nullable=False)
    band: Mapped[str] = mapped_column(String(2), nullable=False)
    employment_type: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)
    base_salary: Mapped[float] = mapped_column(Float, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    salary_history: Mapped[list[SalaryHistory]] = relationship(
        "SalaryHistory",
        back_populates="employee",
        cascade="all, delete-orphan",
    )


class SalaryHistory(Base):
    __tablename__ = "salary_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    changed_by: Mapped[str] = mapped_column(String, nullable=False)
    previous_salary: Mapped[float] = mapped_column(Float, nullable=False)
    new_salary: Mapped[float] = mapped_column(Float, nullable=False)
    reason: Mapped[str] = mapped_column(String, nullable=False)
    changed_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    employee: Mapped[Employee] = relationship("Employee", back_populates="salary_history")
