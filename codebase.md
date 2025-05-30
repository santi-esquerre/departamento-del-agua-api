# .coverage

This is a binary file of the type: Binary

# .github/workflows/test.yml

```yml
name: Test FastAPI Backend

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: cenur
          POSTGRES_PASSWORD: cenur_pass
          POSTGRES_DB: cenur_test
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-asyncio pytest-cov httpx

      - name: Set up test environment
        run: |
          echo "DATABASE_URL=postgresql+psycopg2://cenur:cenur_pass@localhost:5432/cenur_test" > .env

      - name: Run tests
        run: |
          pytest -q

      - name: Generate coverage report
        run: |
          pytest --cov=app --cov-report=xml

      - name: Upload coverage report
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
          fail_ci_if_error: false

```

# .gitignore

```
__pycache__/
*.pyc
.env
pgdata/

```

# .pytest_cache/.gitignore

```
# Created by pytest automatically.
*

```

# .pytest_cache/CACHEDIR.TAG

```TAG
Signature: 8a477f597d28d172789f06886806bc55
# This file is a cache directory tag created by pytest.
# For information about cache directory tags, see:
#	https://bford.info/cachedir/spec.html

```

# .pytest_cache/README.md

```md
# pytest cache directory #

This directory contains data from the pytest's cache plugin,
which provides the `--lf` and `--ff` options, as well as the `cache` fixture.

**Do not** commit this to version control.

See [the docs](https://docs.pytest.org/en/stable/how-to/cache.html) for more information.

```

# .pytest_cache/v/cache/lastfailed

```
{
  "tests/routes/test_routes.py::TestClient": true,
  "tests/routes/test_routes.py::test_read_personal": true,
  "tests/routes/test_routes.py::test_read_proyectos": true,
  "tests/routes/test_routes.py::test_read_publicaciones": true,
  "tests/routes/test_routes.py::test_read_equipamiento": true,
  "tests/routes/test_routes.py::test_read_servicios": true,
  "tests/routes/test_routes.py::test_create_personal": true,
  "tests/routes/test_routes.py::test_update_personal": true,
  "tests/routes/test_routes.py::test_delete_personal": true,
  "tests/routes/test_routes.py::test_create_proyecto": true,
  "tests/routes/test_routes.py::test_proyecto_date_validation": true,
  "tests/routes/test_routes.py::test_create_servicio": true,
  "tests/routes/test_routes.py::test_tarifa_validation": true,
  "tests/test_basic.py::test_root": true
}
```

# .pytest_cache/v/cache/nodeids

```
[
  "tests/routes/test_personal_routes.py::test_create_and_get_personal",
  "tests/routes/test_personal_routes.py::test_create_personal_email_invalido",
  "tests/routes/test_personal_routes.py::test_delete_personal",
  "tests/routes/test_personal_routes.py::test_delete_personal_no_existente",
  "tests/routes/test_personal_routes.py::test_get_personal_no_existente",
  "tests/routes/test_personal_routes.py::test_list_personal",
  "tests/routes/test_personal_routes.py::test_update_personal",
  "tests/routes/test_personal_routes.py::test_update_personal_no_existente",
  "tests/routes/test_routes.py::test_create_personal",
  "tests/routes/test_routes.py::test_create_proyecto",
  "tests/routes/test_routes.py::test_create_servicio",
  "tests/routes/test_routes.py::test_delete_personal",
  "tests/routes/test_routes.py::test_proyecto_date_validation",
  "tests/routes/test_routes.py::test_read_equipamiento",
  "tests/routes/test_routes.py::test_read_personal",
  "tests/routes/test_routes.py::test_read_proyectos",
  "tests/routes/test_routes.py::test_read_publicaciones",
  "tests/routes/test_routes.py::test_read_servicios",
  "tests/routes/test_routes.py::test_tarifa_validation",
  "tests/routes/test_routes.py::test_update_personal",
  "tests/services/test_equipamiento_service.py::test_actualizar_equipamiento",
  "tests/services/test_equipamiento_service.py::test_asignar_servicio",
  "tests/services/test_equipamiento_service.py::test_borrar_equipamiento_con_asociaciones",
  "tests/services/test_equipamiento_service.py::test_borrar_equipamiento_sin_asociaciones",
  "tests/services/test_equipamiento_service.py::test_crear_equipamiento",
  "tests/services/test_equipamiento_service.py::test_listar_equipamientos",
  "tests/services/test_proyectos_service.py::test_actualizar_proyecto",
  "tests/services/test_proyectos_service.py::test_actualizar_proyecto_fecha_invalida",
  "tests/services/test_proyectos_service.py::test_crear_proyecto_fecha_fin_antes_de_inicio",
  "tests/services/test_proyectos_service.py::test_crear_proyecto_valido",
  "tests/services/test_proyectos_service.py::test_eliminar_proyecto",
  "tests/services/test_proyectos_service.py::test_eliminar_proyecto_no_existente",
  "tests/services/test_proyectos_service.py::test_listar_proyectos",
  "tests/services/test_proyectos_service.py::test_obtener_proyecto",
  "tests/services/test_proyectos_service.py::test_obtener_proyecto_no_existente",
  "tests/services/test_publicaciones_service.py::test_actualizar_publicacion",
  "tests/services/test_publicaciones_service.py::test_borrar_publicacion",
  "tests/services/test_publicaciones_service.py::test_crear_publicacion",
  "tests/services/test_publicaciones_service.py::test_listar_publicaciones_con_filtros",
  "tests/services/test_publicaciones_service.py::test_validacion_authors",
  "tests/services/test_servicios_service.py::test_actualizar_servicio",
  "tests/services/test_servicios_service.py::test_actualizar_servicio_tarifa_negativa",
  "tests/services/test_servicios_service.py::test_crear_servicio_tarifa_negativa_schema",
  "tests/services/test_servicios_service.py::test_crear_servicio_tarifa_negativa_service_logic",
  "tests/services/test_servicios_service.py::test_crear_servicio_valido",
  "tests/services/test_servicios_service.py::test_eliminar_servicio",
  "tests/services/test_servicios_service.py::test_listar_servicios",
  "tests/services/test_servicios_service.py::test_obtener_servicio",
  "tests/storage/test_local_repo.py::test_abrir_archivo_no_existente",
  "tests/storage/test_local_repo.py::test_eliminar_archivo_no_existente_no_error",
  "tests/storage/test_local_repo.py::test_guardar_abrir_eliminar_archivo",
  "tests/storage/test_local_repo.py::test_guardar_archivo_sin_extension",
  "tests/test_basic.py::test_root",
  "tests/test_minimal.py::test_async",
  "tests/test_minimal.py::test_sync",
  "tests/test_standalone_db.py::test_create_and_query"
]
```

# .pytest_cache/v/cache/stepwise

```
[]
```

# alembic.ini

```ini
[alembic]
script_location = alembic
# sqlalchemy.url se configurará desde env.py
# sqlalchemy.url = driver://user:pass@localhost/dbname

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = INFO
handlers = console

[logger_sqlalchemy]
level = INFO
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stdout,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %Y-%m-%d %H:%M:%S

```

# alembic/env.py

```py
import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Añadir el directorio raíz al PYTHONPATH para que alembic encuentre 'app'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Importar SQLModel después de ajustar el PYTHONPATH
from sqlmodel import SQLModel

# Importar los modelos para que se registren con SQLModel.metadata
# Primero importamos los modelos
import app.models

# Configuración de Alembic
config = context.config

# Obtener la URL de la base de datos del entorno
# Y convertirla de asyncpg a psycopg2 para que funcione con Alembic
db_url = os.environ.get("DATABASE_URL")
if not db_url:
    raise ValueError("No se ha configurado DATABASE_URL en el entorno")

# Reemplazar el driver asyncpg por psycopg2 para las migraciones
sync_url = db_url.replace("postgresql+asyncpg", "postgresql+psycopg2")
config.set_main_option("sqlalchemy.url", sync_url)

# Cargar configuración de logging si existe
if config.config_file_name:
    fileConfig(config.config_file_name)

# Configurar el target_metadata con SQLModel.metadata
target_metadata = SQLModel.metadata


def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section) or {},
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

```

# alembic/script.py.mako

```mako
"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade() -> None:
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    ${downgrades if downgrades else "pass"}

```

# alembic/versions/002_timestamp_with_tz.py

```py
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

```

# alembic/versions/9ccd2c8ca70d_initial_migration.py

```py
"""Initial migration

Revision ID: 9ccd2c8ca70d
Revises:
Create Date: 2024-05-28 13:40:00.000000

"""

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "9ccd2c8ca70d"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "actividad",
        sa.Column("id", sa.Integer(), nullable=True),
        sa.Column("tipo", sa.String(), nullable=True),
        sa.Column("descripcion", sa.String(), nullable=True),
        sa.Column("fecha", sa.Date(), nullable=True),
        sa.Column("resultado_url", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "archivo",
        sa.Column("id", sa.Integer(), nullable=True),
        sa.Column("nombre", sa.String(), nullable=False),
        sa.Column("ruta", sa.String(), nullable=False),
        sa.Column("tipo", sa.String(), nullable=True),
        sa.Column("tamano", sa.Integer(), nullable=True),
        sa.Column("fecha_subida", sa.DateTime(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "equipamiento",
        sa.Column("id", sa.Integer(), nullable=True),
        sa.Column("nombre", sa.String(), nullable=False),
        sa.Column("marca", sa.String(), nullable=True),
        sa.Column("modelo", sa.String(), nullable=True),
        sa.Column("n_serie", sa.String(), nullable=True),
        sa.Column("hoja_especificaciones_url", sa.String(), nullable=True),
        sa.Column("fecha_adquisicion", sa.Date(), nullable=True),
        sa.Column("estado", sa.String(), nullable=True),
        sa.Column("ubicacion", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "personal",
        sa.Column("id", sa.Integer(), nullable=True),
        sa.Column("nombre", sa.String(), nullable=False),
        sa.Column("cargo", sa.String(), nullable=True),
        sa.Column("descripcion", sa.String(), nullable=True),
        sa.Column("foto_url", sa.String(), nullable=True),
        sa.Column("cv_url", sa.String(), nullable=True),
        sa.Column("orcid", sa.String(), nullable=True),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("fecha_alta", sa.Date(), nullable=True),
        sa.Column("fecha_baja", sa.Date(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "proyecto",
        sa.Column("id", sa.Integer(), nullable=True),
        sa.Column("nombre", sa.String(), nullable=False),
        sa.Column("descripcion", sa.String(), nullable=True),
        sa.Column("fecha_inicio", sa.Date(), nullable=True),
        sa.Column("fecha_fin", sa.Date(), nullable=True),
        sa.Column("financiador", sa.String(), nullable=True),
        sa.Column("presupuesto", sa.Float(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "publicacion",
        sa.Column("id", sa.Integer(), nullable=True),
        sa.Column("titulo", sa.String(), nullable=False),
        sa.Column("cita_formateada", sa.String(), nullable=True),
        sa.Column("doi_url", sa.String(), nullable=True),
        sa.Column("enlace_pdf", sa.String(), nullable=True),
        sa.Column("anio", sa.Integer(), nullable=True),
        sa.Column("estado", sa.String(), nullable=True),
        sa.Column("fecha_registro", sa.DateTime(), nullable=False),
        sa.Column("authors", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "servicio",
        sa.Column("id", sa.Integer(), nullable=True),
        sa.Column("nombre", sa.String(), nullable=False),
        sa.Column("descripcion", sa.String(), nullable=True),
        sa.Column("publico_objetivo", sa.String(), nullable=True),
        sa.Column("tarifa", sa.Float(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "equipamientoactividad",
        sa.Column("equipamiento_id", sa.Integer(), nullable=False),
        sa.Column("actividad_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["actividad_id"],
            ["actividad.id"],
        ),
        sa.ForeignKeyConstraint(
            ["equipamiento_id"],
            ["equipamiento.id"],
        ),
        sa.PrimaryKeyConstraint("equipamiento_id", "actividad_id"),
    )
    op.create_table(
        "personalproyecto",
        sa.Column("personal_id", sa.Integer(), nullable=False),
        sa.Column("proyecto_id", sa.Integer(), nullable=False),
        sa.Column("rol", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["personal_id"],
            ["personal.id"],
        ),
        sa.ForeignKeyConstraint(
            ["proyecto_id"],
            ["proyecto.id"],
        ),
        sa.PrimaryKeyConstraint("personal_id", "proyecto_id"),
    )
    op.create_table(
        "servicioequipamiento",
        sa.Column("servicio_id", sa.Integer(), nullable=False),
        sa.Column("equipamiento_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["equipamiento_id"],
            ["equipamiento.id"],
        ),
        sa.ForeignKeyConstraint(
            ["servicio_id"],
            ["servicio.id"],
        ),
        sa.PrimaryKeyConstraint("servicio_id", "equipamiento_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("servicioequipamiento")
    op.drop_table("personalproyecto")
    op.drop_table("equipamientoactividad")
    op.drop_table("servicio")
    op.drop_table("publicacion")
    op.drop_table("proyecto")
    op.drop_table("personal")
    op.drop_table("equipamiento")
    op.drop_table("archivo")
    op.drop_table("actividad")
    # ### end Alembic commands ###

```

# alembic/versions/b110a17a7f53_change_publicacion_authors_to_jsonb.py

```py
"""change_publicacion_authors_to_jsonb

Revision ID: b110a17a7f53
Revises: 002_timestamp_with_tz
Create Date: 2025-05-29 10:00:00.000000

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = "b110a17a7f53"
down_revision = "002_timestamp_with_tz"  # Adjusted to the correct previous revision
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "publicacion",
        "authors",
        existing_type=sa.VARCHAR(),
        type_=postgresql.JSONB(astext_type=sa.Text()),
        existing_nullable=True,
        postgresql_using="authors::jsonb",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "publicacion",
        "authors",
        existing_type=postgresql.JSONB(astext_type=sa.Text()),
        type_=sa.VARCHAR(),
        existing_nullable=True,
        postgresql_using="authors::text",
    )
    # ### end Alembic commands ###

```

# app/__init__.py

```py
# app/__init__.py
# Este archivo asegura que 'app' sea reconocido como un módulo Python

```

# app/db.py

```py
from os import getenv
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker  # Corrected import
from sqlmodel import SQLModel

DATABASE_URL = getenv("DATABASE_URL")
if DATABASE_URL is None:  # Added check for DATABASE_URL
    raise ValueError("DATABASE_URL environment variable is not set")

# Only add connect_args for Postgres
if DATABASE_URL.startswith("postgresql"):
    connect_args = {"server_settings": {"timezone": "UTC"}}
else:
    connect_args = {}

async_engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True,
    connect_args=connect_args,
)

# Use async_sessionmaker for AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker

async_session_factory = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:  # Use the factory
        yield session


# al arrancar la app, sólo crea las tablas si es necesario:
async def init_db() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

```

# app/deps.py

```py
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import async_session_factory


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()

```

# app/main.py

```py
from fastapi import FastAPI
from .db import init_db

# Importamos los routers directamente desde sus módulos
from app.routes.archivos import router as archivos_router
from app.routes.personal import router as personal_router
from app.routes.publicaciones import router as publicaciones_router
from app.routes.proyectos import router as proyectos_router
from app.routes.equipamiento import router as equipamiento_router
from app.routes.servicios import router as servicios_router

# Configuración mejorada para Swagger
app = FastAPI(
    title="API Departamento del Agua",
    description="API para gestionar recursos del departamento del agua",
    version="0.1.1",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)


@app.on_event("startup")
async def on_startup():
    await init_db()


# Incluir routers de forma explícita
app.include_router(archivos_router)
app.include_router(personal_router)
app.include_router(publicaciones_router)
app.include_router(proyectos_router)
app.include_router(equipamiento_router)
app.include_router(servicios_router)


@app.get("/")
def root():
    return {"status": "ok"}

```

# app/models/__init__.py

```py
from .models import *

```

# app/models/models.py

```py
# app/models/models.py

from datetime import date, datetime, timezone
from typing import List, Optional
from sqlmodel import Field, JSON, Relationship, SQLModel
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Personal(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    cargo: Optional[str]
    descripcion: Optional[str]
    foto_url: Optional[str]
    cv_url: Optional[str]
    orcid: Optional[str]
    email: Optional[str]
    fecha_alta: Optional[date]
    fecha_baja: Optional[date]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    proyectos: List["PersonalProyecto"] = Relationship(back_populates="personal")


class Publicacion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str
    cita_formateada: Optional[str] = None
    doi_url: Optional[str] = None
    enlace_pdf: Optional[str] = None
    anio: Optional[int] = None
    estado: Optional[str] = None
    fecha_registro: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    authors: List[dict] = Field(
        sa_column=Column(JSON), default_factory=list
    )  # Use JSON for cross-db compatibility
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Proyecto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    descripcion: Optional[str]
    fecha_inicio: Optional[date]
    fecha_fin: Optional[date]
    financiador: Optional[str]
    presupuesto: Optional[float]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    personal: List["PersonalProyecto"] = Relationship(back_populates="proyecto")


class PersonalProyecto(SQLModel, table=True):
    personal_id: int = Field(foreign_key="personal.id", primary_key=True)
    proyecto_id: int = Field(foreign_key="proyecto.id", primary_key=True)
    rol: Optional[str]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    personal: "Personal" = Relationship(back_populates="proyectos")
    proyecto: "Proyecto" = Relationship(back_populates="personal")


class Actividad(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tipo: Optional[str]
    descripcion: Optional[str]
    fecha: Optional[date]
    resultado_url: Optional[str]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    equipamientos: List["EquipamientoActividad"] = Relationship(
        back_populates="actividad"
    )


class Equipamiento(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    marca: Optional[str]
    modelo: Optional[str]
    n_serie: Optional[str]
    hoja_especificaciones_url: Optional[str]
    fecha_adquisicion: Optional[date]
    estado: Optional[str]
    ubicacion: Optional[str]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    actividades: List["EquipamientoActividad"] = Relationship(
        back_populates="equipamiento"
    )
    servicios: List["ServicioEquipamiento"] = Relationship(
        back_populates="equipamiento"
    )


class EquipamientoActividad(SQLModel, table=True):
    equipamiento_id: int = Field(foreign_key="equipamiento.id", primary_key=True)
    actividad_id: int = Field(foreign_key="actividad.id", primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    equipamiento: "Equipamiento" = Relationship(back_populates="actividades")
    actividad: "Actividad" = Relationship(back_populates="equipamientos")


class Servicio(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    descripcion: Optional[str]
    publico_objetivo: Optional[str]
    tarifa: Optional[float]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    equipamientos: List["ServicioEquipamiento"] = Relationship(
        back_populates="servicio"
    )


class ServicioEquipamiento(SQLModel, table=True):
    servicio_id: int = Field(foreign_key="servicio.id", primary_key=True)
    equipamiento_id: int = Field(foreign_key="equipamiento.id", primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    servicio: "Servicio" = Relationship(back_populates="equipamientos")
    equipamiento: "Equipamiento" = Relationship(back_populates="servicios")


class Archivo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    ruta: str
    tipo: Optional[str]
    tamano: Optional[int]
    fecha_subida: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

```

# app/routes/__init__.py

```py
# Inicialización del paquete routes
from app.routes import (
    archivos,
    personal,
    publicaciones,
    proyectos,
    equipamiento,
    servicios,
)

```

# app/routes/archivos.py

```py
"""
Rutas para la gestión de archivos.
"""

from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File,
    HTTPException,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from typing import List

from app.storage import local_repo
from app.models.models import Archivo
from app.db import get_session
from app.services import archivos_service

router = APIRouter(prefix="/archivos", tags=["Archivos"])


@router.post("/upload", status_code=status.HTTP_201_CREATED, response_model=Archivo)
async def upload_file(
    file: UploadFile = File(...), db: AsyncSession = Depends(get_session)
):
    """
    Sube un archivo al servidor y lo registra en la base de datos.
    """
    if not file or not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se ha proporcionado un archivo válido",
        )

    ruta_guardado = None

    try:
        # Guardar el archivo físicamente y crear registro en la base de datos
        archivo_db = await archivos_service.guardar_archivo(db=db, file=file)
        return archivo_db
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al subir el archivo: {str(e)}",
        )


@router.get("/download/{file_id}")
async def download_file(file_id: int, db: AsyncSession = Depends(get_session)):
    """
    Descarga un archivo por su ID.
    Utiliza el servicio para obtener la información del archivo y local_repo para servirlo.
    """
    archivo = await archivos_service.obtener_archivo(db=db, aid=file_id)
    if not archivo:
        raise HTTPException(status_code=404, detail="Archivo no encontrado")

    # local_repo.abrir ahora es asíncrono y devuelve StreamingResponse
    return await local_repo.abrir(archivo.ruta)


@router.get("/files/", response_model=List[Archivo])
async def list_files(
    skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_session)
):
    """
    Lista todos los archivos almacenados.
    """
    archivos = await archivos_service.listar_archivos(db=db, offset=skip, limit=limit)
    return archivos


@router.delete("/files/{file_id}", response_model=Archivo)
async def delete_file_route(file_id: int, db: AsyncSession = Depends(get_session)):
    """
    Elimina un archivo por su ID, tanto de la base de datos como del almacenamiento.
    """
    archivo_a_eliminar = await archivos_service.obtener_archivo(db=db, aid=file_id)
    if not archivo_a_eliminar:
        raise HTTPException(status_code=404, detail="Archivo no encontrado")

    try:
        # Eliminar usando la función de servicio borrar_archivo
        await archivos_service.borrar_archivo(db=db, aid=file_id)
        return (
            archivo_a_eliminar  # Devolver los datos del registro de archivo eliminado
        )
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar el archivo: {str(e)}",
        )

```

# app/routes/equipamiento.py

```py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, update, delete
from typing import List, Optional
from datetime import datetime, timezone

from app.db import get_session
from app.models.models import (
    Equipamiento,
    Actividad,
    EquipamientoActividad,
    Servicio,
    ServicioEquipamiento,
)
from app.schemas.equipamiento import (
    EquipamientoCreate,
    EquipamientoRead,
    EquipamientoUpdate,
    EquipamientoActividadRead,
)
from app.routes.utils import not_found

router = APIRouter(prefix="/equipamiento", tags=["Equipamiento"])


@router.post("/", response_model=EquipamientoRead, status_code=status.HTTP_201_CREATED)
async def create_equipamiento(
    equipamiento: EquipamientoCreate, session: AsyncSession = Depends(get_session)
):
    """Crear un nuevo equipamiento"""
    now = datetime.now(timezone.utc)
    nuevo_equipamiento = Equipamiento(
        **equipamiento.dict(), created_at=now, updated_at=now
    )
    session.add(nuevo_equipamiento)
    await session.commit()
    await session.refresh(nuevo_equipamiento)
    return nuevo_equipamiento


@router.get("/", response_model=List[EquipamientoRead])
async def read_all_equipamiento(
    offset: int = 0, limit: int = 100, session: AsyncSession = Depends(get_session)
):
    """Obtener lista paginada de equipamiento"""
    query = select(Equipamiento).offset(offset).limit(limit)
    result = await session.execute(query)
    equipamiento_list = result.scalars().all()
    return equipamiento_list


@router.get("/{equipamiento_id}", response_model=EquipamientoRead)
async def read_equipamiento(
    equipamiento_id: int, session: AsyncSession = Depends(get_session)
):
    """Obtener un equipamiento por su ID"""
    query = select(Equipamiento).where(Equipamiento.id == equipamiento_id)
    result = await session.execute(query)
    equipamiento = result.scalar_one_or_none()

    if not equipamiento:
        not_found("Equipamiento")
        return  # Add return to satisfy type checker, though not_found raises HTTPException

    return equipamiento


@router.put("/{equipamiento_id}", response_model=EquipamientoRead)
async def update_equipamiento(
    equipamiento_id: int,
    equipamiento_update: EquipamientoUpdate,
    session: AsyncSession = Depends(get_session),
):
    """Actualizar un equipamiento"""
    query = select(Equipamiento).where(Equipamiento.id == equipamiento_id)
    result = await session.execute(query)
    equipamiento = result.scalar_one_or_none()

    if not equipamiento:
        not_found("Equipamiento")
        return

    # Actualizar todos los campos
    equipamiento_data = equipamiento_update.dict(exclude_unset=False, exclude_none=True)
    for key, value in equipamiento_data.items():
        setattr(equipamiento, key, value)

    equipamiento.updated_at = datetime.now(timezone.utc)

    session.add(equipamiento)
    await session.commit()
    await session.refresh(equipamiento)

    return equipamiento


@router.patch("/{equipamiento_id}", response_model=EquipamientoRead)
async def partial_update_equipamiento(
    equipamiento_id: int,
    equipamiento_update: EquipamientoUpdate,
    session: AsyncSession = Depends(get_session),
):
    """Actualizar parcialmente un equipamiento"""
    query = select(Equipamiento).where(Equipamiento.id == equipamiento_id)
    result = await session.execute(query)
    equipamiento = result.scalar_one_or_none()

    if not equipamiento:
        not_found("Equipamiento")
        return

    # Actualizar solo los campos proporcionados
    equipamiento_data = equipamiento_update.dict(exclude_unset=True, exclude_none=True)
    for key, value in equipamiento_data.items():
        setattr(equipamiento, key, value)

    equipamiento.updated_at = datetime.now(timezone.utc)

    session.add(equipamiento)
    await session.commit()
    await session.refresh(equipamiento)

    return equipamiento


@router.delete("/{equipamiento_id}", response_model=EquipamientoRead)
async def delete_equipamiento(
    equipamiento_id: int, session: AsyncSession = Depends(get_session)
):
    """Eliminar un equipamiento"""
    query = select(Equipamiento).where(Equipamiento.id == equipamiento_id)
    result = await session.execute(query)
    equipamiento = result.scalar_one_or_none()

    if not equipamiento:
        not_found("Equipamiento")
        return

    # Verificar si el equipamiento está asociado a actividades o servicios
    actividades_query = select(EquipamientoActividad).where(
        EquipamientoActividad.equipamiento_id == equipamiento_id
    )
    actividades_result = await session.execute(actividades_query)
    actividades_count = len(actividades_result.scalars().all())

    servicios_query = select(ServicioEquipamiento).where(
        ServicioEquipamiento.equipamiento_id == equipamiento_id
    )
    servicios_result = await session.execute(servicios_query)
    servicios_count = len(servicios_result.scalars().all())

    if actividades_count > 0 or servicios_count > 0:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"No se puede eliminar equipamiento con ID {equipamiento_id} porque está asociado a {actividades_count} actividades y {servicios_count} servicios",
        )

    await session.delete(equipamiento)
    await session.commit()

    return equipamiento


@router.get(
    "/{equipamiento_id}/actividades", response_model=List[EquipamientoActividadRead]
)
async def read_equipamiento_actividades(
    equipamiento_id: int, session: AsyncSession = Depends(get_session)
):
    """Obtener actividades vinculadas a un equipamiento"""
    # Verificar que el equipamiento existe
    equipamiento_query = select(Equipamiento).where(Equipamiento.id == equipamiento_id)
    equipamiento_result = await session.execute(equipamiento_query)
    equipamiento = equipamiento_result.scalar_one_or_none()

    if not equipamiento:
        not_found("Equipamiento")
        return

    # Obtener actividades relacionadas
    query = select(EquipamientoActividad).where(
        EquipamientoActividad.equipamiento_id == equipamiento_id
    )
    result = await session.execute(query)
    actividades = result.scalars().all()

    return actividades


@router.get("/{equipamiento_id}/servicios", response_model=List[dict])
async def read_equipamiento_servicios(
    equipamiento_id: int, session: AsyncSession = Depends(get_session)
):
    """Obtener servicios vinculados a un equipamiento"""
    # Verificar que el equipamiento existe
    equipamiento_query = select(Equipamiento).where(Equipamiento.id == equipamiento_id)
    equipamiento_result = await session.execute(equipamiento_query)
    equipamiento = equipamiento_result.scalar_one_or_none()

    if not equipamiento:
        not_found("Equipamiento")
        return

    # Obtener servicios relacionados
    servicios_query = (
        select(ServicioEquipamiento, Servicio)
        .join(Servicio, ServicioEquipamiento.servicio_id == Servicio.id)  # type: ignore
        .where(ServicioEquipamiento.equipamiento_id == equipamiento_id)
    )

    servicios_result = await session.execute(servicios_query)
    servicios_data = []

    for pivote, servicio in servicios_result:
        servicios_data.append(
            {
                "servicio_id": servicio.id,
                "nombre": servicio.nombre,
                "descripcion": servicio.descripcion,
                "created_at": pivote.created_at,
            }
        )

    return servicios_data


@router.post("/{equipamiento_id}/servicios", response_model=List[dict])
async def assign_equipamiento_servicios(
    equipamiento_id: int,
    servicio_ids: List[int],
    session: AsyncSession = Depends(get_session),
):
    """Asignar servicios a un equipamiento"""
    # Verificar que el equipamiento existe
    equipamiento_query = select(Equipamiento).where(Equipamiento.id == equipamiento_id)
    equipamiento_result = await session.execute(equipamiento_query)
    equipamiento = equipamiento_result.scalar_one_or_none()

    if not equipamiento:
        not_found("Equipamiento")
        return

    # Verificar que los servicios existen
    for servicio_id in servicio_ids:
        servicio_query = select(Servicio).where(Servicio.id == servicio_id)
        servicio_result = await session.execute(servicio_query)
        servicio = servicio_result.scalar_one_or_none()

        if not servicio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Servicio con ID {servicio_id} no encontrado",
            )

    # Crear registros en la tabla pivote
    now = datetime.now(timezone.utc)

    for servicio_id in servicio_ids:
        # Verificar si la relación ya existe
        relation_query = select(ServicioEquipamiento).where(
            ServicioEquipamiento.equipamiento_id == equipamiento_id,
            ServicioEquipamiento.servicio_id == servicio_id,
        )
        relation_result = await session.execute(relation_query)
        existing_relation = relation_result.scalar_one_or_none()

        if not existing_relation:
            # Crear nueva relación
            new_relation = ServicioEquipamiento(
                equipamiento_id=equipamiento_id, servicio_id=servicio_id, created_at=now
            )
            session.add(new_relation)

    await session.commit()

    # Devolver todos los servicios asociados
    return await read_equipamiento_servicios(equipamiento_id, session)

```

# app/routes/personal.py

```py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.deps import get_async_session
from app.services import personal_service as svc
from app.schemas.personal import (
    PersonalCreate,
    PersonalRead,
    PersonalUpdate,
    PersonalProyectoRead,
    PersonalProyectoCreate,
)
from app.routes.utils import not_found

router = APIRouter(prefix="/personal", tags=["Personal"])


@router.post("/", response_model=PersonalRead, status_code=status.HTTP_201_CREATED)
async def create_personal(
    personal: PersonalCreate, db: AsyncSession = Depends(get_async_session)
):
    """Crear un nuevo registro de personal"""
    try:
        return await svc.crear_personal(db, personal.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=List[PersonalRead])
async def read_all_personal(
    offset: int = 0, limit: int = 100, db: AsyncSession = Depends(get_async_session)
):
    """Obtener lista paginada de personal"""
    return await svc.listar_personal(db, offset, limit)


@router.get("/{personal_id}", response_model=PersonalRead)
async def read_personal(
    personal_id: int, db: AsyncSession = Depends(get_async_session)
):
    """Obtener un registro de personal por su ID"""
    personal = await svc.obtener_personal(db, personal_id)

    if not personal:
        not_found("Personal")

    return personal


@router.put("/{personal_id}", response_model=PersonalRead)
async def update_personal(
    personal_id: int,
    personal_update: PersonalUpdate,
    db: AsyncSession = Depends(get_async_session),
):
    """Actualizar un registro de personal"""
    try:
        personal = await svc.actualizar_personal(
            db,
            personal_id,
            personal_update.model_dump(exclude_unset=False, exclude_none=True),
            partial=False,
        )

        if not personal:
            not_found("Personal")

        return personal
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch("/{personal_id}", response_model=PersonalRead)
async def partial_update_personal(
    personal_id: int,
    personal_update: PersonalUpdate,
    db: AsyncSession = Depends(get_async_session),
):
    """Actualizar parcialmente un registro de personal"""
    try:
        personal = await svc.actualizar_personal(
            db,
            personal_id,
            personal_update.model_dump(exclude_unset=True, exclude_none=True),
            partial=True,
        )

        if not personal:
            not_found("Personal")

        return personal
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{personal_id}", response_model=PersonalRead)
async def delete_personal(
    personal_id: int, db: AsyncSession = Depends(get_async_session)
):
    """Realizar soft delete de un registro de personal"""
    personal = await svc.borrar_personal(db, personal_id)

    if not personal:
        not_found("Personal")

    return personal


@router.get("/{personal_id}/proyectos", response_model=List[PersonalProyectoRead])
async def read_personal_proyectos(
    personal_id: int, db: AsyncSession = Depends(get_async_session)
):
    """Obtener proyectos vinculados a un personal"""
    # Verificar que el personal existe
    personal = await svc.obtener_personal(db, personal_id)

    if not personal:
        not_found("Personal")

    return await svc.listar_proyectos_personal(db, personal_id)


@router.post(
    "/{personal_id}/proyectos",
    response_model=List[PersonalProyectoRead],
    status_code=status.HTTP_201_CREATED,
)
async def create_personal_proyectos(
    personal_id: int,
    personal_proyectos: List[PersonalProyectoCreate],
    db: AsyncSession = Depends(get_async_session),
):
    """Vincular proyectos a un personal"""
    try:
        return await svc.vincular_proyectos(
            db, personal_id, [item.model_dump() for item in personal_proyectos]
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

```

# app/routes/proyectos.py

```py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.deps import get_async_session
from app.services import proyectos_service as svc
from app.schemas.proyectos import (
    ProyectoCreate,
    ProyectoRead,
    ProyectoUpdate,
    ProyectoPersonalCreate,
    ProyectoPersonalRead,
)
from app.routes.utils import not_found

router = APIRouter(prefix="/proyectos", tags=["Proyectos"])


@router.post("/", response_model=ProyectoRead, status_code=status.HTTP_201_CREATED)
async def create_proyecto(
    proyecto: ProyectoCreate, db: AsyncSession = Depends(get_async_session)
):
    """Crear un nuevo proyecto"""
    try:
        return await svc.crear_proyecto(db, proyecto.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=List[ProyectoRead])
async def read_all_proyectos(
    offset: int = 0, limit: int = 100, db: AsyncSession = Depends(get_async_session)
):
    """Obtener lista paginada de proyectos"""
    return await svc.listar_proyectos(db, offset, limit)


@router.get("/{proyecto_id}", response_model=ProyectoRead)
async def read_proyecto(
    proyecto_id: int, db: AsyncSession = Depends(get_async_session)
):
    """Obtener un proyecto por su ID"""
    proyecto = await svc.obtener_proyecto(db, proyecto_id)

    if not proyecto:
        not_found("Proyecto")

    return proyecto


@router.put("/{proyecto_id}", response_model=ProyectoRead)
async def update_proyecto(
    proyecto_id: int,
    proyecto_update: ProyectoUpdate,
    db: AsyncSession = Depends(get_async_session),
):
    """Actualizar un proyecto"""
    try:
        proyecto = await svc.actualizar_proyecto(
            db, proyecto_id, proyecto_update.model_dump()
        )

        if not proyecto:
            not_found("Proyecto")

        return proyecto
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{proyecto_id}")
async def delete_proyecto(
    proyecto_id: int, db: AsyncSession = Depends(get_async_session)
):
    """Eliminar un proyecto"""
    try:
        await svc.borrar_proyecto(db, proyecto_id)
        return {"message": f"Proyecto {proyecto_id} eliminado"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{proyecto_id}/personal", response_model=List[ProyectoPersonalRead])
async def read_personal_proyecto(
    proyecto_id: int, db: AsyncSession = Depends(get_async_session)
):
    """Obtener personal vinculado a un proyecto"""
    proyecto = await svc.obtener_proyecto(db, proyecto_id)

    if not proyecto:
        not_found("Proyecto")

    return await svc.listar_personal_proyecto(db, proyecto_id)


@router.post(
    "/{proyecto_id}/personal",
    response_model=List[ProyectoPersonalRead],
    status_code=status.HTTP_201_CREATED,
)
async def assign_personal(
    proyecto_id: int,
    personal_data: List[ProyectoPersonalCreate],
    db: AsyncSession = Depends(get_async_session),
):
    """Asignar personal a un proyecto"""
    try:
        return await svc.asignar_personal(
            db, proyecto_id, [item.model_dump() for item in personal_data]
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

```

# app/routes/publicaciones.py

```py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, update, delete
from typing import List, Optional
from datetime import datetime, timezone

from app.db import get_session
from app.models.models import Publicacion, Personal
from app.schemas.publicaciones import (
    PublicacionCreate,
    PublicacionRead,
    PublicacionUpdate,
    Author,
)
from app.routes.utils import not_found

router = APIRouter(prefix="/publicaciones", tags=["Publicaciones"])


async def validate_authors(authors: List[Author], session: AsyncSession):
    """Validar que los personal_id referenciados existen"""
    for author in authors:
        if author.personal_id:
            query = select(Personal).where(Personal.id == author.personal_id)
            result = await session.execute(query)
            personal = result.scalar_one_or_none()

            if not personal:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Personal con ID {author.personal_id} no encontrado",
                )


@router.post("/", response_model=PublicacionRead, status_code=status.HTTP_201_CREATED)
async def create_publicacion(
    publicacion: PublicacionCreate, session: AsyncSession = Depends(get_session)
):
    """Crear una nueva publicación"""
    # Validar que los personal_id referenciados existen
    if publicacion.authors:
        await validate_authors(publicacion.authors, session)

    now = datetime.now(timezone.utc)
    # Convertir el modelo Pydantic a diccionario y procesarlo para la BD
    publicacion_data = publicacion.dict()

    nueva_publicacion = Publicacion(
        **publicacion_data, fecha_registro=now, created_at=now, updated_at=now
    )

    session.add(nueva_publicacion)
    await session.commit()
    await session.refresh(nueva_publicacion)

    return nueva_publicacion


@router.get("/", response_model=List[PublicacionRead])
async def read_all_publicaciones(
    offset: int = 0,
    limit: int = 100,
    anio: Optional[int] = None,
    estado: Optional[str] = None,
    autor_id: Optional[int] = None,
    session: AsyncSession = Depends(get_session),
):
    """Obtener lista paginada de publicaciones con filtros opcionales"""
    query = select(Publicacion)

    # Aplicar filtros si se proporcionan
    if anio:
        query = query.where(Publicacion.anio == anio)

    if estado:
        query = query.where(Publicacion.estado == estado)

    # Filtrar por autor_id (esto requiere procesamiento adicional)
    results = await session.execute(query.offset(offset).limit(limit))
    publicaciones = results.scalars().all()

    # Si se especifició autor_id, filtrar manualmente las publicaciones
    if autor_id:
        filtered_publicaciones = []
        for pub in publicaciones:
            authors = pub.authors  # Now a list, not a JSON string
            if any(author.get("personal_id") == autor_id for author in authors):
                filtered_publicaciones.append(pub)
        return filtered_publicaciones

    return publicaciones


@router.get("/{publicacion_id}", response_model=PublicacionRead)
async def read_publicacion(
    publicacion_id: int, session: AsyncSession = Depends(get_session)
):
    """Obtener una publicación por su ID"""
    query = select(Publicacion).where(Publicacion.id == publicacion_id)
    result = await session.execute(query)
    publicacion = result.scalar_one_or_none()

    if not publicacion:
        not_found("Publicación")

    return publicacion


@router.put("/{publicacion_id}", response_model=PublicacionRead)
async def update_publicacion(
    publicacion_id: int,
    publicacion_update: PublicacionUpdate,
    session: AsyncSession = Depends(get_session),
):
    """Actualizar una publicación completa"""
    query = select(Publicacion).where(Publicacion.id == publicacion_id)
    result = await session.execute(query)
    publicacion = result.scalar_one_or_none()

    if not publicacion:
        not_found("Publicación")
        return  # Add return to satisfy type checker, though not_found raises HTTPException

    # Validar autores si se proporcionan
    if publicacion_update.authors:
        await validate_authors(publicacion_update.authors, session)

    # Actualizar la publicación
    publicacion_data = publicacion_update.dict(exclude_unset=False, exclude_none=True)
    for key, value in publicacion_data.items():
        setattr(publicacion, key, value)

    publicacion.updated_at = datetime.now(timezone.utc)

    session.add(publicacion)
    await session.commit()
    await session.refresh(publicacion)

    return publicacion


@router.patch("/{publicacion_id}", response_model=PublicacionRead)
async def partial_update_publicacion(
    publicacion_id: int,
    publicacion_update: PublicacionUpdate,
    session: AsyncSession = Depends(get_session),
):
    """Actualizar parcialmente una publicación"""
    query = select(Publicacion).where(Publicacion.id == publicacion_id)
    result = await session.execute(query)
    publicacion = result.scalar_one_or_none()

    if not publicacion:
        not_found("Publicación")
        return  # Add return to satisfy type checker, though not_found raises HTTPException

    # Validar autores si se proporcionan
    if publicacion_update.authors:
        await validate_authors(publicacion_update.authors, session)

    # Actualizar solo los campos proporcionados
    publicacion_data = publicacion_update.dict(exclude_unset=True, exclude_none=True)
    for key, value in publicacion_data.items():
        setattr(publicacion, key, value)

    publicacion.updated_at = datetime.now(timezone.utc)

    session.add(publicacion)
    await session.commit()
    await session.refresh(publicacion)

    return publicacion


@router.delete("/{publicacion_id}", response_model=PublicacionRead)
async def delete_publicacion(
    publicacion_id: int, session: AsyncSession = Depends(get_session)
):
    """Eliminar una publicación"""
    query = select(Publicacion).where(Publicacion.id == publicacion_id)
    result = await session.execute(query)
    publicacion = result.scalar_one_or_none()

    if not publicacion:
        not_found("Publicación")
        return  # Add return to satisfy type checker, though not_found raises HTTPException

    await session.delete(publicacion)
    await session.commit()

    # Para devolver la entidad eliminada
    return publicacion

```

# app/routes/servicios.py

```py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, update, delete
from typing import List, Optional
from datetime import datetime, timezone

from app.db import get_session
from app.models.models import Servicio, Equipamiento, ServicioEquipamiento
from app.schemas.servicios import ServicioCreate, ServicioRead, ServicioUpdate
from app.schemas.equipamiento import EquipamientoRead
from app.routes.utils import not_found

router = APIRouter(prefix="/servicios", tags=["Servicios"])


@router.post("/", response_model=ServicioRead, status_code=status.HTTP_201_CREATED)
async def create_servicio(
    servicio: ServicioCreate, session: AsyncSession = Depends(get_session)
):
    """Crear un nuevo servicio (requiere al menos un equipamiento asignado)"""
    # Verificar que los equipamientos existen
    if not servicio.equipamiento_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Se requiere al menos un equipamiento asignado al servicio",
        )

    for equip_id in servicio.equipamiento_ids:
        equip_query = select(Equipamiento).where(Equipamiento.id == equip_id)
        equip_result = await session.execute(equip_query)
        equipamiento = equip_result.scalar_one_or_none()

        if not equipamiento:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Equipamiento con ID {equip_id} no encontrado",
            )

    # Crear el servicio
    now = datetime.now(timezone.utc)
    servicio_data = servicio.dict(exclude={"equipamiento_ids"})
    nuevo_servicio = Servicio(**servicio_data, created_at=now, updated_at=now)

    session.add(nuevo_servicio)
    await session.commit()
    await session.refresh(nuevo_servicio)

    # Crear relaciones con equipamientos
    for equip_id in servicio.equipamiento_ids:
        # Verificar que `nuevo_servicio.id` no sea None antes de usarlo
        if nuevo_servicio.id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El servicio no tiene un ID válido",
            )

        # Crear la relación solo si el ID es válido
        relacion = ServicioEquipamiento(
            servicio_id=nuevo_servicio.id, equipamiento_id=equip_id, created_at=now
        )
        session.add(relacion)

    await session.commit()
    await session.refresh(nuevo_servicio)

    return nuevo_servicio


@router.get("/", response_model=List[ServicioRead])
async def read_all_servicios(
    offset: int = 0, limit: int = 100, session: AsyncSession = Depends(get_session)
):
    """Obtener lista paginada de servicios"""
    query = select(Servicio).offset(offset).limit(limit)
    result = await session.execute(query)
    servicios = result.scalars().all()
    return servicios


@router.get("/{servicio_id}", response_model=ServicioRead)
async def read_servicio(servicio_id: int, session: AsyncSession = Depends(get_session)):
    """Obtener un servicio por su ID"""
    query = select(Servicio).where(Servicio.id == servicio_id)
    result = await session.execute(query)
    servicio = result.scalar_one_or_none()

    if not servicio:
        not_found("Servicio")
        return  # Add return to satisfy type checker, though not_found raises HTTPException

    return servicio


@router.put("/{servicio_id}", response_model=ServicioRead)
async def update_servicio(
    servicio_id: int,
    servicio_update: ServicioUpdate,
    session: AsyncSession = Depends(get_session),
):
    """Actualizar un servicio"""
    query = select(Servicio).where(Servicio.id == servicio_id)
    result = await session.execute(query)
    servicio = result.scalar_one_or_none()

    if not servicio:
        not_found("Servicio")
        return  # Add return to satisfy type checker, though not_found raises HTTPException

    # Actualizar los campos básicos
    servicio_data = servicio_update.dict(
        exclude={"equipamiento_ids"}, exclude_unset=False, exclude_none=True
    )
    for key, value in servicio_data.items():
        setattr(servicio, key, value)

    servicio.updated_at = datetime.now(timezone.utc)

    # Si se proporciona equipamiento_ids, reemplazar el conjunto de equipamiento
    if servicio_update.equipamiento_ids is not None:
        # Verificar que los nuevos equipamientos existen
        for equip_id in servicio_update.equipamiento_ids:
            equip_query = select(Equipamiento).where(Equipamiento.id == equip_id)
            equip_result = await session.execute(equip_query)
            equipamiento = equip_result.scalar_one_or_none()

            if not equipamiento:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Equipamiento con ID {equip_id} no encontrado",
                )

        # Eliminar todas las relaciones existentes
        delete_query = delete(ServicioEquipamiento).where(
            ServicioEquipamiento.servicio_id == servicio_id  # type: ignore
        )
        await session.execute(delete_query)

        # Crear nuevas relaciones
        now = datetime.now(timezone.utc)
        for equip_id in servicio_update.equipamiento_ids:
            relacion = ServicioEquipamiento(
                servicio_id=servicio_id, equipamiento_id=equip_id, created_at=now
            )
            session.add(relacion)

    await session.commit()
    await session.refresh(servicio)

    return servicio


@router.patch("/{servicio_id}", response_model=ServicioRead)
async def partial_update_servicio(
    servicio_id: int,
    servicio_update: ServicioUpdate,
    session: AsyncSession = Depends(get_session),
):
    """Actualizar parcialmente un servicio"""
    query = select(Servicio).where(Servicio.id == servicio_id)
    result = await session.execute(query)
    servicio = result.scalar_one_or_none()

    if not servicio:
        not_found("Servicio")
        return  # Add return to satisfy type checker, though not_found raises HTTPException

    # Actualizar solo los campos proporcionados
    servicio_data = servicio_update.dict(
        exclude={"equipamiento_ids"}, exclude_unset=True, exclude_none=True
    )
    for key, value in servicio_data.items():
        setattr(servicio, key, value)

    servicio.updated_at = datetime.now(timezone.utc)

    # Si se proporciona equipamiento_ids, reemplazar el conjunto de equipamiento
    if servicio_update.equipamiento_ids is not None:
        # Verificar que los nuevos equipamientos existen
        for equip_id in servicio_update.equipamiento_ids:
            equip_query = select(Equipamiento).where(Equipamiento.id == equip_id)
            equip_result = await session.execute(equip_query)
            equipamiento = equip_result.scalar_one_or_none()

            if not equipamiento:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Equipamiento con ID {equip_id} no encontrado",
                )

        # Eliminar todas las relaciones existentes
        delete_query = delete(ServicioEquipamiento).where(
            ServicioEquipamiento.servicio_id == servicio_id  # type: ignore
        )
        await session.execute(delete_query)

        # Crear nuevas relaciones
        now = datetime.now(timezone.utc)
        for equip_id in servicio_update.equipamiento_ids:
            relacion = ServicioEquipamiento(
                servicio_id=servicio_id, equipamiento_id=equip_id, created_at=now
            )
            session.add(relacion)

    await session.commit()
    await session.refresh(servicio)

    return servicio


@router.delete("/{servicio_id}", response_model=ServicioRead)
async def delete_servicio(
    servicio_id: int, session: AsyncSession = Depends(get_session)
):
    """Eliminar un servicio"""
    query = select(Servicio).where(Servicio.id == servicio_id)
    result = await session.execute(query)
    servicio = result.scalar_one_or_none()

    if not servicio:
        not_found("Servicio")
        return  # Add return to satisfy type checker, though not_found raises HTTPException

    # Eliminar relaciones en tabla pivote
    delete_query = delete(ServicioEquipamiento).where(
        ServicioEquipamiento.servicio_id == servicio_id  # type: ignore
    )
    await session.execute(delete_query)

    # Eliminar el servicio
    await session.delete(servicio)
    await session.commit()

    return servicio


@router.get("/{servicio_id}/equipamiento", response_model=List[EquipamientoRead])
async def read_servicio_equipamiento(
    servicio_id: int, session: AsyncSession = Depends(get_session)
):
    """Obtener equipamiento vinculado a un servicio"""
    # Verificar que el servicio existe
    servicio_query = select(Servicio).where(Servicio.id == servicio_id)
    servicio_result = await session.execute(servicio_query)
    db_servicio = servicio_result.scalar_one_or_none()

    if not db_servicio:
        not_found("Servicio")
        return []

    # 1. Get ServicioEquipamiento links
    links_query = select(ServicioEquipamiento).where(
        ServicioEquipamiento.servicio_id == db_servicio.id
    )  # Use db_servicio.id
    links_result = await session.execute(links_query)
    servicio_equipamiento_links = links_result.scalars().all()

    if not servicio_equipamiento_links:
        return []

    # 2. Get equipamiento_ids
    equipamiento_ids = [
        link.equipamiento_id
        for link in servicio_equipamiento_links
        if link.equipamiento_id is not None
    ]

    if not equipamiento_ids:
        return []

    # 3. Fetch Equipamiento objects
    # Correct usage of in_ operator with SQLModel/SQLAlchemy
    equipos_query = select(Equipamiento).where(
        getattr(Equipamiento.id, "in_")(equipamiento_ids)
    )
    equipos_result = await session.execute(equipos_query)
    equipamientos = equipos_result.scalars().all()

    return equipamientos


@router.get(
    "/equipamiento/{equipamiento_id}/servicios", response_model=List[ServicioRead]
)
async def read_equipamiento_servicios(
    equipamiento_id: int, session: AsyncSession = Depends(get_session)
):
    """Obtener servicios vinculados a un equipamiento"""
    # Verificar que el equipamiento existe
    equipamiento_query = select(Equipamiento).where(Equipamiento.id == equipamiento_id)
    equipamiento_result = await session.execute(equipamiento_query)
    equipamiento = equipamiento_result.scalar_one_or_none()

    if not equipamiento:
        not_found("Equipamiento")
        return []  # Return empty list or raise error

    # Obtener servicios relacionados
    # Correct join condition for SQLAlchemy/SQLModel
    # 1. Get ServicioEquipamiento links for the given equipamiento_id
    links_query = select(ServicioEquipamiento).where(
        ServicioEquipamiento.equipamiento_id == equipamiento_id
    )
    links_result = await session.execute(links_query)
    servicio_equipamiento_links = links_result.scalars().all()

    if not servicio_equipamiento_links:
        return []

    # 2. Get servicio_ids
    servicio_ids = [
        link.servicio_id
        for link in servicio_equipamiento_links
        if link.servicio_id is not None
    ]

    if not servicio_ids:
        return []

    # 3. Fetch Servicio objects
    servicios_query = select(Servicio).where(getattr(Servicio.id, "in_")(servicio_ids))
    servicios_result = await session.execute(servicios_query)
    servicios = servicios_result.scalars().all()

    return servicios

```

# app/routes/utils.py

```py
from fastapi import HTTPException


def not_found(name: str):
    raise HTTPException(status_code=404, detail=f"{name} no encontrado")

```

# app/schemas/__init__.py

```py
# Import all schemas to make them available when importing from app.schemas
from app.schemas.personal import (
    PersonalCreate,
    PersonalRead,
    PersonalUpdate,
    PersonalProyectoCreate,
    PersonalProyectoRead,
)
from app.schemas.publicaciones import (
    PublicacionCreate,
    PublicacionRead,
    PublicacionUpdate,
)
from app.schemas.proyectos import (
    ProyectoCreate,
    ProyectoRead,
    ProyectoUpdate,
    ProyectoPersonalRead,
    ProyectoPersonalCreate,
)
from app.schemas.equipamiento import (
    EquipamientoCreate,
    EquipamientoRead,
    EquipamientoUpdate,
    EquipamientoActividadCreate,
    EquipamientoActividadRead,
)
from app.schemas.servicios import (
    ServicioCreate,
    ServicioRead,
    ServicioUpdate,
    ServicioEquipamientoCreate,
    ServicioEquipamientoRead,
)

```

# app/schemas/equipamiento.py

```py
from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, Field


# Esquemas base para Equipamiento
class EquipamientoBase(BaseModel):
    nombre: str
    marca: Optional[str] = None
    modelo: Optional[str] = None
    n_serie: Optional[str] = None
    hoja_especificaciones_url: Optional[str] = None
    fecha_adquisicion: Optional[date] = None
    estado: Optional[str] = None
    ubicacion: Optional[str] = None


class EquipamientoCreate(EquipamientoBase):
    pass


class EquipamientoRead(EquipamientoBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class EquipamientoUpdate(BaseModel):
    nombre: Optional[str] = None
    marca: Optional[str] = None
    modelo: Optional[str] = None
    n_serie: Optional[str] = None
    hoja_especificaciones_url: Optional[str] = None
    fecha_adquisicion: Optional[date] = None
    estado: Optional[str] = None
    ubicacion: Optional[str] = None


# Esquemas para relaciones con Actividades
class EquipamientoActividadBase(BaseModel):
    equipamiento_id: int
    actividad_id: int


class EquipamientoActividadCreate(EquipamientoActividadBase):
    pass


class EquipamientoActividadRead(EquipamientoActividadBase):
    created_at: datetime

    class Config:
        orm_mode = True

```

# app/schemas/personal.py

```py
from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr


# Esquemas base para Personal
class PersonalBase(BaseModel):
    nombre: str
    cargo: Optional[str] = None
    descripcion: Optional[str] = None
    foto_url: Optional[str] = None
    cv_url: Optional[str] = None
    orcid: Optional[str] = None
    email: Optional[EmailStr] = None
    fecha_alta: Optional[date] = None


class PersonalCreate(PersonalBase):
    pass


class PersonalRead(PersonalBase):
    id: int
    fecha_baja: Optional[date] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class PersonalUpdate(BaseModel):
    nombre: Optional[str] = None
    cargo: Optional[str] = None
    descripcion: Optional[str] = None
    foto_url: Optional[str] = None
    cv_url: Optional[str] = None
    orcid: Optional[str] = None
    email: Optional[str] = None
    fecha_alta: Optional[date] = None
    fecha_baja: Optional[date] = None


# Esquemas para relaciones
class PersonalProyectoBase(BaseModel):
    personal_id: int
    proyecto_id: int
    rol: Optional[str] = None


class PersonalProyectoCreate(PersonalProyectoBase):
    pass


class PersonalProyectoRead(PersonalProyectoBase):
    created_at: datetime

    class Config:
        orm_mode = True

```

# app/schemas/proyectos.py

```py
from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, Field, validator


# Esquemas base para Proyecto
class ProyectoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    financiador: Optional[str] = None
    presupuesto: Optional[float] = None

    @validator("fecha_fin")
    def validate_fecha_fin(cls, v, values):
        if v and values.get("fecha_inicio") and v < values["fecha_inicio"]:
            raise ValueError("La fecha de fin debe ser posterior a la fecha de inicio")
        return v


class ProyectoCreate(ProyectoBase):
    pass


class ProyectoRead(ProyectoBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class ProyectoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    financiador: Optional[str] = None
    presupuesto: Optional[float] = None

    @validator("fecha_fin")
    def validate_fecha_fin(cls, v, values):
        if v and values.get("fecha_inicio") and v < values["fecha_inicio"]:
            raise ValueError("La fecha de fin debe ser posterior a la fecha de inicio")
        return v


# Esquemas para la relación Personal-Proyecto
class ProyectoPersonalCreate(BaseModel):
    personal_id: int
    rol: Optional[str] = None


class ProyectoPersonalRead(BaseModel):
    personal_id: int
    proyecto_id: int
    rol: Optional[str] = None
    created_at: datetime

    class Config:
        orm_mode = True

```

# app/schemas/publicaciones.py

```py
from datetime import datetime
from typing import List, Optional, Dict, Union
from pydantic import BaseModel, Field, validator
import json


# Esquema para autores en JSON
class Author(BaseModel):
    name: str
    personal_id: Optional[int] = None


# Esquemas base para Publicación
class PublicacionBase(BaseModel):
    titulo: str
    cita_formateada: Optional[str] = None
    doi_url: Optional[str] = None
    enlace_pdf: Optional[str] = None
    anio: Optional[int] = None
    estado: Optional[str] = None
    authors: List[Author] = Field(default_factory=list)

    @validator("anio")
    def validate_anio(cls, v):
        if v is not None and (v < 1900 or v > datetime.now().year + 5):
            raise ValueError(f"Año debe estar entre 1900 y {datetime.now().year + 5}")
        return v


class PublicacionCreate(PublicacionBase):
    # Convertir la lista de autores a string JSON para almacenar
    def dict(self, *args, **kwargs):
        data = super().dict(*args, **kwargs)
        return data


class PublicacionRead(PublicacionBase):
    id: int
    fecha_registro: datetime
    created_at: datetime
    updated_at: datetime

    # Convertir el string JSON a lista de autores al leer
    @validator("authors", pre=True)
    def parse_authors(cls, v):
        if isinstance(v, str):
            return json.loads(
                v
            )  # Keep json.loads for compatibility if needed during transition
        return v

    class Config:
        orm_mode = True


class PublicacionUpdate(BaseModel):
    titulo: Optional[str] = None
    cita_formateada: Optional[str] = None
    doi_url: Optional[str] = None
    enlace_pdf: Optional[str] = None
    anio: Optional[int] = None
    estado: Optional[str] = None
    authors: Optional[List[Author]] = None

    # Validar año si se proporciona
    @validator("anio")
    def validate_anio(cls, v):
        if v is not None and (v < 1900 or v > datetime.now().year + 5):
            raise ValueError(f"Año debe estar entre 1900 y {datetime.now().year + 5}")
        return v

    # Convertir la lista de autores a string JSON para almacenar
    def dict(self, *args, **kwargs):
        data = super().dict(*args, **kwargs)
        if data.get("authors") is not None:
            pass  # Authors will be handled as a list of dicts
        return data

```

# app/schemas/servicios.py

```py
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


# Esquemas base para Servicio
class ServicioBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    publico_objetivo: Optional[str] = None
    tarifa: Optional[float] = Field(default=None, ge=0)  # Add ge=0 validation


class ServicioCreate(ServicioBase):
    equipamiento_ids: List[int]  # Requiere al menos un equipamiento asignado


class ServicioRead(ServicioBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class ServicioUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    publico_objetivo: Optional[str] = None
    tarifa: Optional[float] = None
    equipamiento_ids: Optional[List[int]] = (
        None  # Para reemplazar el conjunto de equipamiento
    )


# Esquemas para relaciones
class ServicioEquipamientoBase(BaseModel):
    servicio_id: int
    equipamiento_id: int


class ServicioEquipamientoCreate(ServicioEquipamientoBase):
    pass


class ServicioEquipamientoRead(ServicioEquipamientoBase):
    created_at: datetime

    class Config:
        orm_mode = True

```

# app/services/__init__.py

```py
from . import (
    personal_service,
    publicaciones_service,
    proyectos_service,
    equipamiento_service,
    servicios_service,
    archivos_service,
)

```

# app/services/archivos_service.py

```py
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
from fastapi import UploadFile, HTTPException
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import Archivo
from app.storage import local_repo

# Tamaño máximo de archivo: 50 MB
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB en bytes


# CREATE
async def guardar_archivo(db: AsyncSession, file: UploadFile) -> Archivo:
    # Verificar tamaño del archivo
    file.file.seek(0, 2)  # Mover al final del archivo
    file_size = file.file.tell()  # Obtener posición (tamaño)
    file.file.seek(0)  # Volver al inicio

    if file_size > MAX_FILE_SIZE:
        raise ValueError(
            f"El archivo excede el tamaño máximo permitido de 50 MB. Tamaño actual: {file_size / (1024 * 1024):.2f} MB"
        )

    # Guardar archivo en el sistema de archivos
    filename = await local_repo.guardar(file)

    # Determinar tipo de archivo
    file_type = file.content_type if file.content_type else "application/octet-stream"

    # Crear registro en la base de datos
    now = datetime.now(timezone.utc)
    archivo = Archivo(
        nombre=file.filename or filename,
        ruta=filename,
        tipo=file_type,
        tamano=file_size,
        fecha_subida=now,
        created_at=now,
        updated_at=now,
    )

    db.add(archivo)
    await db.commit()
    await db.refresh(archivo)
    return archivo


# READ ALL
async def listar_archivos(
    db: AsyncSession, offset: int = 0, limit: int = 100
) -> List[Archivo]:
    query = select(Archivo).offset(offset).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


# READ ONE
async def obtener_archivo(db: AsyncSession, aid: int) -> Optional[Archivo]:
    query = select(Archivo).where(Archivo.id == aid)
    result = await db.execute(query)
    return result.scalar_one_or_none()


# Abrir archivo
def abrir_archivo(ruta: str):
    """Abrir un archivo desde el sistema de archivos"""
    return local_repo.abrir(ruta)


# DELETE
async def borrar_archivo(db: AsyncSession, aid: int) -> None:
    archivo = await obtener_archivo(db, aid)

    if not archivo:
        return

    # Eliminar archivo del sistema de archivos
    try:
        local_repo.eliminar(archivo.ruta)
    except Exception as e:
        # Log error pero continuar para eliminar el registro de BD
        print(f"Error al eliminar archivo físico: {str(e)}")

    # Eliminar registro de la base de datos
    await db.delete(archivo)
    await db.commit()

```

# app/services/equipamiento_service.py

```py
from datetime import datetime, timezone
from typing import List, Optional, Sequence, Dict, Any
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import Equipamiento, EquipamientoActividad, ServicioEquipamiento


# CREATE
async def crear_equipamiento(db: AsyncSession, data: Dict[str, Any]) -> Equipamiento:
    now = datetime.now(timezone.utc)
    obj = Equipamiento(**data, created_at=now, updated_at=now)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


# READ ALL
async def listar_equipamientos(
    db: AsyncSession, offset: int = 0, limit: int = 100
) -> List[Equipamiento]:
    query = select(Equipamiento).offset(offset).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


# READ ONE
async def obtener_equipamiento(db: AsyncSession, eid: int) -> Optional[Equipamiento]:
    query = select(Equipamiento).where(Equipamiento.id == eid)
    result = await db.execute(query)
    return result.scalar_one_or_none()


# UPDATE
async def actualizar_equipamiento(
    db: AsyncSession, eid: int, data: Dict[str, Any]
) -> Optional[Equipamiento]:
    equipamiento = await obtener_equipamiento(db, eid)

    if not equipamiento:
        return None

    # Actualizar campos
    for key, value in data.items():
        setattr(equipamiento, key, value)

    equipamiento.updated_at = datetime.now(timezone.utc)
    db.add(equipamiento)
    await db.commit()
    await db.refresh(equipamiento)
    return equipamiento


# DELETE
async def borrar_equipamiento(db: AsyncSession, eid: int) -> None:
    equipamiento = await obtener_equipamiento(db, eid)

    if not equipamiento:
        return

    # Verificar si el equipamiento está asociado a actividades o servicios
    actividades_query = select(EquipamientoActividad).where(
        EquipamientoActividad.equipamiento_id == eid
    )
    actividades_result = await db.execute(actividades_query)
    actividades = actividades_result.scalars().all()

    servicios_query = select(ServicioEquipamiento).where(
        ServicioEquipamiento.equipamiento_id == eid
    )
    servicios_result = await db.execute(servicios_query)
    servicios = servicios_result.scalars().all()

    if actividades or servicios:
        raise ValueError(
            "No se puede eliminar el equipamiento porque está asociado a actividades o servicios"
        )

    await db.delete(equipamiento)
    await db.commit()


# ASIGNAR SERVICIO
async def asignar_servicio(
    db: AsyncSession, eid: int, servicio_id: int
) -> ServicioEquipamiento:
    # Verificar que el equipamiento existe
    equipamiento = await obtener_equipamiento(db, eid)
    if not equipamiento:
        raise ValueError(f"Equipamiento with ID {eid} not found")

    # Verificar que el servicio existe
    from app.services.servicios_service import obtener_servicio

    servicio = await obtener_servicio(db, servicio_id)
    if not servicio:
        raise ValueError(f"Servicio with ID {servicio_id} not found")

    # Verificar si la relación ya existe
    relation_query = select(ServicioEquipamiento).where(
        ServicioEquipamiento.equipamiento_id == eid,
        ServicioEquipamiento.servicio_id == servicio_id,
    )
    relation_result = await db.execute(relation_query)
    existing_relation = relation_result.scalar_one_or_none()

    if existing_relation:
        return existing_relation

    # Crear nueva relación
    now = datetime.now(timezone.utc)
    new_relation = ServicioEquipamiento(
        equipamiento_id=eid, servicio_id=servicio_id, created_at=now
    )
    db.add(new_relation)
    await db.commit()
    await db.refresh(new_relation)
    return new_relation


# LISTAR SERVICIOS DEL EQUIPAMIENTO
async def listar_servicios_equipamiento(
    db: AsyncSession, eid: int
) -> List[ServicioEquipamiento]:
    # Verificar que el equipamiento existe
    equipamiento = await obtener_equipamiento(db, eid)
    if not equipamiento:
        return []

    # Obtener relaciones
    query = select(ServicioEquipamiento).where(
        ServicioEquipamiento.equipamiento_id == eid
    )
    result = await db.execute(query)
    return result.scalars().all()

```

# app/services/personal_service.py

```py
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import Personal, PersonalProyecto, Proyecto


# CREATE
async def crear_personal(db: AsyncSession, data: Dict[str, Any]) -> Personal:
    # Verificar que el email es único si está presente
    if "email" in data and data["email"]:
        email_query = select(Personal).where(Personal.email == data["email"])
        email_result = await db.execute(email_query)
        existing_personal = email_result.scalar_one_or_none()

        if existing_personal:
            raise ValueError(f"Ya existe un personal con el email {data['email']}")

    now = datetime.now(timezone.utc)
    obj = Personal(**data, created_at=now, updated_at=now)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


# READ ALL
async def listar_personal(
    db: AsyncSession, offset: int = 0, limit: int = 100
) -> List[Personal]:
    query = select(Personal).offset(offset).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


# READ ONE
async def obtener_personal(db: AsyncSession, pid: int) -> Optional[Personal]:
    query = select(Personal).where(Personal.id == pid)
    result = await db.execute(query)
    return result.scalar_one_or_none()


# UPDATE
async def actualizar_personal(
    db: AsyncSession, pid: int, data: Dict[str, Any], partial: bool = False
) -> Optional[Personal]:
    personal = await obtener_personal(db, pid)

    if not personal:
        return None

    # Filter data based on whether it's a partial update
    update_data = {k: v for k, v in data.items() if not partial or v is not None}

    # Update fields
    for key, value in update_data.items():
        setattr(personal, key, value)

    personal.updated_at = datetime.now(timezone.utc)
    db.add(personal)
    await db.commit()
    await db.refresh(personal)
    return personal


# DELETE (soft delete)
async def borrar_personal(db: AsyncSession, pid: int) -> Optional[Personal]:
    personal = await obtener_personal(db, pid)

    if not personal:
        return None

    # Soft delete: establecer fecha_baja
    personal.fecha_baja = datetime.now(timezone.utc).date()
    personal.updated_at = datetime.now(timezone.utc)

    # Remove relationships in pivot table
    pivot_query = select(PersonalProyecto).where(PersonalProyecto.personal_id == pid)
    pivot_result = await db.execute(pivot_query)
    pivot_records = pivot_result.scalars().all()

    for record in pivot_records:
        await db.delete(record)

    await db.commit()
    await db.refresh(personal)
    return personal


# LIST PROJECTS
async def listar_proyectos_personal(
    db: AsyncSession, pid: int
) -> List[PersonalProyecto]:
    # Check if personal exists
    personal = await obtener_personal(db, pid)
    if not personal:
        return []

    # Get related projects
    query = select(PersonalProyecto).where(PersonalProyecto.personal_id == pid)
    result = await db.execute(query)
    return result.scalars().all()


# LINK PROJECTS
async def vincular_proyectos(
    db: AsyncSession, pid: int, items: List[Dict[str, Any]]
) -> List[PersonalProyecto]:
    # Check if personal exists
    personal = await obtener_personal(db, pid)
    if not personal:
        raise ValueError(f"Personal with ID {pid} not found")

    # Create records in pivot table
    now = datetime.now(timezone.utc)
    created_relations = []

    for item in items:
        proyecto_id = item.get("proyecto_id")
        if proyecto_id is None:
            raise ValueError("Cada item debe tener un proyecto_id")

        rol = item.get("rol", "Investigador")

        # Validate project exists
        proyecto_query = select(Proyecto).where(Proyecto.id == proyecto_id)
        proyecto_result = await db.execute(proyecto_query)
        proyecto = proyecto_result.scalar_one_or_none()

        if not proyecto:
            raise ValueError(f"Project with ID {proyecto_id} not found")

        # Check if relation already exists
        relation_query = select(PersonalProyecto).where(
            PersonalProyecto.personal_id == pid,
            PersonalProyecto.proyecto_id == proyecto_id,
        )
        relation_result = await db.execute(relation_query)
        existing_relation = relation_result.scalar_one_or_none()

        if existing_relation:
            # Update role if different
            if existing_relation.rol != rol:
                existing_relation.rol = rol
                db.add(existing_relation)
                created_relations.append(existing_relation)
        else:
            # Create new relation
            new_relation = PersonalProyecto(
                personal_id=pid, proyecto_id=proyecto_id, rol=rol, created_at=now
            )
            db.add(new_relation)
            created_relations.append(new_relation)

    await db.commit()

    # Refresh created relations
    for relation in created_relations:
        await db.refresh(relation)

    # Return all relations for this personal
    return await listar_proyectos_personal(db, pid)

```

# app/services/proyectos_service.py

```py
from datetime import datetime, timezone
from typing import List, Optional, Sequence, Dict, Any
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import Proyecto, PersonalProyecto, Personal
from app.services.personal_service import obtener_personal


# CREATE
async def crear_proyecto(db: AsyncSession, data: Dict[str, Any]) -> Proyecto:
    now = datetime.now(timezone.utc)

    # Validar que fecha_inicio <= fecha_fin
    if data.get("fecha_inicio") and data.get("fecha_fin"):
        if data["fecha_inicio"] > data["fecha_fin"]:
            raise ValueError(
                "La fecha de inicio debe ser anterior o igual a la fecha de fin"
            )

    obj = Proyecto(**data, created_at=now, updated_at=now)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    # Patch tzinfo if missing (SQLite)
    if obj.created_at.tzinfo is None:
        obj.created_at = obj.created_at.replace(tzinfo=timezone.utc)
    if obj.updated_at.tzinfo is None:
        obj.updated_at = obj.updated_at.replace(tzinfo=timezone.utc)
    return obj


# READ ALL
async def listar_proyectos(
    db: AsyncSession, offset: int = 0, limit: int = 100
) -> List[Proyecto]:
    query = select(Proyecto).offset(offset).limit(limit)
    result = await db.execute(query)
    return list(result.scalars().all())


# READ ONE
async def obtener_proyecto(db: AsyncSession, pid: int) -> Optional[Proyecto]:
    query = select(Proyecto).where(Proyecto.id == pid)
    result = await db.execute(query)
    return result.scalar_one_or_none()


# UPDATE
async def actualizar_proyecto(
    db: AsyncSession, pid: int, data: Dict[str, Any]
) -> Optional[Proyecto]:
    proyecto = await obtener_proyecto(db, pid)

    if not proyecto:
        return None

    # Validar que fecha_inicio <= fecha_fin
    fecha_inicio = data.get("fecha_inicio", proyecto.fecha_inicio)
    fecha_fin = data.get("fecha_fin", proyecto.fecha_fin)

    if fecha_inicio and fecha_fin and fecha_inicio > fecha_fin:
        raise ValueError(
            "La fecha de inicio debe ser anterior o igual a la fecha de fin"
        )

    # Actualizar campos
    for key, value in data.items():
        setattr(proyecto, key, value)

    proyecto.updated_at = datetime.now(timezone.utc)
    db.add(proyecto)
    await db.commit()
    await db.refresh(proyecto)
    # Patch tzinfo if missing (SQLite)
    if proyecto.updated_at.tzinfo is None:
        proyecto.updated_at = proyecto.updated_at.replace(tzinfo=timezone.utc)
    if proyecto.created_at.tzinfo is None:
        proyecto.created_at = proyecto.created_at.replace(tzinfo=timezone.utc)
    return proyecto


# DELETE
async def borrar_proyecto(db: AsyncSession, pid: int) -> None:
    proyecto = await obtener_proyecto(db, pid)

    if not proyecto:
        return

    # Eliminar relaciones con personal
    pivot_query = select(PersonalProyecto).where(PersonalProyecto.proyecto_id == pid)
    pivot_result = await db.execute(pivot_query)
    pivot_records = pivot_result.scalars().all()

    for record in pivot_records:
        await db.delete(record)

    await db.delete(proyecto)
    await db.commit()


# ASIGNAR PERSONAL
async def asignar_personal(
    db: AsyncSession, proyecto_id: int, personal_data: List[Dict[str, Any]]
) -> List[PersonalProyecto]:
    # Verificar que el proyecto existe
    proyecto = await obtener_proyecto(db, proyecto_id)
    if not proyecto:
        raise ValueError(f"Proyecto with ID {proyecto_id} not found")

    # Crear relaciones en la tabla pivote
    now = datetime.now(timezone.utc)
    created_relations = []

    for item in personal_data:
        personal_id = item.get("personal_id")
        if personal_id is None:
            raise ValueError("Cada item debe tener un personal_id")
        rol = item.get("rol", "Investigador")

        # Verificar que el personal existe
        personal_query = select(Personal).where(Personal.id == personal_id)
        personal_result = await db.execute(personal_query)
        personal = personal_result.scalar_one_or_none()

        if not personal:
            raise ValueError(f"Personal with ID {personal_id} not found")

        # Verificar si la relación ya existe
        relation_query = select(PersonalProyecto).where(
            PersonalProyecto.personal_id == personal_id,
            PersonalProyecto.proyecto_id == proyecto_id,
        )
        relation_result = await db.execute(relation_query)
        existing_relation = relation_result.scalar_one_or_none()

        if existing_relation:
            # Actualizar el rol si es diferente
            if existing_relation.rol != rol:
                existing_relation.rol = rol
                db.add(existing_relation)
                created_relations.append(existing_relation)
        else:
            # Crear nueva relación
            new_relation = PersonalProyecto(
                personal_id=personal_id,
                proyecto_id=proyecto_id,
                rol=rol,
                created_at=now,
            )
            db.add(new_relation)
            created_relations.append(new_relation)

    await db.commit()

    # Refrescar las relaciones creadas/actualizadas
    for relation in created_relations:
        await db.refresh(relation)

    # Retornar todas las relaciones para este proyecto
    pivot_query = select(PersonalProyecto).where(
        PersonalProyecto.proyecto_id == proyecto_id
    )
    pivot_result = await db.execute(pivot_query)
    return list(pivot_result.scalars().all())


# LISTAR PERSONAL DEL PROYECTO
async def listar_personal_proyecto(
    db: AsyncSession, proyecto_id: int
) -> List[PersonalProyecto]:
    # Verificar que el proyecto existe
    proyecto = await obtener_proyecto(db, proyecto_id)
    if not proyecto:
        return []

    # Obtener relaciones
    query = select(PersonalProyecto).where(PersonalProyecto.proyecto_id == proyecto_id)
    result = await db.execute(query)
    return list(result.scalars().all())


# LISTAR PROYECTOS DEL PERSONAL
async def listar_proyectos_personal(
    db: AsyncSession, pid: int
) -> List[PersonalProyecto]:
    # Check if personal exists
    personal = await obtener_personal(db, pid)
    if not personal:
        return []
    # Get related projects
    query = select(PersonalProyecto).where(PersonalProyecto.personal_id == pid)
    result = await db.execute(query)
    return list(result.scalars().all())

```

# app/services/publicaciones_service.py

```py
from datetime import datetime, timezone
from typing import List, Optional, Sequence, Dict, Any
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import Publicacion, Personal


# CREATE
async def crear_publicacion(db: AsyncSession, data: Dict[str, Any]) -> Publicacion:
    now = datetime.now(timezone.utc)

    # Validar que los personal_id en authors existan
    authors_data = data.get("authors", "[]")
    if isinstance(authors_data, str):
        import json

        try:
            authors = json.loads(authors_data)
        except json.JSONDecodeError:
            authors = []
    else:
        authors = authors_data

    # Validar que los personal_id en authors existan
    if authors and isinstance(authors, list):
        for author in authors:
            if isinstance(author, dict) and "personal_id" in author:
                personal_id = author["personal_id"]
                personal = await db.execute(
                    select(Personal).where(Personal.id == personal_id)
                )
                if not personal.scalar_one_or_none():
                    raise ValueError(f"Personal with ID {personal_id} not found")

    obj = Publicacion(**data, created_at=now, updated_at=now)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


# READ ALL
async def listar_publicaciones(
    db: AsyncSession,
    offset: int = 0,
    limit: int = 100,
    anio: Optional[int] = None,
    estado: Optional[str] = None,
) -> List[Publicacion]:
    query = select(Publicacion)

    # Aplicar filtros si están definidos
    if anio is not None:
        query = query.where(Publicacion.anio == anio)
    if estado:
        query = query.where(Publicacion.estado == estado)

    # Paginación
    query = query.offset(offset).limit(limit)

    result = await db.execute(query)
    return result.scalars().all()


# READ ONE
async def obtener_publicacion(db: AsyncSession, pid: int) -> Optional[Publicacion]:
    query = select(Publicacion).where(Publicacion.id == pid)
    result = await db.execute(query)
    return result.scalar_one_or_none()


# UPDATE
async def actualizar_publicacion(
    db: AsyncSession, pid: int, data: Dict[str, Any]
) -> Optional[Publicacion]:
    publicacion = await obtener_publicacion(db, pid)

    if not publicacion:
        return None

    # Validar que los personal_id en authors existan
    if "authors" in data:
        authors_data = data.get("authors", "[]")
        if isinstance(authors_data, str):
            import json

            try:
                authors = json.loads(authors_data)
            except json.JSONDecodeError:
                authors = []
        else:
            authors = authors_data

        if authors and isinstance(authors, list):
            for author in authors:
                if isinstance(author, dict) and "personal_id" in author:
                    personal_id = author["personal_id"]
                    personal = await db.execute(
                        select(Personal).where(Personal.id == personal_id)
                    )
                    if not personal.scalar_one_or_none():
                        raise ValueError(f"Personal with ID {personal_id} not found")

    # Actualizar campos
    for key, value in data.items():
        setattr(publicacion, key, value)

    publicacion.updated_at = datetime.now(timezone.utc)
    db.add(publicacion)
    await db.commit()
    await db.refresh(publicacion)
    return publicacion


# DELETE
async def borrar_publicacion(db: AsyncSession, pid: int) -> None:
    publicacion = await obtener_publicacion(db, pid)

    if not publicacion:
        return

    await db.delete(publicacion)
    await db.commit()

```

# app/services/servicios_service.py

```py
from datetime import datetime, timezone
from typing import List, Optional, Sequence, Dict, Any
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.models import Servicio, ServicioEquipamiento, Equipamiento


# CREATE
async def crear_servicio(
    db: AsyncSession,
    data: Dict[str, Any],
    equipamiento_ids: Optional[List[int]] = None,  # Allow None
) -> Servicio:
    now = datetime.now(timezone.utc)

    # Validar tarifa
    if data.get("tarifa") is not None and data["tarifa"] < 0:
        raise ValueError("La tarifa no puede ser negativa.")

    # Crear servicio
    obj = Servicio(**data, created_at=now, updated_at=now)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)

    # Asociar equipamientos
    if equipamiento_ids:
        for eid in equipamiento_ids:
            # Asegurarse que obj.id no es None antes de usarlo
            if obj.id is None:
                raise ValueError(
                    "ID de servicio no puede ser None al asociar equipamiento"
                )
            se = ServicioEquipamiento(
                servicio_id=obj.id, equipamiento_id=eid, created_at=now
            )
            db.add(se)
        await db.commit()  # Commit after adding all associations
    # Eagerly load equipamiento_objs (the many-to-many relationship)
    query = (
        select(Servicio)
        .options(selectinload(Servicio.equipamientos))
        .where(Servicio.id == obj.id)
    )
    result = await db.execute(query)
    obj = result.scalar_one()
    return obj


# READ ALL
async def listar_servicios(
    db: AsyncSession, offset: int = 0, limit: int = 100
) -> List[Servicio]:  # Return List instead of Sequence
    query = select(Servicio).offset(offset).limit(limit)
    result = await db.execute(query)
    return list(result.scalars().all())  # Convert to list


# READ ONE
async def obtener_servicio(db: AsyncSession, sid: int) -> Optional[Servicio]:
    query = select(Servicio).where(Servicio.id == sid)
    result = await db.execute(query)
    return result.scalar_one_or_none()


# UPDATE
async def actualizar_servicio(
    db: AsyncSession, sid: int, data: Dict[str, Any]
) -> Optional[Servicio]:
    servicio = await obtener_servicio(db, sid)

    if not servicio:
        return None

    # Validar tarifa
    if data.get("tarifa") is not None and data["tarifa"] < 0:
        raise ValueError("La tarifa no puede ser negativa.")

    # Actualizar campos
    for key, value in data.items():
        setattr(servicio, key, value)

    servicio.updated_at = datetime.now(timezone.utc)
    db.add(servicio)
    await db.commit()
    await db.refresh(servicio)
    return servicio


# DELETE
async def borrar_servicio(db: AsyncSession, sid: int) -> None:
    servicio = await obtener_servicio(db, sid)

    if not servicio:
        return

    # Eliminar relaciones con equipamientos
    pivot_query = select(ServicioEquipamiento).where(
        ServicioEquipamiento.servicio_id == sid
    )
    pivot_result = await db.execute(pivot_query)
    pivot_records = pivot_result.scalars().all()

    for record in pivot_records:
        await db.delete(record)

    await db.delete(servicio)
    await db.commit()


# LISTAR EQUIPAMIENTOS DEL SERVICIO
async def listar_equipamientos_servicio(
    db: AsyncSession, sid: int
) -> List[ServicioEquipamiento]:  # Return List instead of Sequence
    query = select(ServicioEquipamiento).where(ServicioEquipamiento.servicio_id == sid)
    result = await db.execute(query)
    return list(result.scalars().all())  # Convert to list


# AGREGAR EQUIPAMIENTO A SERVICIO
async def agregar_equipamiento(
    db: AsyncSession, sid: int, eid: int
) -> ServicioEquipamiento:
    # Verificar que el servicio existe
    servicio = await obtener_servicio(db, sid)
    if not servicio:
        raise ValueError(f"Servicio with ID {sid} not found")

    # Verificar que el equipamiento existe
    from app.services.equipamiento_service import obtener_equipamiento

    equipamiento = await obtener_equipamiento(db, eid)
    if not equipamiento:
        raise ValueError(f"Equipamiento with ID {eid} not found")

    # Verificar si la relación ya existe
    relation_query = select(ServicioEquipamiento).where(
        ServicioEquipamiento.servicio_id == sid,
        ServicioEquipamiento.equipamiento_id == eid,
    )
    relation_result = await db.execute(relation_query)
    existing_relation = relation_result.scalar_one_or_none()

    if existing_relation:
        return existing_relation

    # Crear nueva relación
    now = datetime.now(timezone.utc)
    new_relation = ServicioEquipamiento(
        servicio_id=sid, equipamiento_id=eid, created_at=now
    )
    db.add(new_relation)
    await db.commit()
    await db.refresh(new_relation)
    return new_relation

```

# app/storage/__init__.py

```py
# Archivo de inicialización del paquete storage

```

# app/storage/local_repo.py

```py
"""
Módulo para gestionar el almacenamiento local de archivos.
"""

import os
import uuid
import logging
import aiofiles
import aiofiles.os as aios  # Import aiofiles.os
import mimetypes
from pathlib import Path
from typing import BinaryIO, Generator, AsyncGenerator
from fastapi import UploadFile, HTTPException
from fastapi.responses import StreamingResponse

# Configuración de logging
logger = logging.getLogger(__name__)

# Ruta base para almacenamiento de archivos
UPLOAD_DIR = "/app/uploads"


async def guardar(file: UploadFile) -> str:
    """
    Guarda un archivo subido en el sistema de archivos local.

    Args:
        file: El archivo subido mediante FastAPI

    Returns:
        str: La ruta relativa del archivo guardado
    """
    # Crear el directorio si no existe
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Generar nombre único para el archivo
    file_extension = os.path.splitext(file.filename)[1] if file.filename else ""
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    try:
        # Guardar el archivo
        async with aiofiles.open(file_path, "wb") as out_file:
            while content := await file.read(1024):  # Read file in chunks
                await out_file.write(content)

        logger.info(f"Archivo guardado: {file_path}")
        return unique_filename
    except Exception as e:
        logger.error(f"Error al guardar archivo: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error al guardar archivo: {str(e)}"
        )


async def abrir(ruta: str) -> StreamingResponse:
    """
    Abre un archivo y lo retorna como StreamingResponse.

    Args:
        ruta: Ruta relativa del archivo a abrir

    Returns:
        StreamingResponse: Stream del archivo
    """
    file_path = os.path.join(UPLOAD_DIR, ruta)

    if not os.path.exists(file_path):
        logger.error(f"Archivo no encontrado: {file_path}")
        raise HTTPException(status_code=404, detail="Archivo no encontrado")

    async def file_iterator(file_path: str) -> AsyncGenerator[bytes, None]:
        async with aiofiles.open(file_path, mode="rb") as f:
            while chunk := await f.read(1024):
                yield chunk

    try:
        # Guess media type from file extension
        mime_type, _ = mimetypes.guess_type(file_path)
        if not mime_type:
            mime_type = "application/octet-stream"
        return StreamingResponse(file_iterator(file_path), media_type=mime_type)
    except Exception as e:
        logger.error(f"Error al abrir archivo: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al abrir archivo: {str(e)}")


async def eliminar(ruta: str) -> None:
    """
    Elimina un archivo del sistema de archivos.

    Args:
        ruta: Ruta relativa del archivo a eliminar
    """
    file_path = os.path.join(UPLOAD_DIR, ruta)

    if not await aios.path.exists(file_path):  # Use aios.path.exists
        logger.warning(f"Intento de eliminar archivo no existente: {file_path}")
        return

    try:
        await aios.remove(file_path)  # Use aios.remove
        logger.info(f"Archivo eliminado: {file_path}")
    except Exception as e:
        logger.error(f"Error al eliminar archivo: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error al eliminar archivo: {str(e)}"
        )

```

# docker-compose.yml

```yml
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: cenur
      POSTGRES_PASSWORD: cenur_pass
      POSTGRES_DB: cenur_db
    volumes:
      - pgdata:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  web:
    working_dir: /app
    # image: python:3.12-slim
    build:
      context: .
      dockerfile: Dockerfile
    depends_on:
      - db
    environment:
      DATABASE_URL: postgresql+asyncpg://cenur:cenur_pass@db:5432/cenur_db
      PYTHONPATH: /app
    volumes:
      - ./app:/app/app
      - ./alembic:/app/alembic
      - ./uploads:/app/uploads
      - ./alembic.ini:/app/alembic.ini
      - ./requirements.txt:/app/requirements.txt
    ports:
      - "8000:8000"

volumes:
  pgdata:

```

# Dockerfile

```
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ./app /app/app
COPY ./alembic /app/alembic
COPY alembic.ini .
RUN mkdir -p /app/uploads && chmod 777 /app/uploads
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

```

# requirements.txt

```txt
fastapi[all]
uvicorn[standard]
sqlmodel
alembic
asyncpg
psycopg2-binary
python-dotenv
httpx
python-multipart
aiofiles
pytest
```

# test_archivos.sh

```sh
#!/bin/bash
# filepath: /home/sesquerre/departamento_del_agua/test_archivos.sh

# Colores para la salida
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# URL base de la API
API_URL="http://localhost:8000"

# Función para imprimir mensajes con formato
function log_message() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

function log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

function log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Crear archivo de prueba
function create_test_file() {
    local filename=$1
    local content=$2
    
    log_message "Creando archivo de prueba: $filename"
    echo "$content" > "$filename"
    
    if [ -f "$filename" ]; then
        log_success "Archivo creado correctamente: $filename"
        return 0
    else
        log_error "Error al crear archivo: $filename"
        return 1
    fi
}

# Subir archivo
function upload_file() {
    local filename=$1
    local TEMP_FILE="upload_response.tmp"
    
    log_message "Subiendo archivo: $filename"
    curl -s -F "file=@$filename" "${API_URL}/archivos/upload" > "$TEMP_FILE"
    
    # Leer la respuesta
    local response=$(cat "$TEMP_FILE")
    
    # Extraer ID del archivo usando expresiones regulares
    local file_id=$(grep -oP '"id":\s*\K[0-9]+' "$TEMP_FILE" || echo "")
    local file_path=$(grep -oP '"ruta":\s*"\K[^"]+' "$TEMP_FILE" || echo "")
    
    # Depuración
    echo "Response: $response"
    echo "ID: $file_id"
    echo "Path: $file_path"
    
    if [ -n "$file_id" ] && [ -n "$file_path" ]; then
        log_success "Archivo subido correctamente. ID: $file_id, Ruta: $file_path"
        echo "$file_id" > "file_id.tmp"
        echo "$file_path" > "file_path.tmp"
        return 0
    else
        log_error "Error al subir archivo. Respuesta: $response"
        return 1
    fi
}

# Descargar archivo
function download_file() {
    local file_id=$1
    local output_file=$2
    
    if [ -z "$file_id" ]; then
        log_error "ID de archivo no válido: '$file_id'"
        return 1
    fi
    
    log_message "Descargando archivo con ID: $file_id"
    local status_code=$(curl -s -w "%{http_code}" -o "$output_file" "${API_URL}/archivos/${file_id}")
    
    if [ "$status_code" == "200" ]; then
        log_success "Archivo descargado correctamente: $output_file"
        return 0
    else
        log_error "Error al descargar archivo. Código HTTP: $status_code"
        return 1
    fi
}

# Verificar contenido
function verify_content() {
    local file1=$1
    local file2=$2
    
    if [ ! -f "$file1" ] || [ ! -f "$file2" ]; then
        log_error "Uno o ambos archivos no existen: $file1 o $file2"
        return 1
    fi
    
    log_message "Verificando que el contenido de los archivos coincida"
    if cmp -s "$file1" "$file2"; then
        log_success "El contenido de los archivos coincide"
        return 0
    else
        log_error "El contenido de los archivos no coincide"
        return 1
    fi
}

# Eliminar archivo
function delete_file() {
    local file_id=$1
    
    if [ -z "$file_id" ]; then
        log_error "ID de archivo no válido: '$file_id'"
        return 1
    fi
    
    log_message "Eliminando archivo con ID: $file_id"
    local status_code=$(curl -s -X DELETE -w "%{http_code}" -o /dev/null "${API_URL}/archivos/${file_id}")
    
    if [ "$status_code" == "204" ]; then
        log_success "Archivo eliminado correctamente"
        return 0
    else
        log_error "Error al eliminar archivo. Código HTTP: $status_code"
        return 1
    fi
}

# Verificar que el archivo ya no existe
function verify_file_deleted() {
    local file_id=$1
    
    if [ -z "$file_id" ]; then
        log_error "ID de archivo no válido: '$file_id'"
        return 1
    fi
    
    log_message "Verificando que el archivo con ID $file_id ya no existe"
    local status_code=$(curl -s -o /dev/null -w "%{http_code}" "${API_URL}/archivos/${file_id}")
    
    if [ "$status_code" == "404" ]; then
        log_success "Archivo con ID $file_id ya no existe (404 recibido)"
        return 0
    else
        log_error "El archivo con ID $file_id aún existe o se recibió un código inesperado: $status_code"
        return 1
    fi
}

# Iniciar pruebas
log_message "=== INICIANDO PRUEBAS DEL SISTEMA DE ARCHIVOS ==="

# Eliminar archivos temporales anteriores
rm -f upload_response.tmp file_id.tmp file_path.tmp

# Prueba 1: Subir un archivo de texto
log_message "PRUEBA 1: Subir un archivo de texto"
create_test_file "test_texto.txt" "Este es un archivo de texto de prueba para el sistema de almacenamiento."

if upload_file "test_texto.txt"; then
    # Obtener ID y ruta de los archivos temporales
    file_id=$(cat file_id.tmp)
    file_path=$(cat file_path.tmp)
    
    # Prueba 2: Descargar el archivo
    log_message "PRUEBA 2: Descargar el archivo"
    if download_file "$file_id" "downloaded_text.txt"; then
        # Prueba 3: Verificar contenido
        log_message "PRUEBA 3: Verificar contenido"
        verify_content "test_texto.txt" "downloaded_text.txt"
    fi
    
    # Prueba 4: Eliminar archivo
    log_message "PRUEBA 4: Eliminar archivo"
    if delete_file "$file_id"; then
        # Prueba 5: Verificar que el archivo ya no existe
        log_message "PRUEBA 5: Verificar que el archivo ya no existe"
        verify_file_deleted "$file_id"
    fi
else
    log_error "No se pudo subir el archivo de texto. Omitiendo pruebas 2-5."
fi

# Prueba 6: Subir un archivo binario (imagen)
log_message "PRUEBA 6: Subir un archivo binario (imagen)"

# Crear una imagen de prueba
log_message "Creando imagen de prueba"
dd if=/dev/urandom of=test_image.png bs=1k count=5 2>/dev/null

if upload_file "test_image.png"; then
    # Obtener ID y ruta de los archivos temporales
    file_id=$(cat file_id.tmp)
    file_path=$(cat file_path.tmp)
    
    # Prueba 7: Descargar la imagen
    log_message "PRUEBA 7: Descargar la imagen"
    if download_file "$file_id" "downloaded_image.png"; then
        # Prueba 8: Verificar contenido
        log_message "PRUEBA 8: Verificar contenido de la imagen"
        verify_content "test_image.png" "downloaded_image.png"
    fi
    
    # Prueba 9: Eliminar imagen
    log_message "PRUEBA 9: Eliminar imagen"
    if delete_file "$file_id"; then
        # Prueba 10: Verificar que la imagen ya no existe
        log_message "PRUEBA 10: Verificar que la imagen ya no existe"
        verify_file_deleted "$file_id"
    fi
else
    log_error "No se pudo subir la imagen. Omitiendo pruebas 7-10."
fi

# Limpiar archivos temporales
log_message "Limpiando archivos temporales"
rm -f test_texto.txt downloaded_text.txt test_image.png downloaded_image.png
rm -f upload_response.tmp file_id.tmp file_path.tmp

log_message "=== PRUEBAS COMPLETADAS ==="
```

# tests/__init__.py

```py

```

# tests/conftest.py

```py
import os

os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"

import asyncio
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport  # Import ASGITransport
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from sqlmodel import SQLModel

from app.db import get_session  # Corrected import for get_session
from app.main import app

ASYNC_URL = "sqlite+aiosqlite:///:memory:"  # In-memory SQLite for tests
engine_test = create_async_engine(ASYNC_URL, echo=False, future=True)

# Use async_sessionmaker for SQLAlchemy 1.4+ style
async_session_factory = async_sessionmaker(
    engine_test, class_=AsyncSession, expire_on_commit=False
)


@pytest.fixture(scope="session")
def anyio_backend():  # evita warning asyncio_mode
    return "asyncio"


@pytest.fixture(scope="session", autouse=True)
async def _create_schema():
    async with engine_test.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


@pytest.fixture
async def db() -> AsyncGenerator[AsyncSession, None]:  # Correct type hint
    async with async_session_factory() as session:
        yield session


@pytest.fixture
async def client(
    db: AsyncSession,
) -> AsyncGenerator[AsyncClient, None]:  # Correct type hint and db type
    # Correctly override dependencies. Assuming get_session is the primary one.
    app.dependency_overrides[get_session] = lambda: db

    # Use ASGITransport for testing FastAPI apps with httpx
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as c:
        yield c

    # Clean up overrides after test
    app.dependency_overrides.clear()


@pytest.fixture(scope="session", autouse=True)
def _init_app_db():
    # Ensure app.db tables are created for the app's engine
    import app.db

    asyncio.get_event_loop().run_until_complete(app.db.init_db())

```

# tests/routes/test_personal_routes.py

```py
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)  # For type hinting client fixture if needed
from app.models.models import Personal  # To check response structure
from app.schemas.personal import PersonalCreate, PersonalUpdate  # For request payloads


@pytest.mark.anyio
async def test_create_and_get_personal(
    client: AsyncClient, db: AsyncSession
):  # db fixture might be needed if direct db interaction is planned post-request
    # Create Personal
    personal_data = PersonalCreate(
        nombre="Ana De Armas",
        email="ana.dearmas@example.com",
    )
    response = await client.post("/personal/", json=personal_data.model_dump())
    assert response.status_code == 201, response.text
    created_personal_data = response.json()
    personal_id = created_personal_data["id"]
    assert personal_id is not None
    assert created_personal_data["nombre"] == personal_data.nombre
    assert created_personal_data["email"] == personal_data.email

    # Get Personal by ID
    response = await client.get(f"/personal/{personal_id}")
    assert response.status_code == 200, response.text
    retrieved_personal_data = response.json()
    assert retrieved_personal_data["id"] == personal_id
    assert retrieved_personal_data["nombre"] == personal_data.nombre
    assert retrieved_personal_data["email"] == personal_data.email


@pytest.mark.anyio
async def test_create_personal_email_invalido(client: AsyncClient):
    personal_data = {
        "nombre": "Email Invalido",
        "email": "emailinvalido",  # Invalid email format
    }
    response = await client.post("/personal/", json=personal_data)
    assert (
        response.status_code == 422
    )  # Unprocessable Entity for Pydantic validation errors
    # Optionally, check the error detail
    # error_detail = response.json()["detail"][0]
    # assert error_detail["type"] == "value_error.email"


@pytest.mark.anyio
async def test_get_personal_no_existente(client: AsyncClient):
    response = await client.get("/personal/999999")  # Assuming 999999 does not exist
    assert response.status_code == 404, response.text


@pytest.mark.anyio
async def test_update_personal(client: AsyncClient, db: AsyncSession):
    # First, create a personal record to update
    initial_data = PersonalCreate(
        nombre="Usuario Original", email="original@example.com"
    )
    response = await client.post("/personal/", json=initial_data.model_dump())
    assert response.status_code == 201
    personal_id = response.json()["id"]

    # Now, update it
    update_data = PersonalUpdate(nombre="Usuario Actualizado")
    response = await client.put(
        f"/personal/{personal_id}", json=update_data.model_dump(exclude_unset=True)
    )
    assert response.status_code == 200, response.text
    updated_personal_data = response.json()
    assert updated_personal_data["nombre"] == update_data.nombre
    assert (
        updated_personal_data["email"] == initial_data.email
    )  # Email should remain unchanged


@pytest.mark.anyio
async def test_update_personal_no_existente(client: AsyncClient):
    update_data = PersonalUpdate(nombre="No Existe")
    response = await client.put(
        "/personal/999999", json=update_data.model_dump(exclude_unset=True)
    )
    assert response.status_code == 404, response.text


@pytest.mark.anyio
async def test_delete_personal(client: AsyncClient, db: AsyncSession):
    # Create a personal record to delete
    personal_data = PersonalCreate(nombre="Para Borrar", email="borrar@example.com")
    response = await client.post("/personal/", json=personal_data.model_dump())
    assert response.status_code == 201
    personal_id = response.json()["id"]

    # Delete it
    response = await client.delete(f"/personal/{personal_id}")
    assert response.status_code == 200, response.text
    deleted = response.json()
    assert deleted["id"] == personal_id
    assert deleted["fecha_baja"] is not None

    # Verify soft-deleted: GET returns the object with fecha_baja set
    response = await client.get(f"/personal/{personal_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["fecha_baja"] is not None


@pytest.mark.anyio
async def test_delete_personal_no_existente(client: AsyncClient):
    response = await client.delete("/personal/999999")
    assert response.status_code == 404, response.text


@pytest.mark.anyio
async def test_list_personal(client: AsyncClient, db: AsyncSession):
    # Create a couple of entries to ensure there's data
    await client.post(
        "/personal/",
        json=PersonalCreate(nombre="Persona A", email="a@example.com").model_dump(),
    )
    await client.post(
        "/personal/",
        json=PersonalCreate(nombre="Persona B", email="b@example.com").model_dump(),
    )

    response = await client.get("/personal/")
    assert response.status_code == 200, response.text
    personal_list = response.json()
    assert isinstance(personal_list, list)
    assert len(personal_list) >= 2  # Check if at least the two created are present

    nombres = [p["nombre"] for p in personal_list]
    assert "Persona A" in nombres
    assert "Persona B" in nombres

```

# tests/services/__init__.py

```py

```

# tests/services/test_proyectos_service.py

```py
import pytest
from datetime import date, timedelta, timezone, datetime
from app.services import proyectos_service
from app.schemas.proyectos import ProyectoCreate
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.anyio
async def test_crear_proyecto_valido(
    db: AsyncSession,
):
    proyecto_data = ProyectoCreate(
        nombre="Proyecto Test Valido",
        descripcion="Descripción del proyecto",
        fecha_inicio=date.today(),
        fecha_fin=date.today() + timedelta(days=30),
        presupuesto=10000.00,
    )
    proyecto = await proyectos_service.crear_proyecto(
        db=db, data=proyecto_data.model_dump()
    )
    assert proyecto.id is not None
    assert proyecto.nombre == "Proyecto Test Valido"
    assert proyecto.fecha_inicio == proyecto_data.fecha_inicio
    assert proyecto.created_at is not None
    assert proyecto.created_at.tzinfo == timezone.utc


@pytest.mark.anyio
async def test_crear_proyecto_fecha_fin_antes_de_inicio(db: AsyncSession):
    now = date.today()
    proyecto_data = {
        "nombre": "Proyecto Fechas Invalidas",
        "fecha_inicio": now,
        "fecha_fin": now - timedelta(days=1),
    }
    with pytest.raises(ValueError) as exc_info:
        await proyectos_service.crear_proyecto(db=db, data=proyecto_data)
    assert "La fecha de inicio debe ser anterior o igual a la fecha de fin" in str(
        exc_info.value
    )


@pytest.mark.anyio
async def test_obtener_proyecto(db: AsyncSession):
    proyecto_data = ProyectoCreate(
        nombre="Proyecto Para Obtener",
        fecha_inicio=date.today(),
        fecha_fin=date.today() + timedelta(days=5),
    )
    proyecto_creado = await proyectos_service.crear_proyecto(
        db=db, data=proyecto_data.model_dump()
    )
    assert proyecto_creado.id is not None
    proyecto_obtenido = await proyectos_service.obtener_proyecto(
        db=db, pid=proyecto_creado.id
    )
    assert proyecto_obtenido is not None
    assert proyecto_obtenido.id == proyecto_creado.id
    assert proyecto_obtenido.nombre == "Proyecto Para Obtener"


@pytest.mark.anyio
async def test_obtener_proyecto_no_existente(db: AsyncSession):
    proyecto = await proyectos_service.obtener_proyecto(db=db, pid=99999)
    assert proyecto is None


@pytest.mark.anyio
async def test_actualizar_proyecto(db: AsyncSession):
    proyecto_data = ProyectoCreate(
        nombre="Proyecto Original", fecha_inicio=date.today(), presupuesto=5000.0
    )
    proyecto_creado = await proyectos_service.crear_proyecto(
        db=db, data=proyecto_data.model_dump()
    )
    assert proyecto_creado.id is not None
    datos_actualizacion = {"nombre": "Proyecto Actualizado", "presupuesto": 7500.0}
    proyecto_actualizado = await proyectos_service.actualizar_proyecto(
        db=db, pid=proyecto_creado.id, data=datos_actualizacion
    )
    assert proyecto_actualizado is not None
    assert proyecto_actualizado.nombre == "Proyecto Actualizado"
    assert proyecto_actualizado.presupuesto == 7500.0
    assert proyecto_actualizado.updated_at is not None
    assert proyecto_actualizado.updated_at > proyecto_creado.created_at
    assert proyecto_actualizado.updated_at.tzinfo == timezone.utc


@pytest.mark.anyio
async def test_actualizar_proyecto_fecha_invalida(db: AsyncSession):
    proyecto_data = ProyectoCreate(
        nombre="Proyecto Fechas Originales",
        fecha_inicio=date.today(),
        fecha_fin=date.today() + timedelta(days=10),
    )
    proyecto_creado = await proyectos_service.crear_proyecto(
        db=db, data=proyecto_data.model_dump()
    )
    assert proyecto_creado.id is not None
    assert proyecto_creado.fecha_inicio is not None
    datos_actualizacion_invalidos = {
        "fecha_fin": proyecto_creado.fecha_inicio - timedelta(days=1)
    }
    with pytest.raises(ValueError) as exc_info:
        await proyectos_service.actualizar_proyecto(
            db=db, pid=proyecto_creado.id, data=datos_actualizacion_invalidos
        )
    assert "La fecha de inicio debe ser anterior o igual a la fecha de fin" in str(
        exc_info.value
    )


@pytest.mark.anyio
async def test_eliminar_proyecto(db: AsyncSession):
    proyecto_data = ProyectoCreate(
        nombre="Proyecto a Eliminar", fecha_inicio=date.today()
    )
    proyecto_creado = await proyectos_service.crear_proyecto(
        db=db, data=proyecto_data.model_dump()
    )
    assert proyecto_creado.id is not None
    await proyectos_service.borrar_proyecto(db=db, pid=proyecto_creado.id)
    proyecto_no_encontrado = await proyectos_service.obtener_proyecto(
        db=db, pid=proyecto_creado.id
    )
    assert proyecto_no_encontrado is None


@pytest.mark.anyio
async def test_eliminar_proyecto_no_existente(db: AsyncSession):
    await proyectos_service.borrar_proyecto(db=db, pid=99999)
    # Should not raise, just do nothing


@pytest.mark.anyio
async def test_listar_proyectos(db: AsyncSession):
    await proyectos_service.crear_proyecto(
        db=db, data=ProyectoCreate(nombre="P1", fecha_inicio=date.today()).model_dump()
    )
    await proyectos_service.crear_proyecto(
        db=db, data=ProyectoCreate(nombre="P2", fecha_inicio=date.today()).model_dump()
    )
    proyectos = await proyectos_service.listar_proyectos(db=db, offset=0, limit=10)
    assert len(proyectos) >= 2
    nombres_proyectos = [p.nombre for p in proyectos]
    assert "P1" in nombres_proyectos
    assert "P2" in nombres_proyectos

```

# tests/services/test_servicios_service.py

```py
import pytest
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import servicios_service
from app.schemas.servicios import ServicioCreate, ServicioUpdate
from app.models.models import (
    Equipamiento,
)  # Assuming Equipamiento model exists and is needed for setup
import datetime


@pytest.fixture
async def setup_equipamientos(db: AsyncSession) -> List[Equipamiento]:
    # Helper to create some equipamientos for service tests
    eq1_data = {
        "nombre": "Equipo Test 1",
        "descripcion": "Desc Equipo 1",
        "modelo": "M1",
        "numero_serie": "SN1",
        "fecha_adquisicion": datetime.date(2023, 1, 1),
        "estado": "Operativo",
    }
    eq2_data = {
        "nombre": "Equipo Test 2",
        "descripcion": "Desc Equipo 2",
        "modelo": "M2",
        "numero_serie": "SN2",
        "fecha_adquisicion": datetime.date(2023, 1, 2),
        "estado": "Mantenimiento",
    }

    # This is a simplified way; ideally, you'd use an equipamiento_service if it exists
    # For now, creating directly if the model allows, or using a basic insert.
    # This might need adjustment based on how Equipamiento is created/managed.
    # Let's assume Equipamiento can be created directly for test setup.

    # Check if 'created_at' and 'updated_at' are auto-generated or need to be supplied
    # For now, assuming they are auto-generated or have defaults

    equipamiento1 = Equipamiento(**eq1_data)
    equipamiento2 = Equipamiento(**eq2_data)

    db.add_all([equipamiento1, equipamiento2])
    await db.commit()
    await db.refresh(equipamiento1)
    await db.refresh(equipamiento2)
    return [equipamiento1, equipamiento2]


@pytest.mark.anyio
async def test_crear_servicio_valido(
    db: AsyncSession, setup_equipamientos: List[Equipamiento]
):
    equipamiento_ids = [eq.id for eq in setup_equipamientos]
    servicio_data = ServicioCreate(
        nombre="Servicio Test Valido",
        descripcion="Descripción del servicio",
        publico_objetivo="General",
        tarifa=100.50,
        equipamiento_ids=equipamiento_ids,
    )
    # The service function expects a dict, so convert Pydantic model
    servicio = await servicios_service.crear_servicio(
        db=db, data=servicio_data.model_dump(), equipamiento_ids=equipamiento_ids
    )

    assert servicio.id is not None
    assert servicio.nombre == "Servicio Test Valido"
    assert servicio.tarifa == 100.50
    assert len(servicio.equipamientos) == len(equipamiento_ids)


@pytest.mark.anyio
async def test_crear_servicio_tarifa_negativa_schema(
    db: AsyncSession, setup_equipamientos: List[Equipamiento]
):
    # Schema validation should catch this if pydantic model is used directly
    # For Pydantic v2, use model_validate, for v1 use constructor
    equipamiento_ids = [eq.id for eq in setup_equipamientos]
    with pytest.raises(
        ValueError
    ):  # Pydantic's ValidationError is a subclass of ValueError
        ServicioCreate(
            nombre="Servicio Tarifa Negativa",
            tarifa=-50.0,
            equipamiento_ids=equipamiento_ids,
        )


@pytest.mark.anyio
async def test_crear_servicio_tarifa_negativa_service_logic(
    db: AsyncSession, setup_equipamientos: List[Equipamiento]
):
    # Test the service layer's explicit check
    equipamiento_ids = [eq.id for eq in setup_equipamientos]
    servicio_data_dict = {
        "nombre": "Servicio Tarifa Negativa Logic",
        "tarifa": -50.0,
        # equipamiento_ids will be passed as a separate arg to crear_servicio
    }
    with pytest.raises(ValueError) as exc_info:
        await servicios_service.crear_servicio(
            db=db, data=servicio_data_dict, equipamiento_ids=equipamiento_ids
        )
    assert "La tarifa no puede ser negativa." in str(exc_info.value)


@pytest.mark.anyio
async def test_obtener_servicio(
    db: AsyncSession, setup_equipamientos: List[Equipamiento]
):
    equipamiento_ids = [eq.id for eq in setup_equipamientos]
    servicio_data = ServicioCreate(
        nombre="Servicio Para Obtener", tarifa=75.0, equipamiento_ids=equipamiento_ids
    )
    servicio_creado = await servicios_service.crear_servicio(
        db=db, data=servicio_data.model_dump(), equipamiento_ids=equipamiento_ids
    )

    servicio_obtenido = await servicios_service.obtener_servicio(
        db=db, sid=servicio_creado.id
    )
    assert servicio_obtenido is not None
    assert servicio_obtenido.id == servicio_creado.id
    assert servicio_obtenido.nombre == "Servicio Para Obtener"


@pytest.mark.anyio
async def test_actualizar_servicio(
    db: AsyncSession, setup_equipamientos: List[Equipamiento]
):
    equipamiento_ids = [eq.id for eq in setup_equipamientos]
    servicio_data = ServicioCreate(
        nombre="Servicio Original", tarifa=120.0, equipamiento_ids=equipamiento_ids
    )
    servicio_creado = await servicios_service.crear_servicio(
        db=db, data=servicio_data.model_dump(), equipamiento_ids=equipamiento_ids
    )

    # Note: ServicioUpdate schema is used by the route, service layer takes a dict
    datos_actualizacion: Dict[str, Any] = {
        "nombre": "Servicio Actualizado",
        "tarifa": 150.75,
    }
    servicio_actualizado = await servicios_service.actualizar_servicio(
        db=db, sid=servicio_creado.id, data=datos_actualizacion
    )
    assert servicio_actualizado is not None
    assert servicio_actualizado.nombre == "Servicio Actualizado"
    assert servicio_actualizado.tarifa == 150.75


@pytest.mark.anyio
async def test_actualizar_servicio_tarifa_negativa(
    db: AsyncSession, setup_equipamientos: List[Equipamiento]
):
    equipamiento_ids = [eq.id for eq in setup_equipamientos]
    servicio_data = ServicioCreate(
        nombre="Servicio Tarifa Original",
        tarifa=99.0,
        equipamiento_ids=equipamiento_ids,
    )
    servicio_creado = await servicios_service.crear_servicio(
        db=db, data=servicio_data.model_dump(), equipamiento_ids=equipamiento_ids
    )

    datos_actualizacion_invalidos: Dict[str, Any] = {"tarifa": -25.0}
    with pytest.raises(ValueError) as exc_info:
        await servicios_service.actualizar_servicio(
            db=db, sid=servicio_creado.id, data=datos_actualizacion_invalidos
        )
    assert "La tarifa no puede ser negativa." in str(exc_info.value)


@pytest.mark.anyio
async def test_eliminar_servicio(
    db: AsyncSession, setup_equipamientos: List[Equipamiento]
):
    equipamiento_ids = [int(eq.id) for eq in setup_equipamientos if eq.id is not None]
    servicio_data = ServicioCreate(
        nombre="Servicio a Eliminar", tarifa=50.0, equipamiento_ids=equipamiento_ids
    )
    servicio_creado = await servicios_service.crear_servicio(
        db=db, data=servicio_data.model_dump(), equipamiento_ids=equipamiento_ids
    )
    assert servicio_creado.id is not None
    await servicios_service.borrar_servicio(db=db, sid=int(servicio_creado.id))
    servicio_no_encontrado = await servicios_service.obtener_servicio(
        db=db, sid=int(servicio_creado.id)
    )
    assert servicio_no_encontrado is None


@pytest.mark.anyio
async def test_listar_servicios(
    db: AsyncSession, setup_equipamientos: List[Equipamiento]
):
    equipamiento_ids = [int(eq.id) for eq in setup_equipamientos if eq.id is not None]
    await servicios_service.crear_servicio(
        db=db,
        data=ServicioCreate(
            nombre="S1", tarifa=10, equipamiento_ids=equipamiento_ids[:1]
        ).model_dump(),
        equipamiento_ids=equipamiento_ids[:1],
    )
    await servicios_service.crear_servicio(
        db=db,
        data=ServicioCreate(
            nombre="S2", tarifa=20, equipamiento_ids=equipamiento_ids[1:]
        ).model_dump(),
        equipamiento_ids=equipamiento_ids[1:],
    )
    servicios = await servicios_service.listar_servicios(db=db, offset=0, limit=10)
    assert len(servicios) >= 2
    nombres_servicios = [s.nombre for s in servicios]
    assert "S1" in nombres_servicios
    assert "S2" in nombres_servicios

```

# tests/storage/test_local_repo.py

```py
import pytest
import asyncio
import os
from pathlib import Path
import aiofiles
from fastapi import UploadFile
from fastapi.responses import StreamingResponse
from app.storage import local_repo  # Import the module directly
from typing import AsyncGenerator, Any, cast
import io


@pytest.fixture
def mock_upload_dir(tmp_path: Path, monkeypatch):
    # Create a temporary directory for uploads
    mock_dir = tmp_path / "test_uploads"
    mock_dir.mkdir()
    # Monkeypatch the UPLOAD_DIR in the local_repo module
    monkeypatch.setattr(local_repo, "UPLOAD_DIR", str(mock_dir))
    return str(mock_dir)


# A more compliant mock for UploadFile
# Based on Starlette's UploadFile implementation for testing
class CompliantMockUploadFile:
    def __init__(self, filename: str, content: bytes, content_type: str = "text/plain"):
        self.file = io.BytesIO(content)
        self.filename = filename
        self.content_type = content_type
        self.spool_max_size = 1024 * 1024  # Default from Starlette
        self._content = content  # Keep a reference if needed

    async def read(self, size: int = -1) -> bytes:
        return self.file.read(size)

    async def write(self, data: bytes) -> None:  # write returns None in UploadFile
        # This mock doesn't really support writing back to the UploadFile object in a way that
        # local_repo.guardar would use. local_repo.guardar reads from it.
        # For a true file-like object that supports async write, aiofiles.os.wrap would be needed
        # but that's for wrapping sync file operations. Here, we just need to satisfy the interface.
        # The actual writing is done by aiofiles.open in local_repo.guardar.
        # So, this method in the mock might not be strictly necessary for these tests.
        # However, to match the signature:
        # self.file.write(data) # This would write to the BytesIO buffer if needed.
        pass

    async def seek(self, offset: int) -> None:  # seek returns None in UploadFile
        self.file.seek(offset)

    async def close(self) -> None:
        self.file.close()

    # Add a size property if your UploadFile usage relies on it
    @property
    def size(self) -> int:
        return len(self._content)


@pytest.mark.anyio
async def test_guardar_abrir_eliminar_archivo(mock_upload_dir):
    # 1. Guardar archivo
    test_content = b"Hello, world! This is a test file."
    # Cast the mock to UploadFile to satisfy the type checker for local_repo.guardar
    mock_file = cast(
        UploadFile,
        CompliantMockUploadFile(filename="test_file.txt", content=test_content),
    )

    # Ensure UPLOAD_DIR is the mocked one
    assert local_repo.UPLOAD_DIR == mock_upload_dir

    relative_file_path = await local_repo.guardar(mock_file)
    assert isinstance(relative_file_path, str)
    full_file_path = Path(mock_upload_dir) / relative_file_path
    assert full_file_path.exists()

    async with aiofiles.open(full_file_path, "rb") as f:
        saved_content = await f.read()
        assert saved_content == test_content

    # 2. Abrir archivo
    # Reset cursor for re-reading if necessary (though guardar should handle it)
    await mock_file.seek(0)

    response = await local_repo.abrir(relative_file_path)
    assert isinstance(response, StreamingResponse)
    assert response.media_type == "text/plain"  # Based on .txt extension

    # Consume the stream to verify content (optional, but good for testing)
    stream_content = b""
    async for chunk in response.body_iterator:
        if isinstance(chunk, str):  # Ensure we are dealing with bytes
            stream_content += chunk.encode("utf-8")
        else:
            stream_content += chunk
    assert stream_content == test_content

    # 3. Eliminar archivo
    await local_repo.eliminar(relative_file_path)
    assert not full_file_path.exists()


@pytest.mark.anyio
async def test_abrir_archivo_no_existente(mock_upload_dir):
    from fastapi import HTTPException

    with pytest.raises(HTTPException) as exc_info:
        await local_repo.abrir("non_existent_file.txt")
    assert exc_info.value.status_code == 404


@pytest.mark.anyio
async def test_eliminar_archivo_no_existente_no_error(mock_upload_dir):
    # Eliminar un archivo que no existe no debería lanzar un error
    try:
        await local_repo.eliminar("non_existent_file_for_deletion.txt")
    except Exception as e:
        pytest.fail(f"eliminar raised an exception unexpectedly: {e}")


@pytest.mark.anyio
async def test_guardar_archivo_sin_extension(mock_upload_dir):
    test_content = b"File with no extension"
    mock_file = cast(
        UploadFile,
        CompliantMockUploadFile(
            filename="testfile",
            content=test_content,
            content_type="application/octet-stream",
        ),
    )

    relative_file_path = await local_repo.guardar(mock_file)
    full_file_path = Path(mock_upload_dir) / relative_file_path
    assert full_file_path.exists()
    async with aiofiles.open(full_file_path, "rb") as f:
        saved_content = await f.read()
        assert saved_content == test_content

    response = await local_repo.abrir(relative_file_path)
    assert response.media_type == "application/octet-stream"

    await local_repo.eliminar(relative_file_path)
    assert not full_file_path.exists()

```

# uploads/209f0240-6c47-47e2-8a10-41ee4f52c618.txt

```txt
Este es un archivo de texto de prueba para el sistema de almacenamiento.

```

# uploads/77900414-b52b-4bf1-85cb-9c2f0acb4c68.png

This is a binary file of the type: Image

