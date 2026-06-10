from statistics import median

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.employee import Employee


def get_salary_stats(db: Session) -> dict:
    active_employees = db.query(Employee).filter(Employee.status == "active").all()
    
    if not active_employees:
        return {
            "overall": {"avg": 0.0, "median": 0.0, "min": 0.0, "max": 0.0, "count": 0},
            "by_department": [],
            "by_country": [],
        }
    
    salaries = [emp.base_salary for emp in active_employees]
    overall_avg = sum(salaries) / len(salaries)
    overall_median = median(salaries)
    overall_min = min(salaries)
    overall_max = max(salaries)
    
    result = {
        "overall": {
            "avg": round(overall_avg, 2),
            "median": round(overall_median, 2),
            "min": overall_min,
            "max": overall_max,
            "count": len(active_employees),
        },
        "by_department": [],
        "by_country": [],
    }
    
    dept_stats = (
        db.query(
            Employee.department,
            func.avg(Employee.base_salary).label("avg"),
            func.min(Employee.base_salary).label("min"),
            func.max(Employee.base_salary).label("max"),
            func.count(Employee.id).label("count"),
        )
        .filter(Employee.status == "active")
        .group_by(Employee.department)
        .order_by(Employee.department)
        .all()
    )
    
    for dept, avg, min_sal, max_sal, count in dept_stats:
        result["by_department"].append(
            {
                "department": dept,
                "avg": round(avg, 2),
                "min": min_sal,
                "max": max_sal,
                "count": count,
            }
        )
    
    country_stats = (
        db.query(
            Employee.country,
            func.avg(Employee.base_salary).label("avg"),
            func.min(Employee.base_salary).label("min"),
            func.max(Employee.base_salary).label("max"),
            func.count(Employee.id).label("count"),
        )
        .filter(Employee.status == "active")
        .group_by(Employee.country)
        .order_by(Employee.country)
        .all()
    )
    
    for country, avg, min_sal, max_sal, count in country_stats:
        result["by_country"].append(
            {
                "country": country,
                "avg": round(avg, 2),
                "min": min_sal,
                "max": max_sal,
                "count": count,
            }
        )
    
    return result


def get_headcount(db: Session) -> dict:
    total_active = db.query(func.count(Employee.id)).filter(Employee.status == "active").scalar()
    
    dept_counts = (
        db.query(Employee.department, func.count(Employee.id).label("count"))
        .filter(Employee.status == "active")
        .group_by(Employee.department)
        .order_by(Employee.department)
        .all()
    )
    
    country_counts = (
        db.query(Employee.country, func.count(Employee.id).label("count"))
        .filter(Employee.status == "active")
        .group_by(Employee.country)
        .order_by(Employee.country)
        .all()
    )
    
    employment_counts = (
        db.query(
            Employee.employment_type, func.count(Employee.id).label("count")
        )
        .filter(Employee.status == "active")
        .group_by(Employee.employment_type)
        .order_by(Employee.employment_type)
        .all()
    )
    
    return {
        "total": total_active,
        "by_department": [
            {"department": dept, "count": count} for dept, count in dept_counts
        ],
        "by_country": [{"country": country, "count": count} for country, count in country_counts],
        "by_employment_type": [
            {"employment_type": emp_type, "count": count}
            for emp_type, count in employment_counts
        ],
    }


def get_band_distribution(db: Session) -> list[dict]:
    band_stats = (
        db.query(
            Employee.band,
            func.count(Employee.id).label("count"),
            func.avg(Employee.base_salary).label("avg_salary"),
            func.min(Employee.base_salary).label("min_salary"),
            func.max(Employee.base_salary).label("max_salary"),
        )
        .filter(Employee.status == "active")
        .group_by(Employee.band)
        .order_by(Employee.band)
        .all()
    )
    
    return [
        {
            "band": band,
            "count": count,
            "avg_salary": round(avg_salary, 2),
            "min_salary": min_salary,
            "max_salary": max_salary,
        }
        for band, count, avg_salary, min_salary, max_salary in band_stats
    ]


def get_top_earners(db: Session, limit: int = 10) -> list[Employee]:
    return (
        db.query(Employee)
        .filter(Employee.status == "active")
        .order_by(Employee.base_salary.desc())
        .limit(limit)
        .all()
    )
