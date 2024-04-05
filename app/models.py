from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .database import Base

class Bill(Base):
    __tablename__ = "bills"
    id = Column(Integer, primary_key=True, index=True)
    total = Column(Float, nullable=False)
    sub_bills = relationship("SubBill", back_populates="bill")

class SubBill(Base):
    __tablename__ = "sub_bills"
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    reference = Column(String, unique=True, nullable=True, index=True, collation='NOCASE')
    bill_id = Column(Integer, ForeignKey("bills.id"))
    bill = relationship("Bill", back_populates="sub_bills")