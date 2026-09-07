from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Transaction as TransactionModel
from models import Category as CategoryModel
from models import Account as AccountModel
from schemas import TransactionCreate, TransactionUpdate, Transaction

router = APIRouter()


@router.post("/transactions", response_model=Transaction, status_code=201)
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    if transaction.amount == 0:
        raise HTTPException(
            status_code=400, detail="A transaction cannot have a zero amount.")

    account = db.query(AccountModel).filter(
        AccountModel.id == transaction.account_id).first()

    if account is None:
        raise HTTPException(
            status_code=404, detail="The transaction cannot be linked to a non-existent account.")

    category = db.query(CategoryModel).filter(
        CategoryModel.id == transaction.category_id).first()

    if category is None:
        raise HTTPException(
            status_code=404, detail="The transaction cannot be linked to a non-existent category.")

    db_transaction = TransactionModel(**transaction.model_dump())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


@router.get("/transactions", response_model=list[Transaction])
def get_transactions(db: Session = Depends(get_db)):
    return db.query(TransactionModel).all()


@router.get("/transactions/{transaction_id}", response_model=Transaction)
def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = db.query(TransactionModel).filter(
        TransactionModel.id == transaction_id).first()
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction


@router.patch("/transactions/{transaction_id}", response_model=Transaction)
def patch_transaction(transaction_id: int, transaction: TransactionUpdate, db: Session = Depends(get_db)):
    if transaction.amount == 0:
        raise HTTPException(
            status_code=400, detail="A transaction cannot have a zero amount.")

    transaction_to_update = db.query(TransactionModel).filter(
        TransactionModel.id == transaction_id).first()

    if transaction_to_update is None:
        raise HTTPException(status_code=404, detail="Transaction not found")

    updated_transaction = transaction.model_dump()
    for key, value in updated_transaction.items():
        if value is None:
            continue
        setattr(transaction_to_update, key, value)

    db.commit()
    db.refresh(transaction_to_update)

    return transaction_to_update


@router.put("/transactions/{transaction_id}", response_model=Transaction)
def put_transaction(transaction_id: int, transaction: TransactionUpdate, db: Session = Depends(get_db)):
    if transaction.amount == 0:
        raise HTTPException(
            status_code=400, detail="A transaction cannot have a zero amount.")

    transaction_to_update = db.query(TransactionModel).filter(
        TransactionModel.id == transaction_id).first()

    if transaction_to_update is None:
        raise HTTPException(status_code=404, detail="Transaction not found")

    updated_transaction = transaction.model_dump()
    for key, value in updated_transaction.items():
        setattr(transaction_to_update, key, value)

    db.commit()
    db.refresh(transaction_to_update)

    return transaction_to_update


@router.delete("/transactions/{transaction_id}", response_model=bool)
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction_to_delete = db.query(TransactionModel).filter(
        TransactionModel.id == transaction_id).first()

    if transaction_to_delete is None:
        raise HTTPException(status_code=404, detail="Transaction not found")

    db.delete(transaction_to_delete)
    db.commit()

    return True
