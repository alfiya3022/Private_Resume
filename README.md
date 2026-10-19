## Development Status

**Current database milestone:** E01 — Database Schema

**Foundation milestone:** E00 — Project Foundation

### E00 — Project Foundation

Implemented foundation:

- React, Vite, and Tailwind CSS frontend
- FastAPI backend with health endpoints
- PostgreSQL through Docker Compose with persistent storage
- Environment-based database configuration
- Frontend-to-backend development proxy
- Pytest backend tests
- Playwright browser integration test

E00 remains in progress until its required CI checks, documentation, QA records, pull request review, and merge into `main` are complete.

### E01 — Database Schema

Implemented work reported so far:

- SQLAlchemy ORM models and model tests
- Alembic migration configuration and migration files
- Additive migration for `skills`, `match_results`, and `project_skill_evidence`
- Migration command completed without a reported error
- Backend regression suite: 10 passed, 1 warning

The migration and test results have been reported by the developer. Post-migration data preservation, complete schema parity, and CI results must not be considered verified until evidence is recorded.

## Local Development

### PostgreSQL

From the repository root:

```powershell
docker compose up -d db
docker compose ps
```

The development database is exposed on `127.0.0.1:5433`.

### Backend

From `backend/`, activate the virtual environment and run:

```powershell
python -m uvicorn app.main:app --reload
```

API documentation: http://127.0.0.1:8000/docs

Health endpoints:

- `/api/health`
- `/api/health/db`

### Frontend

From `frontend/`:

```powershell
npm run dev
```

The frontend development server proxies `/api` requests to the local FastAPI server on port 8000.

### Testing

Run the frontend production build from `frontend/`:

```powershell
npm run build
```

Run the browser end-to-end test from `frontend/`:

```powershell
npm run test:e2e
```

Run backend tests from `backend/`:

```powershell
python -m pytest -v
```

The latest reported backend regression result is **10 passed, 1 warning**.

## Environment Variables

Create `.env` from `.env.example` and configure the local PostgreSQL credentials.

Never commit `.env`, database backups, or other secrets. `.env.example` must contain placeholder values only.
