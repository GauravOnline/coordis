"""
Bot Setup

This module handles the setup and configuration of the Discord bot.
"""
import discord
from discord.ext import commands
from discord import client

from commands.ping_command import PingCommand
from core.registry import CommandRegistry
from commands.help_command import HelpCommand
from commands.event_command import EventCommand
from core.alarm import alarm

# Global Variables
default_alarm = 60  # Seconds before Due Date to Alert User
default_alarm_interval = 60  # Seconds between each check for Due Events
default_channel = ""

async def setup_bot():
    """
    Set up and configure the Discord bot.

    Returns:
        discord.ext.commands.Bot: Configured bot instance
    """

    # Read Config File
    with open("config.txt") as f:
        for line in f:
            print(line)
            if line.casefold().startswith("default_alarm".casefold()):
                default_alarm = int(line.split("=", 1)[1])
            elif line.casefold().startswith("default_alarm_interval".casefold()):
                default_alarm_interval = line.split("=", 1)[1].rstrip()
            elif line.casefold().startswith("default_channel".casefold()):
                default_channel = line.split("=", 1)[1].rstrip()

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


    event_cmd = EventCommand()
    registry.register_command(event_cmd)

    # Add to bot
    @bot.command(name='event')
    async def event_command(ctx, *args):
        await event_cmd.execute(ctx, args)

    # Add help command to bot
    @bot.command(name='help')
    async def help_command(ctx, role=None):
        await help_cmd.execute(ctx, role)

    # Add ping command to bot
    @bot.command(name='ping')
    async def ping_command(ctx, role=None):
        await ping_cmd.execute(ctx, role)
        # Add ping command to bot

    @bot.event
    async def on_ready():
        channel = discord.utils.get(client.get_all_channels(), name=default_channel)
        if channel:
            await alarm(channel)
        else:
            print(f"Channel '{default_channel}' not found.")

    return bot
