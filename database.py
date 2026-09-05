from sqlalchemy import create_engine           # функция: создаёт движок (подключение к базе)
from sqlalchemy.orm import sessionmaker         # функция: создаёт фабрику сессий
from sqlalchemy.orm import DeclarativeBase      # класс: от него наследуем наши таблицы

DB_URL = "sqlite:///db/finance.db"
engine = create_engine(DB_URL, echo=True)

Session = sessionmaker(engine)

class Base(DeclarativeBase):
    pass