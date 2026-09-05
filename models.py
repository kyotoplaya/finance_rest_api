from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from database import Base

class Category(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    category_type = Column(String)

class Transaction(Base):
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    transaction_type = Column(String)
    date = Column(Date)
    category_id = Column(Integer, ForeignKey("category.id"))
    comment = Column(String)