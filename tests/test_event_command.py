import pytest
import re
from datetime import datetime
from commands.event_command import EventCommand
from db.models.event import Event


@pytest.mark.asyncio
async def test_add_and_delete_event(mock_ctx):
    event_command = EventCommand()
    event_name = "Midterm"
    due_time = datetime.now().isoformat()

    # Add event
    await event_command.execute(mock_ctx, ["add", event_name, due_time])
    mock_ctx.send.assert_called_with(f"✅ Event '{event_name}' added.")

    # List events
    await event_command.execute(mock_ctx, ["list"])
    list_msg = mock_ctx.send.call_args[0][0]
    assert "📅 Events:" in list_msg
    assert event_name in list_msg

    # Extract ID
    match = re.search(r"\[(\d+)\] Midterm", list_msg)
    assert match, "Could not find the event ID"
    event_id = int(match.group(1))

    # Delete event
    await event_command.execute(mock_ctx, ["delete", str(event_id)])
    mock_ctx.send.assert_called_with("🗑️ Event deleted.")

    # Confirm deletion
    await event_command.execute(mock_ctx, ["list"])
    assert "No events found" in mock_ctx.send.call_args[0][0]
