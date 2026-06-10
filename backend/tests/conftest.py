import sys
from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.database import Base
from app.models.employee import Employee


@pytest.fixture()
def db():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


@pytest.fixture()
def sample_employee(db):
    employee = Employee(
        emp_id="EMP00001",
        full_name="Alice Smith",
        email="alice@acme.com",
        department="Engineering",
        country="United States",
        job_title="Engineer",
        band="L3",
        employment_type="full-time",
        status="active",
        base_salary=90000.0,
        currency="USD",
    )
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee
