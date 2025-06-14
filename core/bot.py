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

def setup_bot():
    """
    Set up and configure the Discord bot.

    Returns:
        discord.ext.commands.Bot: Configured bot instance
    """
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

    # Add role command to bot
    @bot.command(name='user')
    async def user_command(ctx, *args):
        print(f"args {args}")
        await user_cmd.execute(bot, ctx, args)
        #Add role command for dot
    
    @bot.event
    async def on_ready():
        #await bot.invoke(user_cmd, bot, bot.event, "list") 
        for guild in bot.guilds:
            for channel in guild.text_channels:
                print(f"\n\nname: {bot.get_channel(channel.id)} id: {channel.id}\n\n")
                #ctx = await  bot.get_context(guild)
                args = ['create']
                await user_cmd.execute(bot, bot.get_channel(channel.id), args)

    return bot
