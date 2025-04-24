from typing import List

from sqlmodel import Field, Relationship, SQLModel

from coordis.db.event import Event, EventUserLink


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str

    events: List["Event"] = Relationship(
        back_populates="participants", link_model=EventUserLink
    )


__all__ = ["User"]
