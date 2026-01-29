import pytest
from src.main import index, greeting

@pytest.mark.asyncio
async def test_index():
    result = await index()
    print(f"Result: {result}")
    assert result == "Hello World from MCP Inspector!"

@pytest.mark.asyncio
async def test_greeting():
    name = "TestUser"
    result = await greeting(name)
    print(result)
    assert result.startswith(f"Hello {name}")
