from pydantic import BaseModel, ConfigDict, computed_field
import datetime
from decimal import Decimal

from enums import CategoryType


class CategoryBase(BaseModel):
    name: str
    category_type: CategoryType


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int
    is_system: bool = False
    model_config = ConfigDict(from_attributes=True)


class CategoryUpdate(CategoryBase):
    name: str | None = None
    category_type: CategoryType | None = None


class TransactionBase(BaseModel):
    amount: Decimal
    account_id: int
    date: datetime.date | None = None
    category_id: int
    comment: str | None = None


class TransactionCreate(TransactionBase):
    pass


class Transaction(TransactionBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class TransactionUpdate(TransactionBase):
    amount: Decimal | None = None
    account_id: int | None = None
    date: datetime.date | None = None
    category_id: int | None = None
    comment: str | None = None


class AccountBase(BaseModel):
    name: str
    currency: str


class AccountCreate(AccountBase):
    initial_balance: Decimal


class Account(AccountBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
    balance: Decimal = Decimal("0")


class AccountUpdate(AccountBase):
    name: str | None = None
    currency: str | None = None
    initial_balance: Decimal | None = None


class Report(BaseModel):
    income: Decimal
    expense: Decimal
    net: Decimal
    transactions_count: int
