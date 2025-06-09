import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)  # For type hinting client fixture if needed
from app.models.models import Personal  # To check response structure
from app.schemas.personal import PersonalCreate, PersonalUpdate  # For request payloads


@pytest.mark.anyio
async def test_create_and_get_personal(
    client: AsyncClient, db: AsyncSession, auth_headers
):
    # Create Personal
    personal_data = PersonalCreate(
        nombre="Ana De Armas",
        email="ana.dearmas@example.com",
    )
    response = await client.post(
        "/personal/", json=personal_data.model_dump(), headers=auth_headers
    )
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
async def test_create_personal_email_invalido(client: AsyncClient, auth_headers):
    personal_data = {
        "nombre": "Email Invalido",
        "email": "emailinvalido",  # Invalid email format
    }
    response = await client.post("/personal/", json=personal_data, headers=auth_headers)
    assert (
        response.status_code == 422
    )  # Unprocessable Entity for Pydantic validation errors
    # Optionally, check the error detail
    # error_detail = response.json()["detail"][0]
    # assert error_detail["type"] == "value_error.email"


@pytest.mark.anyio
async def test_get_personal_no_existente(client: AsyncClient, auth_headers):
    response = await client.get(
        "/personal/999999", headers=auth_headers
    )  # Assuming 999999 does not exist
    assert response.status_code == 404, response.text


@pytest.mark.anyio
async def test_update_personal(client: AsyncClient, db: AsyncSession, auth_headers):
    # First, create a personal record to update
    initial_data = PersonalCreate(
        nombre="Usuario Original", email="original@example.com"
    )
    response = await client.post(
        "/personal/", json=initial_data.model_dump(), headers=auth_headers
    )
    assert response.status_code == 201
    personal_id = response.json()["id"]

    # Now, update it
    update_data = PersonalUpdate(nombre="Usuario Actualizado")
    response = await client.put(
        f"/personal/{personal_id}",
        json=update_data.model_dump(exclude_unset=True),
        headers=auth_headers,
    )
    assert response.status_code == 200, response.text
    updated_personal_data = response.json()
    assert updated_personal_data["nombre"] == update_data.nombre
    assert (
        updated_personal_data["email"] == initial_data.email
    )  # Email should remain unchanged


@pytest.mark.anyio
async def test_update_personal_no_existente(client: AsyncClient, auth_headers):
    update_data = PersonalUpdate(nombre="No Existe")
    response = await client.put(
        "/personal/999999",
        json=update_data.model_dump(exclude_unset=True),
        headers=auth_headers,
    )
    assert response.status_code == 404, response.text


@pytest.mark.anyio
async def test_delete_personal(client: AsyncClient, db: AsyncSession, auth_headers):
    # Create a personal record to delete
    personal_data = PersonalCreate(nombre="Para Borrar", email="borrar@example.com")
    response = await client.post(
        "/personal/", json=personal_data.model_dump(), headers=auth_headers
    )
    assert response.status_code == 201
    personal_id = response.json()["id"]

    # Delete it
    response = await client.delete(f"/personal/{personal_id}", headers=auth_headers)
    assert response.status_code == 200, response.text
    deleted = response.json()
    assert deleted["id"] == personal_id
    assert deleted["fecha_baja"] is not None

    # Verify soft-deleted: GET returns the object with fecha_baja set
    response = await client.get(f"/personal/{personal_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["fecha_baja"] is not None


@pytest.mark.anyio
async def test_delete_personal_no_existente(client: AsyncClient, auth_headers):
    response = await client.delete("/personal/999999", headers=auth_headers)
    assert response.status_code == 404, response.text


@pytest.mark.anyio
async def test_list_personal(client: AsyncClient, db: AsyncSession, auth_headers):
    # Create a couple of entries to ensure there's data
    await client.post(
        "/personal/",
        json=PersonalCreate(nombre="Persona A", email="a@example.com").model_dump(),
        headers=auth_headers,
    )
    await client.post(
        "/personal/",
        json=PersonalCreate(nombre="Persona B", email="b@example.com").model_dump(),
        headers=auth_headers,
    )

    response = await client.get("/personal/")
    assert response.status_code == 200
    personal_list = response.json()
    assert isinstance(personal_list, list)
    assert len(personal_list) >= 2  # Check if at least the two created are present

    nombres = [p["nombre"] for p in personal_list]
    assert "Persona A" in nombres
    assert "Persona B" in nombres
