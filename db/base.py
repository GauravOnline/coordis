from sqlmodel import SQLModel, Session, create_engine

sqlite_file_name = "database.db"
engine = create_engine(f"sqlite:///{sqlite_file_name}", echo=True)


def init_db():
    SQLModel.metadata.drop_all(engine)  # REMOVE FOR PRODUCTION
    SQLModel.metadata.create_all(engine)


def get_session():
    return Session(engine)
