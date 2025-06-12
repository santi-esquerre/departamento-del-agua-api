"""Merge timestamp-with-tz branches

Revision ID: 50f3b40ed684
Revises: 655d2ff3e5da, 003_tz_remaining
Create Date: 2025-06-12 15:49:52.156210

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = '50f3b40ed684'
down_revision = ('655d2ff3e5da', '003_tz_remaining')
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
