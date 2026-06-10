from sqlalchemy import Column, Integer, String, Numeric, Date, DateTime, ForeignKey
from app.database.database import Base
from datetime import datetime

class User(Base):
    __tablename__="users"
    id=Column(Integer, primary_key=True, nullable=False)
    email=Column(String(255), nullable=False, unique=True)
    hashed_password=Column(String(255), nullable=False)
    created_at=Column(DateTime, default=datetime.utcnow, nullable=False)

class Transaction(Base):
    __tablename__="transactions"
    id=Column(Integer,primary_key=True, nullable=False)
    amount=Column(Numeric(10,2),nullable=False)
    category=Column(String(255), nullable=False)
    description = Column(String(255))
    merchant=Column(String(255), nullable=False)
    transaction_date=Column(Date, nullable=False)
    user_id=Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at=Column(DateTime, default=datetime.utcnow, nullable=False)