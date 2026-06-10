from app.models.employee import Employee
from app.services.analytics_service import (
    get_band_distribution,
    get_headcount,
    get_salary_stats,
    get_top_earners,
)


def seed_employee(db, **overrides):
    defaults = {
        "emp_id": "EMP",
        "full_name": "Employee",
        "email": "employee@example.com",
        "department": "Engineering",
        "country": "United States",
        "job_title": "Engineer",
        "band": "L3",
        "employment_type": "full-time",
        "status": "active",
        "base_salary": 100000.0,
        "currency": "USD",
    }
    defaults.update(overrides)
    employee = Employee(**defaults)
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee


def test_get_salary_stats_returns_correct_structure(db):
    seed_employee(db, emp_id="EMP10001", email="a@example.com", base_salary=100000.0)
    seed_employee(db, emp_id="EMP10002", email="b@example.com", full_name="B", department="Sales", country="Canada", base_salary=120000.0)
    seed_employee(db, emp_id="EMP10003", email="c@example.com", full_name="C", department="Sales", country="Canada", base_salary=110000.0)

    result = get_salary_stats(db)

    assert set(result.keys()) == {"overall", "by_department", "by_country"}
    assert set(result["overall"].keys()) == {"avg", "median", "min", "max", "count"}


def test_get_salary_stats_only_counts_active(db):
    seed_employee(db, emp_id="EMP20001", email="active@example.com", base_salary=100000.0, status="active")
    seed_employee(db, emp_id="EMP20002", email="inactive@example.com", full_name="Inactive", base_salary=999999.0, status="inactive")

    result = get_salary_stats(db)

    assert result["overall"]["count"] == 1
    assert result["overall"]["max"] == 100000.0


def test_get_headcount_totals(db):
    seed_employee(db, emp_id="EMP30001", email="h1@example.com", base_salary=90000.0)
    seed_employee(db, emp_id="EMP30002", email="h2@example.com", full_name="Headcount 2", base_salary=95000.0)
    seed_employee(db, emp_id="EMP30003", email="h3@example.com", full_name="Headcount 3", base_salary=98000.0)

    result = get_headcount(db)

    assert result["total"] == 3


def test_get_band_distribution_ordered(db):
    seed_employee(db, emp_id="EMP40001", email="l1@example.com", band="L1", base_salary=70000.0)
    seed_employee(db, emp_id="EMP40002", email="l3@example.com", full_name="L3", band="L3", base_salary=110000.0)
    seed_employee(db, emp_id="EMP40003", email="l2@example.com", full_name="L2", band="L2", base_salary=90000.0)

    result = get_band_distribution(db)

    assert [entry["band"] for entry in result] == ["L1", "L2", "L3"]


def test_get_top_earners_returns_highest_first(db):
    seed_employee(db, emp_id="EMP50001", email="t1@example.com", base_salary=120000.0)
    seed_employee(db, emp_id="EMP50002", email="t2@example.com", full_name="Top 2", base_salary=150000.0)
    seed_employee(db, emp_id="EMP50003", email="t3@example.com", full_name="Top 3", base_salary=130000.0)
    seed_employee(db, emp_id="EMP50004", email="t4@example.com", full_name="Top 4", base_salary=140000.0)
    seed_employee(db, emp_id="EMP50005", email="t5@example.com", full_name="Top 5", base_salary=125000.0)

    result = get_top_earners(db)

    assert result[0].base_salary >= result[1].base_salary
