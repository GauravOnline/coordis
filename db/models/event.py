from datetime import datetime
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class Event(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    event_name: str
    date_due: datetime
    date_assigned: datetime = Field(default_factory=datetime.utcnow)
    event_info: Optional[str] = None
    notification: Optional["Notification"] = Relationship(back_populates="event")
