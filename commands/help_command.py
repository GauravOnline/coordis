"""
Help Command Implementation

Provides a help command that displays available commands based on user roles.
"""

import discord

from commands.base import Command
from core.registry import CommandRegistry


class HelpCommand(Command):
    """Help command to display available commands"""

    def __init__(self):
        super().__init__(
            name="help",
            description="Displays available commands",
            roles=["all", "student", "teacher"],
        )

    async def execute(self, ctx, role=None):
        """
        Process the help command.

        Args:
            ctx: The Discord context
            role (str, optional): The role to show commands for
        """
        registry = CommandRegistry()
        print(role, ctx)
        print("inside the help command")

        if not role:
            await ctx.send(
                "Please specify your role: `!help student` or `!help teacher`"
            )
            return

        role = role.lower()
        if role not in ["student", "teacher"]:
            await ctx.send(
                "Unknown role. Please use `!help student` or `!help teacher`"
            )
            return

        # Get commands for the specified role
        commands = registry.get_commands_by_role(role)

        # Create and send help message
        embed = self._format_help_message(commands, role)
        await ctx.send(embed=embed)

    def _format_help_message(self, commands, role):
        """
        Format help message as Discord embed.

        Args:
            commands (list): List of Command objects
            role (str): Role being displayed

        Returns:
            discord.Embed: Formatted embed with command information
        """
        embed = discord.Embed(
            title=f"📚 {role.capitalize()} Commands",
            description="Here are the commands available to you:",
            color=discord.Color.blue(),
        )

        for cmd in commands:
            print(cmd.name)
            help_text = cmd.get_help_text()
            command_name, description = help_text.split(" - ", 1)
            embed.add_field(name=command_name, value=description, inline=False)

        return embed

    def get_help_text(self):
        """
        Get help text for this command.

        Returns:
            str: Help text describing the command usage
        """
        return f"!{self.name} [role] - {self.description}"
