import pytest

from src.main import greeting, index


@pytest.mark.asyncio
async def test_index():
    result = await index()
    print(result)
    assert result == "Hello World from MCP!"


@pytest.mark.asyncio
async def test_greeting():
    name = "TestUser"
    result = await greeting(name)
    print(result)
    assert result.startswith(f"Hello {name}")
