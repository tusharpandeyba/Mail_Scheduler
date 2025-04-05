from apscheduler.schedulers.background import BackgroundScheduler
from .database import SessionLocal
from .models import EmailSchedule
from .email_sender import send_email
from datetime import datetime

scheduler = BackgroundScheduler()

@scheduler.scheduled_job('interval', seconds=30)
def check_and_send_emails():
    db = SessionLocal()
    now = datetime.utcnow()
    emails = db.query(EmailSchedule).filter(EmailSchedule.send_time <= now, EmailSchedule.status == "scheduled").all()
    for email in emails:
        send_email(email.to_email, email.subject, email.body)
        email.status = "sent"
        db.commit()
    db.close()
