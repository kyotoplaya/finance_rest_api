from pydantic import BaseModel, ConfigDict
from datetime import date

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
    amount: float
    account_id: int
    date: date
    category_id: int
    comment: str | None = None


class TransactionCreate(TransactionBase):
    pass


class Transaction(TransactionBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class AccountBase(BaseModel):
    name: str
    currency: str
    balance: float


class AccountCreate(AccountBase):
    pass


class Account(AccountBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class AccountUpdate(AccountBase):
    name: str | None = None
    currency: str | None = None
    balance: float | None = None
