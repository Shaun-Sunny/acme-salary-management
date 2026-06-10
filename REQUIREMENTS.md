# Requirements Document — ACME Salary Management System

## Goal
Replace Excel-based salary management for ACME org's 10,000-employee HR team with a 
web application that enables structured data management, salary change tracking, and 
analytical querying across departments, countries, and pay bands.

## User Persona
**HR Manager** — responsible for maintaining accurate compensation records across the 
organization. Needs to add and update employee records, record salary changes with 
reasons, and answer organizational questions like "what is the average salary in 
Engineering?" or "how many contractors do we have in the US?"

## In Scope
- Employee directory: create, view, edit, and deactivate employee records with fields 
  for name, email, department, country, job title, band (L1–L6), employment type, 
  status, base salary, and currency
- Salary change tracking: every salary update records the previous value, new value, 
  reason, and who made the change
- Audit log: HR Manager can view the full salary change history for any employee
- Search and filter: find employees by name, department, country, band, or status
- Analytics dashboard: salary aggregates by department, country, and band; headcount 
  breakdown; top earners list
- Bulk seed: system pre-loaded with 10,000 realistic employee records for demonstration
- CSV import: HR Manager can upload a CSV to bulk-add or update employees

## Deliberately Out of Scope
- **Payroll processing, tax calculation, payslips** — payroll execution is a separate 
  regulated domain with legal requirements per country; out of scope for this tool
- **Authentication and role-based access control** — single HR Manager persona for now; 
  adding auth before the core product is validated adds complexity without value
- **Multi-currency conversion** — salaries are stored and displayed in their native 
  currency; live FX conversion depends on external rate feeds and is a v2 concern
- **Email notifications and approval workflows** — salary changes in this version are 
  direct edits; a multi-step approval workflow requires org-specific process design
- **Cloud database (Postgres/MySQL)** — SQLite is sufficient for 10,000 records and 
  keeps the stack simple; migration to Postgres is a one-line config change when needed

## Success Criteria
- HR Manager can find any employee in under 3 seconds
- Salary changes are never lost — every update has a corresponding history record
- Analytics page answers the 5 most common compensation questions without custom queries
- A new developer can run the full stack locally in under 5 minutes using the README
