import pytest
from datetime import date, timedelta


@pytest.mark.anyio
async def test_proyecto_crud_flow(client, auth_headers):
    data = {"nombre": "P1", "fecha_inicio": date.today().isoformat()}
    r = await client.post("/proyectos/", json=data, headers=auth_headers)
    assert r.status_code == 201
    proyecto = r.json()
    pid = proyecto["id"]

    r = await client.get(f"/proyectos/{pid}")
    assert r.status_code == 200

    update_payload = {"nombre": "P1", "financiador": "ACME"}
    r = await client.put(f"/proyectos/{pid}", json=update_payload, headers=auth_headers)
    assert r.status_code == 200
    assert r.json()["financiador"] == "ACME"

    r = await client.delete(f"/proyectos/{pid}", headers=auth_headers)
    assert r.status_code == 200
    r = await client.get(f"/proyectos/{pid}")
    assert r.status_code == 404


@pytest.mark.anyio
async def test_proyecto_fecha_invalida(client, auth_headers):
    today = date.today()
    data = {
        "nombre": "BadDates",
        "fecha_inicio": today.isoformat(),
        "fecha_fin": (today - timedelta(days=1)).isoformat(),
    }
    r = await client.post("/proyectos/", json=data, headers=auth_headers)
    assert r.status_code == 422

@pytest.mark.anyio
async def test_proyecto_asignar_personal(client, auth_headers):
    # create personal
    p_resp = await client.post("/personal/", json={"nombre": "Ana", "email": "ana@example.com"}, headers=auth_headers)
    personal_id = p_resp.json()["id"]
    # create proyecto
    proj_resp = await client.post("/proyectos/", json={"nombre": "PP"}, headers=auth_headers)
    proj_id = proj_resp.json()["id"]
    # assign
    items = [{"personal_id": personal_id, "rol": "Investigador"}]
    resp = await client.post(f"/proyectos/{proj_id}/personal", json=items, headers=auth_headers)
    assert resp.status_code == 201
    data = resp.json()
    assert data[0]["personal_id"] == personal_id
