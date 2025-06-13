import pytest


@pytest.mark.anyio
async def test_subscribe_and_notify(client, db, monkeypatch, auth_headers):
    sent = {}

    async def fake_send(to, sub, html):
        sent[to] = (sub, html)

    # Parchear el servicio de email
    monkeypatch.setattr("app.routes.blog.send_html", fake_send)

    # Suscribir
    r = await client.post("/suscriptores/", json={"email": "test@example.com"})
    assert r.status_code == 201

    # Crear post publicado
    post_data = {
        "titulo": "Demo",
        "contenido": "<p>hola</p>",
        "publicado": True,
    }
    await client.post("/blog/posts", json=post_data, headers=auth_headers)

    assert "test@example.com" in sent
    assert sent["test@example.com"][0] == "Demo"

@pytest.mark.anyio
async def test_subscriber_duplicate_email(client):
    r1 = await client.post("/suscriptores/", json={"email": "dup@example.com"})
    assert r1.status_code == 201
    r2 = await client.post("/suscriptores/", json={"email": "dup@example.com"})
    assert r2.status_code == 409
