from sqlmodel import Session, select
from db.models.event import Event
from typing import List, Optional

class EventRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_event(self, event: Event) -> Event:
        self.session.add(event)
        self.session.commit()
        self.session.refresh(event)
        return event

    def get_event_by_id(self, event_id: int) -> Optional[Event]:
        statement = select(Event).where(Event.id == event_id)
        result = self.session.exec(statement).first()
        return result

    def get_all_events(self) -> List[Event]:
        statement = select(Event)
        results = self.session.exec(statement).all()
        return results

    def delete_event(self, event_id: int) -> bool:
        event = self.get_event_by_id(event_id)
        if event:
            self.session.delete(event)
            self.session.commit()
            return True
        return False

    def event_alarm_off(self, event_id: int) -> bool:
        event = self.get_event_by_id(event_id)
        if event:
            current_event_id = event_id
            event.alarm_off = True
            self.session.commit()
            return True
        return False
