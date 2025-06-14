from datetime import datetime, timedelta

from discord.channel import TextChannel

from db.base import get_session
from db.models.notification import Notification
from db.repositories.notification_repo import NotificationRepo

NOTIFY_TIME: timedelta = timedelta(days=1)  # timedelta(hours=1)


class Notify:
    async def run_notify(self, ctx: TextChannel) -> None:
        repo: NotificationRepo = NotificationRepo(session=get_session())
        now = datetime.now()
        print(f"Notify.run_notify() called at {now}")
        for event in repo.get_upcoming_events_to_notify():
            due_in: timedelta = event.date_due - now
            if due_in < NOTIFY_TIME:
                msg = f"Event {event.event_name} is due in"
                if due_in.days > 0:
                    msg += f" {due_in.days} day(s)"
                hours, remainder = divmod(due_in.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                await ctx.send(
                    f"@everyone {msg} {int(hours):02}:{int(minutes):02}:{int(seconds):02}."
                )
                repo.create_notification(
                    Notification(
                        sent=now, event_due_date=event.date_due, event_id=event.id
                    )
                )
        repo.session.close()
