# функция: создаёт движок (подключение к базе)
from sqlalchemy import create_engine
# функция: создаёт фабрику сессий
from sqlalchemy.orm import sessionmaker, Session
# класс: от него наследуем наши таблицы
from sqlalchemy.orm import DeclarativeBase


DB_URL = "sqlite:///db/finance.db"
engine = create_engine(DB_URL, echo=True)

SessionLocal = sessionmaker(engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
