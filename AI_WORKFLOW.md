\# AI Workflow — ACME Salary Management



\## Tools Used

\- \*\*GitHub Copilot (Agent Mode)\*\* — primary code generation tool used throughout

\- \*\*Claude (Anthropic)\*\* — used for planning, prompt engineering, architecture decisions, 

&#x20; and reviewing Copilot output at each step



\## How AI Was Used



\### Planning Phase

Claude was used to design the full architecture before writing any code — database schema, 

folder structure, API surface, and feature scope. This produced a clear blueprint that 

Copilot could execute against rather than generating speculatively.



\### Prompt Engineering

Each Copilot prompt was written by Claude with explicit file paths, function signatures, 

field names, and behavior expectations. Vague prompts were avoided intentionally — 

specificity reduced hallucinations and rework.



\### Code Generation

Copilot Agent mode generated all implementation files in sequence:

1\. Project scaffold and ORM models

2\. Employee CRUD service and router

3\. Analytics service and router

4\. Seed script (10,000 employees with realistic distributions)

5\. Unit tests (14 tests across employee and analytics services)

6\. Frontend: employee list, add/edit modal, salary history modal

7\. Analytics dashboard with Recharts visualizations

8\. Docker + nginx configuration



\### Review and Correction

After each Copilot generation step, output was reviewed before proceeding:

\- React Query v4/v5 API mismatch caught and corrected (keepPreviousData syntax)

\- Locale formatting bug caught and fixed (toLocaleString → toLocaleString('en-US'))

\- Docker networking issue diagnosed and fixed (nginx proxy path + VITE\_API\_URL)

\- Copilot context overflow errors handled by starting fresh sessions per feature



\### What Was Not AI-Generated

\- REQUIREMENTS.md content (written deliberately, then improved via prompted rewrite)

\- Architecture decisions (SQLite choice, audit log as separate table, no auth rationale)

\- Commit message strategy and sequencing

\- This document



\## Key Insight

AI tools are most effective when the engineer maintains a clear mental model of the 

system and uses AI to execute against it — not to think for them. Every generated file 

was understood before being committed.

