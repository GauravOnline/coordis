import discord
from commands.base import Command
from ui import ping_ui  # 👈 import the UI module


class PingCommand(Command):
    """Ping command to check if the bot is responsive"""

    def __init__(self):
        super().__init__(
            name="ping",
            description="Check the bot's response time",
            roles=["all", "student", "teacher"]
        )

    async def execute(self, ctx, *args):
        latency = round(ctx.bot.latency * 1000)
        print("inside the ping command")

        embed = ping_ui.ping_response(latency)
        await ctx.send(embed=embed, delete_after=5)

    def get_help_text(self):
        return f"!{self.name} - {self.description}"
