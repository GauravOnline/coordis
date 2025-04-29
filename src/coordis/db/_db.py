from typing import Literal

from sqlmodel import SQLModel, create_engine

from coordis.db.tables import *  # noqa: F401, F403

SQLITE_FILE_NAME: str = "database.db3"  # Should change to load from config/env when set
SQLITE_URL: str = f"sqlite:///{SQLITE_FILE_NAME}"

SQL_SERVER_URL: str = "SOME_SQL_SERVER_URL"

SQL_TYPE: Literal["sqlite", "server"] = (
    "sqlite"  # Should change to load from config/env when set (defaults to "sqlite" to avoid errors)
)

ECHO_SQL: bool = True  # Should change to load from config/env when set

ENGINE = create_engine(
    SQLITE_URL if SQL_TYPE == "sqlite" else SQL_SERVER_URL, echo=ECHO_SQL
)
SQLModel.metadata.create_all(ENGINE, checkfirst=True)
