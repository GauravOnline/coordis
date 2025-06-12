"""
Core package initialization
"""

from core.bot import setup_bot
from core.registry import CommandRegistry

__all__ = ["CommandRegistry", "setup_bot"]
