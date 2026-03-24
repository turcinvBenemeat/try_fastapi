import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import StaticPool

# Prefer explicit DATABASE_URL; in tests Compose may only set TEST_DATABASE_URL.
DATABASE_URL = (
    os.getenv("DATABASE_URL")
    or os.getenv("TEST_DATABASE_URL")
    or "sqlite:///./sql_app.db"
)

connect_args: dict = {}
engine_kwargs: dict = {}

if DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False
    # :memory: needs a single shared connection pool or each DB API connection
    # sees a different empty database ("no such table" / OperationalError).
    if DATABASE_URL in ("sqlite:///:memory:", "sqlite://") or ":memory:" in DATABASE_URL:
        engine_kwargs["poolclass"] = StaticPool

engine = create_engine(DATABASE_URL, connect_args=connect_args, **engine_kwargs)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
