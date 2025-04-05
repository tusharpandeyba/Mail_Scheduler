# email_test.py

from fastapi import APIRouter
from dotenv import load_dotenv
import os
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()  # Ensure environment variables are loaded

router = APIRouter()

def send_email(to_email: str, subject: str, body: str):
    try:
        print("🚨 send_email was called!")

        sender_email = os.getenv("EMAIL_ADDRESS")
        password = os.getenv("EMAIL_PASSWORD")

        if not sender_email or not password:
            print("❌ Missing EMAIL_ADDRESS or EMAIL_PASSWORD in .env file.")
            return {"error": "Missing credentials in .env"}

        print(f"From: {sender_email}")
        print(f"To: {to_email}")
        print(f"Subject: {subject}")
        print("Body Preview:", body[:50] + "..." if len(body) > 50 else body)

        # Compose the email
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Connect to SMTP server
        print("🔌 Connecting to SMTP server...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)

        # Optional: SMTP debug
        # server.set_debuglevel(1)

        # Send the email
        print("📤 Sending email...")
        server.sendmail(sender_email, to_email, msg.as_string())
        server.quit()

        print("✅ Email sent successfully to", to_email)
        return {"message": f"Email sent successfully to {to_email}"}

    except Exception as e:
        print("❌ Failed to send email:", str(e))
        return {"error": str(e)}


    


@router.post("/test-email")
def test_email_route():
    return send_email(
        to_email="your_verified_email@gmail.com",  # change this
        subject="📧 FastAPI Email Test",
        body="Hey there!\n\nThis is a test email from your FastAPI backend.\n\n🚀"
    )
