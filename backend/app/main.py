import logging
from fastapi import FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.database import engine
logger = logging.getLogger(__name__)

app = FastAPI(
    title="PrivateResume API",
    description="Backend API for PrivateResume.",
    version="0.1.0",
)


@app.get("/api/health")
def health_check():
    return {"status": "ok"}


@app.get("/api/health/db")
def database_health_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {"status": "ok", "database": "connected"}

    except SQLAlchemyError:
        logger.exception("Database health check failed")

        raise HTTPException(
            status_code=503,
            detail="Database connection unavailable",
        )
