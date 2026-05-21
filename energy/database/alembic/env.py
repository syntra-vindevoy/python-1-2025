"""Alembic environment.

Imports our `MetaData` so `alembic revision --autogenerate` works against
the schema in `schema.py`. The sqlalchemy.url is taken from alembic.ini
unless overridden by the ENERGY_DATABASE_URL env var (for Postgres /
test SQLite paths).
"""

import os
import sys
from logging.config import fileConfig
from pathlib import Path

from alembic import context
from sqlalchemy import engine_from_config, pool

# env.py lives at database/alembic/env.py so parents[2] is the project root.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from database.schema import metadata  # noqa: E402

config = context.config

env_url = os.environ.get("ENERGY_DATABASE_URL")
if env_url:
    config.set_main_option("sqlalchemy.url", env_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
