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
