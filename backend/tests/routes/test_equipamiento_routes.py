import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_crear_equipamiento(client: AsyncClient, auth_headers):
    datos = {
        "nombre": "Bomba de agua",
        "marca": "Acme",
        "modelo": "X100",
        "fecha_adquisicion": "2023-01-01",
        "estado": "Operativo",
    }
    resp = await client.post("/equipamiento/", json=datos, headers=auth_headers)
    assert resp.status_code == 201
    data = resp.json()
    assert data["nombre"] == datos["nombre"]
    assert data["marca"] == datos["marca"]
    assert "id" in data


@pytest.mark.anyio
async def test_obtener_equipamiento_por_id(client: AsyncClient, auth_headers):
    datos = {
        "nombre": "Medidor de Caudal",
        "marca": "FlowTech",
    }
    resp = await client.post("/equipamiento/", json=datos, headers=auth_headers)
    eq_id = resp.json()["id"]

    resp = await client.get(f"/equipamiento/{eq_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == eq_id
    assert data["nombre"] == datos["nombre"]


@pytest.mark.anyio
async def test_actualizar_equipamiento(client: AsyncClient, auth_headers):
    datos = {"nombre": "Equipo Base"}
    resp = await client.post("/equipamiento/", json=datos, headers=auth_headers)
    eq_id = resp.json()["id"]

    update = {"estado": "Mantenimiento"}
    resp = await client.patch(
        f"/equipamiento/{eq_id}", json=update, headers=auth_headers
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["estado"] == update["estado"]
    assert data["id"] == eq_id


@pytest.mark.anyio
async def test_eliminar_equipamiento(client: AsyncClient, auth_headers):
    datos = {"nombre": "Equipo para borrar"}
    resp = await client.post("/equipamiento/", json=datos, headers=auth_headers)
    eq_id = resp.json()["id"]

    resp = await client.delete(f"/equipamiento/{eq_id}", headers=auth_headers)
    assert resp.status_code == 200

    resp = await client.get(f"/equipamiento/{eq_id}")
    assert resp.status_code == 404


@pytest.mark.anyio
async def test_listar_equipamiento(client: AsyncClient, auth_headers):
    datos = {"nombre": "Equipo listado"}
    await client.post("/equipamiento/", json=datos, headers=auth_headers)

    resp = await client.get("/equipamiento/")
    assert resp.status_code == 200
    lst = resp.json()
    assert isinstance(lst, list)
    assert any(item["nombre"] == datos["nombre"] for item in lst)
