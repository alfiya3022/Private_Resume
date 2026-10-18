
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import URL, create_engine

PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")

database_url = URL.create(
    drivername="postgresql+psycopg",
    username=os.environ["POSTGRES_USER"],
    password=os.environ["POSTGRES_PASSWORD"],
    host="127.0.0.1",
    port=5433,
    database=os.environ["POSTGRES_DB"],
)

engine = create_engine(database_url, pool_pre_ping=True)
