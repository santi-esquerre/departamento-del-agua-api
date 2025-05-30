"""Cambiar a timestamp with time zone

Revision ID: 002_timestamp_with_tz
Revises: 9ccd2c8ca70d
Create Date: 2025-05-28 13:40:00.000000

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "002_timestamp_with_tz"
down_revision = "9ccd2c8ca70d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Cambiar los tipos de columna a TIMESTAMP WITH TIME ZONE
    op.alter_column("archivo", "fecha_subida", type_=sa.TIMESTAMP(timezone=True))
    op.alter_column("archivo", "created_at", type_=sa.TIMESTAMP(timezone=True))
    op.alter_column("archivo", "updated_at", type_=sa.TIMESTAMP(timezone=True))

    op.alter_column("actividad", "created_at", type_=sa.TIMESTAMP(timezone=True))
    op.alter_column("actividad", "updated_at", type_=sa.TIMESTAMP(timezone=True))

    op.alter_column("equipamiento", "created_at", type_=sa.TIMESTAMP(timezone=True))
    op.alter_column("equipamiento", "updated_at", type_=sa.TIMESTAMP(timezone=True))

    op.alter_column(
        "equipamientoactividad", "created_at", type_=sa.TIMESTAMP(timezone=True)
    )

    op.alter_column("personal", "created_at", type_=sa.TIMESTAMP(timezone=True))
    op.alter_column("personal", "updated_at", type_=sa.TIMESTAMP(timezone=True))

    op.alter_column("personalproyecto", "created_at", type_=sa.TIMESTAMP(timezone=True))

    op.alter_column("proyecto", "created_at", type_=sa.TIMESTAMP(timezone=True))
    op.alter_column("proyecto", "updated_at", type_=sa.TIMESTAMP(timezone=True))

    op.alter_column("publicacion", "fecha_registro", type_=sa.TIMESTAMP(timezone=True))
    op.alter_column("publicacion", "created_at", type_=sa.TIMESTAMP(timezone=True))
    op.alter_column("publicacion", "updated_at", type_=sa.TIMESTAMP(timezone=True))


def downgrade() -> None:
    # Revertir los tipos de columna a TIMESTAMP WITHOUT TIME ZONE (o el tipo original)
    op.alter_column("archivo", "fecha_subida", type_=sa.DateTime())
    op.alter_column("archivo", "created_at", type_=sa.DateTime())
    op.alter_column("archivo", "updated_at", type_=sa.DateTime())

    op.alter_column("actividad", "created_at", type_=sa.DateTime())
    op.alter_column("actividad", "updated_at", type_=sa.DateTime())

    op.alter_column("equipamiento", "created_at", type_=sa.DateTime())
    op.alter_column("equipamiento", "updated_at", type_=sa.DateTime())

    op.alter_column("equipamientoactividad", "created_at", type_=sa.DateTime())

    op.alter_column("personal", "created_at", type_=sa.DateTime())
    op.alter_column("personal", "updated_at", type_=sa.DateTime())

    op.alter_column("personalproyecto", "created_at", type_=sa.DateTime())

    op.alter_column("proyecto", "created_at", type_=sa.DateTime())
    op.alter_column("proyecto", "updated_at", type_=sa.DateTime())

    op.alter_column("publicacion", "fecha_registro", type_=sa.DateTime())
    op.alter_column("publicacion", "created_at", type_=sa.DateTime())
    op.alter_column("publicacion", "updated_at", type_=sa.DateTime())
