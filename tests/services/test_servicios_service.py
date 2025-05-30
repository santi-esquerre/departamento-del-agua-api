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
        db=db, data=servicio_data.model_dump(), equipamiento_ids=equipamiento_ids  # type: ignore # type: ignore
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
            db=db, data=servicio_data_dict, equipamiento_ids=equipamiento_ids  # type: ignore
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
        db=db, data=servicio_data.model_dump(), equipamiento_ids=equipamiento_ids  # type: ignore
    )

    servicio_obtenido = await servicios_service.obtener_servicio(
        db=db, sid=servicio_creado.id  # type: ignore
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
        db=db, data=servicio_data.model_dump(), equipamiento_ids=equipamiento_ids  # type: ignore
    )

    # Note: ServicioUpdate schema is used by the route, service layer takes a dict
    datos_actualizacion: Dict[str, Any] = {
        "nombre": "Servicio Actualizado",
        "tarifa": 150.75,
    }
    servicio_actualizado = await servicios_service.actualizar_servicio(
        db=db, sid=servicio_creado.id, data=datos_actualizacion  # type: ignore
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
        db=db, data=servicio_data.model_dump(), equipamiento_ids=equipamiento_ids  # type: ignore
    )

    datos_actualizacion_invalidos: Dict[str, Any] = {"tarifa": -25.0}
    with pytest.raises(ValueError) as exc_info:
        await servicios_service.actualizar_servicio(
            db=db, sid=servicio_creado.id, data=datos_actualizacion_invalidos  # type: ignore
        )
    assert "La tarifa no puede ser negativa." in str(exc_info.value)


@pytest.mark.anyio
async def test_eliminar_servicio(
    db: AsyncSession, setup_equipamientos: List[Equipamiento]
):
    equipamiento_ids = [int(eq.id) for eq in setup_equipamientos if eq.id is not None]
    servicio_data = ServicioCreate(
        nombre="Servicio a Eliminar", tarifa=50.0, equipamiento_ids=equipamiento_ids  # type: ignore
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
            nombre="S1", tarifa=10, equipamiento_ids=equipamiento_ids[:1]  # type: ignore
        ).model_dump(),
        equipamiento_ids=equipamiento_ids[:1],
    )
    await servicios_service.crear_servicio(
        db=db,
        data=ServicioCreate(
            nombre="S2", tarifa=20, equipamiento_ids=equipamiento_ids[1:]  # type: ignore
        ).model_dump(),
        equipamiento_ids=equipamiento_ids[1:],
    )
    servicios = await servicios_service.listar_servicios(db=db, offset=0, limit=10)
    assert len(servicios) >= 2
    nombres_servicios = [s.nombre for s in servicios]
    assert "S1" in nombres_servicios
    assert "S2" in nombres_servicios
