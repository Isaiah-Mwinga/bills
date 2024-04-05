from fastapi import FastAPI, HTTPException, Depends
from .database import engine, get_db, Base, Session
from .app import schemas, models


Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/bills/", response_model=Bill)
def create_bill(bill: BillCreate, db: Session = Depends(get_db)):
    db_bill = Bill(total=bill.total)
    for sub_bill in bill.sub_bills:
        db_sub_bill = SubBill(amount=sub_bill.amount, reference=sub_bill.reference)
        db_bill.sub_bills.append(db_sub_bill)
    db.add(db_bill)
    db.commit()
    db.refresh(db_bill)
    return db_bill

@app.get("/bills/{bill_id}", response_model=Bill)
def read_bill(bill_id: int, db: Session = Depends(get_db)):
    db_bill = db.query(Bill).filter(Bill.id == bill_id).first()
    if db_bill is None:
        raise HTTPException(status_code=404, detail="Bill not found")
    return db_bill

@app.get("/bills/", response_model=list[Bill])  
def read_bills(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Bill).offset(skip).limit(limit).all()

