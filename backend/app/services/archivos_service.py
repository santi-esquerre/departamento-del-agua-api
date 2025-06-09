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
