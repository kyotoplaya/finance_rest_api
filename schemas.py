from pydantic import BaseModel, ConfigDict
from datetime import date

class CategoryBase(BaseModel):
    name: str
    category_type: str
    
class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
    
class TransactionBase(BaseModel):
    amount: float
    transaction_type: str
    date: date
    category_id: int
    comment: str | None = None

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int
    model_config = ConfigDict(from_attributes=True)