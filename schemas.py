from pydantic import BaseModel, ConfigDict, computed_field
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


class TransactionUpdate(TransactionBase):
    amount: float | None = None
    account_id: int | None = None
    # date: date | None = None  Unable to evaluate type annotation 'date | None'.
    category_id: int | None = None
    comment: str | None = None


class AccountBase(BaseModel):
    name: str
    currency: str


class AccountCreate(AccountBase):
    initial_balance: float


class Account(AccountBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

    @computed_field
    def balance(self) -> float:
        return 999


class AccountUpdate(AccountBase):
    name: str | None = None
    currency: str | None = None
    initial_balance: float | None = None
