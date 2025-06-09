from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.deps import get_async_session
from app.services import academico_service as svc
from app.services import archivos_service
from app.schemas.academico import (
    CarreraCreate,
    CarreraRead,
    CarreraUpdate,
    MateriaCreate,
    MateriaRead,
    MateriaUpdate,
    RequisitoCreate,
    RequisitoRead,
    RequisitoUpdate,
)
from app.routes.utils import not_found
from fastapi import Depends
from app.deps import get_current_admin

ADMIN = Depends(get_current_admin)

router = APIRouter(prefix="/academico", tags=["Académico"])

# Carreras


@router.post(
    "/carreras",
    response_model=CarreraRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[ADMIN],
)
async def create_carrera(
    carrera: CarreraCreate, db: AsyncSession = Depends(get_async_session)
):
    """Crear una nueva carrera"""
    try:
        return await svc.crear_carrera(db, carrera.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/carreras", response_model=List[CarreraRead])
async def read_all_carreras(
    offset: int = 0, limit: int = 100, db: AsyncSession = Depends(get_async_session)
):
    """Obtener lista paginada de carreras"""
    return await svc.listar_carreras(db, offset, limit)


@router.get("/carreras/{carrera_id}", response_model=CarreraRead)
async def read_carrera(carrera_id: int, db: AsyncSession = Depends(get_async_session)):
    """Obtener una carrera por su ID"""
    carrera = await svc.obtener_carrera(db, carrera_id)

    if not carrera:
        not_found("Carrera")

    return carrera


@router.put("/carreras/{carrera_id}", response_model=CarreraRead, dependencies=[ADMIN])
async def update_carrera(
    carrera_id: int,
    carrera_update: CarreraUpdate,
    db: AsyncSession = Depends(get_async_session),
):
    """Actualizar una carrera"""
    try:
        carrera = await svc.actualizar_carrera(
            db,
            carrera_id,
            carrera_update.model_dump(exclude_unset=False, exclude_none=True),
        )

        if not carrera:
            not_found("Carrera")

        return carrera
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch(
    "/carreras/{carrera_id}", response_model=CarreraRead, dependencies=[ADMIN]
)
async def partial_update_carrera(
    carrera_id: int,
    carrera_update: CarreraUpdate,
    db: AsyncSession = Depends(get_async_session),
):
    """Actualizar parcialmente una carrera"""
    try:
        carrera = await svc.actualizar_carrera(
            db,
            carrera_id,
            carrera_update.model_dump(exclude_unset=True, exclude_none=True),
        )

        if not carrera:
            not_found("Carrera")

        return carrera
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete(
    "/carreras/{carrera_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[ADMIN],
)
async def delete_carrera(
    carrera_id: int, db: AsyncSession = Depends(get_async_session)
):
    """Eliminar una carrera"""
    carrera = await svc.borrar_carrera(db, carrera_id)

    if not carrera:
        not_found("Carrera")

    # No content returned
    return None


# Materias


@router.post(
    "/materias",
    response_model=MateriaRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[ADMIN],
)
async def create_materia(
    materia: MateriaCreate, db: AsyncSession = Depends(get_async_session)
):
    """Crear una nueva materia"""
    try:
        return await svc.crear_materia(db, materia.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/materias", response_model=List[MateriaRead])
async def read_all_materias(
    offset: int = 0,
    limit: int = 100,
    carrera_id: Optional[int] = None,
    db: AsyncSession = Depends(get_async_session),
):
    """Obtener lista paginada de materias"""
    return await svc.listar_materias(db, offset, limit, carrera_id)


@router.get("/materias/{materia_id}", response_model=MateriaRead)
async def read_materia(materia_id: int, db: AsyncSession = Depends(get_async_session)):
    """Obtener una materia por su ID"""
    materia = await svc.obtener_materia(db, materia_id)

    if not materia:
        not_found("Materia")

    return materia


@router.put("/materias/{materia_id}", response_model=MateriaRead, dependencies=[ADMIN])
async def update_materia(
    materia_id: int,
    materia_update: MateriaUpdate,
    db: AsyncSession = Depends(get_async_session),
):
    """Actualizar una materia"""
    try:
        materia = await svc.actualizar_materia(
            db,
            materia_id,
            materia_update.model_dump(exclude_unset=False, exclude_none=True),
        )

        if not materia:
            not_found("Materia")

        return materia
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch(
    "/materias/{materia_id}", response_model=MateriaRead, dependencies=[ADMIN]
)
async def partial_update_materia(
    materia_id: int,
    materia_update: MateriaUpdate,
    db: AsyncSession = Depends(get_async_session),
):
    """Actualizar parcialmente una materia"""
    try:
        materia = await svc.actualizar_materia(
            db,
            materia_id,
            materia_update.model_dump(exclude_unset=True, exclude_none=True),
        )

        if not materia:
            not_found("Materia")

        return materia
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete(
    "/materias/{materia_id}", response_model=MateriaRead, dependencies=[ADMIN]
)
async def delete_materia(
    materia_id: int, db: AsyncSession = Depends(get_async_session)
):
    """Eliminar una materia"""
    materia = await svc.borrar_materia(db, materia_id)

    if not materia:
        not_found("Materia")

    return materia


@router.post("/materias/{materia_id}/programa", response_model=MateriaRead)
async def upload_programa_pdf(
    materia_id: int,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_async_session),
):
    """Subir un archivo PDF con el programa de la materia"""
    materia = await svc.obtener_materia(db, materia_id)

    if not materia:
        not_found("Materia")

    # Verificar que el archivo es un PDF
    if not file.content_type or "application/pdf" not in file.content_type.lower():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El archivo debe ser un PDF"
        )

    try:
        # Guardar el archivo
        archivo = await archivos_service.guardar_archivo(db, file)

        # Actualizar la referencia en la materia
        materia = await svc.actualizar_materia(
            db, materia_id, {"programa_pdf_url": archivo.ruta}
        )

        return materia
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/materias/{materia_id}/upload-pdf", response_model=MateriaRead)
async def upload_pdf_alias(
    materia_id: int,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_async_session),
):
    """Alias para subir un archivo PDF con el programa de la materia (para compatibilidad de tests)"""
    return await upload_programa_pdf(materia_id, file, db)


# Requisitos


@router.post(
    "/requisitos",
    response_model=RequisitoRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[ADMIN],
)
async def create_requisito(
    requisito: RequisitoCreate, db: AsyncSession = Depends(get_async_session)
):
    """Crear un nuevo requisito entre materias"""
    try:
        return await svc.crear_requisito(db, requisito.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/requisitos", response_model=List[RequisitoRead])
async def read_all_requisitos(
    materia_id: Optional[int] = None, db: AsyncSession = Depends(get_async_session)
):
    """Obtener lista de requisitos, opcionalmente filtrados por materia"""
    return await svc.listar_requisitos(db, materia_id)


@router.get("/requisitos/{requisito_id}", response_model=RequisitoRead)
async def read_requisito(
    requisito_id: int, db: AsyncSession = Depends(get_async_session)
):
    """Obtener un requisito por su ID"""
    requisito = await svc.obtener_requisito(db, requisito_id)

    if not requisito:
        not_found("Requisito")

    return requisito


@router.put(
    "/requisitos/{requisito_id}", response_model=RequisitoRead, dependencies=[ADMIN]
)
async def update_requisito(
    requisito_id: int,
    requisito_update: RequisitoUpdate,
    db: AsyncSession = Depends(get_async_session),
):
    """Actualizar un requisito"""
    try:
        requisito = await svc.actualizar_requisito(
            db,
            requisito_id,
            requisito_update.model_dump(exclude_unset=False, exclude_none=True),
        )

        if not requisito:
            not_found("Requisito")

        return requisito
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete(
    "/requisitos/{requisito_id}", response_model=RequisitoRead, dependencies=[ADMIN]
)
async def delete_requisito(
    requisito_id: int, db: AsyncSession = Depends(get_async_session)
):
    """Eliminar un requisito"""
    requisito = await svc.borrar_requisito(db, requisito_id)

    if not requisito:
        not_found("Requisito")

    return requisito
