from datetime import datetime, timedelta
from typing import List, Optional

from sqlmodel import Session, select

from db.models.event import Event
from db.models.notification import Notification

try:
    from rich.traceback import install

    install(show_locals=True)
except ImportError:
    pass


class NotificationRepo:
    def __init__(self, session: Session):
        self.session = session

    def create_notification(self, notification: Notification) -> Notification:
        self.session.add(notification)
        self.session.commit()
        self.session.refresh(notification)
        return notification

    def get_notification_by_id(self, notification_id: int) -> Optional[Notification]:
        query = select(Notification).where(Notification.id == notification_id)
        response = self.session.exec(query).first()
        return response

    def get_all_notifications(self) -> List[Notification]:
        query = select(Notification)
        response = self.session.exec(query).all()
        return response

    def delete_notification(self, notification_id: int) -> bool:
        ntf = self.get_notification_by_id(notification_id=notification_id)
        if ntf is not None:
            self.session.delete(ntf)
            self.session.commit()
            return True
        return False

    def get_upcoming_events_to_notify(
        self, alert: timedelta = timedelta(days=1)
    ) -> List[Event]:
        now = datetime.now()
        events: List[Event] = []
        for event in self.session.exec(select(Event).where(Event.date_due > now)).all():
            if (event.date_due - now) <= alert:
                _ntf = self.session.exec(
                    select(Notification).where(Notification.event_id == event.id)
                ).first()
                if (_ntf is None) or (_ntf.event_due_date != event.date_due):
                    events.append(event)
        return events
