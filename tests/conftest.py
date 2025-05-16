# tests/conftest.py
import sys
import os
import pytest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from unittest.mock import AsyncMock
from core.registry import CommandRegistry
from db.base import init_db

@pytest.fixture(scope="session", autouse=True)
def initialize_database():
    init_db()

@pytest.fixture
def mock_ctx():
    ctx = AsyncMock()
    ctx.send = AsyncMock()
    return ctx