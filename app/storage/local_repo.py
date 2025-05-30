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
UPLOAD_DIR = os.environ.get("UPLOAD_DIR", "./uploads")


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
