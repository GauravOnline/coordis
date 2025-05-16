import pytest
from core.registry import CommandRegistry
from commands.help_command import HelpCommand
from commands.event_command import EventCommand

@pytest.mark.asyncio
async def test_help_command_for_roles(mock_ctx):
    registry = CommandRegistry()
    registry.commands.clear()
    registry.register_command(HelpCommand())
    registry.register_command(EventCommand())

    help_command = HelpCommand()

    for role in ["student", "teacher"]:
        await help_command.execute(mock_ctx, role=role)
        embed = mock_ctx.send.call_args[1]["embed"]
        actual_commands = {field.name: field.value for field in embed.fields}

        expected_commands = {
            "!help [role]": "Displays available commands",
            "!event [add|list|delete] <name> <due-date>": "Manage events",
        }

        assert actual_commands == expected_commands
