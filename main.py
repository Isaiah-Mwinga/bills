from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy.orm import Session
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
def create_bill(bill: BillCreate, db: Session = Depends(get_db)):
    # Extract sub_bills data from BillCreate schema
    sub_bills_data = bill.sub_bills
    
    # Ensure that sub_bills_data is not empty
    if not sub_bills_data:
        raise HTTPException(status_code=400, detail="Sub-bills data cannot be empty")

    # Create Bill instance
    db_bill = models.Bill(total=bill.total)
    
    # Create SubBill instances and associate with the Bill
    for sub_bill_data in sub_bills_data:
        db_sub_bill = models.SubBill(amount=sub_bill_data.amount, reference=sub_bill_data.reference)
        db_bill.sub_bills.append(db_sub_bill)
    
    # Add Bill to session, commit changes, and refresh
    db.add(db_bill)
    db.commit()
    db.refresh(db_bill)
    
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
