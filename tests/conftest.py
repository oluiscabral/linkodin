"""Test configuration and fixtures."""
import pytest
import asyncio
from typing import AsyncGenerator

# Configure asyncio for pytest
pytest_plugins = ('pytest_asyncio',)


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def async_setup() -> AsyncGenerator[None, None]:
    """Setup for async tests."""
    # Setup code here if needed
    yield
    # Cleanup code here if needed