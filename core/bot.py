"""
Bot Setup

This module handles the setup and configuration of the Discord bot.
"""
import discord
from discord.ext import commands

from commands.ping_command import PingCommand
from core.registry import CommandRegistry
from commands.help_command import HelpCommand


def setup_bot():
    """
    Set up and configure the Discord bot.

    Returns:
        discord.ext.commands.Bot: Configured bot instance
    """
    # Set up intents
    intents = discord.Intents.default()
    intents.message_content = True

    # Create bot instance
    bot = commands.Bot(command_prefix='!', intents=intents)

    # Remove default help command
    bot.remove_command('help')

    # Create registry
    registry = CommandRegistry()

    # Register our help command
    help_cmd = HelpCommand()
    registry.register_command(help_cmd)

    # Register our ping command
    ping_cmd = PingCommand()
    registry.register_command(ping_cmd)

    # Add help command to bot
    @bot.command(name='help')
    async def help_command(ctx, role=None):
        await help_cmd.execute(ctx, role)

    # Add ping command to bot
    @bot.command(name='ping')
    async def ping_command(ctx, role=None):
        await ping_cmd.execute(ctx, role)

    return bot
