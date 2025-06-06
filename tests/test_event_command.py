import pytest
import re
from datetime import datetime
from commands.event_command import EventCommand
from db.models.event import Event
from ui import event_ui
from types import SimpleNamespace
from core.constants import USAGE_MESSAGE_DISPLAY_TIME, FEEDBACK_MESSAGE_DISPLAY_TIME


@pytest.mark.asyncio
async def test_event_command_complete_usage(mock_ctx):
    """
    Test the full lifecycle of an event: add, list, delete, and confirm deletion.

    Args:
       mock_ctx: Mock context for Discord commands
    """
    event_command = EventCommand()
    event_name = "Midterm"
    due_time = datetime.now().isoformat()
    mock_event = SimpleNamespace(event_name=event_name)

    # add event
    await event_command.execute(mock_ctx, ["add", event_name, due_time])
    mock_ctx.send.assert_called_with(event_ui.event_added_message(mock_event), delete_after=FEEDBACK_MESSAGE_DISPLAY_TIME)

    # list events
    await event_command.execute(mock_ctx, ["list"])
    list_msg = mock_ctx.send.call_args[0][0]
    assert "📅 Events:" in list_msg
    assert event_name in list_msg

    # extract ID
    match = re.search(r"\[(\d+)\] Midterm", list_msg)
    assert match, "Could not find the event ID"
    event_id = int(match.group(1))

    # delete event
    await event_command.execute(mock_ctx, ["delete", str(event_id)])
    mock_ctx.send.assert_called_with(event_ui.delete_result_message(deleted=True), delete_after=FEEDBACK_MESSAGE_DISPLAY_TIME)

    # confirm deletion
    await event_command.execute(mock_ctx, ["list"])
    assert event_ui.no_events_message() in mock_ctx.send.call_args[0][0]


@pytest.mark.asyncio
async def test_event_command_add_missing_args(mock_ctx):
    """
    Test adding an event with missing arguments.

    Args:
        mock_ctx: Mock context for Discord commands
    """
    event_command = EventCommand()
    await event_command.execute(mock_ctx, ["add"])
    mock_ctx.send.assert_called_with(event_ui.add_usage_message(), delete_after=USAGE_MESSAGE_DISPLAY_TIME)


@pytest.mark.asyncio
async def test_event_command_add_invalid_date(mock_ctx):
    """
    Test adding an event with an invalid date format.

    Args:
        mock_ctx: Mock context for Discord commands
    """
    event_command = EventCommand()
    await event_command.execute(mock_ctx, ["add", "TestEvent", "beautiful-day"])
    mock_ctx.send.assert_called_with(event_ui.invalid_date_message(), delete_after=USAGE_MESSAGE_DISPLAY_TIME)


@pytest.mark.asyncio
async def test_event_command_delete_missing_id(mock_ctx):
    """
    Test deleting an event without providing an ID.

    Args:
        mock_ctx: Mock context for Discord commands
    """
    event_command = EventCommand()
    await event_command.execute(mock_ctx, ["delete"])
    mock_ctx.send.assert_called_with(event_ui.delete_usage_message(), delete_after=USAGE_MESSAGE_DISPLAY_TIME)


@pytest.mark.asyncio
async def test_event_command_delete_non_integer_id(mock_ctx):
    """
    Test deleting an event with a non-integer ID.

    Args:
        mock_ctx: Mock context for Discord commands
    """
    event_command = EventCommand()
    await event_command.execute(mock_ctx, ["delete", "latest-event"])
    mock_ctx.send.assert_called_with(event_ui.delete_usage_message(), delete_after=USAGE_MESSAGE_DISPLAY_TIME)


@pytest.mark.asyncio
async def test_event_command_unknown_action(mock_ctx):
    """
    Test executing the event command with an unknown action.

    Args:
        mock_ctx: Mock context for Discord commands
    """
    event_command = EventCommand()
    await event_command.execute(mock_ctx, ["do-something"])
    mock_ctx.send.assert_called_with(event_ui.unknown_action_message(), delete_after=USAGE_MESSAGE_DISPLAY_TIME)