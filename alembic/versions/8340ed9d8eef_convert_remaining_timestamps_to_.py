"""convert_remaining_timestamps_to_timezone_aware

Revision ID: 8340ed9d8eef
Revises: 50f3b40ed684
Create Date: 2025-06-12 13:01:44.081732

"""

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = "8340ed9d8eef"
down_revision = "50f3b40ed684"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Convertir los campos restantes de tipo TIMESTAMP WITHOUT TIME ZONE a TIMESTAMP WITH TIME ZONE

    # Tabla admin (creada en una migración posterior a las migraciones de timezone)
    op.alter_column(
        "admin",
        "created_at",
        existing_type=sa.DateTime(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
    )

    # Tabla subscriber (creada en una migración posterior a las migraciones de timezone)
    op.alter_column(
        "subscriber",
        "created_at",
        existing_type=sa.DateTime(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
    )

    # Verificar que todas las demás columnas timestamp tengan timezone=True
    # La siguiente consulta SQL identifica cualquier columna de tipo timestamp sin timezone
    # que no se haya convertido en las migraciones anteriores o en esta migración

    # Ejecutar la consulta sólo para propósitos informativos en los logs
    op.execute(
        """
    SELECT table_name, column_name, data_type
    FROM information_schema.columns
    WHERE data_type = 'timestamp without time zone'
      AND table_schema = 'public'
    ORDER BY table_name, column_name;
    """
    )


def downgrade() -> None:
    # Revertir los campos a TIMESTAMP WITHOUT TIME ZONE

    # Tabla admin
    op.alter_column(
        "admin",
        "created_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=sa.DateTime(),
        existing_nullable=False,
    )

    # Tabla subscriber
    op.alter_column(
        "subscriber",
        "created_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=sa.DateTime(),
        existing_nullable=False,
    )
