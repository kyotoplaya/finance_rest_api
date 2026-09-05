from fastapi import APIRouter, Depends, HTTPException
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

@router.get("/categories", response_model=list[Category])
def get_categories(db: Session = Depends(get_db)):
    return db.query(CategoryModel).all()

@router.get("/categories/{category_id}", response_model=Category)
def get_category(category_id: int, db: Session = Depends(get_db)):
    answer = db.query(CategoryModel).filter(CategoryModel.id == category_id).first()
    if answer is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return answer