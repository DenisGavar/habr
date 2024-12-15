import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.mark.asyncio
async def test_add_item():
    """Тестируем добавление товара"""
    item_data = {"name": "Apple", "category": "fruits"}
    
    response = client.post("/api/items", json=item_data)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data  # Проверяем, что id присутствует
    assert data["status"] == "item_added"

