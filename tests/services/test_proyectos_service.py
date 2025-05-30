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
