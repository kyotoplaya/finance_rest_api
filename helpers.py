from fastapi.exceptions import HTTPException
from decimal import Decimal

from models import Category as CategoryModel
from models import Transaction as TransactionModel
from enums import CategoryType


def compute_balance(db, account) -> Decimal:
    rows = (
        db.query(CategoryModel.category_type, TransactionModel.amount)
        .join(CategoryModel, TransactionModel.category_id == CategoryModel.id)
        .filter(TransactionModel.account_id == account.id)
        .all()
    )
    balance = account.initial_balance
    for category_type, amount in rows:
        if category_type == CategoryType.EXPENSE:
            balance -= amount
        else:
            balance += amount
    return balance


def transaction_delta(category_type: CategoryType, amount: Decimal) -> Decimal:
    return -amount if category_type == CategoryType.EXPENSE else amount


def ensure_balance_not_negative(balance: Decimal, delta: Decimal) -> None:
    if balance + delta < 0:
        raise HTTPException(status_code=400, detail="Insufficient funds")
