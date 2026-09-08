from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Boolean, Enum
from database import Base

from enums import CategoryType


class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    currency = Column(String)
    initial_balance = Column(Float)


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    category_type = Column(Enum(CategoryType))
    is_system = Column(Boolean, default=False)


class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    account_id = Column(Integer, ForeignKey(
        "accounts.id", ondelete="RESTRICT"))
    date = Column(Date)
    category_id = Column(Integer, ForeignKey(
        "categories.id", ondelete="RESTRICT"))
    comment = Column(String)
