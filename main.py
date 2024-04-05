from fastapi import FastAPI, HTTPException, Depends, Query
from app.database import SessionLocal, engine
from app.schemas import SubBillCreate, BillCreate
from app import models
from app.models import Bill, SubBill


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/bills", response_model=BillCreate)
def create_bill(bill: BillCreate):
    db = SessionLocal()
    db_bill = Bill(total=bill.total)
    for sub_bill in bill.sub_bills:
        db_sub_bill = SubBill(amount=sub_bill.amount, reference=sub_bill.reference)
        db_bill.sub_bills.append(db_sub_bill)
    db.add(db_bill)
    db.commit()
    db.refresh(db_bill)
    db.close()
    return db_bill

@app.get("/bills", response_model=list[BillCreate])
def get_bills(
    reference: str = Query(None, description="Case-insensitive substring search for reference"),
    total_from: float = Query(None, description="Filter bills with total greater than or equal to this value"),
    total_to: float = Query(None, description="Filter bills with total less than or equal to this value"),
):
    db = SessionLocal()
    query = db.query(Bill)
    if reference:
        query = query.join(Bill.sub_bills).filter(SubBill.reference.ilike(f"%{reference}%"))
    if total_from:
        query = query.filter(Bill.total >= total_from)
    if total_to:
        query = query.filter(Bill.total <= total_to)
    bills = query.all()
    db.close()
    return bills
