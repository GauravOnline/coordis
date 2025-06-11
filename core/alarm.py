import asyncio
import core.bot as bot
from datetime import datetime
from core.constants import FEEDBACK_MESSAGE_DISPLAY_TIME, ALARM_MESSAGE_DISPLAY_TIME
from db.base import get_session
from services.event_service import EventService
from commands.base import Command
from ui import event_ui

async def alarm(channel):
    while True:
        await asyncio.sleep(bot.default_alarm_interval)
        with get_session() as session:
            service = EventService(session)
            events = service.list_events()
            if not events:
                await channel.send(event_ui.no_events_message(), delete_after=FEEDBACK_MESSAGE_DISPLAY_TIME)
            else:
                for event in events:
                    if event.date_due:
                        delta = event.date_due - datetime.now()
                        if delta.total_seconds() < bot.default_alarm:
                            await channel.send(event_ui.alarm_message(event), delete_after=ALARM_MESSAGE_DISPLAY_TIME)