import random
from datetime import datetime

from faker import Faker

from app.database import SessionLocal, Base, engine
from app.models.employee import Employee, SalaryHistory


DEPARTMENTS = [
    "Engineering",
    "Product",
    "Sales",
    "Marketing",
    "Finance",
    "HR",
    "Operations",
    "Legal",
]

COUNTRIES = [
    ("United States", "USD"),
    ("United Kingdom", "GBP"),
    ("India", "INR"),
    ("Germany", "EUR"),
    ("United Arab Emirates", "AED"),
]

BANDS = ["L1", "L2", "L3", "L4", "L5", "L6"]

EMPLOYMENT_TYPES = ["full-time", "contractor"]

BAND_WEIGHTS = {
    "L1": 0.20,
    "L2": 0.25,
    "L3": 0.25,
    "L4": 0.15,
    "L5": 0.10,
    "L6": 0.05,
}

SALARY_RANGES = {
    "L1": (30000, 50000),
    "L2": (50000, 75000),
    "L3": (75000, 110000),
    "L4": (110000, 150000),
    "L5": (150000, 200000),
    "L6": (200000, 350000),
}

EMPLOYMENT_TYPE_WEIGHTS = {"full-time": 0.80, "contractor": 0.20}

STATUS_WEIGHTS = {"active": 0.95, "inactive": 0.05}

BATCH_SIZE = 500
TOTAL_EMPLOYEES = 10000


def seed_database():
    random.seed(42)
    fake = Faker()
    Faker.seed(42)
    
    db = SessionLocal()
    try:
        db.query(SalaryHistory).delete()
        db.query(Employee).delete()
        db.commit()
        
        employees = []
        
        for i in range(1, TOTAL_EMPLOYEES + 1):
            emp_id = f"EMP{i:05d}"
            
            band = random.choices(
                list(BAND_WEIGHTS.keys()),
                weights=list(BAND_WEIGHTS.values()),
                k=1,
            )[0]
            
            employment_type = random.choices(
                list(EMPLOYMENT_TYPE_WEIGHTS.keys()),
                weights=list(EMPLOYMENT_TYPE_WEIGHTS.values()),
                k=1,
            )[0]
            
            status = random.choices(
                list(STATUS_WEIGHTS.keys()),
                weights=list(STATUS_WEIGHTS.values()),
                k=1,
            )[0]
            
            salary_min, salary_max = SALARY_RANGES[band]
            base_salary = round(random.uniform(salary_min, salary_max), 2)
            
            country, currency = random.choice(COUNTRIES)
            
            created_at = fake.date_time_between(start_date="-3y", end_date="now")
            updated_at = fake.date_time_between(start_date=created_at, end_date="now")
            
            employee = Employee(
                emp_id=emp_id,
                full_name=fake.name(),
                email=f"emp{i:05d}@acme.com",
                department=random.choice(DEPARTMENTS),
                country=country,
                job_title=fake.job()[:100],
                band=band,
                employment_type=employment_type,
                status=status,
                base_salary=base_salary,
                currency=currency,
                created_at=created_at,
                updated_at=updated_at,
            )
            employees.append(employee)
            
            if len(employees) % BATCH_SIZE == 0:
                db.bulk_save_objects(employees)
                db.commit()
                print(f"Seeded {len(employees)}/{TOTAL_EMPLOYEES} employees...")
                employees = []
        
        if employees:
            db.bulk_save_objects(employees)
            db.commit()
        
        print("Seeding complete.")
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
