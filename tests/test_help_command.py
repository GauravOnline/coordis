import pytest
from core.registry import CommandRegistry
from commands.help_command import HelpCommand
from commands.event_command import EventCommand
from commands.ping_command import PingCommand
from ui import help_ui
from core.constants import USAGE_MESSAGE_DISPLAY_TIME


@pytest.fixture(autouse=True)
def setup_registry():
    """
    Fixture to clear and register commands before each test.
    """
    registry = CommandRegistry()
    registry.commands.clear()
    registry.register_command(HelpCommand())
    registry.register_command(EventCommand())
    registry.register_command(PingCommand())


@pytest.mark.asyncio
async def test_help_command_no_role(mock_ctx):
    """
    Test the help command with no role provided.

    Args:
        mock_ctx: Mock context for Discord commands
    """
    help_command = HelpCommand()
    await help_command.execute(mock_ctx, role="")
    mock_ctx.send.assert_called_with(help_ui.prompt_for_role(), delete_after=USAGE_MESSAGE_DISPLAY_TIME)


@pytest.mark.asyncio
async def test_help_command_invalid_role(mock_ctx):
    """
    Test the help command with an invalid role.

    Args:
        mock_ctx: Mock context for Discord commands
    """
    help_command = HelpCommand()
    await help_command.execute(mock_ctx, role="admin")
    mock_ctx.send.assert_called_with(help_ui.unknown_role_message(), delete_after=USAGE_MESSAGE_DISPLAY_TIME)


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

    # get expected embed from help_ui
    commands = CommandRegistry().get_commands_by_role(role)
    expected_embed = help_ui.help_embed(commands, role)

    # compare embed fields
    assert embed.title == expected_embed.title
    assert embed.description == expected_embed.description
    assert len(embed.fields) == len(expected_embed.fields)

    # compare command fields
    for actual_field, expected_field in zip(embed.fields, expected_embed.fields):
        assert actual_field.name == expected_field.name
        assert actual_field.value == expected_field.value