from typing import Optional
from sqlmodel import SQLModel, Field

class Event(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    event_name: str
    #class_name: str
    #class_id: str
    date_due: Optional[str] = None
    date_assigned: str

class EventList(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    class_id: int
    name: str