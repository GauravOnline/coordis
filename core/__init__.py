"""
Core package initialization
"""
from core.registry import CommandRegistry
from core.bot import setup_bot

__all__ = ['CommandRegistry', 'setup_bot']