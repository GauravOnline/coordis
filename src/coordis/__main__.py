#!/usr/bin/env python3
from sqlmodel import SQLModel

from coordis.db import ENGINE  # noqa: F401

try:
    from rich import print
except ImportError:
    pass


def main() -> None:
    print(SQLModel.metadata.tables)


if __name__ == "__main__":
    main()
