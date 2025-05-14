from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

class Event(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    event_name: str
    date_due: Optional[datetime] = None
    date_assigned: datetime = Field(default_factory=datetime.utcnow)
