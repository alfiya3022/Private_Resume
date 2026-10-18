## Development Status

**Current epic:** E00 — Project Foundation

Implemented foundation:

- React, Vite, and Tailwind CSS frontend
- FastAPI backend with health endpoints
- PostgreSQL through Docker Compose with persistent storage
- Environment-based database configuration
- Frontend-to-backend development proxy
- Pytest backend tests
- Playwright browser integration test

The build, browser test, backend tests, and real database
health check must be executed successfully before being
recorded as verified.

E00 remains in progress until the required CI checks,
documentation, QA records, pull request review, and merge
into `main` are complete.

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

### Testing

Frontend build:

```powershell
npm run build
```

Browser end-to-end test:

```powershell
npm run test:e2e
```

Backend tests, from `backend/`:

```powershell
python -m pytest -v
```

The frontend development server proxies `/api` requests to
the local FastAPI server on port 8000.

## Environment Variables

Create `.env` from `.env.example` and configure the local
PostgreSQL credentials.

Never commit `.env` or other secrets. `.env.example` should
contain placeholder values only.

```

Review the existing README afterward so you don't duplicate sections. Keep its current product and architecture descriptions.

## `PROJECT_STATE.md`

Update the current state using this structure, retaining any additional project decisions already documented in your file:

<CodeBlock language="markdown" editable>
# PrivateResume — Project State

## Current Epic

E00 — Project Foundation

## Implemented

- React + Vite + Tailwind CSS frontend foundation.
- FastAPI backend with health endpoints.
- PostgreSQL 17 through Docker Compose.
- Persistent PostgreSQL volume.
- Environment-based database credentials.
- SQLAlchemy connection to PostgreSQL.
- Vite proxy for `/api` requests.
- Temporary frontend/backend integration screen.
- Pytest backend health tests.
- Playwright foundation integration test configuration.

## Verified Results

Record only commands actually executed and their results.

- Backend health tests: 3 passed.
- PostgreSQL container: healthy.
- PostgreSQL SQL smoke check: `SELECT 1` returned one row.
- Real FastAPI database health endpoint: confirmed by user.
- Frontend build: pending verification.
- Playwright end-to-end test: pending verification.

## Current Branch

feature/e00-project-foundation

## Pending E00 Work

- Execute the frontend production build and Playwright test.
- Re-run backend tests after the final changes.
- Review environment-secret protection.
- Update manual and automation QA records with actual results.
- Configure and verify GitHub Actions CI.
- Review the complete diff.
- Commit and push changes.
- Open a pull request, review it, and merge into `main`.

## Known Scope Limitations

- The current frontend is an integration screen, not the final product UI.
- Authentication and resume-related features are not implemented.
- CI, PR review, and merge are not complete until verified.

## Next Step

Complete foundation verification, documentation, CI, and the
E00 GitHub pull-request workflow before beginning the next epic.
```

Important: because you confirmed the earlier three Pytest tests passed and the real database health endpoint worked, those results can be recorded. Only mark the frontend checks passed after running them.

# 4. Review and create the Git checkpoint

From the repository root:

```powershell
cd "D:\Alfiya Placemenet Prep\Projects\Private_Resume"
git status --short --branch
git branch --show-current
git diff --check
git diff
```

Review the output. Make sure `.env`, `.venv`, `node_modules`, generated files, and secrets are not staged.

Stage the relevant changes:

```powershell
git add README.md PROJECT_STATE.md frontend/package.json frontend/package-lock.json frontend/playwright.config.js frontend/tests/foundation.spec.js
```

If you modified `frontend/vite.config.js`, `frontend/src/App.jsx`, `frontend/src/api.js`, or other tracked project files as part of this task, stage those too.

Review exactly what will be committed:

```powershell
git diff --cached --check
git diff --cached --stat
git diff --cached
```

If the staged changes look correct, create a focused commit:

```powershell
git commit -m "test: verify frontend and backend foundation"
git push -u origin feature/e00-project-foundation
```

If the branch already tracks the remote, ordinary `git push` is sufficient.

# 5. Finish the GitHub workflow

Once the push succeeds:

1. Open the repository on GitHub.
2. Create a pull request from `feature/e00-project-foundation` into `main`.
3. Review the changed files and confirm CI checks pass.
4. Merge only after the required checks and review are complete.

Do not merge just because the local tests pass; the E00 definition of done includes CI, documentation, QA records, and PR review.

---

## Final E00 checklist

{@body const tasks = [
"Frontend production build passes",
"Playwright integration test passes",
"All three backend tests pass after final changes",
"Real PostgreSQL health endpoint works",
"README.md and PROJECT_STATE.md are accurate",
"Manual and automation QA records are updated",
"Git diff is reviewed and changes are committed",
"Changes are pushed and GitHub Actions CI passes",
"Pull request is reviewed and merged into main"
]}
{@body const [done, setDone] = DIL.useState([])}
<box border radius="xl" padding={3} gap={3}>
<row align="center" justify="between">
<title size="lg">E00 completion tracker</title>
<text color="secondary" size="sm">{done.length} of {tasks.length}</text>
</row>
<box background="surface-tertiary" height="6px" radius="full" clip>
<box background="surface-inverted" height="6px" radius="full" width={`${done.length / tasks.length * 100}%`} />
</box>
{#each tasks as task}
<checkbox key={task} checked={done.includes(task)} onChange={checked => setDone(prev => checked ? [...prev, task] : prev.filter(item => item !== task))}>{task}</checkbox>
{/each}
<text color="secondary" size="sm">This checklist is for tracking your progress in this response; it doesn't inspect your repository or verify test results automatically.</text>
</box>

**One important project rule:** E00 is still a foundation milestone. After these checks, we finish CI, QA records, and the PR workflow before moving into database models and Alembic migrations. No jumping ahead. 💪
