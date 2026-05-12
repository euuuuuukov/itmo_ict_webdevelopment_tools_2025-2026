from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from enum import Enum


class Priority(Enum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'


class TaskStatus(Enum):
    PENDING = 'pending'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

    tasks: List['Task'] = Relationship(back_populates='owner')
    notifications: List['Notification'] = Relationship(back_populates='user')
    daily_schedules: List['DailySchedule'] = Relationship(back_populates='user')


class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = ''
    deadline: Optional[datetime] = None
    priority: Priority = Priority.MEDIUM
    status: TaskStatus = TaskStatus.PENDING
    estimated_hours: float = 0.0
    total_spent_hours: float = 0.0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    owner_id: int = Field(foreign_key='user.id')

    owner: User = Relationship(back_populates='tasks')
    time_logs: List['TimeLog'] = Relationship(back_populates='task')
    notifications: List['Notification'] = Relationship(back_populates='task')
    category_links: List['TaskCategoryLink'] = Relationship(back_populates='task')


class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    description: Optional[str] = ''

    task_links: List['TaskCategoryLink'] = Relationship(back_populates='category')


# associated thing
class TaskCategoryLink(SQLModel, table=True):
    task_id: int = Field(foreign_key='task.id', primary_key=True)
    category_id: int = Field(foreign_key='category.id', primary_key=True)
    assigned_at: datetime = Field(default_factory=datetime.utcnow)
    notes: Optional[str] = None

    task: Task = Relationship(back_populates='category_links')
    category: Category = Relationship(back_populates='task_links')


class TimeLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: int = Field(foreign_key='task.id')
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_hours: float = 0.0
    note: Optional[str] = ''

    task: Task = Relationship(back_populates='time_logs')


class Notification(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key='user.id')
    task_id: Optional[int] = Field(foreign_key='task.id')
    message: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_read: bool = False

    user: User = Relationship(back_populates='notifications')
    task: Task = Relationship(back_populates='notifications')


class DailySchedule(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key='user.id')
    date: datetime
    planned_hours: float = 0.0
    actual_hours: float = 0.0
    notes: Optional[str] = ''

    user: User = Relationship(back_populates='daily_schedules')
