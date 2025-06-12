#!/usr/bin/env python3
import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError


def main():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("❌ La variable DATABASE_URL no está definida.")
        sys.exit(1)

    # Si el URL usa asyncpg, reemplazamos para usar driver sync
    if db_url.startswith("postgresql+asyncpg://"):
        sync_url = db_url.replace("postgresql+asyncpg://", "postgresql://", 1)
        print("🔄 Usando URL síncrono para migración:", sync_url)
        db_url = sync_url

    # Creamos un engine síncrono
    engine = create_engine(db_url, future=True)

    # SQL para listar columnas sin zona
    list_sql = """
    SELECT table_schema, table_name, column_name
      FROM information_schema.columns
     WHERE data_type = 'timestamp without time zone'
       AND table_schema NOT IN ('information_schema','pg_catalog');
    """

    try:
        with engine.begin() as conn:
            cols = conn.execute(text(list_sql)).all()
            if not cols:
                print(
                    "✅ No se encontraron columnas de tipo TIMESTAMP WITHOUT TIME ZONE."
                )
                return

            for schema, table, column in cols:
                full_table = f'"{schema}"."{table}"'
                stmt = f"""
                ALTER TABLE {full_table}
                ALTER COLUMN "{column}"
                TYPE TIMESTAMP WITH TIME ZONE
                USING "{column}" AT TIME ZONE 'UTC';
                """
                print(f"🔄 Migrando {schema}.{table}.{column} → timestamptz")
                conn.execute(text(stmt))

            print("✅ Todas las columnas migradas a TIMESTAMP WITH TIME ZONE.")
    except SQLAlchemyError as e:
        print("❌ Error al migrar columnas:", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
