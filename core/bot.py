# ruff: noqa: F811

"""
Bot Setup

This module handles the setup and configuration of the Discord bot.
"""

import discord
from discord.ext import commands, tasks

from commands.event_command import EventCommand
from commands.help_command import HelpCommand
from commands.home_command import HomeworkCommand
from commands.ping_command import PingCommand
from notify.notify import Notify
from core.registry import CommandRegistry


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
    bot = commands.Bot(command_prefix="!", intents=intents)

    # Remove default help command
    bot.remove_command("help")

    # Create registry
    registry = CommandRegistry()

    # Register our help command
    help_cmd = HelpCommand()
    registry.register_command(help_cmd)

    # Register our ping command
    ping_cmd = PingCommand()
    registry.register_command(ping_cmd)

    # Register our help command
    home_work = HomeworkCommand()
    registry.register_command(home_work)

    event_cmd = EventCommand()
    registry.register_command(event_cmd)

    # Add to bot
    @bot.command(name="event")
    async def event_command(ctx, *args):
        await event_cmd.execute(ctx, args)

    # Add help command to bot
    @bot.command(name="help")
    async def help_command(ctx, role=None):
        await help_cmd.execute(ctx, role)

    # Add ping command to bot
    @bot.command(name="ping")
    async def ping_command(ctx, role=None):
        await ping_cmd.execute(ctx, role)
        # Add ping command to bot

    @bot.command(name="hw")
    async def ping_command(ctx, role=None):
        await home_work.execute(ctx, role)
    
    notify: Notify = Notify()
    @tasks.loop(hours=1)
    async def notifier(ctx):
        # do notify
        notify.run_notify(ctx=ctx)
    
    @notifier.before_loop
    async def before_notifier(ctx):
        await ctx.wait_until_ready()

    return bot
