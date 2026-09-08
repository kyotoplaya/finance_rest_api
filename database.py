# функция: создаёт движок (подключение к базе)
from sqlalchemy import create_engine
# функция: создаёт фабрику сессий
from sqlalchemy.orm import sessionmaker, Session
# класс: от него наследуем наши таблицы
from sqlalchemy.orm import DeclarativeBase

from sqlalchemy import event


DB_URL = "sqlite:///db/finance.db"
engine = create_engine(DB_URL, echo=True)


# Включаем проверку внешних ключей на каждом подключении.
# Без этого SQLite не применяет ON DELETE RESTRICT.


@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    cursor.close()


SessionLocal = sessionmaker(engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
