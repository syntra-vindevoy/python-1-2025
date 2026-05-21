"""Initial schema - all tables from database.schema.

Revision ID: 0001
Revises:
Create Date: 2026-05-21 00:00:00
"""

from alembic import op

from database.schema import metadata

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    metadata.create_all(bind=bind)


def downgrade() -> None:
    bind = op.get_bind()
    metadata.drop_all(bind=bind)
