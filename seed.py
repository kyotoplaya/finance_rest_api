from sqlalchemy import select, exists

from models import Category as CategoryModel
from enums import CategoryType
from database import SessionLocal


def seed():
    db = SessionLocal()

    stmt = select(exists().where(CategoryModel.is_system == True))
    is_exists = db.scalar(stmt)

    if not is_exists:
        adjustment = CategoryModel(
            name="Корректировка",
            category_type=CategoryType.ADJUSTMENT,
            is_system=True
        )
        db.add(adjustment)
        db.commit()

    db.close()
