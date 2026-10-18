# PrivateResume

A privacy-first, local-first resume tailoring and job application management platform.

## Technology

- Frontend: React, Vite, JavaScript, Tailwind CSS
- Backend: Python, FastAPI
- Database: PostgreSQL
- Local AI runtime: Ollama

## Architecture

The React frontend communicates with the FastAPI backend over HTTP.
The backend owns business logic and communicates with the database and
other approved local services. The frontend does not access PostgreSQL
or Ollama directly.

## Development

Frontend setup instructions will be maintained here as the development
environment is established.

## Project status

See [PROJECT_STATE.md](PROJECT_STATE.md) for verified progress.
