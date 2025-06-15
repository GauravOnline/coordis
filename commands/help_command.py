from commands.base import Command
from core.registry import CommandRegistry
from services.user_service import UserService
from db.base import get_session
from ui import help_ui  # <- import UI helpers
from core.constants import USAGE_MESSAGE_DISPLAY_TIME


class HelpCommand(Command):
    """Help command to display available commands"""

    def __init__(self):
        super().__init__(
            name="help",
            description="Displays available commands",
            roles=["student", "teacher"]
        )

    async def execute(self, ctx, role=None):
        registry = CommandRegistry()

        with get_session() as session:
            service = UserService(session)
            messenger = service.get_user(ctx.author.name)

        if not messenger.user_role:
            await ctx.send(help_ui.prompt_for_role(), delete_after=USAGE_MESSAGE_DISPLAY_TIME)
            return
        role = messenger.user_role
        role = role.lower()
        if role not in self.roles:
            await ctx.send(help_ui.unknown_role_message(), delete_after=USAGE_MESSAGE_DISPLAY_TIME)
            return

        commands = registry.get_commands_by_role(role)
        embed = help_ui.help_embed(commands, role)
        await ctx.send(embed=embed)

    def get_help_text(self):
        return f"!{self.name} [role] - {self.description}"
