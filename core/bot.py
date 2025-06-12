"""
Bot Setup

This module handles the setup and configuration of the Discord bot.
"""

import discord
from discord.ext import commands, tasks

from commands.event_command import EventCommand
from commands.help_command import HelpCommand
from commands.ping_command import PingCommand
from core.registry import CommandRegistry
from notify.notify import Notify


def setup_bot():
    """
    Set up and configure the Discord bot.

    Returns:
        discord.ext.commands.Bot: Configured bot instance
    """
    # Global Variables
    default_alarm = 0
    default_channel = ""
    # Read Config File
    with open("config.txt") as f:
        for line in f:
            print(line)
            if line.casefold().startswith("default_alarm".casefold()):
                default_alarm = int(line.split("=", 1)[1])
            elif line.casefold().startswith("default_channel".casefold()):
                default_channel = line.split("=", 1)[1].rstrip()

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

    notify: Notify = Notify()

    # @tasks.loop(hours=1)
    @tasks.loop(minutes=1)
    async def notifier(ctx):
        # do notify
        await notify.run_notify(ctx)

    @bot.listen()
    async def on_ready():
        _chans = [
            chan
            for chan in [
                cc for cc in bot.get_all_channels() if cc.name == "Text Channels"
            ][0].text_channels
            if chan.name in [default_channel, "general"]
        ]
        notifier.start(
            _chans[0]
            if len(_chans) == 1
            else [chan for chan in _chans if chan == default_channel][0]
        )

    return bot
