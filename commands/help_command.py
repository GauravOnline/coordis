from commands.base import Command
from core.constants import USAGE_MESSAGE_DISPLAY_TIME
from core.registry import CommandRegistry
from ui import help_ui  # <- import UI helpers


class HelpCommand(Command):
    """Help command to display available commands"""

    def __init__(self):
        super().__init__(
            name="help",
            description="Displays available commands",
            roles=["all", "student", "teacher"],
        )

    async def execute(self, ctx, role=None):
        registry = CommandRegistry()

        if not role:
            await ctx.send(
                help_ui.prompt_for_role(), delete_after=USAGE_MESSAGE_DISPLAY_TIME
            )
            return

        role = role.lower()
        if role not in ["student", "teacher"]:
            await ctx.send(
                help_ui.unknown_role_message(), delete_after=USAGE_MESSAGE_DISPLAY_TIME
            )
            return

        commands = registry.get_commands_by_role(role)
        embed = help_ui.help_embed(commands, role)
        await ctx.send(embed=embed)

    def get_help_text(self):
        return f"!{self.name} [role] - {self.description}"
