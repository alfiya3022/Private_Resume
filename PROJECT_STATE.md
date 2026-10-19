# PrivateResume — Project State

## Current Status

- Foundation milestone: E00 — Project Foundation
- Active implementation milestone: E01 — Database Schema
- Current branch: `feature/e01-database-schema`

E00 and E01 have separate completion gates. Work on E01 does not automatically mean E00 is complete.

## E00 — Project Foundation

### Implemented

- React, Vite, and Tailwind CSS frontend foundation.
- FastAPI backend with health endpoints.
- PostgreSQL through Docker Compose with persistent storage.
- Environment-based database configuration.
- Frontend-to-backend development proxy.
- Pytest backend tests.
- Playwright browser integration test configuration.

### Completion Requirements

- Verify the frontend production build.
- Verify the Playwright end-to-end test.
- Verify backend tests after final changes.
- Verify the real PostgreSQL health endpoint.
- Review environment-secret protection.
- Update manual and automation QA records with actual results.
- Configure and verify GitHub Actions CI.
- Review the complete Git diff.
- Commit and push the intended changes.
- Open and review a pull request into `main`.
- Merge only after required checks and review are complete.

E00 remains in progress until its required completion gates are satisfied.

## E01 — Database Schema

### Implemented Work

- SQLAlchemy model definitions and model tests.
- Alembic configuration and migration files.
- Additive migration intended to introduce:
  - `skills`
  - `match_results`
  - `project_skill_evidence`
- Database backup created before schema work, according to the recorded project history.

### Verified Results

- Backend regression suite: **10 passed, 1 warning**, as reported by the developer.
- Alembic upgrade command completed without a reported error.
- Earlier model test run: 7 passed.

### Pending Verification

- Confirm the database is at the intended Alembic revision.
- Confirm the three new tables and their constraints match the ORM models.
- Confirm existing records and relationships remain intact after migration.
- Review migration rollback behavior where safe and appropriate.
- Complete QA evidence and documentation.
- Review the staged diff and ensure no secrets or database backups are included.
- Verify CI and complete the pull request workflow.

Do not describe pending checks as passed without supporting evidence.

## Database Safety Rules

- Preserve existing user and application data.
- Use additive migrations when compatible with the existing schema.
- Do not drop or replace the legacy `resume_validations` table as part of E01.
- Keep database backups out of Git.
- Do not rewrite historical resume snapshots when candidate profile data changes.
- Preserve user ownership and foreign-key relationships.
- Do not mark a migration as fully verified based on a successful command alone.

## Known Scope Limitations

- The frontend foundation is not the final product UI.
- Authentication and resume-related workflows are not considered complete solely because ORM models exist.
- Local test success does not establish that GitHub Actions CI, pull request review, or merge is complete.

## Next Step

Finish the E01 schema and data-preservation review, update QA evidence, and review the Git diff before committing.

Continue to track E00 completion requirements independently. Do not mark either milestone complete until its own required checks and review gates are satisfied.
