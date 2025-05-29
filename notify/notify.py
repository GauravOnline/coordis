from datetime import datetime, timedelta
from typing import List

from db.base import get_session
from db.repositories.event_repo import EventRepository



NOTIFY_TIME: timedelta = timedelta(hours=1)

class Notify:
    notified: List[int] = []

    async def run_notify(self, ctx) -> None:
        repo: EventRepository = EventRepository(session=get_session())
        now = datetime.now()
        for event in repo.get_all_events():
            due_in: timedelta = event.date_due - now
            if (due_in < NOTIFY_TIME) and (event.id not in self.notified):
                # send notification
                ctx.send(f"Event {event.event_name} is due in {due_in}.")
                self.notified.append(event.id)
        repo.session.close()

