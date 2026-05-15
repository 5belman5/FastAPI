import pytest
import os

@pytest.mark.asyncio
async def test_get_posts_empty(client):
    response = await client.get("/posts/")
    assert response.status_code == 200
    assert response.json() == []

from src.api.dependencies import get_current_user
from src.infrastructure import models
from src.main import app
import pytest_asyncio

@pytest_asyncio.fixture
async def authorized_client(client):
    """Клиент с подменой авторизованного пользователя"""
    mock_user = models.User(id=1, username="testuser", email="test@test.com")
    app.dependency_overrides[get_current_user] = lambda: mock_user
    yield client
    app.dependency_overrides.pop(get_current_user, None)

@pytest.mark.asyncio
async def test_upload_image(authorized_client, db_session):
    # 1. Создаем пост для теста
    from src.infrastructure.models import Post
    post = Post(text="Пост для теста картинки", author_id=1)
    db_session.add(post)
    await db_session.commit()
    await db_session.refresh(post)

    # 2. Имитируем загрузку файла
    file_content = b"fake image content"
    files = {"file": ("test.jpg", file_content, "image/jpeg")}
    
    response = await authorized_client.post(f"/posts/{post.id}/image", files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert data["image"] is not None
    assert data["image"].endswith(".jpg")
    
    # Проверяем, что файл реально создался на диске
    image_path = f"media/{data['image']}"
    assert os.path.exists(image_path)
    
    # Чистим за собой
    if os.path.exists(image_path):
        os.remove(image_path)

@pytest.mark.asyncio
async def test_delete_image(authorized_client, db_session):
    # 1. Создаем пост с картинкой
    from src.infrastructure.models import Post
    filename = "test_to_delete.jpg"
    with open(f"media/{filename}", "wb") as f:
        f.write(b"content")
        
    post = Post(text="Пост с картинкой", author_id=1, image=filename)
    db_session.add(post)
    await db_session.commit()
    await db_session.refresh(post)

    # 2. Удаляем картинку через API
    response = await authorized_client.delete(f"/posts/{post.id}/image")
    
    assert response.status_code == 200
    assert response.json()["image"] is None
    assert not os.path.exists(f"media/{filename}")
