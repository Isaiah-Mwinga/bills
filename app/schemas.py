from pydantic import BaseModel


class SubBillCreate(BaseModel):
    amount: float
    reference: str

class BillCreate(BaseModel):
    total: float
    sub_bills: conlist(SubBillCreate, min_items=1)

class SubBillResponse(BaseModel):
    id: int
    amount: float
    reference: str

class BillResponse(BaseModel):
    id: int
    total: float
    sub_bills: list[SubBillResponse]