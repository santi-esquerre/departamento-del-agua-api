import io
import pytest
from pathlib import Path
from app.storage import local_repo


@pytest.fixture
def patch_upload_dir(tmp_path, monkeypatch):
    upload_dir = tmp_path / "uploads"
    upload_dir.mkdir()
    monkeypatch.setattr(local_repo, "UPLOAD_DIR", str(upload_dir))

    def noawait(*args, **kwargs):
        return None

    monkeypatch.setattr(local_repo, "eliminar", noawait)
    return upload_dir


@pytest.mark.anyio
async def test_upload_list_download_delete_file(client, auth_headers, patch_upload_dir):
    content = b"hello world"
    files = {"file": ("hello.txt", io.BytesIO(content), "text/plain")}
    resp = await client.post("/archivos/upload", files=files, headers=auth_headers)
    assert resp.status_code == 201
    data = resp.json()
    assert "id" in data and data["ruta"]
    file_id = data["id"]

    # listing
    resp = await client.get("/archivos/files/", headers=auth_headers)
    assert resp.status_code == 200
    assert any(item["id"] == file_id for item in resp.json())

    # download
    resp = await client.get(f"/archivos/download/{file_id}")
    assert resp.status_code == 200
    body = resp.content
    assert body == content

    # delete
    resp = await client.delete(f"/archivos/files/{file_id}", headers=auth_headers)
    assert resp.status_code == 200

    resp = await client.get(f"/archivos/download/{file_id}")
    assert resp.status_code == 404
