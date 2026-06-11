\# Trade-offs and Design Decisions



\## SQLite over PostgreSQL

\*\*Decision:\*\* Use SQLite for the database.  

\*\*Reasoning:\*\* SQLite is sufficient for 10,000 employee records with read-heavy workloads. 

It requires zero infrastructure, making local setup a single command. Migrating to 

PostgreSQL requires only a one-line connection string change in SQLAlchemy.  

\*\*Trade-off:\*\* No concurrent writes — acceptable for a single HR Manager persona.



\## Separate SalaryHistory Table

\*\*Decision:\*\* Store salary changes in a dedicated table rather than soft fields on Employee.  

\*\*Reasoning:\*\* A separate table supports full audit history (not just the last change), 

enables queries like "all salary changes in Q1", and keeps the Employee table clean.  

\*\*Trade-off:\*\* Slightly more complex update logic — worth it for auditability.



\## No Authentication

\*\*Decision:\*\* No login or role-based access control.  

\*\*Reasoning:\*\* Single user persona (HR Manager) at MVP stage. Adding auth before the 

core product is validated adds complexity without demonstrating value.  

\*\*Trade-off:\*\* Anyone with the URL can access all data — acceptable for an internal demo, 

not for production.



\## No Multi-Currency Conversion

\*\*Decision:\*\* Salaries stored and displayed in native currency, no conversion.  

\*\*Reasoning:\*\* Live FX conversion requires an external rate feed, introduces staleness 

risk, and adds complexity disproportionate to MVP value.  

\*\*Trade-off:\*\* HR cannot compare salaries across countries on an equal basis — flagged 

as a v2 feature.



\## React Query v4 over v5

\*\*Decision:\*\* Pin @tanstack/react-query to version 4.  

\*\*Reasoning:\*\* Version 5 introduced breaking API changes (keepPreviousData renamed, 

new import paths) that caused compatibility issues with the Vite + React 19 setup.  

\*\*Trade-off:\*\* Not on the latest version — acceptable given stability requirements.



\## Deactivation over Deletion

\*\*Decision:\*\* DELETE endpoint sets status=inactive rather than removing the record.  

\*\*Reasoning:\*\* Hard deletes destroy salary history and audit trails. Soft deletes 

preserve data integrity and allow reactivation if needed.  

\*\*Trade-off:\*\* Database grows over time — negligible at this scale.

