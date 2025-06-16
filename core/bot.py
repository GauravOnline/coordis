"""
Bot Setup

This module handles the setup and configuration of the Discord bot.
"""
import discord
from discord.ext import commands


from core.registry import CommandRegistry
from commands.help_command import HelpCommand
from commands.event_command import EventCommand
from commands.user_command import UserCommand
from commands.ping_command import PingCommand
from core.alarm import alarm
from db.base import get_session
from services.event_service import EventService
from ui import event_ui

# Global Variables
default_alarm_margin = 60       # Seconds before Due Date to Alert User
default_alarm_interval = 60     # Seconds between each check for Due Events
default_channel = "general"     # Name of the default channel for alarms to ping in

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
    intents.reactions = True

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

    # Add ping command to bot
    @bot.command(name='ping')
    async def ping_command(ctx):
        await ping_cmd.execute(ctx)
        # Add ping command to bot

    # Add role command to bot
    @bot.command(name='user')
    async def user_command(ctx, *args):
        print(f"args {args}")
        await user_cmd.execute(bot, ctx, args)


    # Add help command to bot
    @bot.command(name='help')
    async def help_command(ctx):
        await help_cmd.execute(ctx)



    # Start Alarm Async Event once bot is in ready state
    @bot.event
    async def on_ready():
        #await bot.invoke(user_cmd, bot, bot.event, "list") 
        for guild in bot.guilds:
            for channel in guild.text_channels:
                print(f"\n\nname: {bot.get_channel(channel.id)} id: {channel.id}\n\n")
                #ctx = await  bot.get_context(guild)
                args = ['create']
                test_args = ['add','test','teacher']
                await user_cmd.execute(bot, bot.get_channel(channel.id), args)
                await user_cmd.execute(bot,bot.get_channel(channel.id),test_args)


        channel = discord.utils.get(bot.get_all_channels(), name=default_channel)
        if channel:
            await alarm(channel, default_alarm_margin, default_alarm_interval)
        else:
            print(f"Channel '{default_channel}' not found.")



    # Set up reaction listener
    @bot.event
    async def on_reaction_add(reaction, user):
        if user == bot.user:
            return  # ignore bot's own reactions
        # React to alarm messages with alarm clock react so users can react again with it
        if reaction.emoji == '⏰' and reaction.message.content.startswith("@here Event Alarm!"):
            lines = reaction.message.content.splitlines()
            current_event_id = int(lines[-1].rstrip())
            with get_session() as session:
                service = EventService(session)
                off = service.event_alarm_off(current_event_id)
            await reaction.message.channel.send(event_ui.alarm_off_message(off))

    return bot

