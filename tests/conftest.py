# tests/conftest.py
import sys
import os
import pytest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from unittest.mock import AsyncMock, MagicMock
from db.base import init_db


# Automatically initialize database once per test session
@pytest.fixture(scope="session", autouse=True)
def initialize_database():
    init_db()

# Provides a mocked Discord context (ctx)
@pytest.fixture
def mock_ctx():
    ctx = AsyncMock()
    ctx.send = AsyncMock()
    ctx.author = MagicMock()
    ctx.author.name = "test_user"
    ctx.guild = None
    return ctx
