# tests/conftest.py
import sys
import os
import pytest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from unittest.mock import AsyncMock, MagicMock
from db.base import init_db

@pytest.fixture(scope="session", autouse=True)
def initialize_database():
    init_db()

@pytest.fixture
def mock_ctx():
    ctx = AsyncMock()
    # Create a mock author with a name and assign to ctx.author
    mock_author = MagicMock()
    mock_author.name = "test_user"
    ctx.author = mock_author
    ctx.send = AsyncMock()
    return ctx