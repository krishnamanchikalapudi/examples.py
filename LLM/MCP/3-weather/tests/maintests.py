import json

import httpx
import pytest


BASE_URL = "http://127.0.0.1:8000"
SESSION_ID = "test_session_12345"


@pytest.fixture(scope="module")
async def initialize_session():
    """Initialize MCP session before running tests"""
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            f"{BASE_URL}/messages/?session_id={SESSION_ID}",
            headers={"Content-Type": "application/json"},
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {"name": "test-client", "version": "1.0"},
                },
            },
        )
        assert response.status_code == 200
        yield


@pytest.mark.asyncio
async def test_index_via_http(initialize_session):
    """Test index tool via HTTP request"""
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            f"{BASE_URL}/messages/?session_id={SESSION_ID}",
            headers={"Content-Type": "application/json"},
            json={
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {"name": "index", "arguments": {}},
            },
        )
        assert response.status_code == 200
        data = response.json()
        print(f"Index response: {json.dumps(data, indent=2)}")
        
        # Check for successful response
        assert "error" not in data, f"Error in response: {data.get('error')}"
        assert "result" in data, "No result in response"
        
        # Extract text from result (FastMCP wraps string returns in content array)
        result = data["result"]
        if isinstance(result, dict) and "content" in result:
            content = result["content"]
            if isinstance(content, list) and len(content) > 0:
                result_text = content[0].get("text", "")
            else:
                result_text = str(result)
        else:
            result_text = str(result)
        
        assert "Hello World from MCP" in result_text
        assert len(result_text) > 0


@pytest.mark.asyncio
async def test_greeting_via_http(initialize_session):
    """Test greeting tool via HTTP request"""
    name = "TestUser"
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            f"{BASE_URL}/messages/?session_id={SESSION_ID}",
            headers={"Content-Type": "application/json"},
            json={
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/call",
                "params": {"name": "greeting", "arguments": {"name": name}},
            },
        )
        assert response.status_code == 200
        data = response.json()
        print(f"Greeting response: {json.dumps(data, indent=2)}")
        
        # Check for successful response
        assert "error" not in data, f"Error in response: {data.get('error')}"
        assert "result" in data, "No result in response"
        
        # Extract text from result
        result = data["result"]
        if isinstance(result, dict) and "content" in result:
            content = result["content"]
            if isinstance(content, list) and len(content) > 0:
                result_text = content[0].get("text", "")
            else:
                result_text = str(result)
        else:
            result_text = str(result)
        
        assert f"Hello {name}" in result_text
        assert len(result_text) > 0


@pytest.mark.asyncio
async def test_weather_via_http(initialize_session):
    """Test weather tool via HTTP request"""
    city = "San Francisco"
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            f"{BASE_URL}/messages/?session_id={SESSION_ID}",
            headers={"Content-Type": "application/json"},
            json={
                "jsonrpc": "2.0",
                "id": 4,
                "method": "tools/call",
                "params": {"name": "weather", "arguments": {"city": city}},
            },
        )
        assert response.status_code == 200
        data = response.json()
        print(f"Weather response: {json.dumps(data, indent=2)}")
        
        # Check for successful response (weather API might fail, so we check for response structure)
        assert "result" in data or "error" in data, "No result or error in response"
        
        if "error" not in data and "result" in data:
            # Extract text from result
            result = data["result"]
            if isinstance(result, dict) and "content" in result:
                content = result["content"]
                if isinstance(content, list) and len(content) > 0:
                    result_text = content[0].get("text", "")
                else:
                    result_text = str(result)
            else:
                result_text = str(result)
            
            # Weather response should contain city name or weather-related text
            assert city in result_text or "weather" in result_text.lower() or "error" in result_text.lower()
            assert len(result_text) > 0


@pytest.mark.asyncio
async def test_index_web_endpoint():
    """Test web endpoint via HTTP GET request"""
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(f"{BASE_URL}/")
        assert response.status_code == 200
        assert "Hello World from MCP" in response.text
        print(f"Web endpoint response: {response.text}")


@pytest.mark.asyncio
async def test_index_web_endpoint_with_params():
    """Test web endpoint with query parameters via HTTP GET request"""
    name = "TestUser"
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(f"{BASE_URL}/?name={name}")
        assert response.status_code == 200
        assert name in response.text
        assert "Hello" in response.text
        print(f"Web endpoint with params response: {response.text}")
