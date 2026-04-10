# Лабораторная работа 1. Реализация серверного приложения FastAPI

Папка с выполненными практиками [здесь](https://github.com/euuuuuukov/ITMO_ICT_WebDevelopment_tools_2025-2026/blob/main/students/k3341/kovalenko_evgenii/lr1/pr).

<details>

<summary>Эндпоинты</summary>

```python
@app.get('/')
def root():
    return {'message': 'the best time manager ever'}


# users (register, login, jwt)
@app.post('/register', response_model=TokenResponse)
def register(user: UserCreate, session: Session = Depends(get_session)):
    existing = session.exec(select(User).where((User.username == user.username) | (User.email == user.email))).first()
    if existing:
        raise HTTPException(400, 'Username or email already exists')
    hashed = get_password_hash(user.password)
    db_user = User(username=user.username, email=user.email, hashed_password=hashed)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    token = create_access_token({'sub': db_user.id})
    return {'access_token': token}


@app.post('/login', response_model=TokenResponse)
def login(login_data: UserLogin, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.username == login_data.username)).first()
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(401, 'Invalid credentials')
    token = create_access_token({'sub': user.id})
    return {'access_token': token}


@app.get('/users/me')
def get_me(current_user: User = Depends(get_current_user)):
    return {'id': current_user.id, 'username': current_user.username, 'email': current_user.email}


@app.post('/users/change-password')
def change_password(pwd: PasswordChange, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    if not verify_password(pwd.old_password, current_user.hashed_password):
        raise HTTPException(401, 'Wrong password')
    current_user.hashed_password = get_password_hash(pwd.new_password)
    session.add(current_user)
    session.commit()
    return {'message': 'Password updated'}


@app.get('/users')
def list_users(session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    users = session.exec(select(User)).all()
    return [{'id': u.id, 'username': u.username, 'email': u.email} for u in users]


# tasks (crud with included categories и time_logs) ----------
@app.post('/tasks', response_model=Task)
def create_task(task: TaskCreate, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    db_task = Task(**task.model_dump(), owner_id=user.id)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@app.get('/tasks')
def list_tasks(session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    tasks = session.exec(select(Task).where(Task.owner_id == user.id)).all()
    result = []
    for t in tasks:
        # подгружаем категории
        links = session.exec(select(TaskCategoryLink).where(TaskCategoryLink.task_id == t.id)).all()
        categories = [session.get(Category, link.category_id) for link in links if session.get(Category, link.category_id)]
        # подгружаем логи времени
        time_logs = session.exec(select(TimeLog).where(TimeLog.task_id == t.id)).all()
        result.append({
            'id': t.id,
            'title': t.title,
            'description': t.description,
            'deadline': t.deadline,
            'priority': t.priority,
            'status': t.status,
            'estimated_hours': t.estimated_hours,
            'total_spent_hours': t.total_spent_hours,
            'created_at': t.created_at,
            'categories': categories,
            'time_logs': time_logs
        })
    return result


@app.get('/tasks/{task_id}')
def get_task(task_id: int, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    task = session.get(Task, task_id)
    if not task or task.owner_id != user.id:
        raise HTTPException(404, 'Task not found')
    links = session.exec(select(TaskCategoryLink).where(TaskCategoryLink.task_id == task.id)).all()
    categories = [session.get(Category, link.category_id) for link in links if session.get(Category, link.category_id)]
    time_logs = session.exec(select(TimeLog).where(TimeLog.task_id == task.id)).all()
    return {
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'deadline': task.deadline,
        'priority': task.priority,
        'status': task.status,
        'estimated_hours': task.estimated_hours,
        'total_spent_hours': task.total_spent_hours,
        'created_at': task.created_at,
        'categories': categories,
        'time_logs': time_logs
    }


@app.patch('/tasks/{task_id}')
def update_task(task_id: int, task_update: TaskUpdate, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    task = session.get(Task, task_id)
    if not task or task.owner_id != user.id:
        raise HTTPException(404, 'Task not found')
    for key, value in task_update.model_dump(exclude_unset=True).items():
        setattr(task, key, value)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@app.delete('/tasks/{task_id}')
def delete_task(task_id: int, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    task = session.get(Task, task_id)
    if not task or task.owner_id != user.id:
        raise HTTPException(404, 'Task not found')
    session.delete(task)
    session.commit()
    return {'ok': True}


# categories and many-to-many relationship with extra field
@app.post('/categories', response_model=Category)
def create_category(cat: CategoryCreate, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    db_cat = Category(**cat.model_dump())
    session.add(db_cat)
    session.commit()
    session.refresh(db_cat)
    return db_cat


@app.get('/categories')
def list_categories(session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    return session.exec(select(Category)).all()


@app.post('/tasks/{task_id}/categories/{category_id}')
def assign_category(task_id: int, category_id: int, link_data: AssignCategory = None, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    task = session.get(Task, task_id)
    cat = session.get(Category, category_id)
    if not task or task.owner_id != user.id or not cat:
        raise HTTPException(404, 'Task or Category not found')
    existing = session.exec(select(TaskCategoryLink).where(TaskCategoryLink.task_id == task_id, TaskCategoryLink.category_id == category_id)).first()
    if existing:
        raise HTTPException(400, 'Already assigned')
    link = TaskCategoryLink(task_id=task_id, category_id=category_id, notes=link_data.notes if link_data else None)
    session.add(link)
    session.commit()
    return {'message': 'Category assigned', 'notes': link.notes}


# time logs
@app.post('/timelogs/{task_id}/start')
def start_timer(task_id: int, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    task = session.get(Task, task_id)
    if not task or task.owner_id != user.id:
        raise HTTPException(404, 'Task not found')
    log = TimeLog(task_id=task_id, start_time=datetime.utcnow())
    session.add(log)
    session.commit()
    return {'log_id': log.id, 'start_time': log.start_time}


@app.patch('/timelogs/{log_id}/stop')
def stop_timer(log_id: int, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    log = session.get(TimeLog, log_id)
    if not log or log.task.owner_id != user.id:
        raise HTTPException(404, 'Log not found')
    log.end_time = datetime.utcnow()
    log.duration_hours = (log.end_time - log.start_time).total_seconds() / 3600
    task = log.task
    task.total_spent_hours += log.duration_hours
    session.add(task)
    session.add(log)
    session.commit()
    return {'duration_hours': log.duration_hours}


# notifications (i'm lazy and notifications are easy)
@app.get('/notifications')
def get_notifications(session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    return session.exec(select(Notification).where(Notification.user_id == user.id)).all()


# daily schedule
@app.post('/schedules')
def create_schedule(date: datetime, planned_hours: float, notes: str = '', session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    schedule = DailySchedule(user_id=user.id, date=date, planned_hours=planned_hours, notes=notes)
    session.add(schedule)
    session.commit()
    return schedule


@app.get('/schedules')
def get_schedule(date: datetime, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    schedule = session.exec(select(DailySchedule).where(DailySchedule.user_id == user.id, DailySchedule.date == date)).first()
    if not schedule:
        return {'message': 'no schedule for this date'}
    return schedule


@app.on_event('startup')
def startup():
    init_db()
```
</details>

<details>

<summary>Модели</summary>

```python
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
    id: Optional[int] = Field(default=True, primary_key=True)
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
    id: Optional[int] = Field(default=True, primary_key=True)
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
    id: Optional[int] = Field(default=True, primary_key=True)
    task_id: int = Field(foreign_key='task.id')
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_hours: float = 0.0
    note: Optional[str] = ''

    task: Task = Relationship(back_populates='time_logs')


class Notification(SQLModel, table=True):
    id: Optional[int] = Field(default=True, primary_key=True)
    user_id: int = Field(foreign_key='user.id')
    task_id: Optional[int] = Field(foreign_key='task.id')
    message: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_read: bool = False

    user: User = Relationship(back_populates='notifications')
    task: Task = Relationship(back_populates='notifications')


class DailySchedule(SQLModel, table=True):
    id: Optional[int] = Field(default=True, primary_key=True)
    user_id: int = Field(foreign_key='user.id')
    date: datetime
    planned_hours: float = 0.0
    actual_hours: float = 0.0
    notes: Optional[str] = ''

    user: User = Relationship(back_populates='daily_schedules')
```

</details>

<details>

<summary>Код соединения с БД</summary>

```python
from sqlmodel import SQLModel, create_engine, Session
from config import DB_URL


engine = create_engine(DB_URL, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
```

</details>