import pytest
from types import SimpleNamespace
from commands.user_command import UserCommand
from ui import user_ui
from datetime import datetime
from core.constants import USAGE_MESSAGE_DISPLAY_TIME, FEEDBACK_MESSAGE_DISPLAY_TIME


@pytest.mark.asyncio
async def test_user_command_add_list_alter(mock_ctx):
    """
    Test adding a user, listing users, and altering roles using UserCommand.

    Args:
        mock_ctx: Mock context for Discord commands
    """
    cmd = UserCommand()

    # Fake Discord users
    test_teacher = SimpleNamespace(name="test_teacher", bot=False)
    test_student = SimpleNamespace(name="test_student", bot=False)

    # Fake Discord guild and bot
    fake_guild = SimpleNamespace(
        members=[test_teacher, test_student],
        owner=SimpleNamespace(id=123)
    )
    bot = SimpleNamespace(
        get_all_members=lambda: [test_teacher, test_student],
        guilds=[fake_guild],
        guild=fake_guild
    )

    # Add teacher
    await cmd.execute(bot, mock_ctx, ["add", "test_teacher", "teacher"])
    mock_teacher = SimpleNamespace(user_name="test_teacher", user_role="teacher", date_assigned=datetime.now())
    msg1 = mock_ctx.send.call_args[0][0]
    assert msg1 == user_ui.user_added_message(mock_teacher)

    # Add student
    await cmd.execute(bot, mock_ctx, ["add", "test_student", "student"])
    mock_student = SimpleNamespace(user_name="test_student", user_role="student", date_assigned=datetime.now())
    msg2 = mock_ctx.send.call_args[0][0]
    assert msg2 == user_ui.user_added_message(mock_student)

    # List users``
    await cmd.execute(bot, mock_ctx, ["list"])
    list_msg = mock_ctx.send.call_args[0][0]
    assert "[test_teacher] teacher" in list_msg
    assert "[test_student] student" in list_msg

    # Alter student role to teacher
    await cmd.execute(bot, mock_ctx, ["alter", "test_student", "teacher"])
    updated_student = SimpleNamespace(user_name="test_student", user_role="teacher")
    alter_msg = mock_ctx.send.call_args[0][0]
    assert alter_msg == user_ui.role_altered_message(updated_student)


@pytest.mark.asyncio
async def test_user_command_add_missing_args(mock_ctx):
    """
    Test adding a user with missing arguments.

    Args:
        mock_ctx: Mock context for Discord commands
    """
    cmd = UserCommand()
    await cmd.execute(None, mock_ctx, ["add"])
    mock_ctx.send.assert_called_with(user_ui.add_usage_message(), delete_after=USAGE_MESSAGE_DISPLAY_TIME)


@pytest.mark.asyncio
async def test_user_command_alter_missing_args(mock_ctx):
    """
    Test altering a user's role with missing arguments.

    Args:
        mock_ctx: Mock context for Discord commands
    """
    cmd = UserCommand()
    await cmd.execute(None, mock_ctx, ["alter"])
    mock_ctx.send.assert_called_with(user_ui.alter_usage_message(), delete_after=USAGE_MESSAGE_DISPLAY_TIME)


@pytest.mark.asyncio
async def test_user_command_unknown_action(mock_ctx):
    """
    Test using an unknown action with the user command.

    Args:
        mock_ctx: Mock context for Discord commands
    """
    cmd = UserCommand()
    await cmd.execute(None, mock_ctx, ["award"])
    mock_ctx.send.assert_called_with(user_ui.usage_message(), delete_after=USAGE_MESSAGE_DISPLAY_TIME)
