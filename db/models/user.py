from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_name: str
    user_role: str = Field(default="student")
    date_assigned: datetime = Field(default_factory=datetime.utcnow)