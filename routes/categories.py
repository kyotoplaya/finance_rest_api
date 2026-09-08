from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Category as CategoryModel
from models import Transaction as TransactionModel
from schemas import CategoryCreate, CategoryUpdate, Category

from enums import CategoryType


router = APIRouter()


@router.post("/categories", response_model=Category, status_code=201)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    if category.category_type == CategoryType.ADJUSTMENT:
        raise HTTPException(
            status_code=403, detail="You cannot create an adjustment category.")

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
    category = db.query(CategoryModel).filter(
        CategoryModel.id == category_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.patch("/categories/{category_id}", response_model=Category)
def patch_category(category_id: int, category: CategoryUpdate, db: Session = Depends(get_db)):
    category_to_update = db.query(CategoryModel).filter(
        CategoryModel.id == category_id).first()

    if category_to_update is None:
        raise HTTPException(status_code=404, detail="Category not found")

    if category_to_update.is_system:
        raise HTTPException(
            status_code=403, detail="You cannot edit a system category.")

    updated_category = category.model_dump()
    for key, value in updated_category.items():
        if value is None:
            continue
        setattr(category_to_update, key, value)

    db.commit()
    db.refresh(category_to_update)

    return category_to_update


@router.put("/categories/{category_id}", response_model=Category)
def put_category(category_id: int, category: CategoryCreate, db: Session = Depends(get_db)):
    category_to_update = db.query(CategoryModel).filter(
        CategoryModel.id == category_id).first()

    if category_to_update is None:
        raise HTTPException(status_code=404, detail="Category not found")

    if category_to_update.is_system:
        raise HTTPException(
            status_code=403, detail="You cannot edit a system category.")

    updated_category = category.model_dump()
    for key, value in updated_category.items():
        setattr(category_to_update, key, value)

    db.commit()
    db.refresh(category_to_update)

    return category_to_update


@router.delete("/categories/{category_id}", response_model=bool)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category_to_delete = db.query(CategoryModel).filter(
        CategoryModel.id == category_id).first()

    if category_to_delete is None:
        raise HTTPException(status_code=404, detail="Category not found")

    if category_to_delete.is_system:
        raise HTTPException(
            status_code=403, detail="You cannot delete a system category.")

    transaction = db.query(TransactionModel).filter(
        TransactionModel.category_id == category_to_delete.id).first()

    if transaction is not None:
        raise HTTPException(
            status_code=409,
            detail=f"Cannot delete category with transaction id {transaction.id}."
        )

    db.delete(category_to_delete)
    db.commit()

    return True
