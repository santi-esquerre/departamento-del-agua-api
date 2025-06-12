"""Agregar zona a columnas restantes

Revision ID: 003_tz_remaining
Revises: 002_timestamp_with_tz
Create Date: 2025-06-12 15:00:00.000000
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "003_tz_remaining"
down_revision = "002_timestamp_with_tz"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Académico
    op.alter_column(
        "carrera",
        "created_at",
        existing_type=sa.DateTime(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
    )
    op.alter_column(
        "carrera",
        "updated_at",
        existing_type=sa.DateTime(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
    )
    op.alter_column(
        "materia",
        "created_at",
        existing_type=sa.DateTime(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
    )
    op.alter_column(
        "materia",
        "updated_at",
        existing_type=sa.DateTime(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
    )
    op.alter_column(
        "requisito",
        "created_at",
        existing_type=sa.DateTime(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
    )
    op.alter_column(
        "requisito",
        "updated_at",
        existing_type=sa.DateTime(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
    )

    # Tablas de relación
    op.alter_column(
        "servicioequipamiento",
        "created_at",
        existing_type=sa.DateTime(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
    )

    # Blog
    op.alter_column(
        "blogpost",
        "fecha_publicacion",
        existing_type=sa.DateTime(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
    )

    # Suscriptores
    op.alter_column(
        "subscriber",
        "created_at",
        existing_type=sa.DateTime(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
    )

    # Administradores
    op.alter_column(
        "admin",
        "created_at",
        existing_type=sa.DateTime(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
    )


def downgrade() -> None:
    # Académico
    op.alter_column(
        "carrera",
        "created_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=sa.DateTime(),
        existing_nullable=False,
    )
    op.alter_column(
        "carrera",
        "updated_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=sa.DateTime(),
        existing_nullable=False,
    )
    op.alter_column(
        "materia",
        "created_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=sa.DateTime(),
        existing_nullable=False,
    )
    op.alter_column(
        "materia",
        "updated_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=sa.DateTime(),
        existing_nullable=False,
    )
    op.alter_column(
        "requisito",
        "created_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=sa.DateTime(),
        existing_nullable=False,
    )
    op.alter_column(
        "requisito",
        "updated_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=sa.DateTime(),
        existing_nullable=False,
    )

    # Tablas de relación
    op.alter_column(
        "servicioequipamiento",
        "created_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=sa.DateTime(),
        existing_nullable=False,
    )

    # Blog
    op.alter_column(
        "blogpost",
        "fecha_publicacion",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=sa.DateTime(),
        existing_nullable=False,
    )

    # Suscriptores
    op.alter_column(
        "subscriber",
        "created_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=sa.DateTime(),
        existing_nullable=False,
    )

    # Administradores
    op.alter_column(
        "admin",
        "created_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=sa.DateTime(),
        existing_nullable=False,
    )
