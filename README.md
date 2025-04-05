# 📧 FastAPI Email Scheduler (SaaS)

A backend-only Email Scheduling SaaS built with **FastAPI** that allows users to schedule emails based on their subscription plan (Free or Pro). The system enforces daily limits and sends scheduled emails using background tasks.

## 🚀 Features

* 🔐 **User Authentication**: Token-based login system
* 📨 **Email Scheduler API**: Schedule emails with subject, body, recipient, and desired send time
* 📊 **Subscription Plans**:
   * **Free**: Max 10 emails/day
   * **Pro**: Max 100 emails/day
* ⏱ **Email Sending**: Scheduled using `APScheduler`
* 📬 **SMTP Support**: Emails are sent using `smtplib`
* 🗃 **Database**: SQLite for storing users, emails, and daily quotas

## 🛠 Tech Stack

* **Backend**: FastAPI
* **Database**: SQLite (can be switched to PostgreSQL)
* **Scheduler**: APScheduler
* **Auth**: JWT Token-based
* **Email**: Python's built-in `smtplib`
* **ORM**: SQLAlchemy

## 📦 Setup Instructions

1. Clone the repo

```bash
git clone https://github.com/your-username/email-scheduler-saas.git
cd email-scheduler-saas
```

2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Environment variables

Create a `.env` file in the root directory with your SMTP and JWT settings:

```
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@example.com
SMTP_PASSWORD=your-password
JWT_SECRET_KEY=your-secret-key
```

## 🚀 Running the App

```bash
uvicorn main:app --reload
```

Scheduler will run in the background and send scheduled emails when their time arrives.

## 📬 API Endpoints

### 🔑 Auth

* `POST /register`: Register new user with plan (`free` or `pro`)
* `POST /login`: Login to receive token

### 📅 Schedule Emails

* `POST /schedule-email`
  Body:

```json
{
  "to_email": "user@example.com",
  "subject": "Hello!",
  "body": "This is a scheduled email.",
  "send_at": "2025-04-06T15:30:00"
}
```

Requires Bearer Token in headers.

## ⚠️ Limit Enforcement

* Quotas reset daily at midnight
* Free users: Max 10 scheduled emails/day
* Pro users: Max 100 scheduled emails/day
* If the user exceeds the quota, a `429` response is returned

## 🧹 Future Improvements

* Admin dashboard for managing users
* Email retry queue on failure
* Webhook support
* Rate-limiting per IP
