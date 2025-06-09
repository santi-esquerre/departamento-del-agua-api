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
