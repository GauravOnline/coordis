"""
Bot Setup

This module handles the setup and configuration of the Discord bot.
"""
import discord
from discord.ext import commands

from commands.ping_command import PingCommand
from core.registry import CommandRegistry
from commands.help_command import HelpCommand
from commands.event_command import EventCommand
from core.alarm import alarm
from db.base import get_session
from services.event_service import EventService
from ui import event_ui

# Global Variables
default_alarm_margin = 60  # Seconds before Due Date to Alert User
default_alarm_interval = 60  # Seconds between each check for Due Events
default_channel = ""

def setup_bot():
    """
    Set up and configure the Discord bot.

    Returns:
        discord.ext.commands.Bot: Configured bot instance
    """

    # Read Config File
    with open("config.txt") as f:
        for line in f:
            print(line)
            if line.casefold().startswith("default_alarm_margin".casefold()):
                global default_alarm_margin
                default_alarm_margin = int(line.split("=", 1)[1])
            elif line.casefold().startswith("default_alarm_interval".casefold()):
                global default_alarm_interval
                default_alarm_interval = int(line.split("=", 1)[1].rstrip())
            elif line.casefold().startswith("default_channel".casefold()):
                global default_channel
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

    # Start Alarm Async Event once bot is in ready state
    @bot.event
    async def on_ready():
        channel = discord.utils.get(bot.get_all_channels(), name=default_channel)
        if channel:
            await alarm(channel, default_alarm_margin, default_alarm_interval)
        else:
            print(f"Channel '{default_channel}' not found.")

    @bot.event
    async def on_reaction_add(reaction, user):
        if user == bot.user:
            return  # ignore bot's own reactions
        if reaction.emoji == '⏰' and reaction.message.content.startswith("@here Event Alarm!"):
            lines = reaction.message.content.splitlines()
            current_event_id = int(lines[-1].rstrip())
            with get_session() as session:
                service = EventService(session)
                off = service.event_alarm_off(current_event_id)
            await reaction.message.channel.send(event_ui.alarm_off_message(off))

    return bot