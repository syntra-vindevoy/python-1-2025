"""Database layer for the energy app.

Holds the SQLAlchemy schema, the Alembic migration tree, and a small
populate-from-YAML helper. SQLite is the default URL so everything works
out of the box; flip the URL via the ENERGY_DATABASE_URL env var or
edit `alembic.ini` once Postgres is up.

Layout:
    schema.py                       all Tables on a single MetaData
    populate.py                     load YAML resources into the DB
    alembic.ini                     Alembic config (sqlalchemy.url)
    alembic/env.py                  Alembic env, imports metadata
    alembic/versions/0001_*.py      initial schema migration
"""

import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

_DEFAULT_DB_FILE = Path(__file__).resolve().parents[1] / "energy.db"
DEFAULT_SQLITE_URL = f"sqlite:///{_DEFAULT_DB_FILE}"


def database_url() -> str:
    return os.environ.get("ENERGY_DATABASE_URL", DEFAULT_SQLITE_URL)


def get_engine(url: str | None = None) -> Engine:
    return create_engine(url or database_url(), future=True)
