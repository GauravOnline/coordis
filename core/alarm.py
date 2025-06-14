import asyncio
from datetime import datetime
from core.constants import FEEDBACK_MESSAGE_DISPLAY_TIME, ALARM_MESSAGE_DISPLAY_TIME
from db.base import get_session
from services.event_service import EventService
from ui import event_ui

async def alarm(channel, alarm_margin, alarm_interval):
    """Sets up an asynchronous alarm object which checks
    the database for events, then checks if any events
    are soon to be due. If time to due date is greater
    than 0 and less than alarm_margin, then fire the alarm."""
    while True:
        await asyncio.sleep(alarm_interval)
        with get_session() as session:
            service = EventService(session)
            events = service.list_events()
            if events:
                for event in events:
                    if event.date_due and not event.alarm_off:
                        delta = event.date_due - datetime.now()
                        if 0 < delta.total_seconds() < alarm_margin:
                            sent = await channel.send(event_ui.alarm_message(event), delete_after=ALARM_MESSAGE_DISPLAY_TIME)
                            await sent.add_reaction('⏰')