"""
Bot Setup

This module handles the setup and configuration of the Discord bot.
"""
import discord
from discord.ext import commands


from core.registry import CommandRegistry
from commands.help_command import HelpCommand
from commands.event_command import EventCommand


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
    intents.members = True

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

    user_cmd = UserCommand()
    registry.register_command(user_cmd)

    # Add to bot
    @bot.command(name='event')
    async def event_command(ctx, *args):
        await event_cmd.execute(ctx, args)

    # Add help command to bot
    @bot.command(name='help')
    async def help_command(ctx):
        await help_cmd.execute(ctx)

    # Add ping command to bot
    @bot.command(name='ping')
    async def ping_command(ctx):
        await ping_cmd.execute(ctx)
        # Add ping command to bot

    return bot