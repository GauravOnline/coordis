from datetime import datetime
from typing import List, Optional

from sqlmodel import DateTime, Field, Relationship, SQLModel

from coordis.db.enums import EventType


class EventUserLink(SQLModel, table=True):
    user_id: int | None = Field(default=None, foreign_key="user.id", primary_key=True)
    event_id: int | None = Field(default=None, foreign_key="event.id", primary_key=True)


class Event(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    date: datetime = Field(sa_type=DateTime)
    event_type: EventType = Field(alias="type")
    participants: List["User"] = Relationship(
        back_populates="events", link_model=EventUserLink
    )


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str
    name: Optional[str] = Field(default=None)
    is_teacher: bool = Field(default=False)

    events: List["Event"] = Relationship(
        back_populates="participants", link_model=EventUserLink
    )


__all__ = ["EventUserLink", "Event", "User"]
