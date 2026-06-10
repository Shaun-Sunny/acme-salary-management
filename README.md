# Salary Management

This repository scaffolds a full-stack salary management application for ACME org with a FastAPI + SQLite backend and a React + Vite frontend.

## Backend Setup
1. Open a terminal in `salary-management/backend`.
2. Create and activate a virtual environment.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the API:
   ```bash
   uvicorn app.main:app --reload
   ```

The backend uses `salary.db` in the backend directory by default.

## Frontend Setup
1. Open a terminal in `salary-management/frontend`.
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the dev server:
   ```bash
   npm run dev
   ```

The frontend expects the API at `http://localhost:8000` by default. Set `VITE_API_URL` if you want to point it somewhere else.

## Project Notes
- This scaffold intentionally contains no business logic yet.
- Backend and frontend placeholder files are ready for the employee and analytics flows.
