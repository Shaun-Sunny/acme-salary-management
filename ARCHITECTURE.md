# Architecture Overview

## Tech Stack
- Backend: Python, FastAPI, SQLAlchemy, SQLite.
- Frontend: React with Vite.
- Shared API transport: HTTP JSON, with Axios on the frontend.

## Why These Choices
- FastAPI keeps the backend lightweight and makes it easy to add typed request and response models later.
- SQLite is enough for local development and scaffold validation because the requested application is a small internal system at this stage.
- SQLAlchemy gives the project a clear ORM layer for the employee and salary history tables.
- Vite provides a fast React development experience and a clean app shell for future screens.

## Folder Structure
- `backend/app/main.py`: FastAPI application entry point and CORS setup.
- `backend/app/database.py`: SQLAlchemy engine, session factory, and declarative base.
- `backend/app/models/employee.py`: ORM models for employees and salary history.
- `backend/app/schemas/employee.py`: Pydantic v2 schemas for create, update, and read operations.
- `backend/app/routers/`: API router placeholders for employees and analytics.
- `backend/app/services/`: Service-layer placeholders for business logic that will be added later.
- `frontend/src/api/client.js`: Shared Axios client with the backend base URL.
- `frontend/src/pages/`: Page placeholders for Employees and Analytics.
- `frontend/src/components/`: Reusable UI components, currently empty.

## Database Schema
### Employee
- `id`: primary key.
- `emp_id`: unique employee identifier.
- `full_name`: employee name.
- `email`: email address.
- `department`: department name.
- `country`: country of employment.
- `job_title`: role title.
- `band`: compensation band, limited to values like L1 through L6.
- `employment_type`: full-time or contractor.
- `status`: active or inactive.
- `base_salary`: numeric salary amount.
- `currency`: 3-character currency code.
- `created_at`: record creation timestamp.
- `updated_at`: last update timestamp.

### SalaryHistory
- `id`: primary key.
- `employee_id`: foreign key to `Employee`.
- `changed_by`: person or system that made the change.
- `previous_salary`: salary before the change.
- `new_salary`: salary after the change.
- `reason`: explanation for the change.
- `changed_at`: change timestamp.
