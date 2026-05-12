from datetime import datetime, timedelta

from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select, func

from connection import init_db, get_session
from models import *
from schemas import *
from security import get_password_hash, verify_password, create_access_token
from dependencies import get_current_user


app = FastAPI()


@app.get('/')
def root():
    return {'message': 'the best time manager ever'}


# users (register, login, jwt)
@app.post('/register', response_model=TokenResponse)
def register(user: UserCreate, session: Session = Depends(get_session)):
    existing = session.exec(select(User).where((User.username == user.username) | (User.email == user.email))).first()
    if existing:
        raise HTTPException(400, 'username or email already exists')
    hashed = get_password_hash(user.password)
    db_user = User(username=user.username, email=user.email, hashed_password=hashed)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    token = create_access_token({'sub': str(db_user.id)})
    return {'access_token': token}


@app.post('/login', response_model=TokenResponse)
def login(login_data: UserLogin, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.username == login_data.username)).first()
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(401, 'invalid credentials')
    token = create_access_token({'sub': str(user.id)})
    return {'access_token': token}


@app.get('/users/me')
def get_me(current_user: User = Depends(get_current_user)):
    return {'id': current_user.id, 'username': current_user.username, 'email': current_user.email}


@app.post('/users/change-password')
def change_password(pwd: PasswordChange, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    if not verify_password(pwd.old_password, current_user.hashed_password):
        raise HTTPException(401, 'wrong password')
    current_user.hashed_password = get_password_hash(pwd.new_password)
    current_user.hashed_password = get_password_hash(pwd.new_password)
    session.add(current_user)
    session.commit()
    return {'message': 'password updated'}


@app.get('/users')
def list_users(session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    users = session.exec(select(User)).all()
    return [{'id': u.id, 'username': u.username, 'email': u.email} for u in users]


# tasks (crud with included categories и time_logs)
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
        raise HTTPException(404, 'task not found')
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
        raise HTTPException(404, 'task not found')
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
        raise HTTPException(404, 'task not found')
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
        raise HTTPException(404, 'task or category not found')
    existing = session.exec(select(TaskCategoryLink).where(TaskCategoryLink.task_id == task_id, TaskCategoryLink.category_id == category_id)).first()
    if existing:
        raise HTTPException(400, 'already assigned')
    link = TaskCategoryLink(task_id=task_id, category_id=category_id, notes=link_data.notes if link_data else None)
    session.add(link)
    session.commit()
    return {'message': 'Category assigned', 'notes': link.notes}


# time logs
@app.post('/timelogs/{task_id}/start')
def start_timer(task_id: int, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    task = session.get(Task, task_id)
    if not task or task.owner_id != user.id:
        raise HTTPException(404, 'task not found')
    log = TimeLog(task_id=task_id, start_time=datetime.utcnow())
    session.add(log)
    session.commit()
    return {'log_id': log.id, 'start_time': log.start_time}


@app.patch('/timelogs/{log_id}/stop')
def stop_timer(log_id: int, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    log = session.get(TimeLog, log_id)
    if not log or log.task.owner_id != user.id:
        raise HTTPException(404, 'log not found')
    log.end_time = datetime.utcnow()
    log.duration_hours = (log.end_time - log.start_time).total_seconds() / 3600
    task = log.task
    task.total_spent_hours += log.duration_hours
    session.add(task)
    session.add(log)
    session.commit()
    return {'duration_hours': log.duration_hours}


@app.get('/notifications')
def get_notifications(session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    return session.exec(select(Notification).where(Notification.user_id == user.id)).all()


@app.post('/notifications/check_deadlines')
def check_deadlines(session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    upcoming = session.exec(select(Task).where(
        Task.owner_id == user.id,
        Task.deadline.is_not(None),
        Task.deadline > datetime.utcnow(),
        Task.deadline <= datetime.utcnow() + timedelta(days=1),
        Task.status != TaskStatus.COMPLETED
    )).all()

    created = []
    for task in upcoming:
        existing = session.exec(select(Notification).where(
            Notification.user_id == user.id,
            Notification.task_id == task.id,
            Notification.is_read == False
        )).first()
        if not existing:
            notif = Notification(user_id=user.id, task_id=task.id, message=f'task "{task.title}" deadline at {task.deadline}')
            session.add(notif)
            created.append(notif)

    session.commit()
    return {'notifications': created}


@app.patch('/notifications/{notif_id}/read')
def mark_notification_read(notif_id: int, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    notif = session.get(Notification, notif_id)
    if not notif or notif.user_id != user.id:
        raise HTTPException(404, 'notification not found')
    notif.is_read = True
    session.add(notif)
    session.commit()
    return {'message': f'notif {notif_id} marked as read'}


# daily schedule
@app.post('/schedules')
def create_schedule(schedule: ScheduleCreate, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    db_schedule = DailySchedule(user_id=user.id, **schedule.model_dump())
    session.add(db_schedule)
    session.commit()
    return db_schedule


@app.get('/schedules')
def get_schedule(date: str, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    try:
        start = datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        raise HTTPException(status_code=400, detail='invalid date format, use yyyy-mm-dd')

    schedule = session.exec(select(DailySchedule).where(DailySchedule.user_id == user.id,
                                                        DailySchedule.date >= start,
                                                        DailySchedule.date < start + timedelta(days=1))).all()
    if not schedule:
        return {'message': 'no schedule for this date'}
    return schedule


@app.patch('/schedules/{schedule_id}')
def update_schedule(schedule_id: int, actual_hours: float, notes: str = None, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    schedule = session.get(DailySchedule, schedule_id)
    if not schedule or schedule.user_id != user.id:
        raise HTTPException(404, 'schedule not found')
    schedule.actual_hours = actual_hours
    if notes is not None:
        schedule.notes = notes

    session.commit()
    session.refresh(schedule)
    return schedule


@app.get('/analytics')
def analytics(session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    total_hours = session.exec(select(func.sum(TimeLog.duration_hours)).where(TimeLog.task.has(owner_id=user.id))).first() or 0
    completed_tasks = session.exec(select(func.count()).where(Task.owner_id == user.id, Task.status == TaskStatus.COMPLETED)).first()
    overdue_tasks = session.exec(select(func.count()).where(Task.owner_id == user.id, Task.deadline < datetime.utcnow(), Task.status != TaskStatus.COMPLETED)).first()
    avg_completion_time = session.exec(select(func.avg(TimeLog.duration_hours)).where(TimeLog.task.has(owner_id=user.id, status=TaskStatus.COMPLETED))).first() or 0
    under_estimation_count = session.exec(select(func.count()).where(Task.owner_id == user.id, Task.status == TaskStatus.COMPLETED, Task.total_spent_hours > Task.estimated_hours)).first()
    over_estimation_count = session.exec(select(func.count()).where(Task.owner_id == user.id, Task.status == TaskStatus.COMPLETED, Task.total_spent_hours < Task.estimated_hours)).first()

    return {
        'total_hours_spent': float(total_hours),
        'completed_tasks': completed_tasks,
        'overdue_tasks': overdue_tasks,
        'avg_completion_time': float(avg_completion_time),
        'tasks_under_estimated': under_estimation_count,
        'tasks_over_estimated': over_estimation_count
    }


@app.on_event('startup')
def startup():
    init_db()
