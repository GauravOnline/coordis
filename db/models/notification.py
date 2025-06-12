from datetime import datetime
from typing import Optional

from sqlmodel import DateTime, Field, Relationship, SQLModel

from db.models.event import Event


class Notification(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sent: Optional[datetime] = Field(default=None, sa_type=DateTime)

    event_id: Optional[int] = Field(default=None, foreign_key="event.id")
    event_due_date: datetime
    event: Event = Relationship(back_populates="notification")
