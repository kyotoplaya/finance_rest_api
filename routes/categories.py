from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Category as CategoryModel
from schemas import CategoryCreate, Category


router = APIRouter()


@router.post("/categories", response_model=Category, status_code=201)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    db_category = CategoryModel(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category