from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class EmailScheduleCreate(BaseModel):
    to_email: EmailStr
    subject: str
    body: str
    send_time: datetime

class EmailScheduleOut(BaseModel):
    id: int
    to_email: str
    subject: str
    body: str
    send_time: datetime

    class Config:
        orm_mode = True
