from datetime import datetime
from typing import List, Optional

from db.models.event import Event
from db.repositories.event_repo import EventRepository


class EventService:
    def __init__(self, session):
        self.repo = EventRepository(session)

    def create_event(
        self,
        event_name: str,
        date_assigned: datetime,
        date_due: Optional[datetime] = None,
        event_info: Optional[str] = None,
    ) -> Event:
        event = Event(
            event_name=event_name,
            date_assigned=date_assigned,
            date_due=date_due,
            event_info=event_info,
        )
        return self.repo.create_event(event)

    def list_events(self) -> List[Event]:
        return self.repo.get_all_events()

    def get_event(self, event_id: int) -> Optional[Event]:
        return self.repo.get_event_by_id(event_id)

    def delete_event(self, event_id: int) -> bool:
        return self.repo.delete_event(event_id)
