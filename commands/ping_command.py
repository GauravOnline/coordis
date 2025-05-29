"""
Ping Command Implementation

A simple command that responds with "Pong!" and the bot's latency.
"""

import discord

from commands.base import Command


class PingCommand(Command):
    """Ping command to check if the bot is responsive"""

    def __init__(self):
        super().__init__(
            name="ping",
            description="Check the bot's response time",
            roles=["all", "student", "teacher"],  # Available to all roles
        )

    async def execute(self, ctx, *args):
        """
        Process the ping command.

        Args:
            ctx: The Discord context
            *args: Additional arguments (not used for this command)
        """
        # Calculate latency in milliseconds
        latency = round(ctx.bot.latency * 1000)
        print("inside the ping command")
        # Create embed response
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"Bot latency: {latency}ms",
            color=discord.Color.green(),
        )

        # Add additional info to the embed
        embed.add_field(name="Status", value="✅ Bot is running normally", inline=False)

        await ctx.send(embed=embed)

    def get_help_text(self):
        """
        Get help text for this command.

        Returns:
            str: Help text describing the command usage
        """
        return f"!{self.name} - {self.description}"
