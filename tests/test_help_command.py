import pytest
from core.registry import CommandRegistry
from commands.help_command import HelpCommand
from commands.event_command import EventCommand


@pytest.fixture(autouse=True)
def setup_registry():
    """
    Fixture to clear and register commands before each test.
    """
    registry = CommandRegistry()
    registry.commands.clear()
    registry.register_command(HelpCommand())
    registry.register_command(EventCommand())


@pytest.mark.asyncio
async def test_help_command_no_role(mock_ctx):
    """
    Test the help command with no role provided.

    Args:
        mock_ctx: Mock context for Discord commands
    """
    help_command = HelpCommand()
    await help_command.execute(mock_ctx, role="")
    mock_ctx.send.assert_called_with("Please specify your role: `!help student` or `!help teacher`")


@pytest.mark.asyncio
async def test_help_command_invalid_role(mock_ctx):
    """
    Test the help command with an invalid role.

    Args:
        mock_ctx: Mock context for Discord commands
    """
    help_command = HelpCommand()
    await help_command.execute(mock_ctx, role="admin")
    mock_ctx.send.assert_called_with("Unknown role. Please use `!help student` or `!help teacher`")


@pytest.mark.asyncio
@pytest.mark.parametrize("role", ["student", "teacher"])
async def test_help_command_valid_roles(mock_ctx, role):
    """
    Test the help command with valid roles: student and teacher.

    Args:
        mock_ctx: Mock context for Discord commands
        role (str): The user role to test help output for
    """
    help_command = HelpCommand()
    await help_command.execute(mock_ctx, role=role)
    embed = mock_ctx.send.call_args[1]["embed"]
    actual_commands = {field.name: field.value for field in embed.fields}

    expected_commands = {
        "!help [role]": "Displays available commands",
        "!event [add|list|delete] <name> <due-date>": "Manage events",
    }

    assert actual_commands == expected_commands
