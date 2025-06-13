import pytest
from datetime import date


@pytest.mark.anyio
async def test_publicacion_crud(client, auth_headers):
    # crear autor
    personal_data = {"nombre": "Autor", "email": "autor@example.com"}
    r = await client.post("/personal/", json=personal_data, headers=auth_headers)
    pid = r.json()["id"]

    data = {
        "titulo": "Investigation",
        "anio": 2024,
        "authors": [{"name": "Autor", "personal_id": pid}],
    }
    r = await client.post("/publicaciones/", json=data, headers=auth_headers)
    assert r.status_code == 201
    pub = r.json()
    pub_id = pub["id"]

    r = await client.get(f"/publicaciones/{pub_id}")
    assert r.status_code == 200

    r = await client.patch(
        f"/publicaciones/{pub_id}", json={"estado": "Publicado"}, headers=auth_headers
    )
    assert r.status_code == 200
    assert r.json()["estado"] == "Publicado"

    r = await client.delete(f"/publicaciones/{pub_id}", headers=auth_headers)
    assert r.status_code == 200
    r = await client.get(f"/publicaciones/{pub_id}")
    assert r.status_code == 404


@pytest.mark.anyio
async def test_publicacion_autor_invalido(client, auth_headers):
    data = {"titulo": "Bad", "anio": 2024, "authors": [{"name": "X", "personal_id": 9999}]}
    r = await client.post("/publicaciones/", json=data, headers=auth_headers)
    assert r.status_code == 404


@pytest.mark.anyio
async def test_publicacion_anio_invalido(client, auth_headers):
    data = {"titulo": "BadYear", "anio": 1800}
    r = await client.post("/publicaciones/", json=data, headers=auth_headers)
    assert r.status_code == 422
