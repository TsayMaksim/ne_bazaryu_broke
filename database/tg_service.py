import telebot
from database import get_db
from database.models import User, Task, Project

BOT_TOKEN = "7870136037:AAE8W0Dl2DkLQUEEBIAvgNlkprFH0WqhqDM"
bot = telebot.TeleBot(BOT_TOKEN)

def send_message(chat_id, text):
    bot.send_message(chat_id, text, parse_mode="Markdown")

def notify_task_to_user(task, user_telegram_id):
    task_info = (
        f"🔔 Вам назначена новая задача!\n\n"
        f"📋 *Название:* {task['title']}\n"
        f"📝 *Описание:* {task.get('description', 'Не указано')}\n"
        f"📅 *Срок выполнения:* {task.get('due_date', 'Не установлен')}\n"
        f"✅ *Статус:* {'Выполнено' if task.get('completed') else 'Не выполнено'}"
    )
    send_message(chat_id=user_telegram_id, text=task_info)

def notify_project_to_user(project, user_telegram_id):
    project_info = (
        f"📢 *Новый проект создан!*\n\n"
        f"📋 *Название:* {project['name']}\n"
        f"📝 *Описание:* {project.get('description', 'Не указано')}\n"
        f"📅 *Создан:* {project.get('created_at')}"
    )
    send_message(chat_id=user_telegram_id, text=project_info)

def send_task_to_user(task_id, user_id):
    db = next(get_db())
    task = db.query(Task).filter_by(id=task_id).first()
    user = db.query(User).filter_by(id=user_id).first()
    if not task or not user:
        raise ValueError("Невозможно найти задачу или пользователя.")
    if not user.telegram_id:
        raise ValueError("У пользователя отсутствует Telegram ID.")
    task_data = {
        "title": task.title,
        "description": task.description,
        "due_date": task.due_date,
        "completed": task.completed,
    }
    notify_task_to_user(task_data, user.telegram_id)

def send_project_to_user(project_id, user_id):
    db = next(get_db())
    project = db.query(Project).filter_by(id=project_id).first()
    user = db.query(User).filter_by(id=user_id).first()
    if not project or not user:
        raise ValueError("Невозможно найти проект или пользователя.")
    if not user.telegram_id:
        raise ValueError("У пользователя отсутствует Telegram ID.")
    project_data = {
        "name": project.name,
        "description": project.description,
        "created_at": project.created_at.strftime("%Y-%m-%d %H:%M:%S"),
    }
    notify_project_to_user(project_data, user.telegram_id)
