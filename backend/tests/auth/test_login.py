import pytest


@pytest.mark.anyio
async def test_login_and_protected(client, db):
    from app.services.auth_service import create_admin

    await create_admin(db, "root", "secret")

    r = await client.post(
        "/auth/login", json={"username": "root", "password": "secret"}
    )
    assert r.status_code == 200
    token = r.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    r2 = await client.get("/personal/", headers=headers)
    assert r2.status_code == 200
