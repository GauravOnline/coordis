import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Command:
    """Interface for all bot commands"""

    def __init__(self, name, description, roles):
        self.name = name
        self.description = description
        self.roles = roles  # List of roles that can use this command

    async def execute(self, ctx):
        """Execute the command logic"""
        pass

    def get_help_text(self):
        """Get help text for this command"""
        return f"!{self.name} - {self.description}"


class CommandRegistry:
    """Central registry for all bot commands"""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CommandRegistry, cls).__new__(cls)
            cls._instance.commands = []
        return cls._instance

    def register_command(self, command):
        """Register a new command"""
        self.commands.append(command)

    def get_all_commands(self):
        """Get all registered commands"""
        return self.commands

    def get_commands_by_role(self, role):
        """Get commands available for a specific role"""
        return [cmd for cmd in self.commands if role in cmd.roles or "all" in cmd.roles]


class HelpCommand(Command):
    """Help command to display available commands"""

    def __init__(self):
        super().__init__(
            name="help",
            description="Displays available commands",
            roles=["all", "student", "teacher"]
        )

    async def execute(self, ctx, role=None):
        """Process the help command"""
        registry = CommandRegistry()

        if not role:
            await ctx.send("Please specify your role: `!help student` or `!help teacher`")
            return

        role = role.lower()
        if role not in ["student", "teacher"]:
            await ctx.send("Unknown role. Please use `!help student` or `!help teacher`")
            return

        # Get commands for the specified role
        commands = registry.get_commands_by_role(role)

        # Create and send help message
        embed = self._format_help_message(commands, role)
        await ctx.send(embed=embed)

    def _format_help_message(self, commands, role):
        """Format help message as Discord embed"""
        embed = discord.Embed(
            title=f"📚 {role.capitalize()} Commands",
            description="Here are the commands available to you:",
            color=discord.Color.blue()
        )

        for cmd in commands:
            help_text = cmd.get_help_text()
            command_name, description = help_text.split(" - ", 1)
            embed.add_field(name=command_name, value=description, inline=False)

        return embed

    def get_help_text(self):
        return f"!{self.name} [role] - {self.description}"


# Example of how to set up the bot with this architecture
def setup_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix='!', intents=intents)

    # Remove default help command
    bot.remove_command('help')

    # Create registry
    registry = CommandRegistry()

    # Register our help command
    help_cmd = HelpCommand()
    registry.register_command(help_cmd)

    # Add help command to bot
    @bot.command(name='help')
    async def help_command(ctx, role=None):
        await help_cmd.execute(ctx, role)

    # In a real project, other team members would register their commands here

    return bot


# Run the bot
if __name__ == "__main__":
    bot = setup_bot()

    # Get the token from the environment variable
    TOKEN = os.getenv('DISCORD_TOKEN')
    if not TOKEN:
        raise ValueError("No token found. Please create a .env file with your DISCORD_TOKEN")

    bot.run(TOKEN)