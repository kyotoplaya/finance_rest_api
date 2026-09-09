from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from decimal import Decimal
from datetime import date

from database import get_db
from models import Transaction as TransactionModel
from models import Category as CategoryModel

from schemas import Report
from enums import CategoryType

router = APIRouter()


@router.get("/reports/summary")
def get_report(account_id: int, month: str | None = None, category_id: int | None = None, db: Session = Depends(get_db)):
    filters = [
        TransactionModel.account_id == account_id      # всегда
    ]

    if month:

        # "2026-09" + "-01" = 2026-09-01
        start = date.fromisoformat(month + "-01")

        if start.month == 12:
            end = date(start.year + 1, 1, 1)
        else:
            end = date(start.year, start.month + 1, 1)

        # только если есть месяц
        filters.append(TransactionModel.date >= start)

        # только если есть месяц
        filters.append(TransactionModel.date < end)

    if category_id is not None:
        filters.append(TransactionModel.category_id == category_id)

    transactions_count = db.query(TransactionModel).filter(*filters).count()

    income = (
        db.query(func.coalesce(func.sum(TransactionModel.amount), Decimal("0.00")))
        .join(CategoryModel, TransactionModel.category_id == CategoryModel.id)
        .filter(
            *filters,
            CategoryModel.category_type ==
            CategoryType.INCOME
        )
        .scalar()
    )

    expense = (
        db.query(func.coalesce(func.sum(TransactionModel.amount), Decimal("0.00")))
        .join(CategoryModel, TransactionModel.category_id == CategoryModel.id)
        .filter(
            *filters,
            CategoryModel.category_type ==
            CategoryType.EXPENSE
        )
        .scalar()
    )

    net = income - expense

    report = Report(
        income=income,
        expense=expense,
        net=net,
        transactions_count=transactions_count,
    )

    return report
