import pytest
from httpx import AsyncClient
import os
import tempfile
from pathlib import Path


@pytest.mark.anyio
async def test_crear_carrera(client: AsyncClient, auth_headers):
    carrera_data = {
        "nombre": "Ingeniería Hidráulica",
        "descripcion": "Carrera especializada en recursos hídricos",
        "duracion_anios": 5,
    }

    response = await client.post(
        "/academico/carreras", json=carrera_data, headers=auth_headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["nombre"] == carrera_data["nombre"]
    assert data["duracion_anios"] == carrera_data["duracion_anios"]
    assert "id" in data


@pytest.mark.anyio
async def test_obtener_carreras(client: AsyncClient, auth_headers):
    # First create a carrera to ensure there's data
    carrera_data = {
        "nombre": "Ingeniería del Agua",
        "descripcion": "Especializada en recursos hídricos y su gestión",
        "duracion_anios": 4,
    }
    await client.post("/academico/carreras", json=carrera_data, headers=auth_headers)

    # Now get all carreras
    response = await client.get("/academico/carreras", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


@pytest.mark.anyio
async def test_obtener_carrera_por_id(client: AsyncClient, auth_headers):
    # First create a carrera to get its ID
    carrera_data = {
        "nombre": "Ingeniería Ambiental",
        "descripcion": "Enfocada en soluciones ambientales",
        "duracion_anios": 5,
    }
    create_response = await client.post(
        "/academico/carreras", json=carrera_data, headers=auth_headers
    )
    created_carrera = create_response.json()
    carrera_id = created_carrera["id"]

    # Now get the carrera by ID
    response = await client.get(
        f"/academico/carreras/{carrera_id}", headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == carrera_id
    assert data["nombre"] == carrera_data["nombre"]


@pytest.mark.anyio
async def test_actualizar_carrera(client: AsyncClient, auth_headers):
    # First create a carrera to update
    carrera_data = {
        "nombre": "Ingeniería Hidrológica",
        "descripcion": "Estudio de sistemas hidrológicos",
        "duracion_anios": 5,
    }
    create_response = await client.post(
        "/academico/carreras", json=carrera_data, headers=auth_headers
    )
    created_carrera = create_response.json()
    carrera_id = created_carrera["id"]

    # Now update the carrera
    update_data = {"nombre": "Ingeniería Hidrológica Avanzada", "duracion_anios": 6}
    response = await client.patch(
        f"/academico/carreras/{carrera_id}", json=update_data, headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == carrera_id
    assert data["nombre"] == update_data["nombre"]
    assert data["duracion_anios"] == update_data["duracion_anios"]
    # Description should remain unchanged
    assert data["descripcion"] == carrera_data["descripcion"]


@pytest.mark.anyio
async def test_eliminar_carrera(client: AsyncClient, auth_headers):
    # First create a carrera to delete
    carrera_data = {
        "nombre": "Carrera para eliminar",
        "descripcion": "Esta carrera será eliminada",
        "duracion_anios": 3,
    }
    create_response = await client.post(
        "/academico/carreras", json=carrera_data, headers=auth_headers
    )
    created_carrera = create_response.json()
    carrera_id = created_carrera["id"]

    # Now delete the carrera
    response = await client.delete(
        f"/academico/carreras/{carrera_id}", headers=auth_headers
    )
    assert response.status_code == 204

    # Verify it's deleted
    get_response = await client.get(
        f"/academico/carreras/{carrera_id}", headers=auth_headers
    )
    assert get_response.status_code == 404


@pytest.mark.anyio
async def test_crear_materia(client: AsyncClient, auth_headers):
    # First create a carrera for the materia
    carrera_data = {
        "nombre": "Ingeniería Civil para Materias",
        "descripcion": "Carrera para prueba de materias",
        "duracion_anios": 5,
    }
    carrera_response = await client.post(
        "/academico/carreras", json=carrera_data, headers=auth_headers
    )
    carrera = carrera_response.json()
    carrera_id = carrera["id"]

    # Now create a materia
    materia_data = {
        "nombre": "Hidráulica Básica",
        "codigo": "HID100",
        "descripcion": "Fundamentos de hidráulica",
        "creditos": 4,
        "semestre": 3,
        "id_carrera": carrera_id,
    }

    response = await client.post(
        "/academico/materias", json=materia_data, headers=auth_headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["nombre"] == materia_data["nombre"]
    assert data["id_carrera"] == carrera_id
    assert "id" in data


@pytest.mark.anyio
async def test_subir_pdf_materia(client: AsyncClient, auth_headers):
    # First create a carrera and materia
    carrera_response = await client.post(
        "/academico/carreras",
        json={
            "nombre": "Ingeniería para PDF",
            "descripcion": "Carrera para prueba de PDF",
            "duracion_anios": 5,
        },
        headers=auth_headers,
    )
    carrera = carrera_response.json()

    materia_response = await client.post(
        "/academico/materias",
        json={
            "nombre": "Materia con PDF",
            "codigo": "PDF101",
            "descripcion": "Para probar subida de PDF",
            "creditos": 4,
            "semestre": 3,
            "id_carrera": carrera["id"],
        },
        headers=auth_headers,
    )
    materia = materia_response.json()
    materia_id = materia["id"]

    # Create a temporary PDF file
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp.write(b"%PDF-1.5\nTest PDF content")
        tmp_path = tmp.name

    try:
        # Upload the PDF
        with open(tmp_path, "rb") as pdf_file:
            files = {"file": ("test.pdf", pdf_file, "application/pdf")}
            response = await client.post(
                f"/academico/materias/{materia_id}/upload-pdf",
                files=files,
                headers=auth_headers,
            )

        assert response.status_code == 200
        data = response.json()
        assert "programa_pdf_url" in data
        assert data["programa_pdf_url"].endswith(".pdf")

    finally:
        # Clean up the temporary file
        os.unlink(tmp_path)


@pytest.mark.anyio
async def test_crear_requisito(client: AsyncClient, auth_headers):
    # First create a carrera and dos materias
    carrera_response = await client.post(
        "/academico/carreras",
        json={
            "nombre": "Ingeniería para Requisitos",
            "descripcion": "Carrera para prueba de requisitos",
            "duracion_anios": 5,
        },
        headers=auth_headers,
    )
    carrera = carrera_response.json()
    carrera_id = carrera["id"]

    # Create first materia
    materia1_response = await client.post(
        "/academico/materias",
        json={
            "nombre": "Hidráulica Avanzada",
            "codigo": "HID200",
            "descripcion": "Materia avanzada",
            "creditos": 5,
            "semestre": 4,
            "id_carrera": carrera_id,
        },
        headers=auth_headers,
    )
    materia1 = materia1_response.json()

    # Create second materia
    materia2_response = await client.post(
        "/academico/materias",
        json={
            "nombre": "Hidráulica Básica",
            "codigo": "HID100",
            "descripcion": "Materia básica",
            "creditos": 4,
            "semestre": 3,
            "id_carrera": carrera_id,
        },
        headers=auth_headers,
    )
    materia2 = materia2_response.json()

    # Now create a requisito (materia2 is prerequisite for materia1)
    requisito_data = {
        "id_materia": materia1["id"],
        "id_materia_requisito": materia2["id"],
        "tipo": "prerequisito",
    }

    response = await client.post(
        "/academico/requisitos", json=requisito_data, headers=auth_headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["id_materia"] == materia1["id"]
    assert data["id_materia_requisito"] == materia2["id"]
    assert "id" in data
