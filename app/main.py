from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, email_sender, scheduler
from .database import engine, SessionLocal
from .auth import router as auth_router, get_current_user
from .models import EmailSchedule
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth_router)

@app.on_event("startup")
def start():
    scheduler.scheduler.start()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "Email Scheduler SaaS is running 🚀"}

@app.post("/schedule_email", response_model=schemas.EmailScheduleOut)
def schedule_email(email: schemas.EmailScheduleCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    today = datetime.utcnow().date()
    count = db.query(EmailSchedule).filter(
        EmailSchedule.user_id == user.id,
        EmailSchedule.send_time >= datetime(today.year, today.month, today.day)
    ).count()

    max_limit = 10 if user.plan == "Free" else 100
    if count >= max_limit:
        raise HTTPException(status_code=400, detail=f"Daily limit of {max_limit} emails reached for your plan")

    db_email = EmailSchedule(**email.dict(), user_id=user.id)
    db.add(db_email)
    db.commit()
    db.refresh(db_email)
    return db_email
