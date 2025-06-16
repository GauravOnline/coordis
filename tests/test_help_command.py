import pytest
from core.registry import CommandRegistry
from commands.help_command import HelpCommand
from ui import help_ui
from core.constants import USAGE_MESSAGE_DISPLAY_TIME
from unittest.mock import patch, MagicMock

@pytest.mark.asyncio
async def test_help_command_no_role(mock_ctx):
    """
    Test the help command with no role provided.

    Args:
        mock_ctx: Mock context for Discord commands
    """
    # Set the author's name on the context
    mock_ctx.author.name = "test_user"

    # Create a fake user object with user_role
    fake_user = MagicMock()
    fake_user.user_role = None

    # Patch UserService.get_user to return our fake user
    with patch("commands.help_command.UserService.get_user", return_value=fake_user):
        help_command = HelpCommand()
        await help_command.execute(mock_ctx)
        mock_ctx.send.assert_called_with(help_ui.prompt_for_role(), delete_after=USAGE_MESSAGE_DISPLAY_TIME)


@pytest.mark.asyncio
async def test_help_command_invalid_role(mock_ctx):
    """
    Test the help command with an invalid role.

    Args:
        mock_ctx: Mock context for Discord commands
    """
    # Set the author's name on the context
    mock_ctx.author.name = "test_user"

    # Create a fake user object with user_role
    fake_user = MagicMock()
    fake_user.user_role = "admin"

    # Patch UserService.get_user to return our fake user
    with patch("commands.help_command.UserService.get_user", return_value=fake_user):
        help_command = HelpCommand()
        await help_command.execute(mock_ctx)
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
    # Set the author's name on the context
    mock_ctx.author.name = "test_user"

    # Create a fake user object with user_role
    fake_user = MagicMock()
    fake_user.user_role = role

    # Patch UserService.get_user to return our fake user
    with patch("commands.help_command.UserService.get_user", return_value=fake_user):
        
        help_command = HelpCommand()
        await help_command.execute(mock_ctx)
        embed = mock_ctx.send.call_args[1]["embed"]

        # Get expected embed from help_ui
        commands = CommandRegistry().get_commands_by_role(role)
        expected_embed = help_ui.help_embed(commands, role)

        # Validate embed structure
        assert embed.title == expected_embed.title
        assert embed.description == expected_embed.description
        assert len(embed.fields) == len(expected_embed.fields)

        # Compare field-by-field
        for actual, expected in zip(embed.fields, expected_embed.fields):
            assert actual.name == expected.name
            assert actual.value == expected.value