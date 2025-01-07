from datetime import datetime
from database import get_db
from database.models import Task
from fastapi import HTTPException
from database.models import User
from database.email_service import send_email_notification

def create_task_db(project_id, title, completed, description=None, due_date=None):
    db = next(get_db())
    new_task = Task(
        project_id=project_id,
        title=title,
        description=description,
        due_date=due_date,
        completed=completed
    )
    db.add(new_task)
    db.commit()
    return True

def get_project_tasks_db(project_id):
    db = next(get_db())
    tasks = db.query(Task).filter_by(project_id=project_id).first()
    return tasks

def get_exact_task_db(task_id):
    db = next(get_db())
    exact_task = db.query(Task).filter_by(id=task_id).first()
    return exact_task

def get_all_tasks_db():
    db = next(get_db())
    all_tasks = db.query(Task).all()
    return all_tasks

def update_task_db(task_id, change_info, new_info):
    db = next(get_db())
    update_task = db.query(Task).filter_by(id=task_id).first()
    if update_task:
        if hasattr(update_task, change_info):
            setattr(update_task, change_info, new_info)
            update_task.updated_at = datetime.utcnow()
            db.commit()
            return True
    return False

def delete_task_db(task_id):
    db = next(get_db())
    delete_task = db.query(Task).filter_by(id=task_id).first()
    if delete_task:
        db.delete(delete_task)
        db.commit()
        return True
    return False

def assign_users_to_task(task_id: int, user_ids: list[int]):
    db = next(get_db())
    task = db.query(Task).filter_by(id=task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    users = db.query(User).filter(User.id.in_(user_ids)).all()
    if not users:
        raise HTTPException(status_code=404, detail="Пользователи не найдены")
    for user in users:
        if user not in task.assignees:
            task.assignees.append(user)
    db.commit()
    db.refresh(task)
    return task

def assign_task_to_user(task_id: int, user_id: int):
    db = next(get_db())
    task = db.query(Task).filter(Task.id == task_id).first()
    user = db.query(User).filter(User.id == user_id).first()
    if not task or not user:
        raise HTTPException(
            status_code=404,
            detail="Невозможно найти задачу или пользователя."
        )
    task.assignees.append(user)
    db.commit()
    task_data = {
        "title": task.title,
        "description": task.description,
        "due_date": task.due_date,
        "completed": task.completed,
    }
    send_email_notification(user.email, task_data)
    return {"message": "Пользователь назначен на задачу и уведомлен по email."}

def remove_users_from_task(task_id: int, user_ids: list[int]):
    db = next(get_db())
    task = db.query(Task).filter_by(id=task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    task.assignees = [user for user in task.assignees if user.id not in user_ids]
    db.commit()
    db.refresh(task)
    return task
