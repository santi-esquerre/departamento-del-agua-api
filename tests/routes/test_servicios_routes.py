import pytest
from datetime import date


@pytest.mark.anyio
async def test_servicio_crud(client, auth_headers):
    # crear equipamiento
    eq_resp = await client.post("/equipamiento/", json={"nombre": "EQ"}, headers=auth_headers)
    eq_id = eq_resp.json()["id"]

    data = {"nombre": "Serv", "tarifa": 10, "equipamiento_ids": [eq_id]}
    r = await client.post("/servicios/", json=data, headers=auth_headers)
    assert r.status_code == 201
    sid = r.json()["id"]

    r = await client.get(f"/servicios/{sid}")
    assert r.status_code == 200

    r = await client.patch(f"/servicios/{sid}", json={"tarifa": 20}, headers=auth_headers)
    assert r.status_code == 200
    assert r.json()["tarifa"] == 20

    r = await client.delete(f"/servicios/{sid}", headers=auth_headers)
    assert r.status_code == 200

    r = await client.get(f"/servicios/{sid}")
    assert r.status_code == 404


@pytest.mark.anyio
async def test_servicio_equipamiento_inexistente(client, auth_headers):
    data = {"nombre": "Bad", "equipamiento_ids": [9999]}
    r = await client.post("/servicios/", json=data, headers=auth_headers)
    assert r.status_code == 404
