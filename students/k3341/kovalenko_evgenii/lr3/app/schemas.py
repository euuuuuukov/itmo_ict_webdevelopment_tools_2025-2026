from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from models import Priority, TaskStatus


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class PasswordChange(BaseModel):
    old_password: str
    new_password: str


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = ''
    deadline: Optional[datetime] = None
    priority: Priority = Priority.MEDIUM
    estimated_hours: float = 0.0


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    priority: Optional[Priority] = None
    status: Optional[TaskStatus] = None
    estimated_hours: Optional[float] = None


class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = ''


class AssignCategory(BaseModel):
    notes: Optional[str] = None


class ScheduleCreate(BaseModel):
    date: datetime
    planned_hours: float
    notes: str = ""
