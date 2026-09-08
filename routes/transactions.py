from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Transaction as TransactionModel
from models import Category as CategoryModel
from models import Account as AccountModel
from schemas import TransactionCreate, TransactionUpdate, Transaction
from enums import CategoryType

from helpers import compute_balance, ensure_balance_not_negative, transaction_delta

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

    balance = compute_balance(db, account)
    delta = transaction_delta(category.category_type, transaction.amount)
    ensure_balance_not_negative(balance, delta)

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

    new_account_id = transaction.account_id or transaction_to_update.account_id
    new_category_id = transaction.category_id or transaction_to_update.category_id
    new_amount = transaction.amount if transaction.amount is not None else transaction_to_update.amount

    account = db.query(AccountModel).filter(
        AccountModel.id == new_account_id).first()

    if account is None:
        raise HTTPException(
            status_code=404, detail="The transaction cannot be linked to a non-existent account.")

    category = db.query(CategoryModel).filter(
        CategoryModel.id == new_category_id).first()

    if category is None:
        raise HTTPException(
            status_code=404, detail="The transaction cannot be linked to a non-existent category.")

    old_category_type = db.query(CategoryModel.category_type).filter(
        CategoryModel.id == transaction_to_update.category_id).scalar()

    old_delta = transaction_delta(
        old_category_type, transaction_to_update.amount)

    balance_without_old = compute_balance(db, account) - old_delta
    delta = transaction_delta(category.category_type, new_amount)
    ensure_balance_not_negative(balance_without_old, delta)

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

    new_account_id = transaction.account_id or transaction_to_update.account_id
    new_category_id = transaction.category_id or transaction_to_update.category_id
    new_amount = transaction.amount if transaction.amount is not None else transaction_to_update.amount

    account = db.query(AccountModel).filter(
        AccountModel.id == new_account_id).first()

    if account is None:
        raise HTTPException(
            status_code=404, detail="The transaction cannot be linked to a non-existent account.")

    category = db.query(CategoryModel).filter(
        CategoryModel.id == new_category_id).first()

    if category is None:
        raise HTTPException(
            status_code=404, detail="The transaction cannot be linked to a non-existent category.")

    old_category_type = db.query(CategoryModel.category_type).filter(
        CategoryModel.id == transaction_to_update.category_id).scalar()

    old_delta = transaction_delta(
        old_category_type, transaction_to_update.amount)

    balance_without_old = compute_balance(db, account) - old_delta
    delta = transaction_delta(category.category_type, new_amount)
    ensure_balance_not_negative(balance_without_old, delta)

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
