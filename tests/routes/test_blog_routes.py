import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_crear_blogpost(client: AsyncClient, auth_headers):
    blog_data = {
        "titulo": "Nuevas tecnologías en tratamiento de agua",
        "contenido": "Este es un contenido de prueba para el blog post sobre nuevas tecnologías",
        "autor": "Dr. Alejandro Martínez",
        "tags": "Tecnología,Tratamiento,Innovación",
    }

    response = await client.post("/blog/posts", json=blog_data, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["titulo"] == blog_data["titulo"]
    assert data["autor"] == blog_data["autor"]
    assert "Tecnología" in data["tags"]
    assert "id" in data


@pytest.mark.anyio
async def test_obtener_blogposts(client: AsyncClient, auth_headers):
    # First create a blog post to ensure there's data
    blog_data = {
        "titulo": "Conservación de acuíferos",
        "contenido": "Contenido sobre conservación de acuíferos",
        "autor": "Dra. Sofía López",
        "tags": "Conservación,Acuíferos",
    }
    await client.post("/blog/posts", json=blog_data, headers=auth_headers)

    # Now get all blog posts
    response = await client.get("/blog/posts", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


@pytest.mark.anyio
async def test_obtener_blogpost_por_id(client: AsyncClient, auth_headers):
    # First create a blog post to get its ID
    blog_data = {
        "titulo": "Impacto del cambio climático en recursos hídricos",
        "contenido": "Contenido sobre cambio climático y agua",
        "autor": "Dr. Fernando Ruiz",
        "tags": "Cambio Climático,Recursos Hídricos",
    }
    create_response = await client.post(
        "/blog/posts", json=blog_data, headers=auth_headers
    )
    created_blog = create_response.json()
    blog_id = created_blog["id"]

    # Now get the blog post by ID
    response = await client.get(f"/blog/posts/{blog_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == blog_id
    assert data["titulo"] == blog_data["titulo"]


@pytest.mark.anyio
async def test_actualizar_blogpost(client: AsyncClient, auth_headers):
    # First create a blog post to update
    blog_data = {
        "titulo": "Post para actualizar",
        "contenido": "Este contenido será actualizado",
        "autor": "Autor Original",
        "tags": "Categoría Original",
    }
    create_response = await client.post(
        "/blog/posts", json=blog_data, headers=auth_headers
    )
    created_blog = create_response.json()
    blog_id = created_blog["id"]

    # Now update the blog post
    update_data = {
        "titulo": "Post actualizado",
        "contenido": "Contenido actualizado",
        "tags": "Categoría Original,Nueva Categoría",
    }
    response = await client.patch(
        f"/blog/posts/{blog_id}", json=update_data, headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == blog_id
    assert data["titulo"] == update_data["titulo"]
    assert data["contenido"] == update_data["contenido"]
    assert "Nueva Categoría" in data["tags"]
    # Author should remain unchanged
    assert data["autor"] == blog_data["autor"]


@pytest.mark.anyio
async def test_eliminar_blogpost(client: AsyncClient, auth_headers):
    # First create a blog post to delete
    blog_data = {
        "titulo": "Post para eliminar",
        "contenido": "Este post será eliminado",
        "autor": "Autor de Prueba",
        "tags": "Prueba,Eliminación",
    }
    create_response = await client.post(
        "/blog/posts", json=blog_data, headers=auth_headers
    )
    created_blog = create_response.json()
    blog_id = created_blog["id"]

    # Now delete the blog post
    response = await client.delete(f"/blog/posts/{blog_id}", headers=auth_headers)
    assert response.status_code == 204

    # Verify it's deleted
    get_response = await client.get(f"/blog/posts/{blog_id}", headers=auth_headers)
    assert get_response.status_code == 404


@pytest.mark.anyio
async def test_buscar_blogposts_por_categoria(client: AsyncClient, auth_headers):
    # First create blog posts with specific categories
    await client.post(
        "/blog/posts",
        json={
            "titulo": "Post sobre categoría específica",
            "contenido": "Contenido de prueba",
            "autor": "Autor de Categoría",
            "tags": "Categoría Especial,Prueba",
        },
        headers=auth_headers,
    )

    # Now search for posts with that category
    response = await client.get(
        "/blog/posts/categoria/Categoría Especial", headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert all("Categoría Especial" in post["tags"] for post in data)


@pytest.mark.anyio
async def test_buscar_blogposts_por_autor(client: AsyncClient, auth_headers):
    # First create blog posts with specific author
    autor_especial = "Dr. Autor Especial"
    await client.post(
        "/blog/posts",
        json={
            "titulo": "Post de autor específico",
            "contenido": "Contenido de prueba",
            "autor": autor_especial,
            "tags": "Prueba",
        },
        headers=auth_headers,
    )

    # Now search for posts by that author
    response = await client.get(
        f"/blog/posts/autor/{autor_especial}", headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert all(post["autor"] == autor_especial for post in data)
