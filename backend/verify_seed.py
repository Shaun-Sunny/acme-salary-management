#!/usr/bin/env python
"""Verify seed data statistics."""
from sqlalchemy import func
from app.database import SessionLocal
from app.models.employee import Employee


db = SessionLocal()
try:
    total = db.query(func.count(Employee.id)).scalar()
    active = db.query(func.count(Employee.id)).filter(Employee.status == "active").scalar()
    inactive = db.query(func.count(Employee.id)).filter(Employee.status == "inactive").scalar()
    
    print("=" * 70)
    print("SEED DATA VERIFICATION")
    print("=" * 70)
    print(f"\nTotal employees: {total:,}")
    print(f"  Active: {active:,} ({active/total*100:.1f}%)")
    print(f"  Inactive: {inactive:,} ({inactive/total*100:.1f}%)")
    
    print("\nBy Band (active only):")
    band_dist = (
        db.query(Employee.band, func.count(Employee.id).label("count"))
        .filter(Employee.status == "active")
        .group_by(Employee.band)
        .order_by(Employee.band)
        .all()
    )
    for band, count in band_dist:
        print(f"  {band}: {count:,} ({count/active*100:.1f}%)")
    
    print("\nEmployment Type (active only):")
    emp_type_dist = (
        db.query(Employee.employment_type, func.count(Employee.id).label("count"))
        .filter(Employee.status == "active")
        .group_by(Employee.employment_type)
        .order_by(Employee.employment_type)
        .all()
    )
    for emp_type, count in emp_type_dist:
        print(f"  {emp_type}: {count:,} ({count/active*100:.1f}%)")
    
    print("\nBy Department (active only):")
    dept_dist = (
        db.query(Employee.department, func.count(Employee.id).label("count"))
        .filter(Employee.status == "active")
        .group_by(Employee.department)
        .order_by(Employee.department)
        .all()
    )
    for dept, count in dept_dist:
        print(f"  {dept}: {count:,} ({count/active*100:.1f}%)")
    
    print("\nBy Country (active only):")
    country_dist = (
        db.query(Employee.country, func.count(Employee.id).label("count"))
        .filter(Employee.status == "active")
        .group_by(Employee.country)
        .order_by(Employee.country)
        .all()
    )
    for country, count in country_dist:
        print(f"  {country}: {count:,} ({count/active*100:.1f}%)")
    
    print("\nSalary Range by Band (active only):")
    salary_stats = (
        db.query(
            Employee.band,
            func.min(Employee.base_salary).label("min"),
            func.avg(Employee.base_salary).label("avg"),
            func.max(Employee.base_salary).label("max"),
        )
        .filter(Employee.status == "active")
        .group_by(Employee.band)
        .order_by(Employee.band)
        .all()
    )
    for band, min_sal, avg_sal, max_sal in salary_stats:
        print(f"  {band}: ${min_sal:,.2f} → ${max_sal:,.2f} (avg: ${avg_sal:,.2f})")
    
    print("\nSample Employees:")
    samples = db.query(Employee).filter(Employee.status == "active").limit(5).all()
    for emp in samples:
        print(f"  {emp.emp_id}: {emp.full_name} | {emp.department} | {emp.band} | ${emp.base_salary:,.2f} {emp.currency}")
    
    print("\n" + "=" * 70)
    print("Seed data verification complete!")
    print("=" * 70)
finally:
    db.close()
