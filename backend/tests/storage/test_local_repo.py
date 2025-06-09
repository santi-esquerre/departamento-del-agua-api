import pytest
import asyncio
import os
from pathlib import Path
import aiofiles
from fastapi import UploadFile
from fastapi.responses import StreamingResponse
from app.storage import local_repo  # Import the module directly
from typing import AsyncGenerator, Any, cast
import io


@pytest.fixture
def mock_upload_dir(tmp_path: Path, monkeypatch):
    # Create a temporary directory for uploads
    mock_dir = tmp_path / "test_uploads"
    mock_dir.mkdir()
    # Monkeypatch the UPLOAD_DIR in the local_repo module
    monkeypatch.setattr(local_repo, "UPLOAD_DIR", str(mock_dir))
    return str(mock_dir)


# A more compliant mock for UploadFile
# Based on Starlette's UploadFile implementation for testing
class CompliantMockUploadFile:
    def __init__(self, filename: str, content: bytes, content_type: str = "text/plain"):
        self.file = io.BytesIO(content)
        self.filename = filename
        self.content_type = content_type
        self.spool_max_size = 1024 * 1024  # Default from Starlette
        self._content = content  # Keep a reference if needed

    async def read(self, size: int = -1) -> bytes:
        return self.file.read(size)

    async def write(self, data: bytes) -> None:  # write returns None in UploadFile
        # This mock doesn't really support writing back to the UploadFile object in a way that
        # local_repo.guardar would use. local_repo.guardar reads from it.
        # For a true file-like object that supports async write, aiofiles.os.wrap would be needed
        # but that's for wrapping sync file operations. Here, we just need to satisfy the interface.
        # The actual writing is done by aiofiles.open in local_repo.guardar.
        # So, this method in the mock might not be strictly necessary for these tests.
        # However, to match the signature:
        # self.file.write(data) # This would write to the BytesIO buffer if needed.
        pass

    async def seek(self, offset: int) -> None:  # seek returns None in UploadFile
        self.file.seek(offset)

    async def close(self) -> None:
        self.file.close()

    # Add a size property if your UploadFile usage relies on it
    @property
    def size(self) -> int:
        return len(self._content)


@pytest.mark.anyio
async def test_guardar_abrir_eliminar_archivo(mock_upload_dir):
    # 1. Guardar archivo
    test_content = b"Hello, world! This is a test file."
    # Cast the mock to UploadFile to satisfy the type checker for local_repo.guardar
    mock_file = cast(
        UploadFile,
        CompliantMockUploadFile(filename="test_file.txt", content=test_content),
    )

    # Ensure UPLOAD_DIR is the mocked one
    assert local_repo.UPLOAD_DIR == mock_upload_dir

    relative_file_path = await local_repo.guardar(mock_file)
    assert isinstance(relative_file_path, str)
    full_file_path = Path(mock_upload_dir) / relative_file_path
    assert full_file_path.exists()

    async with aiofiles.open(full_file_path, "rb") as f:
        saved_content = await f.read()
        assert saved_content == test_content

    # 2. Abrir archivo
    # Reset cursor for re-reading if necessary (though guardar should handle it)
    await mock_file.seek(0)

    response = await local_repo.abrir(relative_file_path)
    assert isinstance(response, StreamingResponse)
    assert response.media_type == "text/plain"  # Based on .txt extension

    # Consume the stream to verify content (optional, but good for testing)
    stream_content = b""
    async for chunk in response.body_iterator:
        if isinstance(chunk, str):  # Ensure we are dealing with bytes
            stream_content += chunk.encode("utf-8")
        else:
            stream_content += chunk
    assert stream_content == test_content

    # 3. Eliminar archivo
    await local_repo.eliminar(relative_file_path)
    assert not full_file_path.exists()


@pytest.mark.anyio
async def test_abrir_archivo_no_existente(mock_upload_dir):
    from fastapi import HTTPException

    with pytest.raises(HTTPException) as exc_info:
        await local_repo.abrir("non_existent_file.txt")
    assert exc_info.value.status_code == 404


@pytest.mark.anyio
async def test_eliminar_archivo_no_existente_no_error(mock_upload_dir):
    # Eliminar un archivo que no existe no debería lanzar un error
    try:
        await local_repo.eliminar("non_existent_file_for_deletion.txt")
    except Exception as e:
        pytest.fail(f"eliminar raised an exception unexpectedly: {e}")


@pytest.mark.anyio
async def test_guardar_archivo_sin_extension(mock_upload_dir):
    test_content = b"File with no extension"
    mock_file = cast(
        UploadFile,
        CompliantMockUploadFile(
            filename="testfile",
            content=test_content,
            content_type="application/octet-stream",
        ),
    )

    relative_file_path = await local_repo.guardar(mock_file)
    full_file_path = Path(mock_upload_dir) / relative_file_path
    assert full_file_path.exists()
    async with aiofiles.open(full_file_path, "rb") as f:
        saved_content = await f.read()
        assert saved_content == test_content

    response = await local_repo.abrir(relative_file_path)
    assert response.media_type == "application/octet-stream"

    await local_repo.eliminar(relative_file_path)
    assert not full_file_path.exists()
