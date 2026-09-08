from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Account as AccountModel
from schemas import AccountCreate, AccountUpdate, Account

from helpers import compute_balance

router = APIRouter()


@router.post("/accounts", response_model=Account, status_code=201)
def create_account(account: AccountCreate, db: Session = Depends(get_db)):
    db_account = AccountModel(**account.model_dump())
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    db_account.balance = compute_balance(db, db_account)
    return db_account


@router.get("/accounts", response_model=list[Account])
def get_accounts(db: Session = Depends(get_db)):
    accounts = db.query(AccountModel).all()
    for account in accounts:
        account.balance = compute_balance(db, account)
    return accounts


@router.get("/accounts/{account_id}", response_model=Account)
def get_account(account_id: int, db: Session = Depends(get_db)):
    account = db.query(AccountModel).filter(
        AccountModel.id == account_id).first()

    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")

    account.balance = compute_balance(db, account)

    return account


@router.patch("/accounts/{account_id}", response_model=Account)
def patch_account(account_id: int, account: AccountUpdate, db: Session = Depends(get_db)):
    account_to_update = db.query(AccountModel).filter(
        AccountModel.id == account_id).first()

    if account_to_update is None:
        raise HTTPException(status_code=404, detail="Account not found")

    updated_account = account.model_dump()
    for key, value in updated_account.items():
        if value is None:
            continue
        setattr(account_to_update, key, value)

    db.commit()
    db.refresh(account_to_update)

    account_to_update.balance = compute_balance(db, account_to_update)
    return account_to_update


@router.put("/accounts/{account_id}", response_model=Account)
def put_account(account_id: int, account: AccountUpdate, db: Session = Depends(get_db)):
    account_to_update = db.query(AccountModel).filter(
        AccountModel.id == account_id).first()

    if account_to_update is None:
        raise HTTPException(status_code=404, detail="Account not found")

    updated_account = account.model_dump()
    for key, value in updated_account.items():
        setattr(account_to_update, key, value)

    db.commit()
    db.refresh(account_to_update)

    account_to_update.balance = compute_balance(db, account_to_update)
    return account_to_update


@router.delete("/accounts/{account_id}", response_model=bool)
def delete_account(account_id: int, db: Session = Depends(get_db)):
    account_to_delete = db.query(AccountModel).filter(
        AccountModel.id == account_id).first()

    if account_to_delete is None:
        raise HTTPException(status_code=404, detail="Account not found")

    db.delete(account_to_delete)
    db.commit()

    return True
