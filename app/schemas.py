# schemas.py
from pydantic import BaseModel

class SubBillCreate(BaseModel):
    amount: float
    reference: str = None

class BillCreate(BaseModel):
    total: float
    sub_bills: list[SubBillCreate]