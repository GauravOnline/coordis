import discord
from commands.base import Command
from ui import ping_ui  # 👈 import the UI module
from core.constants import FEEDBACK_MESSAGE_DISPLAY_TIME


class PingCommand(Command):
    """Ping command to check if the bot is responsive"""

    def __init__(self):
        super().__init__(
            name="ping",
            description="Check the bot's response time",
            roles=["all", "student", "teacher"]
        )

    async def execute(self, ctx, *args):

        if (PingCommand.check_permission_role(self,ctx) == 0):
            await ctx.send(ping_ui.permission_too_low_message(ctx.author.name), delete_after=FEEDBACK_MESSAGE_DISPLAY_TIME)
            return

        latency = round(ctx.bot.latency * 1000)
        print("inside the ping command")

        embed = ping_ui.ping_response(latency)
        await ctx.send(embed=embed, delete_after=FEEDBACK_MESSAGE_DISPLAY_TIME)

    def get_help_text(self):
        return f"!{self.name} - {self.description}"
