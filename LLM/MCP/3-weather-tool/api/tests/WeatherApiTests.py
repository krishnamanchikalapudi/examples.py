import pytest
from fastapi.testclient import TestClient

from src.WeatherApi import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


def test_root_endpoint(client):
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Weather API" in data["message"]


def test_get_city_weather(client):
    """Test getting weather for a city"""
    response = client.get("/city/San%20Francisco")
    assert response.status_code == 200
    data = response.json()
    assert "city" in data
    assert "temperature" in data
    assert "description" in data
    assert data["city"] == "San Francisco"


def test_get_city_weather_invalid_city(client):
    """Test getting weather for an invalid city"""
    response = client.get("/city/InvalidCity12345")
    assert response.status_code == 200
    data = response.json()
    assert "city" in data
    assert data["city"] == "InvalidCity12345"
    # The description might contain an error message or "N/A"
    assert "description" in data


@pytest.mark.asyncio
async def test_get_city_weather_async():
    """Test getting weather for a city using async client"""
    from httpx import AsyncClient, ASGITransport
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/city/San%20Francisco")
        assert response.status_code == 200
        data = response.json()
        assert "city" in data
        assert "temperature" in data
        assert "description" in data
        assert data["city"] == "San Francisco" 
